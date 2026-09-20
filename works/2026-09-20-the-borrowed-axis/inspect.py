#!/usr/bin/env python3
"""
inspect.py -- print every match reconcile.py counted, with its context, so that a reader can
do what the counter cannot: decide whether a hit is the term or an accident.

Written **after** reconcile.py had run, and deliberately not folded into it. reconcile.py's
normalisation is declared loose in one direction -- it deletes spaces and hyphens before
matching, so a term can be found inside a longer word (`especially` contains `special`) or
across a word gap the extractor dropped (`observe rather` contains `observer`). That
looseness is the right default for a count that must not undercount, and it is the wrong
tool for the question *is this word in the source*. So the counts stay as they were declared,
and the judgement is a second, separate, later, hand-made file: `judged.json`.

    python3 inspect.py [term ...]
"""

import os
import re
import sys

import reconcile

HERE = os.path.dirname(os.path.abspath(__file__))


def flat_with_map(readable_text):
    """The same flattening reconcile.py counts in, plus an index back to the readable text,
    so a match can be shown where it actually stands instead of being searched for again."""
    out, idx = [], []
    for i, ch in enumerate(readable_text):
        if ch in "-" or ch.isspace():
            continue
        out.append(ch.lower())
        idx.append(i)
    return "".join(out), idx


def main():
    wanted = sys.argv[1:] or list(reconcile.TERMS)
    for s in reconcile.SOURCES:
        path = os.path.join(HERE, "sources", s["text"])
        if not os.path.exists(path):
            print(f"\n=== {s['id']}: text not present -- re-fetch per sources/MANIFEST.json")
            continue
        raw = open(path, encoding="utf-8").read()
        read = reconcile.readable(raw)
        flat, idx = flat_with_map(read)
        assert flat == reconcile.flat(raw), "flattening drifted from reconcile.py"
        print(f"\n=== {s['id']}  ({len(flat)} chars, spaces and hyphens removed)")
        for term in wanted:
            hits = list(re.finditer(reconcile.TERMS[term], flat))
            print(f"  {term:11s} {len(hits)}")
            for m in hits:
                a, b = idx[m.start()], idx[m.end() - 1] + 1
                print(f"      [{m.start()}] ...{read[max(0, a - 55):b + 55]}...")


if __name__ == "__main__":
    main()
