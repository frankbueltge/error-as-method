#!/usr/bin/env python3
"""reach.py -- Session 88's scan, ported to two more traditions and measured in two units.

For every binding agentless obligation in three committed corpora, how far back must a reader look
before a word for a party is in reach?  Session 88 asked that of 1,190 obligations in 22 WHATWG
living standards and answered in blocks.  `S88.REACH` asked a later session to ask it of the EU acts
and the RFCs, and said that a session wanting the stronger claim should re-run in words and say that
it changed the unit.  Both units are run here, both declared in PREDICTIONS.md before this file
existed.

A party term in reach is a CEILING on a bearer actually named, never naming itself: Session 88's
hand reading of 60 windows put the precision at 0.611 in its own corpus, and that number is not
carried across traditions here.

Run after bounds.py.  Writes results.json.
"""

import bisect
import json
import re
import statistics
from pathlib import Path

import corpora

HERE = Path(__file__).resolve().parent
BLOCK_WINDOWS = (0, 1, 2, 3, 5, 8, 13, 20, 35, 50, 100, 200)
WORD_WINDOWS = (0, 5, 10, 25, 36, 50, 100, 200, 400, 800, 1600, 3200, 6400)
SEP = "\n"            # blocks are joined on a newline so no multi-word term can straddle a join
WORD = re.compile(r"\S+")

# the extensions S88.REACH named, with singular/plural variants and nothing else
EXTENSIONS = {
    "whatwg": [],
    "eu": ["Member State", "Member States", "the Commission"],
    "rfc": ["sender", "senders", "receiver", "receivers"],
}


def term_pattern(names):
    return r"\b(" + "|".join(sorted(names, key=len, reverse=True)) + r")\b"


def scan(name, term_list):
    """Returns per-row nearest distances in blocks and in words, plus the bookkeeping."""
    rows, blocks = corpora.CORPORA[name]()
    party = re.compile(term_pattern(term_list), re.IGNORECASE)

    docs = {}
    for doc, seq in blocks.items():
        text = SEP.join(seq)
        starts, off = [], 0
        for t in seq:
            starts.append(off)
            off += len(t) + len(SEP)
        # nearest previous block carrying a term, for every block index
        has = [bool(party.search(t)) for t in seq]
        prev = []
        last = None
        for i, h in enumerate(has):
            if h:
                last = i
            prev.append(last)
        docs[doc] = {
            "text": text,
            "starts": starts,
            "prev": prev,
            "term_ends": [m.end() for m in party.finditer(text)],
            "word_starts": [m.start() for m in WORD.finditer(text)],
        }

    block_d, word_d, duplicated = [], [], []
    for r in rows:
        d = docs[r["doc"]]
        i = r["block"]
        # ---- in blocks: the smallest k >= 0 with a term in the block k before this one
        p = d["prev"][i]
        block_d.append(None if p is None else i - p)
        # ---- in words: words strictly between the nearest preceding term and the modal
        seq_block = blocks[r["doc"]][i]
        if seq_block.count(r["sentence"]) > 1:
            duplicated.append({"doc": r["doc"], "block": i, "sentence": r["sentence"][:120]})
        pos = d["starts"][i] + seq_block.find(r["sentence"]) + r["offset"]
        j = bisect.bisect_right(d["term_ends"], pos)
        if j == 0:
            word_d.append(None)
        else:
            end = d["term_ends"][j - 1]
            ws = d["word_starts"]
            word_d.append(bisect.bisect_left(ws, pos) - bisect.bisect_left(ws, end))
    return rows, block_d, word_d, duplicated


def curve(dists, windows, n):
    present = [x for x in dists if x is not None]
    return {
        "population": n,
        "counts": {str(w): sum(1 for x in present if x <= w) for w in windows},
        "pct": {str(w): round(100.0 * sum(1 for x in present if x <= w) / n, 2) for w in windows},
        "whole_document": len(present),
        "whole_document_pct": round(100.0 * len(present) / n, 2),
        "none_anywhere": n - len(present),
        "median_where_present": statistics.median(present) if present else None,
        "mean_where_present": round(sum(present) / len(present), 1) if present else None,
    }


def main():
    base = corpora.base_terms()
    out = {
        "note": "Session 88's reach scan, ported to three traditions and run in two units. A party "
                "term in reach is a ceiling on a bearer named, never naming itself.",
        "term_lists": {},
        "block_windows": list(BLOCK_WINDOWS),
        "word_windows": list(WORD_WINDOWS),
        "corpora": {},
    }
    for name in ("whatwg", "eu", "rfc"):
        out["term_lists"][name] = {
            "base": term_pattern(base),
            "row": term_pattern(base + EXTENSIONS[name]),
            "extension": EXTENSIONS[name],
        }

    for name in ("whatwg", "eu", "rfc"):
        entry = {}
        for which in ("row", "base"):
            terms = base + (EXTENSIONS[name] if which == "row" else [])
            rows, bd, wd, dup = scan(name, terms)
            entry[which] = {
                "blocks": curve(bd, BLOCK_WINDOWS, len(rows)),
                "words": curve(wd, WORD_WINDOWS, len(rows)),
            }
            if which == "row":
                entry["population"] = len(rows)
                entry["rows_with_a_duplicated_sentence_in_their_block"] = dup
        out["corpora"][name] = entry
        r = entry["row"]
        print("%-7s pop %5d | blocks w0 %6.2f%%  whole doc %6.2f%%  none %4d | "
              "words w36 %6.2f%%  median %6s"
              % (name, entry["population"], r["blocks"]["pct"]["0"],
                 r["blocks"]["whole_document_pct"], r["blocks"]["none_anywhere"],
                 r["words"]["pct"]["36"], r["words"]["median_where_present"]))

    # the two spreads P3 is scored on
    b0 = {k: v["row"]["blocks"]["pct"]["0"] for k, v in out["corpora"].items()}
    w36 = {k: v["row"]["words"]["pct"]["36"] for k, v in out["corpora"].items()}
    out["spreads"] = {
        "block_window_0": {"by_corpus": b0, "spread": round(max(b0.values()) - min(b0.values()), 2)},
        "word_window_36": {"by_corpus": w36, "spread": round(max(w36.values()) - min(w36.values()), 2)},
    }
    out["median_word_distance"] = {k: v["row"]["words"]["median_where_present"]
                                   for k, v in out["corpora"].items()}
    print("\n  spread at block window 0 : %.2f points  %s" %
          (out["spreads"]["block_window_0"]["spread"], b0))
    print("  spread at word window 36 : %.2f points  %s" %
          (out["spreads"]["word_window_36"]["spread"], w36))
    print("  median word distance     : %s" % out["median_word_distance"])
    (HERE / "results.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
