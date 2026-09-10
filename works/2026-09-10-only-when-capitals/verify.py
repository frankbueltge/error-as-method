#!/usr/bin/env python3
"""Check that the committed corpus is the fetched bytes.  Session 86, 2026-09-10.

`sources/MANIFEST.json` claims the licence permits committing these documents *"in full and without
modification"* and that corpus.json.gz holds each document's complete, unaltered text.  That is a
claim, so it is checked rather than asserted: re-encode every stored text as UTF-8 and compare its
SHA-256 with the hash of the bytes the fetch returned.

It matters because harvest.py decoded with errors="replace", which would silently substitute U+FFFD
for any byte that is not valid UTF-8 -- and a corpus with replacement characters in it is neither
unmodified nor safely re-runnable.  Run: `python3 verify.py`.  Exits non-zero on any mismatch.
"""

import gzip
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    corpus = json.load(gzip.open(HERE / "corpus.json.gz", "rt"))
    rows = {r["rfc"]: r for r in json.load(open(HERE / "manifest-rows.json"))}
    bad = []
    for key in sorted(corpus, key=int):
        n = int(key)
        h = hashlib.sha256(corpus[key]["text"].encode("utf-8")).hexdigest()
        if h != rows[n]["sha256"]:
            bad.append(n)
    if bad:
        print("MISMATCH in %d document(s): %s" % (len(bad), bad), file=sys.stderr)
        sys.exit(1)
    print("%d documents: every stored text re-encodes to exactly the bytes that were fetched."
          % len(corpus))
    print("total %d bytes; the manifest's hashes are the fetch's, not the store's."
          % sum(r["bytes"] for r in rows.values()))


if __name__ == "__main__":
    main()
