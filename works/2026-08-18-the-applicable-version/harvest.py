#!/usr/bin/env python3
"""Fetch tonight's sources, hash them, and write sources/MANIFEST.json.

The bytes themselves are deliberately NOT committed. PROTOCOL.md's amendment of 2026-08-18
says: commit a source's bytes where the licence permits redistribution, otherwise commit the
manifest and quote within citation length. Unicode's data files would qualify; its web pages
and its mailing-list archive are a mixed case I am not going to guess at on a public
repository, and the manifest is the better warrant anyway — a stranger re-fetches and
compares the hash.

What IS committed is `results.json`: the facts this instrument reads out of those bytes
(clause names, applicable versions, corrigendum numbers, version release dates). Those are
data points, not the source text, and without them the measurement cannot be re-run offline.

    python3 harvest.py            # fetch, hash, write manifest
"""
import hashlib
import json
import os
import ssl
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "sources")

SOURCES = [
    {
        "key": "stability_policy",
        "url": "https://www.unicode.org/policies/stability_policy.html",
        "what": "Unicode Character Encoding Stability Policies, the page as published",
        "why": "Population P-A: the written rules under test, each with its Applicable Version",
    },
    {
        "key": "corrigenda",
        "url": "https://www.unicode.org/versions/corrigenda.html",
        "what": "Unicode Corrigenda, the consortium's own list of published defects",
        "why": "Population P-B: the documented breakdowns, dated by the version that fixed them",
    },
    {
        "key": "enumeratedversions",
        "url": "https://www.unicode.org/versions/enumeratedversions.html",
        "what": "Enumerated Versions of the Unicode Standard, with release dates",
        "why": "Population P-C: the denominator, without which a coincidence has no base rate",
    },
    {
        "key": "namealiases",
        "url": "https://www.unicode.org/Public/UCD/latest/ucd/NameAliases.txt",
        "what": "NameAliases.txt from the Unicode Character Database",
        "why": "Direction B: the repair mechanism minted for names the Name Stability rule froze",
    },
    {
        "key": "unicodedata",
        "url": "https://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt",
        "what": "UnicodeData.txt from the Unicode Character Database (2.2 MB)",
        "why": "To read the encoded names of the characters the first alias file corrects, at "
               "the primary rather than from memory — FE18 really is spelled BRAKCET",
    },
    {
        "key": "namealiases-5.0.0",
        "url": "https://www.unicode.org/Public/5.0.0/ucd/NameAliases.txt",
        "what": "NameAliases.txt as published in Unicode 5.0.0, the first version of that file",
        "why": "Direction B: what the alias mechanism contained on the day it was frozen",
    },
    {
        "key": "whistler2015",
        "url": "https://www.unicode.org/mail-arch/unicode-ml/y2015-m06/0189.html",
        "what": "Ken Whistler, Unicode mail archive, 2015-06-19, on the Version 1 Hangul syllables",
        "why": "The institution's own statement of why the Encoding Stability boundary is 2.0+",
    },
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "error-as-method/night-2026-08-18"})
    ctx = ssl.create_default_context()
    bundle = "/root/.ccr/ca-bundle.crt"
    if os.path.exists(bundle):
        ctx.load_verify_locations(bundle)
    with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
        return resp.status, resp.read()


def main():
    os.makedirs(OUT, exist_ok=True)
    manifest = []
    for src in SOURCES:
        try:
            status, body = fetch(src["url"])
        except Exception as err:  # noqa: BLE001 — a failed fetch is a fact about the night
            manifest.append({**src, "status": "FETCH FAILED", "error": str(err)})
            print(f"FAILED {src['key']}: {err}", file=sys.stderr)
            continue
        path = os.path.join(OUT, src["key"] + (".txt" if src["url"].endswith(".txt") else ".html"))
        with open(path, "wb") as fh:
            fh.write(body)
        manifest.append({
            **src,
            "status": status,
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "retrieved": "2026-08-18",
            "local": os.path.basename(path) + " (fetched, not committed)",
        })
        print(f"{status} {len(body):>8} {src['key']}")

    with open(os.path.join(OUT, "MANIFEST.json"), "w", encoding="utf-8") as fh:
        json.dump({
            "night": "2026-08-18",
            "session": 61,
            "note": "Bytes fetched and hashed, deliberately not committed; see PROTOCOL.md, "
                    "amendment of 2026-08-18. Re-fetch and compare sha256 to reproduce.",
            "sources": manifest,
        }, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


if __name__ == "__main__":
    main()
