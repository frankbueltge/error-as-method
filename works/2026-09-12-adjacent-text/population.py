#!/usr/bin/env python3
"""population.py -- the same mechanical scan, over all 1,190 rather than over the 60.

score.py bounds the adjudicator on the sample.  This runs the identical scan across the whole
population, so the curve in figure.svg and in work.md §6 is a fact about the corpus and not about a
draw of sixty.  The party-term list is read out of results.json rather than restated, so the two
scans cannot drift apart.

Run after score.py.
"""

import gzip
import json
import re
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "2026-09-11-eleven-sentences"
WINDOWS = (0, 1, 2, 3, 5, 8, 13, 20, 35, 50, 100, 200)


def main():
    res = json.load(open(HERE / "results.json"))
    party = re.compile(res["mechanical_ceiling"]["party_terms"], re.IGNORECASE)

    corpus = json.load(gzip.open(SRC / "corpus.json.gz"))
    occ = json.load(gzip.open(SRC / "occurrences.json.gz"))
    pop = [x for x in occ
           if x["form"] == "B-FORM" and x["agent"] == "AGENTLESS" and x["register"] == "NORM"]

    nearest = []
    for x in pop:
        blocks = corpus[x["doc"]]["blocks"]
        i = x["block"]
        d = None
        for k in range(0, i + 1):
            if party.search(blocks[i - k]["t"]):
                d = k
                break
        nearest.append(d)

    present = [d for d in nearest if d is not None]
    out = {
        "note": "the same mechanical scan as score.py, over the whole population of agentless "
                "obligations rather than over the 60 sampled. A party term in reach is a CEILING on "
                "naming, never naming itself: score.py's hand reading puts 11 of the 18 windows with "
                "a term at five blocks or closer as actually naming the bearer of that obligation.",
        "party_terms": res["mechanical_ceiling"]["party_terms"],
        "population": len(pop),
        "curve": {str(w): sum(1 for d in present if d <= w) for w in WINDOWS},
        "whole_document": len(present),
        "none_anywhere": len(pop) - len(present),
        "median_distance_where_present": statistics.median(present),
        "mean_distance_where_present": round(sum(present) / len(present), 1),
    }
    (HERE / "population-curve.json").write_text(json.dumps(out, indent=1) + "\n")

    for w in WINDOWS:
        print("  window %-4d %5d of %d  (%.1f%%)"
              % (w, out["curve"][str(w)], len(pop), 100.0 * out["curve"][str(w)] / len(pop)))
    print("  whole doc  %5d of %d  (%.1f%%)   none anywhere: %d"
          % (len(present), len(pop), 100.0 * len(present) / len(pop), out["none_anywhere"]))
    print("  median %s  mean %s" % (out["median_distance_where_present"],
                                    out["mean_distance_where_present"]))


if __name__ == "__main__":
    main()
