#!/usr/bin/env python3
"""sample -- Session 87, 2026-09-11.  The draw, fixed in PREDICTIONS.md §5 before it ran.

Session 86 drew 40 + 40 stratified by case and, because both strata sat inside the agentless
B-FORM population, ended with a sample that could only speak about agentless passives -- 73 of its
80 rows carry the same label.  This draw is deliberately unstratified: 60 rows from **every** modal
occurrence in the normative register, in the order `measure.py` emits them, `random.Random(87)`.
"""

import gzip
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 87
N = 60


def main():
    rows = json.load(gzip.open(HERE / "occurrences.json.gz", "rt"))
    pop = [r for r in rows if r["register"] == "NORM"]
    rng = random.Random(SEED)
    draw = rng.sample(range(len(pop)), N)
    out = []
    for n, i in enumerate(sorted(draw), 1):
        r = dict(pop[i])
        r["id"] = "W%02d" % n
        r["population_index"] = i
        out.append(r)
    (HERE / "audit-sample.json").write_text(json.dumps(
        {"seed": SEED, "n": N, "population": "every modal occurrence in the NORM register",
         "population_size": len(pop), "stratified": False, "rows": out}, indent=1) + "\n")
    for r in out:
        print("%s  %-12s %-6s %-7s %s" % (r["id"], r["doc"], r["modal"], r["form"],
                                          r["sentence"][:150]))


if __name__ == "__main__":
    main()
