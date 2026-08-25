#!/usr/bin/env python3
"""Post-hoc analysis of what the patchset grid holds and the commit grid does not.

measure.py scores the four predictions. This file asks the questions the answers
raised, and every one of them was written AFTER the numbers existed -- which is
why they live here and not in PREDICTIONS.md.

For each name and each (name, Changed) pair that exists in some patchset and in
no commit, it reports:
  * the changes it appears in, their status, and the patchsets that carry it
  * the value that landed instead, where the change was merged
  * the lifetime of the value inside review -- from the upload of the first
    patchset carrying it to the upload of the next patchset that does not

Stdlib only, offline, deterministic.  Usage: python3 analyse.py
Writes: findings.json
"""

import datetime
import json
import os

from measure import parse_state

HERE = os.path.dirname(os.path.abspath(__file__))


def ts(s):
    return datetime.datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S")


def main():
    g = json.load(open(os.path.join(HERE, "grids.json")))
    res = json.load(open(os.path.join(HERE, "results.json")))
    blobs = g["blobs"]

    parsed = {}
    for p in g["points"]:
        es, err = parse_state(blobs[p["blob"]])
        parsed[id(p)] = {e[0]: e for e in es}

    commits = [p for p in g["points"] if p["grid"] == "commit"]
    commit_names = {n for p in commits for n in parsed[id(p)]}
    commit_pairs = {(e[0], e[2]) for p in commits for e in parsed[id(p)].values()}

    by_change = {}
    for p in g["points"]:
        if p["grid"] == "patchset":
            by_change.setdefault(p["change"], []).append(p)
    for v in by_change.values():
        v.sort(key=lambda p: p["patchset"])

    def life(ps_list, holds):
        """First upload that holds the value, and the next upload that does not."""
        first = next((p for p in ps_list if holds(p)), None)
        if first is None:
            return None
        after = [p for p in ps_list if p["patchset"] > first["patchset"] and not holds(p)]
        last_hold = max(p["patchset"] for p in ps_list if holds(p))
        out = {"change": first["change"], "status": first["status"],
               "subject": first["subject"], "branch": first["branch"],
               "first_patchset": first["patchset"], "first_upload": first["created"][:19],
               "first_sha": first["point"], "last_patchset_holding": last_hold,
               "patchsets_total": max(p["patchset"] for p in ps_list),
               "patchsets_holding": sum(1 for p in ps_list if holds(p))}
        if after:
            nxt = min(after, key=lambda p: p["patchset"])
            out["replaced_at_patchset"] = nxt["patchset"]
            out["replaced_at"] = nxt["created"][:19]
            out["lifetime_seconds"] = int((ts(nxt["created"]) - ts(first["created"])).total_seconds())
        return out

    pair_rows = []
    for name, changed in [tuple(x) for x in res["P2"]["pairs"]]:
        for cn, ps_list in by_change.items():
            holds = lambda p, n=name, c=changed: parsed[id(p)].get(n, (None,) * 6)[2] == c \
                and n in parsed[id(p)]
            if not any(holds(p) for p in ps_list):
                continue
            row = life(ps_list, holds)
            row["name"], row["changed"] = name, changed
            # what the same change ended with, at its last patchset
            last = ps_list[-1]
            e = parsed[id(last)].get(name)
            row["value_at_last_patchset"] = None if e is None else e[2]
            row["name_present_at_last_patchset"] = e is not None
            row["name_ever_in_a_commit"] = name in commit_names
            pair_rows.append(row)

    name_rows = []
    for name in res["P1"]["names"]:
        for cn, ps_list in by_change.items():
            holds = lambda p, n=name: n in parsed[id(p)]
            if not any(holds(p) for p in ps_list):
                continue
            row = life(ps_list, holds)
            row["name"] = name
            row["values_seen"] = sorted({parsed[id(p)][name][2] for p in ps_list if holds(p)})
            name_rows.append(row)

    def bucket(rows):
        out = {}
        for r in rows:
            out.setdefault(r["status"], []).append(r)
        return {k: len(v) for k, v in sorted(out.items())}

    # values that were replaced INSIDE a change that later merged: the sharpest set,
    # because the change did land and the project's history still has no trace of them
    superseded = [r for r in pair_rows
                  if r["status"] == "MERGED" and "lifetime_seconds" in r]
    superseded.sort(key=lambda r: r["lifetime_seconds"])

    # --- the floor above: names that reached a commit and no release ------
    # Ordered by committer date, which is the order in which states entered
    # the project's history; author date is preserved across rebase and would
    # put a state before commits it actually followed.
    rel_names = {n for p in g["points"] if p["grid"] == "release"
                 for n in parsed[id(p)]}
    # master only: a state's successor is only defined along one lineage.
    coms = sorted([p for p in g["points"] if p["grid"] == "commit"
                   and p["master_rank"] is not None],
                  key=lambda p: -p["master_rank"])
    commit_only = []
    for name in sorted(commit_names - rel_names):
        car = [p for p in coms if name in parsed[id(p)]]
        if not car:
            commit_only.append({"name": name, "note": "never on origin/master"})
            continue
        idx = coms.index(car[-1])
        nxt = coms[idx + 1] if idx + 1 < len(coms) else None
        row = {"name": name,
               "value": list(parsed[id(car[0])][name]),
               "entered": car[0]["cdate"][:19], "entered_sha": car[0]["point"],
               "entered_subject": car[0]["subject"],
               "commits_carrying": len(car),
               "last_carrier": car[-1]["cdate"][:19],
               "in_newest_commit_state": name in parsed[id(coms[-1])]}
        if nxt is not None and name not in parsed[id(nxt)]:
            row["left"] = nxt["cdate"][:19]
            row["left_sha"] = nxt["point"]
            row["left_subject"] = nxt["subject"]
            row["lifetime_seconds"] = int(
                (ts(nxt["cdate"].replace("T", " ")) - ts(car[0]["cdate"].replace("T", " ")))
                .total_seconds())
        commit_only.append(row)

    # --- the descent: every value whose life is measurable, and the gap in
    # the grid one floor up that swallowed it ------------------------------
    # Go ships patch releases of several series at once, so the tag nearest in
    # time is usually a patch release of an older series and the interval
    # between adjacent tags means nothing. The unit of publication for a NEW
    # setting is the minor release, go1.N.0, and that is the grid used here.
    tags = sorted([(p["cdate"][:19].replace("T", " "), p["point"])
                   for p in g["points"] if p["grid"] == "release"
                   and p["point"].endswith(".0")])
    def enclosing(start, end):
        prev = max((t for t in tags if t[0] <= start), default=None)
        nxt = min((t for t in tags if t[0] >= end), default=None)
        if not prev or not nxt:
            return None
        return {"after": prev[1], "after_at": prev[0], "before": nxt[1],
                "before_at": nxt[0],
                "gap_seconds": int((ts(nxt[0]) - ts(prev[0])).total_seconds())}

    descent = []
    for r in superseded:
        d = {"floor": "review", "name": r["name"], "changed": r["changed"],
             "start": r["first_upload"], "end": r["replaced_at"],
             "lifetime_seconds": r["lifetime_seconds"], "change": r["change"],
             "detail": "CL %d, patch set %d to %d" % (r["change"], r["first_patchset"],
                                                      r["replaced_at_patchset"])}
        d["enclosing_release_interval"] = enclosing(d["start"], d["end"])
        descent.append(d)
    for r in commit_only:
        if "lifetime_seconds" not in r:
            continue
        d = {"floor": "commit", "name": r["name"], "changed": r["value"][2],
             "start": r["entered"].replace("T", " "), "end": r["left"].replace("T", " "),
             "lifetime_seconds": r["lifetime_seconds"],
             "detail": "master, added then reverted"}
        d["enclosing_release_interval"] = enclosing(d["start"], d["end"])
        descent.append(d)
    descent.sort(key=lambda d: d["lifetime_seconds"])

    findings = {
        "session": 70,
        "date": "2026-08-25",
        "note": "Written after the predictions were scored. Post-hoc throughout.",
        "descent": descent,
        "commit_grid_only": commit_only,
        "pairs_by_change_status": bucket(pair_rows),
        "names_by_change_status": bucket(name_rows),
        "superseded_inside_a_merged_change": superseded,
        "pair_rows": sorted(pair_rows, key=lambda r: (r["name"], r["changed"])),
        "name_rows": sorted(name_rows, key=lambda r: r["name"]),
        "commit_grid": {"names": len(commit_names), "pairs": len(commit_pairs)},
    }
    json.dump(findings, open(os.path.join(HERE, "findings.json"), "w"), indent=1)

    print("pairs by status of the change:", findings["pairs_by_change_status"])
    print("names by status of the change:", findings["names_by_change_status"])
    print("\nreplaced inside a change that later merged, shortest life first:")
    for r in superseded:
        print("  %-34s Changed:%-3d %6.1f h  ps%d->%d  landed as %s  CL %d"
              % (r["name"], r["changed"], r["lifetime_seconds"] / 3600.0,
                 r["first_patchset"], r["replaced_at_patchset"],
                 r["value_at_last_patchset"], r["change"]))


if __name__ == "__main__":
    main()
