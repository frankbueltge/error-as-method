#!/usr/bin/env python3
"""Draw the hand-adjudicated sample.  PREDICTIONS.md §3, P6: 80 rows, random.Random(86),
40 from AGENTLESS UPPER and 40 from AGENTLESS LOWER, both after the strict rule.

The seed is the session number and the scheme was fixed before this file ran.  The draw is
uniform over each population; no row is skipped, replaced or re-drawn.
"""

import gzip
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
N_PER_ARM = 40
SEED = 86


def main():
    rows = json.load(gzip.open(HERE / "occurrences.json.gz", "rt"))
    pops = {c: [r for r in rows if r["case"] == c and r["agent"] == "AGENTLESS"]
            for c in ("UPPER", "LOWER")}
    rng = random.Random(SEED)
    sample = []
    for arm in ("UPPER", "LOWER"):
        pop = sorted(pops[arm], key=lambda r: (r["rfc"], r["para"], r["offset"]))
        picked = rng.sample(range(len(pop)), N_PER_ARM)
        for j, idx in enumerate(sorted(picked)):
            r = dict(pop[idx])
            r["id"] = "%s%02d" % (arm[0], j + 1)
            r["population_size"] = len(pop)
            sample.append(r)
    (HERE / "audit-sample.json").write_text(json.dumps(
        {"seed": SEED, "n_per_arm": N_PER_ARM,
         "population": {k: len(v) for k, v in pops.items()},
         "rows": sample}, indent=1) + "\n")
    print("populations: UPPER %d, LOWER %d" % (len(pops["UPPER"]), len(pops["LOWER"])))
    for r in sample:
        s = r["sentence"]
        i = r["offset"]
        print("\n%s  rfc%d  [%s %s]  slot=%s" % (r["id"], r["rfc"], r["modal"], r["case"],
                                                 r["slot_token"]))
        print("   ..." + s[max(0, i - 150):i + 160].strip() + "...")


if __name__ == "__main__":
    main()
