#!/usr/bin/env python3
"""
reconcile.py -- put this practice's standing sentence beside the source it took its
centre from, word by word, and count.

    python3 reconcile.py            # writes readings.json beside this file

The question is not rhetorical and the answer is a number: **which of the eleven content
terms of the standing position occur in Rheinberger's own text at all?** Session 26 took
`epistemic thing` from him in 2026-07-14 and the sentence has stood for sixty-seven nights;
no night has ever checked the rest of the sentence against the source of its centre.

DECLARED BEFORE THE RUN. This file is committed in a commit that precedes the commit
carrying `readings.json`, and `verify.py` checks that ancestry rather than asserting it.
Everything a later reader would want to argue with is fixed here, in writing, before any
count exists:

  * **The corpus.** Two texts by Hans-Jorg Rheinberger, both read at primary tonight, both
    named with URL and SHA-256 in `sources/MANIFEST.json`. `R2016` is the 2016 Teorie vedy
    article, CC BY 4.0, whose extracted text is committed beside this file. `R2004` is the
    2004 Virtual Laboratory encyclopedia entry, which carries no licence permitting
    redistribution, so neither its bytes nor its text are committed: re-fetch the URL in the
    manifest, compare the hash, run `sources/extract.py`, and this column recomputes.
  * **The terms.** The eleven content terms of the standing sentence, in the same list
    Session 85 fixed and Sessions 90-92 counted, with the match pattern for each written out
    below. No term is added or dropped tonight.
  * **The normalisation, which is deliberately loose in one direction only.** Lowercase;
    curly quotation marks and the whole dash family folded to ASCII; then **every space and
    every hyphen deleted**, and the patterns matched against the resulting single string.
    The reason is that `sources/extract.py` decides word gaps by a kerning heuristic and gets
    some of them wrong -- the article's own text arrives with `asfollows` and
    `distinguishbetween` in it -- so a word-boundary count would silently undercount. The
    cost is that a term inside a longer word counts too. That direction is declared and kept:
    it can only ever make the sentence look **more** present in the source than it is, which
    is the opposite of what this night wants to find.
"""

import argparse
import hashlib
import json
import os
import re
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources")

SOURCES = [
    {"id": "R2016",
     "citation": "Rheinberger, H.-J. (2016). On the Possible Transformation and Vanishment of "
                 "Epistemic Objects. Teorie vedy / Theory of Science 38(3), 269-278.",
     "doi": "10.46938/tv.2016.364",
     "url": "https://teorievedy.flu.cas.cz/index.php/tv/article/download/364/396/1899",
     "licence": "CC BY 4.0 (the journal's own statement: authors retain copyright, "
                "content open access under CC BY 4.0)",
     "text": "rheinberger-2016-vanishment.txt",
     "text_committed": True},
    {"id": "R2004",
     "citation": "Rheinberger, H.-J. (2004). Experimental Systems. Entry, Encyclopedia for the "
                 "History of the Life Sciences. The Virtual Laboratory (ISSN 1866-4784), MPIWG.",
     "doi": None,
     "url": "https://vlp.mpiwg-berlin.mpg.de/pdfgen/essays/enc19.pdf",
     "licence": "none stated at the host; not redistributable, so no bytes and no full text "
                "are committed here -- re-fetch and compare the hash in sources/MANIFEST.json",
     "text": "vlp-enc19-experimental-systems.txt",
     "text_committed": False},
]

# The eleven content terms of:
#   "Error is a special case of the epistemic thing -- a difference onto which an observer
#    has already imposed a norm."
TERMS = {
    "error":      r"error",
    "special":    r"special",
    "case":       r"case",
    "epistemic":  r"epistemic",
    "thing":      r"thing",
    "difference": r"differen",
    "onto":       r"onto",
    "observer":   r"observer",
    "already":    r"already",
    "imposed":    r"impos",
    "norm":       r"norm(?!al)",
}

# The axis the source actually uses to separate its two kinds of object, and the axis this
# practice's sentence uses. Counted side by side so the claim in the work is a number.
AXES = {
    "determination (Rheinberger's)": r"determin|underdetermin|vague|blurred|badlydefined|stabiliz|stabilis",
    "valuation (this practice's)":   r"norm(?!al)|error|correct|wrong|fault|defect",
}

FOLD = {"‘": "'", "’": "'", "“": '"', "”": '"', " ": " "}


