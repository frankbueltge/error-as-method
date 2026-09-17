#!/usr/bin/env python3
"""bounds.py -- the geometry of the carriers, computed before PREDICTIONS.md exists.

Session 90 left an open thread: the only validation this line has for its party-term lists is a
reader -- 60 windows at Session 88, 40 at Session 90 -- and Grimmer & Stewart (2013) say a
dictionary that is not validated for its domain is not an instrument.  Tonight asks whether the
validation can be mechanised.  Before any decision rule is written, this file measures the thing
a decision rule would have to decide: the *gap* between the carrier and the obligation it is
supposed to bear, in words and in intervening material, over all 660 rows and all three lists.

No rule here.  Counts only.  Run first.
"""

import bisect
import gzip
import json
import re
import statistics
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
S88 = HERE.parent / "2026-09-12-adjacent-text"
S90 = HERE.parent / "2026-09-15-not-part-of-the-act"

SEP = "\n"
WORD = re.compile(r"\S+")

UK_NARROW = ["Secretary of State", "Minister", "Ministers", "Treasury",
             "local authority", "local authorities", "authority", "authorities",
             "court", "courts", "tribunal", "tribunals", "constable", "officer", "officers"]
UK_WIDE = UK_NARROW + ["person", "persons"]


def base_terms():
    pat = json.load(open(S88 / "results.json"))["mechanical_ceiling"]["party_terms"]
    return pat[len(r"\b("):-len(r")\b")].split("|")


def term_pattern(names):
    return r"\b(" + "|".join(sorted(names, key=len, reverse=True)) + r")\b"


def population():
    occ = json.load(gzip.open(S90 / "occurrences.json.gz"))
    return [{"doc": x["act"], "block": x["block"], "sentence": x["sentence"],
             "modal": x["modal"], "offset": x["offset"]}
            for x in occ
            if x["form"] == "B-FORM" and x["agent"] == "AGENTLESS" and x["register"] == "ACT"]


def blocks():
    corpus = json.load(gzip.open(S90 / "corpus.json.gz", "rt"))
    return {k: d["act"] for k, d in corpus.items()}


def docindex(blks, party):
    docs = {}
    for doc, seq in blks.items():
        text = SEP.join(seq)
        starts, off = [], 0
        for t in seq:
            starts.append(off)
            off += len(t) + len(SEP)
        docs[doc] = {"text": text, "starts": starts,
                     "spans": [(m.start(), m.end()) for m in party.finditer(text)],
                     "word_starts": [m.start() for m in WORD.finditer(text)]}
    return docs


def gaps(rows, blks, term_list):
    """For every row, the nearest PRECEDING carrier and the raw material between it and the modal.

    Returns one record per row that has such a carrier anywhere in its document.  `gap_text` is
    exactly the span a decision rule would have to read.  No rule is applied here.
    """
    party = re.compile(term_pattern(term_list), re.IGNORECASE)
    docs = docindex(blks, party)
    out = []
    for r in rows:
        d = docs[r["doc"]]
        seq_block = blks[r["doc"]][r["block"]]
        pos = d["starts"][r["block"]] + seq_block.find(r["sentence"]) + r["offset"]
        ends = [e for _, e in d["spans"]]
        j = bisect.bisect_right(ends, pos)
        if j == 0:
            continue
        s, e = d["spans"][j - 1]
        ws = d["word_starts"]
        out.append({
            "doc": r["doc"], "block": r["block"], "modal": r["modal"],
            "carrier": d["text"][s:e],
            "word_distance": bisect.bisect_left(ws, pos) - bisect.bisect_left(ws, e),
            "same_block": s >= d["starts"][r["block"]],
            "gap_text": d["text"][e:pos],
            "sentence": r["sentence"],
        })
    return out


def describe(recs, n):
    inw = [g for g in recs if g["word_distance"] <= 36]
    w0 = [g for g in recs if g["same_block"]]
    gapwords = [len(WORD.findall(g["gap_text"])) for g in inw]
    # how much material actually stands between carrier and modal, for the rows in reach
    return {
        "rows_with_a_carrier_anywhere": len(recs),
        "rows_with_a_carrier_within_36_words": len(inw),
        "pct_within_36_words": round(100.0 * len(inw) / n, 2),
        "rows_with_a_carrier_in_the_same_block": len(w0),
        "median_word_distance_where_present": statistics.median(
            [g["word_distance"] for g in recs]) if recs else None,
        "gap_words_within_36": {
            "zero": sum(1 for x in gapwords if x == 0),
            "one": sum(1 for x in gapwords if x == 1),
            "two_to_five": sum(1 for x in gapwords if 2 <= x <= 5),
            "six_or_more": sum(1 for x in gapwords if x >= 6),
        },
        "carriers_within_36": dict(Counter(g["carrier"].lower() for g in inw).most_common(12)),
    }


def main():
    rows, blks = population(), blocks()
    base = base_terms()
    lists = {"base": base, "narrow": base + UK_NARROW, "wide": base + UK_WIDE}

    out = {
        "note": "Counts only.  Written and run before PREDICTIONS.md and before any decision rule "
                "exists.  The question tonight asks is whether the reader can be replaced; this "
                "file measures the material the replacement would have to read.",
        "corpus": "63 UK Public General Acts 2012-2014, committed by Session 90 as corpus.json.gz",
        "population": len(rows),
        "restriction": "B-FORM, AGENTLESS, register ACT -- Session 89's scan population, unchanged",
        "lists": {},
    }
    for name, terms in lists.items():
        recs = gaps(rows, blks, terms)
        out["lists"][name] = describe(recs, len(rows))
        d = out["lists"][name]
        print("%-7s carrier anywhere %4d | within 36 words %4d (%5.2f%%) | same block %4d | "
              "gap 0 words %4d" % (name, d["rows_with_a_carrier_anywhere"],
                                   d["rows_with_a_carrier_within_36_words"],
                                   d["pct_within_36_words"],
                                   d["rows_with_a_carrier_in_the_same_block"],
                                   d["gap_words_within_36"]["zero"]))

    out["the_reader_s_sample"] = {
        "session_90": {"population_window_0_narrow": 112, "sampled": 40, "seed": 90,
                       "bearer": 17, "not_bearer": 23, "precision": 0.425},
        "session_88": {"precision_in_its_own_corpus": 0.611},
        "note": "the only ground truth this line owns.  40 YES/NO verdicts with reasons, committed "
                "by Session 90 as handreading.json.  Tonight scores mechanical rules against them.",
    }
    (HERE / "bounds.json").write_text(json.dumps(out, indent=1) + "\n")
    print("\n  wrote bounds.json")


if __name__ == "__main__":
    main()
