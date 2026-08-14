#!/usr/bin/env python3
"""harvest.py -- download and hash every source this night measures.

Session 55. The question is Session 54's first open thread, written down by that night
before it knew where to look:

    "Which came first, the withdrawal or the promise? ... The question to ask each
     candidate registry is not whether it has ever withdrawn an identifier but which
     came first, its first withdrawal or its promise never to withdraw."

S54's replacement claim, the thing this night is trying to break:

    "An institution learns the reach of its channel by exceeding it once. ... A body
     that has never withdrawn does not yet know what it cannot reach. One that has,
     freezes."

and the falsifier S54 wrote for it:

    "(1) an institution that forbade withdrawal *before* ever performing one -- a
     freeze with no scar; if permanence policies routinely precede any injury, the
     learning story is wrong."

The candidate is the IANA Language Subtag Registry (BCP 47). It has never withdrawn a
subtag, its stability rules were published in 2006, and it is downstream of four
standards that withdraw constantly. What I believed before running measure.py, recorded
here because it is the only genuinely pre-measurement statement I have tonight: that the
registry would turn out to be S54's falsifier 1 exactly -- a freeze with no scar -- and
that the interesting part would be the upstream deprecations it carries.

Network only here. Everything downstream is offline and deterministic.

    python3 harvest.py            -> cache/ + sources/MANIFEST.json
"""

import hashlib
import json
import os
import ssl
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
SOURCES = os.path.join(HERE, "sources")

# Every file this night's argument rests on. Key -> (url, filename, why).
TARGETS = {
    "subtag_registry": (
        "https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry",
        "language-subtag-registry.txt",
        "The registry itself. Every subtag ever assigned, with Added and Deprecated dates.",
    ),
    "iso639_3_retirements": (
        "https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3_Retirements.tab",
        "iso-639-3_Retirements.tab",
        "The upstream registration authority's own list of every code element it has retired.",
    ),
    "rfc1766": (
        "https://www.rfc-editor.org/rfc/rfc1766.txt",
        "rfc1766.txt",
        "1995. Names the editions of ISO 639 and ISO 3166 that fix the registry's memory floor.",
    ),
    "rfc3066": (
        "https://www.rfc-editor.org/rfc/rfc3066.txt",
        "rfc3066.txt",
        "2001. The tag registry the subtag registry was built out of.",
    ),
    "rfc4645": (
        "https://www.rfc-editor.org/rfc/rfc4645.txt",
        "rfc4645.txt",
        "2006. Initialisation rules, and a memo whose own contents were removed before publication.",
    ),
    "rfc4646": (
        "https://www.rfc-editor.org/rfc/rfc4646.txt",
        "rfc4646.txt",
        "2006. The promise: withdrawn codes remain valid in language tags.",
    ),
    "rfc5645": (
        "https://www.rfc-editor.org/rfc/rfc5645.txt",
        "rfc5645.txt",
        "2009. The bulk import of ISO 639-3, and the sentence that sets the second memory floor.",
    ),
    "rfc5646": (
        "https://www.rfc-editor.org/rfc/rfc5646.txt",
        "rfc5646.txt",
        "2009. The promise restated, plus the note on records deprecated before they were added.",
    ),
    "ggm_message": (
        "https://www.alvestrand.no/pipermail/ietf-languages/2014-February/012077.html",
        "ietf-languages-2014-02-10-batch1.html",
        "The Language Subtag Reviewer explaining, in 2014, why one code was never added.",
    ),
}


def fetch(url, path):
    ctx = ssl.create_default_context()
    bundle = "/root/.ccr/ca-bundle.crt"
    if os.path.exists(bundle):
        ctx.load_verify_locations(bundle)
    req = urllib.request.Request(url, headers={"User-Agent": "error-as-method/session-55"})
    with urllib.request.urlopen(req, timeout=90, context=ctx) as r:
        data = r.read()
    with open(path, "wb") as fh:
        fh.write(data)
    return data


def main():
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(SOURCES, exist_ok=True)
    manifest = {
        "harvested_by": "works/2026-08-14-the-threshold/harvest.py",
        "session": 55,
        "note": (
            "Feeds, not copies. The registry and the RFCs stay in the gitignored cache; "
            "sources/ keeps the decisive records cut out of them by evidence.py, plus the "
            "SHA-256 of every whole file, so any claim here can be checked against the "
            "original at its published URL."
        ),
        "files": {},
    }
    for key, (url, name, why) in TARGETS.items():
        path = os.path.join(CACHE, name)
        try:
            data = fetch(url, path)
            status = "ok"
        except Exception as exc:  # recorded, never invented
            if os.path.exists(path):
                data = open(path, "rb").read()
                status = "cached (fetch failed: %s)" % exc
            else:
                manifest["files"][key] = {"url": url, "file": name, "why": why,
                                          "status": "FAILED: %s" % exc}
                print("FAIL %-22s %s" % (key, exc), file=sys.stderr)
                continue
        manifest["files"][key] = {
            "url": url,
            "file": name,
            "why": why,
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "status": status,
        }
        print("ok   %-22s %8d bytes  %s" % (key, len(data), manifest["files"][key]["sha256"][:16]))

    with open(os.path.join(SOURCES, "MANIFEST.json"), "w") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print("\nwrote sources/MANIFEST.json (%d files)" % len(manifest["files"]))


if __name__ == "__main__":
    main()
