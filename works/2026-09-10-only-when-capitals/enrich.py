#!/usr/bin/env python3
"""Session 86 -- replace my header regex with the publisher's own metadata.

harvest.py read title, date and category off the ASCII header block with three regexes of mine, and
they were wrong: the "title" of RFC 8175 came out as "D. Satterwhite" (an author's name in the
right-hand column) and its "category" as "Standards Track  S. Jury" (two columns joined).  The RFC
Editor publishes the same fields as JSON at /rfc/rfcNNNN.json, so the parse is not needed at all.

This is the fourth consecutive night on which this line's instrument failed inside a vocabulary or a
parse it had written itself and not audited (F-111, F-112, F-114, F-121/F-124).  The difference here
is only that it failed loudly, in a printed column, before it was used for anything -- and the repair
is to stop parsing and read the field from whoever assigned it.  Recorded in the register as F-128,
not fixed silently.

The harvested TEXT is untouched.  Only the descriptive fields are replaced.
"""

import gzip
import json
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = "error-as-method nightly research line (contact: f.bueltge@gmail.com)"
FIELDS = ("title", "pub_date", "pub_status", "status", "source", "doi", "page_count", "authors",
          "obsoleted_by", "errata_url")


def meta(n):
    url = "https://www.rfc-editor.org/rfc/rfc%d.json" % n
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, json.load(r)


def main():
    corpus = json.load(gzip.open(HERE / "corpus.json.gz", "rt"))
    rows = json.load(open(HERE / "manifest-rows.json"))
    by_n = {r["rfc"]: r for r in rows}

    for key in sorted(corpus, key=int):
        n = int(key)
        status, m = meta(n)
        time.sleep(0.3)
        assert status == 200, (n, status)
        keep = {f: m.get(f) for f in FIELDS}
        corpus[key].update({"title": keep["title"], "date": keep["pub_date"],
                            "category": keep["pub_status"], "meta": keep})
        row = by_n[n]
        row.update({"title": keep["title"], "date": keep["pub_date"],
                    "category": keep["pub_status"], "doi": keep["doi"],
                    "page_count": keep["page_count"], "authors": keep["authors"],
                    "metadata_url": "https://www.rfc-editor.org/rfc/rfc%d.json" % n})
        print("  rfc%-5d %-14s %-22s %s" % (n, keep["pub_date"], keep["pub_status"],
                                            (keep["title"] or "")[:52]))

    with gzip.open(HERE / "corpus.json.gz", "wt") as fh:
        json.dump(corpus, fh)
    (HERE / "manifest-rows.json").write_text(json.dumps(rows, indent=1) + "\n")
    print("\n%d documents re-described from the publisher's metadata." % len(corpus))


if __name__ == "__main__":
    main()
