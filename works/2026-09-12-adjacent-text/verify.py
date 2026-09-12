#!/usr/bin/env python3
"""verify.py -- Session 88, 2026-09-12.

This night measures over a corpus it did not harvest: the 22 WHATWG living standards Session 87
fetched, parsed and committed on 2026-09-11.  Re-using it rather than re-fetching is deliberate --
the harvest cost that night two hours and five refusals at the network gateway, and a second harvest
would produce a second, differently-refused corpus.

What must be true before anything is reported:

  1. the two inherited files are byte-identical to what Session 87 committed (SHA-256, recorded in
     sources/MANIFEST.json), and
  2. the population this night draws from is derivable from them by the rule PREDICTIONS.md §2
     states, with no code of mine touching the classification.

Run it first.  score.py refuses to run if it has not passed.
"""

import gzip
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "2026-09-11-eleven-sentences"

# SHA-256 of the two inherited files, as they stand in the commit that landed Session 87.
EXPECT = {
    "occurrences.json.gz": "9099b60aaa875c47",
    "corpus.json.gz": "5a24235076dc0d7f",
}

POPULATION = 1190  # B-FORM and AGENTLESS and NORM -- PREDICTIONS.md §2, fixed before the draw


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ok = True
    digests = {}
    for name, prefix in EXPECT.items():
        p = SRC / name
        if not p.exists():
            print("MISSING  %s" % p)
            ok = False
            continue
        d = sha256(p)
        digests[name] = d
        good = d.startswith(prefix)
        ok &= good
        print("%-22s %s  %s" % (name, d, "OK" if good else "CHANGED -- expected %s..." % prefix))

    occ = json.load(gzip.open(SRC / "occurrences.json.gz"))
    pop = [x for x in occ
           if x["form"] == "B-FORM" and x["agent"] == "AGENTLESS" and x["register"] == "NORM"]
    print("population  %d  (expected %d)  %s"
          % (len(pop), POPULATION, "OK" if len(pop) == POPULATION else "CHANGED"))
    ok &= len(pop) == POPULATION

    (HERE / "verification.json").write_text(json.dumps({
        "session": 88, "date": "2026-09-12",
        "inherited_from": "works/2026-09-11-eleven-sentences",
        "sha256": digests,
        "population_rule": "form == B-FORM and agent == AGENTLESS and register == NORM",
        "population": len(pop),
        "occurrences_total": len(occ),
        "passed": bool(ok),
    }, indent=1) + "\n")

    print("\n%s" % ("PASSED" if ok else "FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
