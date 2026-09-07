#!/usr/bin/env python3
"""Joins the hand verdicts to the drawn rows, writes audit.json with every row's full text, and
computes the audit results.  Computes; it does not judge.  If a drawn id has no verdict, this
exits rather than defaulting -- an unadjudicated row must not silently become a category."""

import json
import sys
from collections import Counter
from pathlib import Path

import verdicts

HERE = Path(__file__).resolve().parent
sample = json.load(open(HERE / "audit-sample.json"))

rows = {"sample_a_10_5_2": [], "sample_b_precision": [], "sample_c_recall": []}
missing = []

for r in sample["sample_a_10_5_2"]:
    v = verdicts.SAMPLE_A.get(r["id"])
    if v is None:
        missing.append(r["id"])
        continue
    rows["sample_a_10_5_2"].append(dict(r, verdict=v[0], note=v[1]))

for r in sample["sample_b_precision"]:
    v = verdicts.SAMPLE_B.get(r["id"])
    if v is None:
        missing.append(r["id"])
        continue
    row = dict(r, verdict=v[0], note=v[1])
    if r["id"] in verdicts.ATTRIBUTION_WRONG:
        row["attribution_wrong"] = verdicts.ATTRIBUTION_WRONG[r["id"]]
    rows["sample_b_precision"].append(row)

for r in sample["sample_c_recall"]:
    v = verdicts.SAMPLE_C.get(r["id"], verdicts.SAMPLE_C_DEFAULT)
    row = dict(r, verdict=v[0], note=v[1])
    if r["id"] in verdicts.SAMPLE_C_NOTES:
        row["observation"] = verdicts.SAMPLE_C_NOTES[r["id"]]
    rows["sample_c_recall"].append(row)

if missing:
    print("UNADJUDICATED ROWS -- writing nothing:", file=sys.stderr)
    for m in missing:
        print("  " + m, file=sys.stderr)
    sys.exit(1)

a = Counter(r["verdict"] for r in rows["sample_a_10_5_2"])
b = Counter(r["verdict"] for r in rows["sample_b_precision"])
c = Counter(r["verdict"] for r in rows["sample_c_recall"])

by_verb = {}
for r in rows["sample_b_precision"]:
    d = by_verb.setdefault(r["verb"], Counter())
    d[r["verdict"]] += 1

exhortations = [r for r in rows["sample_b_precision"] if r["verdict"] == "EXHORTATION"]
by_part = Counter(r["part"] for r in exhortations)

results = {
    "sample_a_10_5_2": {
        "n": sum(a.values()), "verdicts": dict(a),
        "reasoned_share": round(a["REASONED"] / sum(a.values()), 3),
        "unit": "the whole recital, not the matched sentence -- see the work; this is NOT comparable "
                "to Session 82's sentence-level audit and does not vindicate it",
    },
    "sample_b_precision": {
        "n": sum(b.values()), "verdicts": dict(b),
        "precision": round(b["EXHORTATION"] / sum(b.values()), 3),
        "by_verb": {k: {"n": sum(v.values()), "exhortation": v["EXHORTATION"],
                        "precision": round(v["EXHORTATION"] / sum(v.values()), 3)}
                    for k, v in sorted(by_verb.items())},
        "exhortations_by_part": dict(by_part),
        "attribution_wrong": len(verdicts.ATTRIBUTION_WRONG),
        "attribution_wrong_share": round(len(verdicts.ATTRIBUTION_WRONG) / max(1, len(exhortations)), 3),
    },
    "sample_c_recall": {"n": sum(c.values()), "verdicts": dict(c),
                        "observations": len(verdicts.SAMPLE_C_NOTES)},
}

json.dump(rows, open(HERE / "audit.json", "w"), indent=1)
json.dump(results, open(HERE / "audit-results.json", "w"), indent=1)
print(json.dumps(results, indent=1))
