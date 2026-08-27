#!/usr/bin/env python3
"""harvest.py — Session 72, 2026-08-27.

Fetches the RFC Editor's complete errata record, the RFC index, and the two
texts that state the norm under which errata are judged.

It fetches; it does not measure. Every number this night reports comes out of
measure.py, which is offline and reads only what this script wrote.

Three rules, kept from Session 71's harvest and not incidental:

  1. No third-party document is committed as bytes. The errata dump carries
     `orig_text`, `correct_text` and `notes` — text written by identifiable
     submitters and reviewers, published by the RFC Editor under the IETF
     Trust's terms, with no general redistribution licence. It is written to a
     raw cache OUTSIDE the repository altogether (--raw, whose default is
     ../../../.raw, one level above the clone); the committed record carries
     metadata, hashes and derived aggregates only, and the work quotes within
     citation length. Outside rather than merely gitignored, and deliberately:
     the landing gate's path allowlist does not cover .gitignore — it refused
     this night's first push for exactly that — and a cache that is only ignored
     is one `git add -A` away from being committed by a session that did not
     read this file, which is the incident no-committed-sources.yml exists
     because of. Same for rfc-index.xml (13.7 MB) and the two
     norm pages. PROTOCOL.md, "Sources are committed only where the licence
     permits redistribution".
  2. Every fetch is recorded in sources/MANIFEST.json with URL, HTTP status,
     byte count and SHA-256, so a stranger re-fetches and compares.
  3. Nothing is retried into silence: a URL that never returns 200 is recorded
     with the status it did return, and the run says so.

Usage:
    python3 harvest.py --raw ../../../.raw
"""

import argparse
import datetime
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request

UA = "error-as-method/night-2026-08-27 (research; contact f.bueltge@gmail.com)"

SOURCES = [
    {
        "name": "errata.json",
        "url": "https://www.rfc-editor.org/errata.json",
        "what": "The RFC Editor's complete errata record: every report against every RFC, "
                "with its status, type, section, submitted and corrected text, and dates.",
    },
    {
        "name": "rfc-index.xml",
        "url": "https://www.rfc-editor.org/rfc-index.xml",
        "what": "The RFC index: per-RFC publication date, stream, current status, and the "
                "obsoletes/obsoleted-by/updates/updated-by relations this night joins against.",
    },
    {
        "name": "errata-definitions.html",
        "url": "https://www.rfc-editor.org/errata-definitions/",
        "what": "The RFC Editor's own definitions of the four errata statuses and two types — "
                "the norm as the publisher states it.",
    },
    {
        "name": "iesg-errata-2021.html",
        "url": "https://datatracker.ietf.org/doc/statement-iesg-iesg-processing-of-rfc-errata-"
               "for-the-ietf-stream-20210507/",
        "what": "IESG Statement, 7 May 2021, active: how errata on the IETF stream are judged. "
                "The written norm, current version.",
    },
    {
        "name": "avizienis-nasa-2012.pdf",
        "url": "https://www.nasa.gov/wp-content/uploads/2015/04/"
               "640147main_day_3-algirdas_avizienis-2.pdf",
        "what": "A. Avizienis, 'Terminology Issues in Dependable Computing', NASA Formal Methods "
                "Workshop, 2012-04-12 — the dependability taxonomy's fault/error/failure "
                "definitions, in the words of one of the four authors of the 2004 paper. Read "
                "because open thread 3 has named this field unread for nine sessions. Not "
                "committed; quoted within citation length.",
    },
    {
        "name": "iesg-errata-2008.html",
        "url": "https://www.ietf.org/about/groups/iesg/statements/processing-rfc-errata/",
        "what": "IESG Statement, 30 July 2008, marked Replaced: the previous version of the same "
                "norm. Fetched because the norm has a date and this night measures that.",
    },
]

# Individual errata pages fetched by hand to verify, against the source of record, the
# claims the bulk dump is used to make. Each is load-bearing in work.md and so is listed
# individually rather than in aggregate. probe_dates.py fetches 40 further pages and
# records them as one aggregate digest in date_probe.json.
VERIFY = {
    "6534": "the impossible date, quarantined: reported 9999-04-13, held 2021-04-13",
    "1463": "RFC 4490 §4.1.1, Verified by one Area Director",
    "1465": "RFC 4490 §4.1.1, the identical claim, Held for Document Update by another",
    "1464": "RFC 4490 §4.2.1, Verified — the same pair again in the same document",
    "1466": "RFC 4490 §4.2.1, the identical claim, Held for Document Update",
    "2974": "RFC 4130 §7.4.3, Rejected: 'requires publication of a replacement RFC'",
    "3028": "RFC 4130 §7.4.3, same reported text, same day, Verified by another reviewer",
    "5899": "RFC 8584 §1.1, Rejected 2024-10-31",
    "5900": "RFC 8584 §1.1, same reported text, Verified by the same reviewer 2025-02-10",
}
for _eid, _why in VERIFY.items():
    SOURCES.append({
        "name": f"eid{_eid}.html",
        "url": f"https://www.rfc-editor.org/errata/eid{_eid}",
        "what": f"Erratum {_eid} on the RFC Editor's own page — {_why}.",
    })


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:  # recorded, never swallowed
        return str(e), b""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="../../../.raw")
    args = ap.parse_args()
    os.makedirs(args.raw, exist_ok=True)

    here = os.path.dirname(os.path.abspath(__file__))
    entries, failures = [], []
    for s in SOURCES:
        status, body = fetch(s["url"])
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if status == 200 and body:
            with open(os.path.join(args.raw, s["name"]), "wb") as fh:
                fh.write(body)
        else:
            failures.append((s["url"], status))
        entries.append({
            "url": s["url"],
            "http_status": status,
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "fetched": stamp,
            "what": s["what"],
            "committed": False,
        })
        print(f"  {status:>4}  {len(body):>10}  {s['url']}", file=sys.stderr)

    manifest = {
        "note": "Fetched, hashed, and NOT committed. The errata dump and the RFC index carry "
                "third-party authored text (submitters' and reviewers' words, RFC metadata) "
                "published without a general redistribution licence; the two norm pages are the "
                "IETF's and the RFC Editor's own texts. All five live only in an uncommitted raw "
                "cache; this work quotes within citation length and commits derived aggregates. "
                "Re-fetch and compare the sha256 to reproduce.",
        "entries": entries,
    }
    out = os.path.join(here, "sources", "MANIFEST.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fh:
        json.dump(manifest, fh, indent=1)
        fh.write("\n")

    if failures:
        print("\nFAILED (recorded in the manifest with the status they returned):", file=sys.stderr)
        for url, status in failures:
            print(f"  {status}  {url}", file=sys.stderr)
        return 1
    print(f"\n  {len(entries)} sources, all 200 -> {args.raw}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
