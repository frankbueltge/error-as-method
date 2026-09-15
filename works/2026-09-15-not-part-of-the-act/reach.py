#!/usr/bin/env python3
"""reach.py -- Session 88's scan, ported to a fourth tradition, in three declared vocabularies.

Session 89 ported this scan to a second and third corpus and found the answer was decided by the
**unit of distance** it was asked in.  Tonight it is ported to a fourth, and the unit is not what
decides it: `bounds.json`, computed before PREDICTIONS.md, found that the 26 party terms that make
the four traditions comparable occur **172 times in 1,283,543 words** of 63 Acts of Parliament, and
that nineteen of the twenty-six never occur at all.  So the scan is run three times, over three
vocabularies all declared in §3 of PREDICTIONS.md before this file existed:

  BASE    Session 88's 26, unchanged, read out of its results.json
  NARROW  + fifteen strings: UK statute's own offices and bodies.  THE ROW'S LIST.
  WIDE    + `person`, `persons`

The scan logic is Session 89's `reach.py`, reimplemented here over this corpus's objects; `verify.py`
reproduces Session 89's published WHATWG curve with this file's own functions, which is the only
warrant a port has.

Run after measure.py.  Writes reach.json and carriers.json.
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

BLOCK_WINDOWS = (0, 1, 2, 3, 5, 8, 13, 20, 35, 50, 100, 200)
WORD_WINDOWS = (0, 5, 10, 25, 36, 50, 100, 200, 400, 800, 1600, 3200, 6400)
SEP = "\n"
WORD = re.compile(r"\S+")

UK_NARROW = ["Secretary of State", "Minister", "Ministers", "Treasury",
             "local authority", "local authorities", "authority", "authorities",
             "court", "courts", "tribunal", "tribunals", "constable", "officer", "officers"]
UK_WIDE = UK_NARROW + ["person", "persons"]

# the three figures S89.WORDUNIT fixed its band against, and the band
PRIOR_W36 = {"whatwg": 15.71, "eu": 23.29, "rfc": 15.59}
BAND_POINTS = 20
MEDIAN_BAND = (60, 500)


def base_terms():
    pat = json.load(open(S88 / "results.json"))["mechanical_ceiling"]["party_terms"]
    return pat[len(r"\b("):-len(r")\b")].split("|")


def term_pattern(names):
    return r"\b(" + "|".join(sorted(names, key=len, reverse=True)) + r")\b"


def population():
    """The rows to measure: B-FORM, AGENTLESS, and in the binding register (the Act itself)."""
    occ = json.load(gzip.open(HERE / "occurrences.json.gz"))
    return [{"doc": x["act"], "block": x["block"], "sentence": x["sentence"],
             "modal": x["modal"], "offset": x["offset"]}
            for x in occ
            if x["form"] == "B-FORM" and x["agent"] == "AGENTLESS" and x["register"] == "ACT"]


def blocks():
    corpus = json.load(gzip.open(HERE / "corpus.json.gz", "rt"))
    return {k: d["act"] for k, d in corpus.items()}


def scan(rows, blks, term_list):
    """Session 89's scan, function for function: nearest preceding party term in blocks and words."""
    party = re.compile(term_pattern(term_list), re.IGNORECASE)
    docs = {}
    for doc, seq in blks.items():
        text = SEP.join(seq)
        starts, off = [], 0
        for t in seq:
            starts.append(off)
            off += len(t) + len(SEP)
        has = [bool(party.search(t)) for t in seq]
        prev, last = [], None
        for i, h in enumerate(has):
            if h:
                last = i
            prev.append(last)
        docs[doc] = {"text": text, "starts": starts, "prev": prev,
                     "term_ends": [m.end() for m in party.finditer(text)],
                     "word_starts": [m.start() for m in WORD.finditer(text)]}

    block_d, word_d, duplicated, carrier = [], [], [], Counter()
    for r in rows:
        d = docs[r["doc"]]
        i = r["block"]
        p = d["prev"][i]
        block_d.append(None if p is None else i - p)
        seq_block = blks[r["doc"]][i]
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
            mm = list(party.finditer(d["text"], max(0, end - 60), end))
            if mm:
                carrier[mm[-1].group(0).lower()] += 1
    return block_d, word_d, duplicated, carrier


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


