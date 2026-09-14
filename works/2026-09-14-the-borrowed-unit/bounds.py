#!/usr/bin/env python3
"""bounds.py -- what the instrument's input looks like, computed BEFORE any prediction is fixed.

Session 88 filed F-137 against itself: a threshold written without computing what the instrument
could possibly return.  Session 82 asked for a sweep for bars nothing could fail; Session 88 found
the inverse and said the category needed widening in both directions.  This file is that lesson
applied forwards, on the one night that inherits both.

`S88.REACH` fixes its test in BLOCKS -- "falsified if either corpus comes in at or below 13.6 % at
window 0", where window 0 is the obligation's own block.  A block is not a unit the three traditions
share; the row says so itself, in the clause headed *what this row cannot do*.  What the row does not
do is say how far apart the units are, and that is a fact about the committed inputs alone: it needs
no party-term list, no scan and no answer.  So it is computed here, first, and the predictions in
PREDICTIONS.md are written against it.

Nothing in this file counts a party term.  Its only output is geometry.

Run first.  Writes bounds.json.
"""

import json
import re
import statistics
from pathlib import Path

import corpora

HERE = Path(__file__).resolve().parent
WORD = re.compile(r"\S+")


def words(s):
    return len(WORD.findall(s))


def quantiles(xs):
    xs = sorted(xs)
    def q(p):
        if not xs:
            return None
        return xs[min(len(xs) - 1, int(round(p * (len(xs) - 1))))]
    return {"min": xs[0], "q1": q(0.25), "median": q(0.5), "q3": q(0.75), "p90": q(0.90),
            "max": xs[-1], "mean": round(sum(xs) / len(xs), 1)}


def main():
    out = {
        "note": "geometry of the three committed corpora, computed before any prediction was "
                "fixed and before any party term was counted. The unit of S88.REACH's test is the "
                "block; these are the blocks.",
        "corpora": {},
    }
    for name in ("whatwg", "eu", "rfc"):
        rows, blocks = corpora.CORPORA[name]()
        all_lengths = [words(t) for seq in blocks.values() for t in seq]
        host_lengths = [words(blocks[r["doc"]][r["block"]]) for r in rows]
        # how much text stands behind an obligation at all, in blocks and in words
        behind_blocks = [r["block"] for r in rows]
        behind_words = []
        for r in rows:
            seq = blocks[r["doc"]]
            behind_words.append(sum(words(t) for t in seq[:r["block"]]))
        out["corpora"][name] = {
            "documents": len(blocks),
            "blocks": len(all_lengths),
            "population": len(rows),
            "words_per_block_all": quantiles(all_lengths),
            "words_per_block_hosting_an_obligation": quantiles(host_lengths),
            "blocks_behind_the_obligation": quantiles(behind_blocks),
            "words_behind_the_obligation": quantiles(behind_words),
        }
        c = out["corpora"][name]
        print("%-7s %3d docs %7d blocks  pop %5d   median words/block %5s  "
              "median words/block hosting an obligation %6s"
              % (name, c["documents"], c["blocks"], c["population"],
                 c["words_per_block_all"]["median"],
                 c["words_per_block_hosting_an_obligation"]["median"]))

    # the ratio that matters, stated as a ratio rather than left to be read off two tables
    med = {k: v["words_per_block_hosting_an_obligation"]["median"] for k, v in out["corpora"].items()}
    out["ratio_of_hosting_block_medians"] = {
        "eu_over_whatwg": round(med["eu"] / med["whatwg"], 2),
        "rfc_over_whatwg": round(med["rfc"] / med["whatwg"], 2),
    }
    print("\n  median hosting block, EU / WHATWG  = %.2f" % out["ratio_of_hosting_block_medians"]["eu_over_whatwg"])
    print("  median hosting block, RFC / WHATWG = %.2f" % out["ratio_of_hosting_block_medians"]["rfc_over_whatwg"])
    (HERE / "bounds.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
