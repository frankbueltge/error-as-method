#!/usr/bin/env python3
"""Harvest -- Session 87, 2026-09-11.

The third corpus S86.CONSTANT asks for: a published system of norms in English that is neither EU
legislation nor the RFC series.  Selection rule, fixed in PREDICTIONS.md §1 before any document was
fetched:

    Every standard linked from https://spec.whatwg.org/ whose canonical single-page HTML is served
    at HTTP 200.  Complete enumeration -- no seeded window, no threshold, no exclusion for size, for
    age or for how many modals a document turns out to hold.  The index links HTML at its multipage
    address; the canonical single-page form https://html.spec.whatwg.org/ is used instead, and that
    is the only substitution.

Writes sources/MANIFEST.json (URL, status, bytes, SHA-256, title, last-updated) and corpus.json.gz
(the register-tagged prose blocks, which is what the instrument reads).  The raw HTML is kept out of
the repository; WHATWG standards are CC BY 4.0 and could lawfully be committed, but 23 MB of markup
is not evidence -- the manifest's hashes are, and the extracted blocks are the object measured.
"""

import gzip
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

from extract import extract

HERE = Path(__file__).resolve().parent
INDEX = "https://spec.whatwg.org/"
# The raw markup is kept out of the repository (see the module docstring). It is written to this
# cache so that verify.py can audit the extractor against the bytes it actually read; set NIGHT_RAW
# to re-run the audit elsewhere.
RAW = Path(os.environ.get("NIGHT_RAW", "/tmp/night-2026-09-11-raw"))
UA = "error-as-method/night-2026-09-11 (research; contact f.bueltge@gmail.com)"

# the one substitution declared in PREDICTIONS.md §1
CANONICAL = {"https://html.spec.whatwg.org/multipage/": "https://html.spec.whatwg.org/"}

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
UPDATED_RE = re.compile(r"Living Standard\s*&mdash;\s*Last Updated\s*([^<]+)", re.I)
UPDATED_RE2 = re.compile(r"Living Standard\s*—\s*Last Updated\s*([^<]+)", re.I)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as fh:
        return fh.status, fh.read()


def rebuild():
    """Re-derive corpus.json.gz from the raw cache, without touching the network.  Same extractor,
    same manifest; used when extract.py changes and the bytes are already hashed."""
    manifest = json.loads((HERE / "sources" / "MANIFEST.json").read_text())
    corpus = {}
    for m in manifest["documents"]:
        if not m["in_corpus"]:
            continue
        key = m["url"].split("//")[1].split(".")[0]
        body = (RAW / (key + ".html")).read_bytes()
        if hashlib.sha256(body).hexdigest() != m["sha256"]:
            raise SystemExit("rebuild: cached %s does not match the manifest hash" % key)
        blocks = extract(body.decode("utf-8", "replace"))
        prose = [b for b in blocks if not b["furniture"]]
        corpus[key] = {"url": m["url"], "title": m["title"], "updated": m["updated"],
                       "blocks": [{"r": b["register"], "m": b["marked_by"], "g": b["tag"],
                                   "t": b["text"]} for b in prose]}
        print("  %-14s %5d blocks (hash verified)" % (key, len(prose)))
    with gzip.open(HERE / "corpus.json.gz", "wt") as fh:
        json.dump(corpus, fh)
    print("rebuilt from cache: %d documents" % len(corpus))


def main():
    if "--rebuild" in sys.argv:
        return rebuild()
    status, raw = get(INDEX)
    index_html = raw.decode("utf-8", "replace")
    urls = sorted({m.group(1) for m in
                   re.finditer(r'href="(https?://[a-z0-9\-]+\.spec\.whatwg\.org/[^"]*)"', index_html)})
    urls = [CANONICAL.get(u, u) for u in urls]
    urls = sorted(set(urls))
    print("index %s -> %d standards" % (status, len(urls)))

    manifest, corpus = [], {}
    for url in urls:
        for attempt in range(4):
            try:
                st, body = get(url)
                break
            except Exception as exc:                       # network, not measurement
                if attempt == 3:
                    st, body = 0, b""
                    print("  FAILED %s -- %s" % (url, exc))
                time.sleep(2 ** attempt)
        if st != 200 or not body:
            manifest.append({"url": url, "status": st, "bytes": len(body), "sha256": None,
                             "in_corpus": False, "reason": "not served at HTTP 200"})
            continue
        RAW.mkdir(parents=True, exist_ok=True)
        (RAW / (url.split("//")[1].split(".")[0] + ".html")).write_bytes(body)
        text = body.decode("utf-8", "replace")
        title = TITLE_RE.search(text)
        upd = UPDATED_RE.search(text) or UPDATED_RE2.search(text)
        key = url.split("//")[1].split(".")[0]
        blocks = extract(text)
        prose = [b for b in blocks if not b["furniture"]]
        corpus[key] = {"url": url, "title": title.group(1).strip() if title else None,
                       "updated": upd.group(1).strip() if upd else None,
                       "blocks": [{"r": b["register"], "m": b["marked_by"], "g": b["tag"],
                                   "t": b["text"]} for b in prose]}
        manifest.append({"url": url, "status": st, "bytes": len(body),
                         "sha256": hashlib.sha256(body).hexdigest(),
                         "title": corpus[key]["title"], "updated": corpus[key]["updated"],
                         "blocks_kept": len(prose), "blocks_dropped_as_furniture":
                             len(blocks) - len(prose),
                         "in_corpus": True})
        print("  %-14s %7d bytes  %5d blocks  %s" % (key, len(body), len(prose),
                                                     (corpus[key]["title"] or "")[:40]))

    (HERE / "sources").mkdir(exist_ok=True)
    (HERE / "sources" / "MANIFEST.json").write_text(json.dumps({
        "harvested": "2026-09-11",
        "index": INDEX,
        "index_status": status,
        "licence": "Copyright (c) WHATWG (Apple, Google, Mozilla, Microsoft). "
                   "Licensed under a Creative Commons Attribution 4.0 International License; "
                   "portions incorporated into source code under BSD 3-Clause. Quoted from the "
                   "'Intellectual property rights' section carried by every document harvested.",
        "note": "The raw HTML is not committed. It is lawful to commit (CC BY 4.0) and was left out "
                "because 23 MB of Bikeshed markup is not the evidence: the SHA-256 below lets a "
                "stranger re-fetch and compare, and corpus.json.gz holds exactly what was measured.",
        "documents": manifest}, indent=1) + "\n")
    with gzip.open(HERE / "corpus.json.gz", "wt") as fh:
        json.dump(corpus, fh)

    served = [m for m in manifest if m["in_corpus"]]
    print("\n%d of %d served; %d blocks; %.1f MB fetched"
          % (len(served), len(manifest), sum(m["blocks_kept"] for m in served),
             sum(m["bytes"] for m in served) / 1e6))


if __name__ == "__main__":
    sys.exit(main())
