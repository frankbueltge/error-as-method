#!/usr/bin/env python3
"""Measure the two channels of the tz database against each other.

Reads only `data/` (committed, with SHA-256 in `data/MANIFEST.md`). Standard library
only, no network, no randomness — so no seed. Prints a table and writes `results.json`.

The question: inside ONE institution, which parts of a published norm can be repaired
and which can only be added to? tzdb's own `theory.html` answers it in its "Interface
stability" section — the set of timezone names is a stable interface; UT offsets and
abbreviations explicitly are not, because "these guesses may be corrected or improved".
This script checks whether the practice matches the constitution, over 87 releases.

Definitions used, all of them consequential:
  identifier   a Zone name or a Link name, i.e. anything a caller may pass as TZ
  retro edit   a change to a Zone in which an already-published data row is rewritten
               or deleted. Pure appends and the tail-close pattern (the last row gains
               an UNTIL and rows follow) are NOT retro edits: they record a future
               change, not a correction of the past.
  row 0        a Zone's first row, which carries its LMT offset — the earliest fact the
               database publishes about that place.
"""

import gzip
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def load():
    with gzip.open(os.path.join(DATA, "releases.json.gz"), "rt", encoding="utf-8") as f:
        rel = json.load(f)["releases"]
    with open(os.path.join(DATA, "edits.json")) as f:
        edits = json.load(f)["edits"]
    return rel, edits


