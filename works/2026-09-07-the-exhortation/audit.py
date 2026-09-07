#!/usr/bin/env python3
"""Draws the three hand-audit samples fixed in PREDICTIONS.md §4.

Seed 20260907, written into PREDICTIONS.md before this file existed.  The scheme -- the verdict
labels and their definitions -- was also written there before any row was drawn, because Session
82's open thread 3 named inventing the scheme while adjudicating as the worst time to invent one.

This script draws and writes.  It adjudicates nothing.  The verdicts are entered by hand in
verdicts.py and scored by write_audit.py.
"""

import gzip
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
S82 = HERE.parent / "2026-09-06-the-rate-of-the-rule"
SEED = 20260907

corpus = json.load(gzip.open(S82 / "corpus.json.gz", "rt"))
res = json.load(open(HERE / "results.json"))
acts = {a["celex"]: a for a in res["acts"]}
family_a = json.load(open(HERE / "family-a.json"))

rng = random.Random(SEED)

# ---- 4a: 40 recitals from Session 82's repaired *directed* set -----------------------------------
directed = []
for celex, a in sorted(acts.items()):
    for div in a["s82_directed"]:
        directed.append({
            "id": "A-%s-r%s" % (celex, div),
            "celex": celex, "division": div, "stratum": a["stratum"],
            "text": corpus[celex]["recitals"][str(div)],
        })
sample_a = rng.sample(directed, 40)

# ---- 4b: up to 40 Family A matches ---------------------------------------------------------------
pool_b = [dict(h, id="B-%02d" % i) for i, h in enumerate(family_a)]
sample_b = rng.sample(pool_b, min(40, len(pool_b)))

# ---- 4c: 30 recitals the rule did NOT match, from acts that exhort somewhere ----------------------
exhorting = {a["celex"] for a in res["acts"]
             if a["recitals"]["family_a"] > 0 or a["articles"]["family_a"] > 0}
unmatched = []
for celex in sorted(exhorting):
    hit_divs = set(acts[celex]["recitals"]["family_a_divisions"])
    for div, text in corpus[celex]["recitals"].items():
        if div not in hit_divs:
            unmatched.append({
                "id": "C-%s-r%s" % (celex, div),
                "celex": celex, "division": div, "text": text,
            })
sample_c = rng.sample(unmatched, 30)

out = {
    "seed": SEED,
    "pools": {
        "directed_recitals": len(directed),
        "family_a_matches": len(pool_b),
        "unmatched_recitals_in_exhorting_acts": len(unmatched),
        "exhorting_acts": len(exhorting),
    },
    "sample_a_10_5_2": sample_a,
    "sample_b_precision": sample_b,
    "sample_c_recall": sample_c,
}
json.dump(out, open(HERE / "audit-sample.json", "w"), indent=1)
print(json.dumps(out["pools"], indent=1))
print("drawn: %d / %d / %d" % (len(sample_a), len(sample_b), len(sample_c)))
