#!/usr/bin/env python3
"""catalogues.py — Session 77, 2026-09-01.

The house's four feeds, consulted before this night claims anything is new, and
counted under BOTH matching rules — substring and word-boundary — with both
recorded, per Session 70's open thread 5 and Session 71's answer to it.

Feeds, never copies: nothing here is written into the repository except counts.

Usage:
    python3 catalogues.py --out catalogues.json
"""

import argparse
import json
import re
import sys
import urllib.request

UA = "error-as-method/night-2026-09-01 (research; contact f.bueltge@gmail.com)"
FEEDS = {
    "atlas/werke.json": "https://frankbueltge.de/atlas/werke.json",
    "papers/index.json": "https://frankbueltge.de/papers/index.json",
    "datasets/register.json": "https://frankbueltge.de/datasets/register.json",
}
TERMS = ["PostgreSQL", "SQLSTATE", "error code", "database", "DBMS",
         "exception handling", "source code", "software", "vocabulary",
         "controlled vocabulary", "SQL standard", "standard", "specification",
         "compliance", "conformance", "dead code", "unreachable", "unused",
         "norm", "normativity", "Canguilhem", "Simondon", "Rheinberger",
         "epistemic thing", "Bowker", "Star", "Desrosieres", "infrastructure",
         "residual category", "classification", "taxonomy", "error"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="catalogues.json")
    args = ap.parse_args()

    out = {"night": "2026-09-01", "session": 77,
           "note": "Counts only. The feeds are read, never mirrored.", "feeds": {}}
    for name, url in FEEDS.items():
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                status, raw = r.status, r.read()
        except Exception as exc:
            out["feeds"][name] = {"url": url, "http_status": str(exc), "reachable": False}
            continue
        doc = json.loads(raw)
        entries = doc.get("entries", doc) if isinstance(doc, dict) else doc
        blob = raw.decode("utf-8", "replace")
        counts = {}
        for t in TERMS:
            sub = len(re.findall(re.escape(t), blob, re.I))
            word = len(re.findall(r"\b" + re.escape(t) + r"\b", blob, re.I))
            counts[t] = {"substring": sub, "word_boundary": word}
        out["feeds"][name] = {
            "url": url, "http_status": status, "bytes": len(raw), "reachable": True,
            "declared_count": doc.get("count") if isinstance(doc, dict) else None,
            "len_entries": len(entries) if hasattr(entries, "__len__") else None,
            "counts": counts,
        }
        print(f"  {status}  {len(raw):>9}  {name}  "
              f"declared={out['feeds'][name]['declared_count']} "
              f"len={out['feeds'][name]['len_entries']}", file=sys.stderr)
    json.dump(out, open(args.out, "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
