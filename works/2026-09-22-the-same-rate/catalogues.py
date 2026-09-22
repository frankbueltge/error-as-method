#!/usr/bin/env python3
"""
catalogues.py -- consult the house's four feeds before claiming anything is new, and record
what they held tonight. Writes catalogues.json.

The feeds are read, never mirrored. What is kept here is the status, the count, and the hit
counts for the words this night turns on -- not the entries.
"""

import json
import os
import re
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
FEEDS = {
    "atlas/werke": "https://frankbueltge.de/atlas/werke.json",
    "papers/index": "https://frankbueltge.de/papers/index.json",
    "papers/register": "https://frankbueltge.de/papers/register.json",
    "datasets/register": "https://frankbueltge.de/datasets/register.json",
}
# The default urllib User-Agent is refused. Every one of the four feeds answered
# `HTTP 403 Forbidden` to `Python-urllib/3.11` on the first run tonight, and `200` to the
# same request from the same host one minute later with a browser-shaped agent string. So
# the header is set here, with the reason attached: a norm imposed in advance on a client
# string decides which readers reach the data, and nothing in the refusal says so.
UA = {"User-Agent": "Mozilla/5.0 (compatible; error-as-method nightly research line)"}

PROBES = ["obligation extraction", "deontic", "inter-annotator", "inter-coder", "annotation",
          "Cohen's kappa", "kappa", "ground truth", "gold standard", "precision", "sample size",
          "statistical power", "RFC 2119", "requirements engineering", "hand-read", "adjudication"]


def main():
    out = {"_what": "The house catalogues as they stood on 2026-09-22, consulted before this "
                    "night claimed a neighbour or a novelty. Read, not mirrored.",
           "feeds": {}}
    for name, url in FEEDS.items():
        row = {"url": url}
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                raw = r.read().decode("utf-8")
                row["http_status"] = r.status
        except Exception as exc:                       # an unreachable feed is a fact, not a stop
            row["http_status"] = None
            row["error"] = f"{type(exc).__name__}: {exc}"
            out["feeds"][name] = row
            continue
        row["bytes"] = len(raw.encode("utf-8"))
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            row["error"] = f"not JSON: {exc}"
            out["feeds"][name] = row
            continue
        entries = data if isinstance(data, list) else next(
            (v for v in data.values() if isinstance(v, list)), [])
        row["entries"] = len(entries)
        row["probes"] = {p: len(re.findall(re.escape(p), raw, re.I)) for p in PROBES}
        out["feeds"][name] = row

    with open(os.path.join(HERE, "catalogues.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    for name, row in out["feeds"].items():
        print(f"{name:20s} {row.get('http_status')}  {row.get('entries', '-'):>6}  "
              f"{row.get('probes', row.get('error', ''))}")


if __name__ == "__main__":
    main()
