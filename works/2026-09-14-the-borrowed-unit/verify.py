#!/usr/bin/env python3
"""verify.py -- the four checks this night must pass before any number of its own is read.

1. THE REPLICATION.  The WHATWG arm is Session 88's own measurement, recomputed by code written
   two nights later that shares no line with `population.py`.  Every cell of its block curve must
   come out identical -- twelve windows, the whole-document count, the five with nothing anywhere,
   the median and the mean.  If it does not, this night has no standing to port anything.
2. THE RE-DERIVED PARAGRAPHS.  Session 86's `para` field is a sentence ordinal.  `corpora.rfc()`
   re-derives the paragraph division from the committed text; every one of the 2,952 stored
   occurrences must sit at a sentence byte-identical to the sentence standing at its own index.
3. THE POPULATIONS.  The three counts must match what the nights that built them reported.
4. THE TERM LIST.  The 26 base terms are read out of Session 88's results.json, not restated; this
   checks the parse round-trips to the exact pattern that file holds.

Exits non-zero on any failure.  Writes verification.json.
"""

import gzip
import json
import sys
from pathlib import Path

import corpora
import reach

HERE = Path(__file__).resolve().parent
S86 = corpora.S86
S88 = corpora.S88


def main():
    checks, failures = [], []

    # ---- 1. the replication
    want = json.load(open(S88 / "population-curve.json"))
    got = json.load(open(HERE / "results.json"))["corpora"]["whatwg"]["row"]["blocks"]
    cells = [("population", want["population"], got["population"]),
             ("whole_document", want["whole_document"], got["whole_document"]),
             ("none_anywhere", want["none_anywhere"], got["none_anywhere"]),
             ("median", want["median_distance_where_present"], got["median_where_present"]),
             ("mean", want["mean_distance_where_present"], got["mean_where_present"])]
    for w in reach.BLOCK_WINDOWS:
        cells.append(("window %d" % w, want["curve"][str(w)], got["counts"][str(w)]))
    bad = [(k, a, b) for k, a, b in cells if a != b]
    checks.append({"check": "replication of Session 88's block curve, independent code",
                   "cells": len(cells), "mismatched": bad, "ok": not bad})
    if bad:
        failures.append("replication: %s" % bad)

    # ---- 2. the re-derived RFC paragraphs
    blocks, s2p, sents = corpora.rfc_blocks()
    occ = json.load(gzip.open(S86 / "occurrences.json.gz"))
    mismatched = 0
    for x in occ:
        stream = sents[x["rfc"]]
        if x["para"] >= len(stream) or stream[x["para"]] != x["sentence"]:
            mismatched += 1
    checks.append({"check": "every stored RFC occurrence sits at its own sentence index",
                   "occurrences": len(occ), "mismatched": mismatched, "ok": mismatched == 0})
    if mismatched:
        failures.append("rfc sentence index: %d mismatched" % mismatched)

    # ---- 3. the populations
    expect = {"whatwg": 1190, "eu": 3864, "rfc": 956}
    pops = {}
    for name in expect:
        rows, _ = corpora.CORPORA[name]()
        pops[name] = len(rows)
    checks.append({"check": "populations", "expected": expect, "got": pops,
                   "ok": pops == expect})
    if pops != expect:
        failures.append("populations: %s" % pops)

    # ---- 4. the term list round-trips
    base = corpora.base_terms()
    rebuilt = r"\b(" + "|".join(base) + r")\b"
    ok = rebuilt == corpora.whatwg_terms() and len(base) == 26
    checks.append({"check": "the 26 base terms parse back to Session 88's exact pattern",
                   "terms": len(base), "ok": ok})
    if not ok:
        failures.append("term list did not round-trip")

    (HERE / "verification.json").write_text(
        json.dumps({"checks": checks, "failures": failures, "passed": not failures}, indent=1) + "\n")
    for c in checks:
        print("  [%s] %s" % ("ok" if c["ok"] else "FAIL", c["check"]))
    if failures:
        print("\nVERIFICATION FAILED", file=sys.stderr)
        sys.exit(1)
    print("\nall four checks pass.")


if __name__ == "__main__":
    main()
