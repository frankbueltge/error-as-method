#!/usr/bin/env python3
"""Draw the afterlife sample, with the seed fixed before the draw.

The afterlife scan finds 192 contexts across three claims old enough to have one. Adjudicating
192 by hand tonight would be a claim about my stamina rather than about the record, so this draws
20 per claim — every context where there are fewer than 20 — and every drawn row is adjudicated by
hand in `adjudication.json` with its reason. The rates that come out are sample rates over a named
population, reported as such.

Seed 85, the session number, fixed here before the draw and before any row was read.

    python3 sample.py
"""
import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 85
PER_CLAIM = 20


def main():
    with open(os.path.join(HERE, "afterlife.json"), encoding="utf-8") as fh:
        after = json.load(fh)

    rng = random.Random(SEED)
    out = {"_seed": SEED, "_per_claim": PER_CLAIM,
           "_what": "The seeded draw. Adjudicate every row of every sample in adjudication.json.",
           "samples": {}}

    for key in sorted(after):
        contexts = after[key]["contexts"]
        if not contexts:
            out["samples"][key] = {"name": after[key]["name"], "population": 0,
                                   "drawn": 0, "census": True, "rows": []}
            continue
        if len(contexts) <= PER_CLAIM:
            drawn, census = list(contexts), True
        else:
            drawn, census = rng.sample(contexts, PER_CLAIM), False
        drawn.sort(key=lambda c: (c["date"], c["file"], c["line"]))
        out["samples"][key] = {"name": after[key]["name"], "population": len(contexts),
                               "drawn": len(drawn), "census": census, "rows": drawn}

    with open(os.path.join(HERE, "sample.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=True)
        fh.write("\n")

    for key, val in sorted(out["samples"].items()):
        print(f"{key:5s} {val['name']:24s} population {val['population']:4d}  "
              f"drawn {val['drawn']:3d}  {'census' if val['census'] else 'sample'}")


if __name__ == "__main__":
    main()
