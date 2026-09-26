#!/usr/bin/env python3
"""harvest.py -- the fifth tradition: 14 CFR Chapter I, Subchapters F and G, as served by the eCFR
API for the date 2026-09-24.

The selection rule, the units and the exclusions are fixed in PREDICTIONS.md, committed before this
file existed.  This file carries them out and records what the source did.

WHAT THE SOURCE DID, observed tonight and kept.  The endpoint
`/api/versioner/v1/full/2026-09-24/title-14.xml` refuses an uncompressed request (HTTP 406, "This
endpoint requires response compression").  With compression allowed, a request qualified by
`?chapter=I&subchapter=F` and one qualified by `?chapter=I&subchapter=G` returned **byte-identical**
bodies: the whole of Title 14, every chapter, 16,000,260 bytes.  The qualifier was ignored.  So the
selection is made here, from the document's own structure -- `DIV3 N="I"` (the chapter),
`DIV4 N in {F, G}` (the subchapter) -- and the fetch is one unqualified request for the title.

UNITS (PREDICTIONS.md §3).  Document = a part (`DIV5`).  Block = one `P` or `FP*` element inside a
section (`DIV8`), flattened.  Excluded, and counted: anything inside `EXTRACT`, `NOTE`, `EDNOTE`,
`GPOTABLE`/`TABLE`, section headings, and appendices (`DIV9`), which are never descended into.

Public domain: works of the United States Government, 17 U.S.C. § 105.  The fetched bytes are
committed, gzipped, in sources/.

Writes corpus.json.gz, sources/title-14-2026-09-24.xml.gz, sources/MANIFEST.json.
"""

import gzip
import hashlib
import json
import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATE = "2026-09-24"
URL = "https://www.ecfr.gov/api/versioner/v1/full/%s/title-14.xml" % DATE
RAW = HERE / "sources" / ("title-14-%s.xml.gz" % DATE)
UA = "error-as-method research night (one-off corpus harvest; contact f.bueltge@gmail.com)"
CHAPTER, SUBCHAPTERS = "I", ("F", "G")
EXCLUDED = {"EXTRACT", "NOTE", "EDNOTE", "GPOTABLE", "TABLE"}


def fetch():
    if RAW.exists():
        return gzip.decompress(RAW.read_bytes()), None
    req = urllib.request.Request(URL, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=300) as fh:
        wire = fh.read()
        status = fh.status
        enc = fh.headers.get("Content-Encoding", "")
    body = gzip.decompress(wire) if enc == "gzip" else wire
    RAW.parent.mkdir(exist_ok=True)
    RAW.write_bytes(gzip.compress(body, mtime=0))
    return body, {"url": URL, "http_status": status, "content_encoding": enc,
                  "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                  "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


def flat(el):
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip()


def section_blocks(sec, excluded_count):
    out = []

    def walk(el):
        for c in el:
            if c.tag in EXCLUDED:
                excluded_count[c.tag] += 1
                continue
            if c.tag == "P" or c.tag.startswith("FP"):
                t = flat(c)
                if t:
                    out.append(t)
                continue
            walk(c)

    walk(sec)
    return out


def main():
    body, fetched = fetch()
    root = ET.fromstring(body)
    corpus, excluded, skipped = {}, Counter(), Counter()
    for ch in root.iter("DIV3"):
        if ch.get("N") != CHAPTER:
            continue
        for sub in ch.iter("DIV4"):
            if sub.get("N") not in SUBCHAPTERS:
                continue
            for part in sub.iter("DIV5"):
                blocks, sections = [], 0
                for sec in part.iter("DIV8"):
                    sections += 1
                    blocks.extend(section_blocks(sec, excluded))
                skipped["DIV9 appendices"] += sum(1 for _ in part.iter("DIV9"))
                head = part.find("HEAD")
                corpus[part.get("N")] = {
                    "subchapter": sub.get("N"), "part": part.get("N"),
                    "title": flat(head) if head is not None else "",
                    "sections": sections, "act": blocks}
        break                     # there is one Chapter I in Title 14; stop at it

    raw_sha = hashlib.sha256(body).hexdigest()
    with gzip.open(HERE / "corpus.json.gz", "wt") as fh:
        json.dump(corpus, fh)

    manifest = {
        "note": "Works of the United States Government are not subject to copyright (17 U.S.C. "
                "§ 105, https://www.law.cornell.edu/uscode/text/17/105). The bytes are committed "
                "gzipped beside this file; re-fetch and compare the SHA-256 of the decompressed "
                "body. The API ignored the chapter/subchapter qualifiers on 2026-09-26 and served "
                "the whole title either way; see harvest.py.",
        "rows": [dict(fetched or {"url": URL, "bytes": len(body), "sha256": raw_sha,
                                  "fetched": "(read from the committed copy)"},
                      what="eCFR full XML of 14 CFR, all chapters, as of 2026-09-24",
                      why="the fifth tradition: Chapter I, Subchapters F and G, selected in "
                          "harvest.py from the document's own DIV3/DIV4 structure",
                      committed_as="sources/" + RAW.name)],
    }
    (HERE / "sources" / "MANIFEST.json").write_text(json.dumps(manifest, indent=1,
                                                                ensure_ascii=False) + "\n")
    parts_nonempty = sum(1 for d in corpus.values() if d["act"])
    words = sum(len(b.split()) for d in corpus.values() for b in d["act"])
    print("title-14 body %d bytes, sha256 %s" % (len(body), raw_sha))
    print("subchapters %s: %d parts (%d with section text), %d sections, %d blocks, %d words"
          % ("+".join(SUBCHAPTERS), len(corpus), parts_nonempty,
             sum(d["sections"] for d in corpus.values()),
             sum(len(d["act"]) for d in corpus.values()), words))
    print("excluded elements:", dict(excluded), "| appendices not entered:", dict(skipped))
    json.dump({"excluded_elements": dict(excluded), "appendices_not_entered": dict(skipped),
               "parts": len(corpus), "parts_with_text": parts_nonempty, "words": words},
              open(HERE / "harvest-log.json", "w"), indent=1)


if __name__ == "__main__":
    main()