def forwards_only(rows, blks, term_list):
    """The defect Session 89 kept rather than repaired: window 0 looks forwards as well as back."""
    party = re.compile(term_pattern(term_list), re.IGNORECASE)
    hits = after = 0
    for r in rows:
        b = blks[r["doc"]][r["block"]]
        if not party.search(b):
            continue
        hits += 1
        pos = b.find(r["sentence"]) + r["offset"]
        if not party.search(b[:pos]):
            after += 1
    return {"window_0_hits": hits, "of_them_term_stands_after_the_obligation": after,
            "pct": round(100.0 * after / hits, 2) if hits else None}


def main():
    rows, blks = population(), blocks()
    base = base_terms()
    lists = {"base": base, "narrow": base + UK_NARROW, "wide": base + UK_WIDE}

    out = {
        "note": "Session 88's reach scan on a fourth tradition, in three vocabularies declared in "
                "PREDICTIONS.md §3 before this file existed. A party term in reach is a CEILING on a "
                "bearer named, never naming itself.",
        "population": len(rows),
        "register": "the Act itself, B-FORM and AGENTLESS",
        "block_windows": list(BLOCK_WINDOWS), "word_windows": list(WORD_WINDOWS),
        "term_lists": {k: {"terms": v, "n": len(v), "pattern": term_pattern(v)}
                       for k, v in lists.items()},
        "prior_word_window_36": PRIOR_W36,
        "lists": {},
    }

    for name, terms in lists.items():
        bd, wd, dup, carrier = scan(rows, blks, terms)
        out["lists"][name] = {
            "blocks": curve(bd, BLOCK_WINDOWS, len(rows)),
            "words": curve(wd, WORD_WINDOWS, len(rows)),
            "carriers": dict(carrier.most_common()),
            "rows_with_a_duplicated_sentence_in_their_block": len(dup),
            "forwards_defect": forwards_only(rows, blks, terms),
        }
        c = out["lists"][name]
        print("%-7s pop %5d | blocks w0 %6.2f%%  whole doc %6.2f%%  none %5d | "
              "words w36 %6.2f%%  median %7s"
              % (name, len(rows), c["blocks"]["pct"]["0"], c["blocks"]["whole_document_pct"],
                 c["blocks"]["none_anywhere"], c["words"]["pct"]["36"],
                 c["words"]["median_where_present"]))

    w36 = {k: v["words"]["pct"]["36"] for k, v in out["lists"].items()}
    out["the_interval"] = {
        "question": "how far apart can one author, declaring every list in advance, put this corpus?",
        "word_window_36_by_list": w36,
        "span_points": round(max(w36.values()) - min(w36.values()), 2),
        "the_row_s_band_width_points": BAND_POINTS,
        "span_exceeds_the_band": round(max(w36.values()) - min(w36.values()), 2) > BAND_POINTS,
        "median_word_distance_by_list": {k: v["words"]["median_where_present"]
                                         for k, v in out["lists"].items()},
        "block_window_0_by_list": {k: v["blocks"]["pct"]["0"] for k, v in out["lists"].items()},
    }
    out["row_arm"] = {
        "list": "narrow",
        "word_window_36": out["lists"]["narrow"]["words"]["pct"]["36"],
        "distance_to_each_prior": {k: round(abs(out["lists"]["narrow"]["words"]["pct"]["36"] - v), 2)
                                   for k, v in PRIOR_W36.items()},
        "median_word_distance": out["lists"]["narrow"]["words"]["median_where_present"],
        "median_band": list(MEDIAN_BAND),
    }
    a = out["row_arm"]
    a["within_20_points_of_at_least_one_prior"] = min(a["distance_to_each_prior"].values()) <= BAND_POINTS
    a["median_inside_band"] = MEDIAN_BAND[0] <= (a["median_word_distance"] or -1) <= MEDIAN_BAND[1]
    a["S89_WORDUNIT_falsified"] = not (a["within_20_points_of_at_least_one_prior"]
                                       and a["median_inside_band"])

    (HERE / "reach.json").write_text(json.dumps(out, indent=1) + "\n")
    (HERE / "carriers.json").write_text(json.dumps({
        "note": "which string actually carried the nearest match, per list. The rejection log: "
                "nothing here was chosen after seeing the answer.",
        "by_list": {k: v["carriers"] for k, v in out["lists"].items()},
        "base_term_occurrences_in_the_corpus": "bounds.json, borrowed_vocabulary",
    }, indent=1) + "\n")

    print("\n  word window 36 by list : %s" % w36)
    print("  span                   : %.2f points against a band of %d"
          % (out["the_interval"]["span_points"], BAND_POINTS))
    print("  row arm (narrow)       : %.2f %%, median %s, falsified: %s"
          % (a["word_window_36"], a["median_word_distance"], a["S89_WORDUNIT_falsified"]))


if __name__ == "__main__":
    main()
