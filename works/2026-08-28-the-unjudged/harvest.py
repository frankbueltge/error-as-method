#!/usr/bin/env python3
"""harvest.py — Session 73, 2026-08-28.

Fetches what tonight reads: the RFC Editor's complete errata record, the RFC
index it is joined against, the texts in which the institution states the norm
under which errata are judged, and the philosophical source read *before* the
measurement (the swerve).

It fetches; it does not measure. Every number in this work comes out of
measure.py, which is offline and reads only what this script wrote.

Three rules, inherited from Session 71's and Session 72's harvests and not
incidental:

  1. **No third-party document is committed as bytes.** The errata dump carries
     `orig_text`, `correct_text` and `notes` — text written by identifiable
     submitters and reviewers, published by the RFC Editor with no general
     redistribution licence. The Canguilhem extract carries an explicit refusal
     of redistribution on its own title page ("Toute reproduction et rediffusion
     de nos fichiers est interdite"). Everything fetched here is written to a raw
     cache OUTSIDE the repository (--raw, default ../../../.raw, one level above
     the clone); the committed record carries metadata, hashes and derived
     aggregates only, and this work quotes within citation length. Outside rather
     than merely gitignored, and deliberately: the landing gate's allowlist does
     not cover .gitignore — it refused Session 72's first push for exactly that —
     and a cache that is only ignored is one `git add -A` away from being
     committed by a session that did not read this file.
     PROTOCOL.md: "Sources are committed only where the licence permits
     redistribution".
  2. **Every fetch is recorded** in sources/MANIFEST.json with URL, HTTP status,
     byte count and SHA-256, so a stranger re-fetches and compares.
  3. **Nothing is retried into silence.** A URL that never returns 200 is
     recorded with the status it did return, and the run says so.

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

UA = "error-as-method/night-2026-08-28 (research; contact f.bueltge@gmail.com)"

SOURCES = [
    {
        "name": "errata.json",
        "url": "https://www.rfc-editor.org/errata.json",
        "what": "The RFC Editor's complete errata record: every report against every RFC, with "
                "its status, type, section, submitted and corrected text, submitter, verifier "
                "and dates. Tonight's population is the subset of it that has no verdict.",
    },
    {
        "name": "rfc-index.xml",
        "url": "https://www.rfc-editor.org/rfc-index.xml",
        "what": "The RFC index: per-RFC publication date, stream, current status and the "
                "obsoletes/obsoleted-by relations. Tonight joins against stream and "
                "obsoleted-by to ask whether a difference waits longer where the applier of "
                "the norm is structurally absent.",
    },
    {
        "name": "errata-definitions.html",
        "url": "https://www.rfc-editor.org/errata-definitions/",
        "what": "The RFC Editor's own definitions of the four errata statuses and two types — "
                "the norm as the publisher states it, including the definition of Reported.",
    },
    {
        "name": "errata-search.html",
        "url": "https://www.rfc-editor.org/errata.php",
        "what": "The errata search page: the public surface on which a Reported erratum stands "
                "beside a Verified one. Fetched to check what a reader is told about waiting.",
    },
    {
        "name": "iesg-statement-2021.html",
        "url": "https://www.ietf.org/about/groups/iesg/statements/processing-errata-ietf-stream/",
        "what": "IESG Statement, 7 May 2021, active: how errata on the IETF stream are judged. "
                "Read for one thing tonight — whether it states any norm about WHEN.",
    },
    {
        "name": "iesg-statement-2021-datatracker.html",
        "url": "https://datatracker.ietf.org/doc/statement-iesg-iesg-processing-of-rfc-errata-"
               "for-the-ietf-stream-20210507/",
        "what": "The same statement in the datatracker, which carries its date and status. "
                "Fetched as the dated copy of the norm.",
    },
    {
        "name": "iesg-statement-2008.html",
        "url": "https://www.ietf.org/about/groups/iesg/statements/processing-rfc-errata/",
        "what": "IESG Statement, 30 July 2008, marked Replaced: the previous version of the "
                "same norm, and the one in force over most of the waiting this work measures.",
    },
    {
        "name": "rfc7322.txt",
        "url": "https://www.rfc-editor.org/rfc/rfc7322.txt",
        "what": "RFC 7322, the RFC Style Guide — the RFC Editor's own procedural document. "
                "Read for the same single question: is there a written norm about when an "
                "erratum must be dealt with?",
    },
    {
        # Added in a second pass, after the measurement showed that the two paths
        # through the norm end at two different kinds of desk. Fetched with
        # --only, so the errata dump this night measures is not re-fetched and
        # cannot change under the numbers already computed.
        "name": "rfc9280.txt",
        "url": "https://www.rfc-editor.org/rfc/rfc9280.txt",
        "what": "RFC 9280, 'RFC Editor Model (Version 3)' — the document that says what the RFC "
                "Editor function is and how it is staffed. Read for one question: whether the "
                "desk that disposes of editorial errata in a median of five days is a contracted "
                "function, where the desk that receives technical ones is not.",
    },
    {
        "name": "canguilhem-normal-pathologique-extract.rtf",
        "url": "https://classiques.uqam.ca/collection_methodologie/canguilhem_georges/"
               "normal_et_pathologique/Canguilhem_normal_et_pathologique.rtf",
        "what": "Georges Canguilhem, 'Le normal et le pathologique' (Paris: PUF, coll. Galien, "
                "1979 [1st ed. 1966]), the excerpt pp. 96-117, 155-157, 175-179 published by "
                "Les Classiques des sciences sociales (UQAC) under the title 'Statistique, "
                "moyenne, norme et anormalite'. THE SWERVE: read before the measurement, not "
                "after. Named unread in this line's open threads for nine sessions. Its own "
                "use policy forbids redistribution, so it is read and quoted, never committed.",
    },
]


def fetch(url, raw_dir, name):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            body = resp.read()
            status = resp.status
            final = resp.geturl()
    except urllib.error.HTTPError as err:
        return {"http_status": err.code, "bytes": 0, "sha256": None, "final_url": url}
    except Exception as err:                                   # noqa: BLE001
        return {"http_status": f"error: {err}", "bytes": 0, "sha256": None, "final_url": url}
    path = os.path.join(raw_dir, name)
    with open(path, "wb") as fh:
        fh.write(body)
    return {
        "http_status": status,
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "final_url": final,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=os.path.join(os.path.dirname(__file__), "..", "..", "..", ".raw"))
    ap.add_argument("--only", default=None,
                    help="fetch just this source name and merge it into the existing manifest. "
                         "Exists so a source found necessary DURING the night can be added "
                         "without re-fetching the dump the night has already measured.")
    args = ap.parse_args()
    raw_dir = os.path.abspath(args.raw)
    os.makedirs(raw_dir, exist_ok=True)

    here = os.path.dirname(os.path.abspath(__file__))
    if raw_dir.startswith(os.path.abspath(os.path.join(here, "..", ".."))):
        sys.exit(f"refusing to write the raw cache inside the repository: {raw_dir}")

    entries = []
    failed = 0
    todo = SOURCES if args.only is None else [s for s in SOURCES if s["name"] == args.only]
    if not todo:
        sys.exit(f"no source named {args.only!r}")
    for src in todo:
        got = fetch(src["url"], raw_dir, src["name"])
        if got["http_status"] != 200:
            failed += 1
        entries.append({
            "url": src["url"],
            "final_url": got["final_url"],
            "http_status": got["http_status"],
            "bytes": got["bytes"],
            "sha256": got["sha256"],
            "fetched": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "what": src["what"],
            "cached_as": src["name"],
            "committed": False,
        })
        print(f"{got['http_status']:>6}  {got['bytes']:>10}  {src['name']}")

    out = os.path.join(here, "sources", "MANIFEST.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if args.only is not None and os.path.exists(out):
        with open(out, encoding="utf-8") as fh:
            previous = json.load(fh)["entries"]
        kept = [e for e in previous if e["cached_as"] != args.only]
        order = {s["name"]: i for i, s in enumerate(SOURCES)}
        entries = sorted(kept + entries, key=lambda e: order.get(e["cached_as"], 99))

    manifest = {
        "note": "Fetched, hashed, and NOT committed. The errata dump and the RFC index carry "
                "third-party authored text published without a general redistribution licence; "
                "the norm pages are the IETF's and the RFC Editor's own; the Canguilhem extract "
                "carries an explicit prohibition on redistribution. All of it lives only in an "
                "uncommitted raw cache outside the repository. This work quotes within citation "
                "length and commits derived aggregates. Re-fetch and compare the sha256 to "
                "reproduce.",
        "raw_cache": raw_dir,
        "entries": entries,
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"\n{len(entries)} sources, {failed} not 200 -> {out}")


if __name__ == "__main__":
    main()
