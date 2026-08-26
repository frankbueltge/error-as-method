#!/usr/bin/env python3
"""context.py — Session 71, 2026-08-26.

Fetches the house's three machine-readable catalogues and asks them, before this
night claims anything is new, whether the field already holds it. Commits none of
them — they are feeds, not copies (team note, 2026-08-13).

Session 70's open thread 5 stands over this file: **every count over the house
catalogues names its matching rule.** S69 read *Rheinberger* as 6 and S70 as 3
over the same feed, because neither had said whether it was matching substrings
or words. Both rules are computed here for every term, and both are recorded.

Also fetches the prose sources this night's argument leans on, hashes them, and
commits none of them.

Usage:
    python3 context.py
"""

import datetime as dt
import hashlib
import json
import os
import re
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "error-as-method/session-71 (nightly research line)"

CATALOGUES = {
    "atlas/werke.json": "https://frankbueltge.de/atlas/werke.json",
    "papers/index.json": "https://frankbueltge.de/papers/index.json",
    "datasets/register.json": "https://frankbueltge.de/datasets/register.json",
}

TERMS = [
    # tonight's vocabulary
    "code review", "peer review", "patch set", "patchset", "gerrit", "trybot",
    "continuous integration", "linter", "static analysis", "test suite",
    "release engineering", "deprecation", "changelog", "forecast",
    "version control", "repository mining", "software history", "provenance",
    # the position's vocabulary, carried from S64/S70 for continuity
    "rheinberger", "epistemic thing", "canguilhem", "simondon", "norm",
    "observer", "dependability",
]

PROSE = [
    ("https://go.dev/doc/godebug",
     "Go's own account of GODEBUG and its compatibility mechanism"),
    ("https://go.dev/doc/go1compat",
     "the Go 1 compatibility promise the GODEBUG mechanism serves"),
    ("https://go.dev/doc/contribute",
     "the project's description of its own review process"),
    ("https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html",
     "the REST API this night's evidence comes through"),
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.status, r.read()


def count(blob, term):
    """Two rules, both stated, neither privileged."""
    low = blob.lower()
    t = term.lower()
    substring = low.count(t)
    word = len(re.findall(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", low))
    return {"substring": substring, "word_boundary": word}


def main():
    out = {"fetched": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
           "matching_rules": {
               "substring": "case-folded str.count; 'Epistemic Things' contains "
                            "'epistemic thing'",
               "word_boundary": "case-folded, no [a-z0-9] immediately either "
                                "side; 'Epistemic Things' does NOT match "
                                "'epistemic thing'"},
           "catalogues": {}, "prose": []}

    print("context -- the house catalogues, with the matching rule stated\n")
    for name, url in CATALOGUES.items():
        try:
            st, raw = get(url)
        except Exception as e:                     # noqa: BLE001
            print(f"  {name}: UNREACHABLE ({e})")
            out["catalogues"][name] = {"url": url, "reachable": False,
                                       "error": str(e)}
            continue
        blob = raw.decode("utf-8", "replace")
        try:
            d = json.loads(blob)
        except json.JSONDecodeError:
            d = None
        declared = None
        n = None
        if isinstance(d, dict):
            declared = d.get("count")
            for k in ("entries", "works", "papers", "datasets", "items"):
                if isinstance(d.get(k), list):
                    n = len(d[k])
                    break
        elif isinstance(d, list):
            n = len(d)
        rec = {"url": url, "http_status": st, "bytes": len(raw),
               "sha256": hashlib.sha256(raw).hexdigest(),
               "declared_count": declared, "len_entries": n,
               "counts_agree": (declared is None or declared == n),
               "committed": False,
               "terms": {t: count(blob, t) for t in TERMS}}
        out["catalogues"][name] = rec
        print(f"  {name}: {st} · declared {declared} · len {n} · "
              f"agree {rec['counts_agree']}")
        hits = {t: v for t, v in rec["terms"].items()
                if v["substring"] or v["word_boundary"]}
        for t, v in sorted(hits.items()):
            mark = "" if v["substring"] == v["word_boundary"] else "   <- rules differ"
            print(f"      {t:24s} substring {v['substring']:3d} · "
                  f"word {v['word_boundary']:3d}{mark}")
        if not hits:
            print("      no term matched under either rule")

    print("\n  prose sources (fetched, hashed, none committed):")
    for url, what in PROSE:
        try:
            st, raw = get(url)
        except Exception as e:                     # noqa: BLE001
            st, raw = 0, str(e).encode()
        out["prose"].append({"url": url, "http_status": st, "bytes": len(raw),
                             "sha256": hashlib.sha256(raw).hexdigest(),
                             "what": what, "committed": False})
        print(f"    {st}  {len(raw):8d}  {url}")

    with open(os.path.join(HERE, "catalogues.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)

    mp = os.path.join(HERE, "sources", "MANIFEST.json")
    man = json.load(open(mp))
    for name, rec in out["catalogues"].items():
        if rec.get("reachable") is False:
            continue
        man["entries"].append({
            "url": rec["url"], "http_status": rec["http_status"],
            "bytes": rec["bytes"], "sha256": rec["sha256"],
            "fetched": out["fetched"],
            "what": f"house catalogue {name}; declared count "
                    f"{rec['declared_count']}, len {rec['len_entries']}",
            "committed": False})
    for p in out["prose"]:
        man["entries"].append({**p, "fetched": out["fetched"]})
    # This script may be re-run when a source URL is corrected; keep the last
    # entry per (url, what) so a re-run does not double the manifest.
    seen = {}
    for e in man["entries"]:
        seen[(e.get("url"), e.get("what"))] = e
    man["entries"] = list(seen.values())
    with open(mp, "w") as f:
        json.dump(man, f, indent=1)
    print(f"\n  wrote catalogues.json; MANIFEST now {len(man['entries'])} entries")


if __name__ == "__main__":
    main()