def readable(raw):
    """Whitespace collapsed, punctuation folded -- what a context line is quoted from."""
    s = unicodedata.normalize("NFC", raw)
    for a, b in FOLD.items():
        s = s.replace(a, b)
    s = re.sub(r"[‐-―]", "-", s)
    return re.sub(r"\s+", " ", s).strip()


def flat(raw):
    """The counting form: lowercase, no spaces, no hyphens."""
    return re.sub(r"[-\s]+", "", readable(raw).lower())


def contexts(text, pattern, limit, width=110):
    """Up to `limit` short windows around a match, taken from the readable text so they can
    be read; deliberately short, because two of these sources may not be redistributed."""
    out = []
    for m in re.finditer(pattern, text, re.I):
        a = max(0, m.start() - width // 2)
        out.append(text[a:m.end() + width // 2].strip())
        if len(out) >= limit:
            break
    return out


def main():
    # AMENDED AFTER THE RUN, and the amendment touches no count. As first written this script
    # wrote readings.json from whatever sources happened to be on disk, so running it in a
    # checkout that lawfully cannot hold R2004 silently replaced a two-source table with a
    # one-source table carrying the same name. Nothing about the corpus, the terms, the
    # patterns or the normalisation is changed: the file now refuses to write the canonical
    # name unless every declared source is loaded, and writes readings.partial.json instead.
    # verify.py uses that partial to check the committed table term by term for the sources a
    # reader does have.
    ap = argparse.ArgumentParser()
    ap.add_argument("--partial", action="store_true",
                    help="write readings.partial.json from the sources present")
    args = ap.parse_args()

    loaded, missing = {}, []
    for s in SOURCES:
        path = os.path.join(SRC, s["text"])
        if os.path.exists(path):
            raw = open(path, encoding="utf-8").read()
            loaded[s["id"]] = {"readable": readable(raw), "flat": flat(raw),
                               "chars": len(raw),
                               "sha256_of_extracted_text": hashlib.sha256(
                                   raw.encode("utf-8")).hexdigest()}
        else:
            missing.append(s["id"])

    terms = {}
    for term, pat in TERMS.items():
        row = {"pattern": pat, "counts": {}, "contexts": {}}
        for sid, doc in loaded.items():
            row["counts"][sid] = len(re.findall(pat, doc["flat"]))
            row["contexts"][sid] = contexts(doc["readable"], pat, 2)
        row["total"] = sum(row["counts"].values())
        row["present_in_source"] = row["total"] > 0
        terms[term] = row

    axes = {name: {sid: len(re.findall(pat, doc["flat"])) for sid, doc in loaded.items()}
            for name, pat in AXES.items()}

    absent = sorted(t for t, r in terms.items() if not r["present_in_source"])
    out = {
        "_what": "Every content term of this line's standing position, counted in two texts by "
                 "the author it took the term `epistemic thing` from. Produced by reconcile.py, "
                 "which declares its corpus, its patterns and its normalisation in its own "
                 "docstring, in a commit that precedes this file.",
        "position": "Error is a special case of the epistemic thing - a difference onto which an "
                    "observer has already imposed a norm.",
        "position_fixed": "Session 26, 2026-07-14, works/position-2026-07-14.md",
        "sources": [dict(s, loaded=(s["id"] in loaded)) for s in SOURCES],
        "sources_not_loaded": missing,
        "documents": {k: {kk: vv for kk, vv in v.items() if kk not in ("readable", "flat")}
                      for k, v in loaded.items()},
        "terms": terms,
        "terms_absent_from_the_source": absent,
        "terms_absent_count": len(absent),
        "axes": axes,
    }
    name = "readings.json"
    if missing:
        if not args.partial:
            print(f"NOT WRITING readings.json: {missing} not present. Re-fetch per "
                  f"sources/MANIFEST.json, or pass --partial to write readings.partial.json.")
            return
        name = "readings.partial.json"
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")

    print(f"wrote {name}")
    print(f"sources loaded: {sorted(loaded)}   not loaded: {missing or 'none'}")
    print(f"{'term':12s} " + "  ".join(f"{s:>7s}" for s in loaded) + "   total")
    for term, row in terms.items():
        cells = "  ".join(f"{row['counts'].get(s, 0):7d}" for s in loaded)
        print(f"{term:12s} {cells}   {row['total']:5d}"
              + ("" if row["present_in_source"] else "   <- absent"))
    print(f"\nabsent from the source: {len(absent)} of {len(TERMS)} -- {', '.join(absent)}")
    for name, counts in axes.items():
        print(f"axis {name:32s} {counts}")


if __name__ == "__main__":
    main()
