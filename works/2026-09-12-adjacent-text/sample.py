#!/usr/bin/env python3
"""sample.py -- draw the 60, and print them in isolation.

Two outputs, and the separation between them is the whole point:

  sample.json   the 60 rows with their sentences and their corpus coordinates
  stage1.txt    the 60 sentences and NOTHING else -- no document, no heading, no neighbour

Stage 1 is adjudicated from stage1.txt.  stage2.py, which assembles the context windows, is not run
until stage1-verdicts.json exists.  PREDICTIONS.md §3 says this is a procedure rather than a proof,
and it is.
"""

import gzip
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "2026-09-11-eleven-sentences"
SEED = 88          # the session number
N = 60


def main():
    occ = json.load(gzip.open(SRC / "occurrences.json.gz"))
    pop = [x for x in occ
           if x["form"] == "B-FORM" and x["agent"] == "AGENTLESS" and x["register"] == "NORM"]
    pop.sort(key=lambda x: (x["doc"], x["block"], x["offset"]))

    rows = random.Random(SEED).sample(pop, N)
    rows.sort(key=lambda x: (x["doc"], x["block"], x["offset"]))

    out = []
    for i, r in enumerate(rows, 1):
        out.append({
            "id": "S%02d" % i,
            "doc": r["doc"],
            "block": r["block"],
            "offset": r["offset"],
            "modal": r["modal"],
            "slot_token": r["slot_token"],
            "sentence": r["sentence"],
        })

    (HERE / "sample.json").write_text(json.dumps(
        {"seed": SEED, "n": N, "population": len(pop),
         "rule": "form == B-FORM and agent == AGENTLESS and register == NORM",
         "rows": out}, indent=1) + "\n")

    with open(HERE / "stage1.txt", "w") as fh:
        fh.write("# Stage 1 -- the sentence and nothing else.  %d rows, seed %d.\n\n" % (N, SEED))
        for r in out:
            fh.write("%s  %s\n\n" % (r["id"], r["sentence"]))

    print("wrote sample.json and stage1.txt -- %d of %d" % (N, len(pop)))


if __name__ == "__main__":
    main()
