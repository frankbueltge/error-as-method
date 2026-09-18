#!/usr/bin/env python3
"""Scores the six predictions of PREDICTIONS.md against results.json. Writes adjudication.json.

Every condition is read out of the file that declared it and applied to the numbers the
instrument produced. No prediction is scored by hand here; if a condition cannot be evaluated
mechanically it is not in this file.

    python3 score.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "results.json"), encoding="utf-8") as fh:
    R = json.load(fh)

ALL = R["watch"]["all"]
OBS = ALL["per_term"]["observer"]["ratio"]
RANK = ALL["ratio_rank"]
GRIP = R["grip_post"]["share"]
AGREE = sum(1 for r in R["cross_check"] if r["agrees_with_me"])

rows = [
    {"id": "P1", "blind": True,
     "claim": "`observer` has the highest post/pre rate ratio of the eleven content terms "
              "(journal entries, Sessions 79-84 against 86-91, all text).",
     "observed": f"ratio rank: {', '.join(RANK[:3])} … — observer {OBS}",
     "verdict": "survives" if RANK and RANK[0] == "observer" else "FALSIFIED"},

    {"id": "P2", "blind": True,
     "claim": "More than 20 % of the post-window paragraphs containing `observer` also contain "
              "the string S85.OVERLOAD.",
     "observed": f"{R['grip_post']['also_naming_the_row']} of "
                 f"{R['grip_post']['observer_paragraphs']} = {GRIP}",
     "verdict": "survives" if GRIP is not None and GRIP > 0.20 else "FALSIFIED"},

    {"id": "P3", "blind": True,
     "claim": "`observer`'s post/pre rate ratio is above 1.5.",
     "observed": f"{OBS}",
     "verdict": "survives" if OBS is not None and OBS > 1.5 else "FALSIFIED"},

    {"id": "P4", "blind": True,
     "claim": "The machine's top sentence-term in each shape's own paragraph agrees with my "
              "`lands_on` verdict for at most 2 of the 5 shapes.",
     "observed": f"{AGREE} of {len(R['cross_check'])}",
     "verdict": "survives" if AGREE <= 2 else "FALSIFIED"},

    {"id": "P5", "blind": True,
     "claim": "In the pre window the highest-rate term of the eleven is `norm`.",
     "observed": f"{ALL['highest_pre_rate_term']}",
     "verdict": "survives" if ALL["highest_pre_rate_term"] == "norm" else "FALSIFIED"},

    {"id": "P6", "blind": False,
     "claim": "Seven of the eleven content terms carry zero fixed readings on Session 85's table.",
     "observed": f"{R['n_unread_terms']}: {', '.join(R['unread_terms'])}",
     "verdict": "survives" if R["n_unread_terms"] == 7 else "FALSIFIED"},
]

out = {
    "_what": "Session 92's predictions, declared in PREDICTIONS.md in a commit that precedes "
             "census.py, scored mechanically against results.json.",
    "blind": sum(1 for r in rows if r["blind"]),
    "survives": sum(1 for r in rows if r["verdict"] == "survives"),
    "falsified": sum(1 for r in rows if r["verdict"] == "FALSIFIED"),
    "rows": rows,
}
with open(os.path.join(HERE, "adjudication.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1, ensure_ascii=False, sort_keys=True)
    fh.write("\n")

for r in rows:
    tag = "blind" if r["blind"] else "declared, not blind"
    print(f"{r['id']} [{tag:>19}]  {r['verdict']:<9}  {r['observed']}")
print(f"\n{out['survives']} survive, {out['falsified']} falsified, {out['blind']} of 6 blind")
