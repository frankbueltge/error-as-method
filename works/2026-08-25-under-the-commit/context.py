#!/usr/bin/env python3
"""Fetch the night's prose sources and the house catalogues; hash, count, record.

Nothing here is committed as bytes: PROTOCOL.md allows a source's bytes into this
repository only where the licence permits redistribution, and the manifest plus a
SHA-256 is the better warrant anyway -- a stranger re-fetches and compares.

The catalogue counts state their matching rule, because a count without one is a
count on an undeclared grid. Session 69 reported `Rheinberger` as 6; tonight the
same word returns 3 under the rule below. The rule is written down here so the
next night can compare like with like instead of inheriting a number.

Usage: python3 context.py    Writes catalogues.json, appends to sources/MANIFEST.json
"""

import hashlib
import json
import os
import re
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))

PROSE = [
    ("https://go.dev/doc/godebug",
     "Go's GODEBUG documentation -- the norm prose for the field under test; "
     "'This section documents the GODEBUG settings introduced and removed in each "
     "major Go release'"),
    ("https://go.dev/doc/go1compat",
     "the Go 1 compatibility promise the GODEBUG mechanism serves"),
    ("https://go.dev/doc/contribute",
     "Go's contribution guide -- documents that every patch set is fetchable as "
     "refs/changes/NN/CCCC/P"),
    ("https://gerrit-review.googlesource.com/Documentation/user-upload.html",
     "Gerrit's own documentation of the refs/changes/* namespace"),
    ("https://go.dev/doc/devel/release",
     "Go's release history -- the release dates the grids are read against"),
]
FEEDS = [
    ("https://frankbueltge.de/atlas/werke.json", "atlas"),
    ("https://frankbueltge.de/papers/index.json", "papers"),
    ("https://frankbueltge.de/datasets/register.json", "datasets"),
]
TERMS = ["gerrit", "code review", "patch set", "patchset", "version control",
         "repository mining", "mining software repositories", "software history",
         "changelog", "release engineering", "provenance", "deprecation", "godebug",
         "epistemic thing", "rheinberger", "canguilhem", "simondon", "revision control",
         "abandoned", "review"]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "error-as-method/session-70"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read(), r.status


def entry(url, status, body, what):
    return {"url": url, "http_status": status, "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "what": what, "committed": False}


def main():
    added = []
    for url, what in PROSE:
        body, status = get(url)
        added.append(entry(url, status, body, what))
        print("%-64s %s %d" % (url, status, len(body)))

    cats = {"matching_rule": "case-insensitive SUBSTRING over json.dumps() of the whole "
                             "entry object; a hit is an entry, not an occurrence",
            "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "feeds": {}}
    for url, name in FEEDS:
        body, status = get(url)
        added.append(entry(url, status, body, "house catalogue: %s" % name))
        d = json.loads(body)
        es = d["entries"]
        blob = [json.dumps(e).lower() for e in es]
        counts = {t: sum(1 for s in blob if t in s) for t in TERMS}
        # the same terms under a word-boundary rule, to show how much the rule decides
        word = {t: sum(1 for s in blob if re.search(r"\b" + re.escape(t) + r"\b", s, re.I))
                for t in TERMS}
        cats["feeds"][name] = {"url": url, "http_status": status,
                               "declared_count": d.get("count"), "len_entries": len(es),
                               "agree": d.get("count") == len(es),
                               "substring": counts, "word_boundary": word}
        print("%-46s %s  count=%s len=%d" % (url, status, d.get("count"), len(es)))

    json.dump(cats, open(os.path.join(HERE, "catalogues.json"), "w"), indent=1)
    mp = os.path.join(HERE, "sources", "MANIFEST.json")
    m = json.load(open(mp))
    have = {e["url"] for e in m["entries"]}
    m["entries"].extend(e for e in added if e["url"] not in have)
    json.dump(m, open(mp, "w"), indent=1)
    print("manifest entries:", len(m["entries"]))


if __name__ == "__main__":
    main()
