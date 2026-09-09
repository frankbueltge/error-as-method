#!/usr/bin/env python3
"""Score the night, and re-run the afterlife scan repaired — the repair scoring nothing.

Two things happen here and they are kept apart on purpose.

  1. SCORING. The six predictions of `PREDICTIONS.md` are scored against the instrument exactly
     as it was pre-registered, faults included. A prediction scored against a repaired instrument
     is a prediction scored after seeing the answer.

  2. THE REPAIR, POST-HOC. The pre-registered scan matched keys as bare substrings over every
     `.md` and `.json` file in the record. Twelve of the twenty rows drawn for *the offer* are
     other people's legislation — 'the offering of goods or services' inside a harvested corpus,
     and inside this line's own generated results files carrying that corpus. The repair is two
     rules: match on word boundaries, and look only at what this practice wrote (`.md`, and the
     `meta.json` it writes by hand). It is run here, reported beside the pre-registered numbers,
     and scores nothing.

    python3 score.py
"""
import json
import os
import re
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATED = re.compile(r"(\d{4}-\d{2}-\d{2})")
TONIGHT = "2026-09-09"   # see measure.py and F-127


def own_writing(rel):
    """What this practice wrote, as against what it harvested or generated.

    `.md` is written by hand. `meta.json` is written by hand. Every other `.json` in a work
    directory is a corpus, a result or an adjudication emitted by that night's code, and the
    text inside it is frequently somebody else's.
    """
    return rel.endswith(".md") or os.path.basename(rel) == "meta.json"


def repaired_scan(satellites):
    out = {}
    for sat in satellites:
        pats = [re.compile(r"(?<![A-Za-z])" + re.escape(k) + r"(?![A-Za-z])", re.I)
                for k in sat["keys"]]
        hits = []
        for base in ("journal", "works"):
            for dirpath, _dirs, names in os.walk(os.path.join(ROOT, base)):
                for name in sorted(names):
                    rel = os.path.relpath(os.path.join(dirpath, name), ROOT)
                    if not own_writing(rel):
                        continue
                    found = DATED.search(rel)
                    # Same window as measure.py, and for the same reason (F-127): after the minting
                    # night, before tonight.
                    if not found or not (sat["minted"] < found.group(1) < TONIGHT):
                        continue
                    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
                        for n, line in enumerate(fh.read().splitlines(), 1):
                            if any(p.search(line) for p in pats):
                                hits.append({"file": rel, "line": n})
        out[sat["id"]] = {"name": sat["name"], "n_contexts": len(hits),
                          "n_files": len({h["file"] for h in hits})}
    return out


def main():
    with open(os.path.join(HERE, "candidates.json"), encoding="utf-8") as fh:
        census = json.load(fh)
    with open(os.path.join(HERE, "results.json"), encoding="utf-8") as fh:
        results = json.load(fh)
    with open(os.path.join(HERE, "sample.json"), encoding="utf-8") as fh:
        sample = json.load(fh)
    with open(os.path.join(HERE, "adjudication.json"), encoding="utf-8") as fh:
        adj = json.load(fh)["rows"]

    # --- the adjudicated sample -------------------------------------------------------------
    scored = {}
    for key, rows in adj.items():
        drawn = sample["samples"][key]
        counts = {"use": 0, "attendance": 0, "noise": 0}
        for row in rows:
            counts[row["verdict"]] += 1
        if len(rows) != drawn["drawn"]:
            raise SystemExit(f"{key}: adjudicated {len(rows)} rows, drew {drawn['drawn']}")
        real = counts["use"] + counts["attendance"]
        scored[key] = {
            "name": drawn["name"], "population": drawn["population"], "drawn": drawn["drawn"],
            "census": drawn["census"], **counts,
            "use_rate_of_real_contexts": round(counts["use"] / real, 3) if real else None,
            "noise_rate": round(counts["noise"] / drawn["drawn"], 3) if drawn["drawn"] else None,
            "estimated_uses_in_population": (
                round(drawn["population"] * counts["use"] / drawn["drawn"], 1)
                if drawn["drawn"] else 0),
        }

    lex = results["lexical"]
    outside = [r for r in lex if r["verdict"] == "outside" and r["tested"]]
    moved = [r for r in lex if r["verdict"] == "entered-the-sentence" and r["tested"]]

    sat_ids = ["S60", "S71", "S78", "S84"]          # Session 84's own list of four
    sat_uses = {k: scored[k]["estimated_uses_in_population"] for k in sat_ids}
    satellites_only = [sat_uses[k] for k in ("S60", "S78", "S84")]

    p1 = "LOST" if moved else "WON"
    p2_num = sum(1 for r in outside if r["n_new"] > 0)
    p2 = "WON" if p2_num / len(outside) >= 0.80 else "LOST"
    heaviest = max(results["load"].items(), key=lambda kv: len(kv[1]))
    p3 = "WON" if heaviest[0] == "observer" and len(heaviest[1]) >= 3 else "LOST"
    p4_num = sum(1 for k in sat_ids if scored[k]["use"] > 0)
    p4 = "WON" if p4_num == 4 else "LOST"
    p5 = "WON" if sat_uses["S71"] > statistics.median(satellites_only) else "LOST"
    p6_actual = max(sat_uses, key=lambda k: sat_uses[k])

    verdicts = [
        ["P1", "no candidate entered the sentence", f"{len(moved)} did ({', '.join(r['id'] for r in moved)})", p1],
        ["P2", "every outside candidate needs a new word", f"{p2_num} of {len(outside)}", p2],
        ["P3", "'observer' carries the most readings, >= 3", f"{heaviest[0]}, {len(heaviest[1])}", p3],
        ["P4", "all four satellites have >= 1 use", f"{p4_num} of 4", p4],
        ["P5", "the promoted claim beats the median satellite", f"{sat_uses['S71']} vs {statistics.median(satellites_only)}", p5],
        ["P6", "the most-used satellite is the offer (unscorable)", f"{p6_actual}", "wrong" if p6_actual != "S78" else "right"],
    ]

    repaired = repaired_scan(census["satellites"])

    out = {
        "_what": "The scoring pass. Predictions scored against the instrument as pre-registered; "
                 "the repaired scan is beside them and scores nothing.",
        "adjudicated": scored,
        "predictions": [{"id": v[0], "prediction": v[1], "observed": v[2], "verdict": v[3]}
                        for v in verdicts],
        "repaired_post_hoc": repaired,
        "repair_rules": ["keys matched on word boundaries",
                         "only files this practice wrote: *.md and hand-written meta.json"],
    }
    with open(os.path.join(HERE, "score.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=True)
        fh.write("\n")

    print(f"{'':6s}{'claim':26s}{'pop':>5s}{'drawn':>7s}{'use':>5s}{'att':>5s}{'noise':>7s}{'est. uses':>11s}")
    for key in ("S50", "S60", "S71", "S78", "S84"):
        s = scored[key]
        print(f"{key:6s}{s['name']:26s}{s['population']:5d}{s['drawn']:7d}"
              f"{s['use']:5d}{s['attendance']:5d}{s['noise']:7d}{s['estimated_uses_in_population']:11}")
    print()
    for v in verdicts:
        print(f"{v[0]}  {v[1]:48s} {v[2]:28s} {v[3]}")
    print()
    print("post-hoc, repaired scan (scores nothing):")
    for key, val in sorted(repaired.items()):
        print(f"  {key:5s} {val['name']:24s} {val['n_contexts']:4d} contexts in {val['n_files']:3d} files")


if __name__ == "__main__":
    main()