def main():
    rel, edits = load()
    tags = [r["tag"] for r in rel]
    by_tag = {r["tag"]: r for r in rel}
    R = {}

    R["n_releases"] = len(rel)
    R["window"] = [rel[0]["tag"], rel[0]["date"], rel[-1]["tag"], rel[-1]["date"]]
    R["n_transitions"] = len(rel) - 1

    # ---- the identifier channel -------------------------------------------------
    counts = [r["n_ids"] for r in rel]
    R["identifiers_first"] = counts[0]
    R["identifiers_last"] = counts[-1]
    R["identifier_count_monotone"] = all(b >= a for a, b in zip(counts, counts[1:]))
    R["identifier_count_drops"] = [
        {"from": tags[i], "to": tags[i + 1], "delta": counts[i + 1] - counts[i]}
        for i in range(len(counts) - 1) if counts[i + 1] < counts[i]]

    removals = [e for e in edits if e["event"] == "removed"]
    additions = [e for e in edits if e["event"] == "added"]
    R["removals"] = removals
    R["n_removals"] = len(removals)
    R["n_additions"] = len(additions)

    union = set()
    for r in rel:
        union |= set(r["ids"])
    R["identifiers_ever"] = len(union)
    R["identifiers_ever_minus_last"] = len(union) - counts[-1]

    demote = [e for e in edits if e["event"] == "kind_change"
              and e["old"] == "Zone" and e["new"] == "Link"]
    promote = [e for e in edits if e["event"] == "kind_change"
               and e["old"] == "Link" and e["new"] == "Zone"]
    R["n_demoted_zone_to_link"] = len(demote)
    R["n_promoted_link_to_zone"] = len(promote)
    R["demoted"] = [{"id": e["id"], "to": e["to"], "target": e["new_target"]}
                    for e in demote]
    R["promoted"] = [{"id": e["id"], "to": e["to"]} for e in promote]

    retarget = [e for e in edits if e["event"] == "retarget"]
    R["n_retargets"] = len(retarget)
    R["n_retargeted_ids"] = len({e["id"] for e in retarget})
    R["retargets"] = [{"id": e["id"], "to": e["to"],
                       "old": e["old"], "new": e["new"]} for e in retarget]

    # backward: the beside-channel
    bw = [(r["tag"], r["date"],
           sum(1 for v in r["ids"].values() if v["file"] == "backward"))
          for r in rel]
    R["backward_first"] = bw[0][2]
    R["backward_last"] = bw[-1][2]
    R["backward_monotone"] = all(b[2] >= a[2] for a, b in zip(bw, bw[1:]))
    R["backward_drops"] = [{"from": bw[i][0], "to": bw[i + 1][0],
                            "delta": bw[i + 1][2] - bw[i][2]}
                           for i in range(len(bw) - 1) if bw[i + 1][2] < bw[i][2]]
    R["backward_series"] = [{"tag": t, "date": d, "n": n} for t, d, n in bw]

    # ---- the value channel ------------------------------------------------------
    retro = [e for e in edits if e["event"] == "retro"]
    append = [e for e in edits if e["event"] == "append"]
    tail = [e for e in edits if e["event"] == "tail_close"]
    R["n_retro_events"] = len(retro)
    R["n_append_events"] = len(append)
    R["n_tail_close_events"] = len(tail)
    R["n_retro_ids"] = len({e["id"] for e in retro})
    R["retro_id_share"] = round(len({e["id"] for e in retro}) / len(union), 4)

    rel_with_retro = {e["to"] for e in retro}
    R["n_releases_with_retro"] = len(rel_with_retro)
    R["releases_with_no_retro"] = [t for t in tags[1:] if t not in rel_with_retro]

    # how many published rows were actually rewritten or deleted
    rows_touched = 0
    rows_deleted = 0
    row0 = set()
    for e in retro:
        for op in e["ops"]:
            if op["op"] == "replace":
                rows_touched += len(op["old"])
            elif op["op"] == "delete":
                rows_touched += len(op["old"])
                rows_deleted += len(op["old"])
            if op["op"] != "insert" and op["i1"] == 0:
                row0.add(e["id"])
    R["rows_rewritten_or_deleted"] = rows_touched
    R["rows_deleted"] = rows_deleted
    R["n_row0_edited_ids"] = len(row0)
    R["row0_edited_ids"] = sorted(row0)

    # The beside-channel is the Link population, NOT the size of the `backward` file.
    # P7 was posed on the file and broke on it: between 2021b and 2021c, 88 links moved
    # from `backward` back into the continent files without a single identifier changing.
    # The file is a curatorial container; the names are the interface.
    links = [(r["tag"], r["date"],
              sum(1 for v in r["ids"].values() if v["kind"] == "Link")) for r in rel]
    R["links_first"] = links[0][2]
    R["links_last"] = links[-1][2]
    R["links_monotone"] = all(b[2] >= a[2] for a, b in zip(links, links[1:]))
    R["links_series"] = [{"tag": t, "date": d, "n": n} for t, d, n in links]

    # Retro edits that rewrite a HISTORICAL row, i.e. one whose UNTIL year had already
    # passed when the release shipped. Computed after the ledger was fixed and therefore
    # not scored as a prediction: P4 as written counts any rewrite of a published row,
    # including rewrites of the database's own predictions about the future, which are
    # not corrections of the past. This is the stricter number.
    def until_year(row):
        f = row.split(" ")
        if len(f) >= 4 and f[3].isdigit():
            return int(f[3])
        return None

    retro_hist = []
    for e in retro:
        year = int(by_tag[e["to"]]["date"][:4])
        hist = False
        for op in e["ops"]:
            if op["op"] == "insert":
                continue
            for row in op["old"]:
                y = until_year(row)
                if y is not None and y < year:
                    hist = True
        if hist:
            retro_hist.append(e)
    R["n_retro_hist_events"] = len(retro_hist)
    R["n_retro_hist_ids"] = len({e["id"] for e in retro_hist})
    R["n_transitions_with_retro_hist"] = len({e["to"] for e in retro_hist})
    R["retro_hist_points"] = [{"tag": e["to"], "date": by_tag[e["to"]]["date"],
                               "id": e["id"]} for e in retro_hist]
    R["removal_points"] = [{"tag": e["to"], "date": by_tag[e["to"]]["date"],
                            "id": e["id"]} for e in removals]
    R["id_count_series"] = [{"tag": r["tag"], "date": r["date"], "n": r["n_ids"]}
                            for r in rel]

    # per-release retro counts, for the figure
    per = {t: 0 for t in tags[1:]}
    for e in retro:
        per[e["to"]] += 1
    R["retro_series"] = [{"tag": t, "date": by_tag[t]["date"], "n": per[t]}
                         for t in tags[1:]]

    # the single most-edited identifiers
    freq = {}
    for e in retro:
        freq[e["id"]] = freq.get(e["id"], 0) + 1
    R["most_retro_edited"] = sorted(freq.items(), key=lambda kv: -kv[1])[:12]

    # ---- the prediction ledger --------------------------------------------------
    P = {}
    P["P1 no identifier ever removed"] = (R["n_removals"] == 0, R["n_removals"])
    P["P2 identifier count monotone"] = (R["identifier_count_monotone"],
                                         R["identifier_count_drops"])
    P["P3 >=20 demotions, <=3 promotions"] = (
        R["n_demoted_zone_to_link"] >= 20 and R["n_promoted_link_to_zone"] <= 3,
        (R["n_demoted_zone_to_link"], R["n_promoted_link_to_zone"]))
    P["P4 >=200 retro events"] = (R["n_retro_events"] >= 200, R["n_retro_events"])
    P["P5 >=150 identifiers retro-edited"] = (R["n_retro_ids"] >= 150, R["n_retro_ids"])
    P["P6 >=44 of 86 transitions carry a retro edit"] = (
        R["n_releases_with_retro"] >= 44, R["n_releases_with_retro"])
    P["P7 backward monotone and at least doubles"] = (
        R["backward_monotone"] and R["backward_last"] >= 2 * R["backward_first"],
        (R["backward_first"], R["backward_last"], R["backward_monotone"]))
    P["P8 appends outnumber retro edits"] = (
        R["n_append_events"] > R["n_retro_events"],
        (R["n_append_events"], R["n_retro_events"]))
    P["P9 >=30 identifiers had row 0 edited"] = (
        R["n_row0_edited_ids"] >= 30, R["n_row0_edited_ids"])
    P["P10 >=5 link names retargeted"] = (
        R["n_retargeted_ids"] >= 5, R["n_retargeted_ids"])
    R["predictions"] = {k: {"held": bool(v[0]), "value": v[1]} for k, v in P.items()}

    # ---- print ------------------------------------------------------------------
    w = R["window"]
    print(f"\ntz database, {R['n_releases']} releases, {w[0]} ({w[1]}) .. {w[2]} ({w[3]})")
    print(f"{R['n_transitions']} consecutive transitions\n")
    print("THE IDENTIFIER CHANNEL (declared a stable interface)")
    print(f"  identifiers, first release      : {R['identifiers_first']}")
    print(f"  identifiers, last release       : {R['identifiers_last']}")
    print(f"  identifiers ever seen           : {R['identifiers_ever']}")
    print(f"  ever seen but gone by the end   : {R['identifiers_ever_minus_last']}")
    print(f"  identifiers ADDED               : {R['n_additions']}")
    print(f"  identifiers REMOVED             : {R['n_removals']}")
    for e in removals:
        print(f"      - {e['id']} ({e['kind']}) removed in {e['to']}")
    print(f"  demoted Zone -> Link            : {R['n_demoted_zone_to_link']}")
    print(f"  promoted Link -> Zone           : {R['n_promoted_link_to_zone']}")
    print(f"  link targets changed            : {R['n_retargets']}"
          f" on {R['n_retargeted_ids']} names")
    print(f"  Link names (the beside-channel) : {R['links_first']} -> {R['links_last']}"
          f"  (monotone: {R['links_monotone']})")
    print(f"  size of the `backward` FILE     : {R['backward_first']} ->"
          f" {R['backward_last']}  (monotone: {R['backward_monotone']})")
    print("\nTHE VALUE CHANNEL (explicitly NOT a stable interface)")
    print(f"  retro edit events               : {R['n_retro_events']}")
    print(f"  distinct identifiers retro-edited: {R['n_retro_ids']}"
          f"  ({R['retro_id_share']:.1%} of all identifiers ever)")
    print(f"  published rows rewritten/deleted : {R['rows_rewritten_or_deleted']}"
          f"  (of which deleted outright: {R['rows_deleted']})")
    print(f"  transitions carrying >=1 retro   : {R['n_releases_with_retro']}"
          f" of {R['n_transitions']}")
    print(f"  identifiers whose row 0 was edited: {R['n_row0_edited_ids']}")
    print(f"  ... of which HISTORICAL rows      : {R['n_retro_hist_events']} events"
          f" on {R['n_retro_hist_ids']} identifiers,"
          f" in {R['n_transitions_with_retro_hist']} transitions")
    print(f"  pure appends / tail-closes       : {R['n_append_events']}"
          f" / {R['n_tail_close_events']}")
    print("\n  most retro-edited identifiers:")
    for name, n in R["most_retro_edited"]:
        print(f"      {n:3d}  {name}")
    print("\nPREDICTION LEDGER")
    for k, v in R["predictions"].items():
        print(f"  [{'HELD ' if v['held'] else 'BROKE'}] {k}   -> {v['value']}")
    held = sum(1 for v in R["predictions"].values() if v["held"])
    print(f"\n  {held} of {len(R['predictions'])} held\n")

    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(R, f, indent=1, sort_keys=True)
    print("wrote results.json")


if __name__ == "__main__":
    main()
