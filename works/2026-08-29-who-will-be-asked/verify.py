#!/usr/bin/env python3
"""verify.py — Session 74, 2026-08-29.

Session 72 published a number out of a bulk feed and Session 73 found the feed's dates had been
overwritten by a migration. Since then every night checks its bulk source against the institution's
own per-item view before it argues from it.

Here the bulk source is Bugzilla's REST *search* endpoint, paged 1,000 at a time. The check is the
classic per-bug XML export, `show_bug.cgi?ctype=xml` — a different code path, and the one a reader
gets. Forty bugs, seeded, compared field by field. Timestamps are normalised: the search endpoint
answers in UTC, the XML export in the server's local time with an offset, and a night that compared
the strings would report a failure that is really its own.

Usage:
    python3 verify.py --raw ../../../.raw
"""

import argparse
import datetime
import html
import json
import os
import random
import re
import sys
import time
import urllib.request

UA = "error-as-method/night-2026-08-29 (research; contact f.bueltge@gmail.com)"
SEED = 740829
N = 40
FIELDS = {
    "product": "product",
    "component": "component",
    "type": "bug_type",
    "severity": "bug_severity",
    "status": "bug_status",
}


def xml_field(text, tag):
    match = re.search(r"<%s[^>]*>(.*?)</%s>" % (tag, tag), text, re.S)
    # XML-escaped: a component named "DOM: Core &amp; HTML" is the same string as the
    # bulk feed's "DOM: Core & HTML". The first run of this file reported two
    # disagreements that were entirely its own -- see the register, F-081.
    return html.unescape(match.group(1).strip()) if match else None


def to_utc(stamp):
    """'2024-01-17 10:46:44 -0800' -> datetime in UTC."""
    match = re.match(r"(\d{4}-\d\d-\d\d) (\d\d:\d\d:\d\d) ([+-]\d{4})", stamp.strip())
    if not match:
        return None
    naive = datetime.datetime.strptime(match.group(1) + " " + match.group(2), "%Y-%m-%d %H:%M:%S")
    sign = 1 if match.group(3)[0] == "+" else -1
    offset = datetime.timedelta(hours=int(match.group(3)[1:3]), minutes=int(match.group(3)[3:5]))
    return naive - sign * offset


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="../../../.raw")
    args = ap.parse_args()
    raw = os.path.abspath(args.raw)
    with open(os.path.join(raw, "population.json"), encoding="utf-8") as fh:
        bugs = {b["id"]: b for b in json.load(fh)}

    rng = random.Random(SEED)
    sample = sorted(rng.sample(sorted(bugs), N))
    checks, disagreements, failures = [], [], []
    for bug_id in sample:
        url = f"https://bugzilla.mozilla.org/show_bug.cgi?ctype=xml&id={bug_id}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as resp:
                text = resp.read().decode("utf-8", "replace")
        except Exception as err:  # noqa: BLE001 - recorded, never swallowed
            failures.append({"id": bug_id, "error": type(err).__name__})
            continue
        bulk = bugs[bug_id]
        row = {"id": bug_id, "fields": {}}
        for ours, theirs in FIELDS.items():
            mine, yours = bulk.get(ours), xml_field(text, theirs)
            agree = (mine or "") == (yours or "")
            row["fields"][ours] = {"bulk": mine, "page": yours, "agree": agree}
            if not agree:
                disagreements.append({"id": bug_id, "field": ours, "bulk": mine, "page": yours})
        their_ts = to_utc(xml_field(text, "creation_ts") or "")
        our_ts = datetime.datetime.strptime(bulk["creation_time"], "%Y-%m-%dT%H:%M:%SZ")
        agree = their_ts is not None and their_ts == our_ts
        row["fields"]["creation_time"] = {
            "bulk": bulk["creation_time"],
            "page_utc": their_ts.isoformat() if their_ts else None,
            "agree": agree,
        }
        if not agree:
            disagreements.append({"id": bug_id, "field": "creation_time",
                                  "bulk": bulk["creation_time"],
                                  "page": their_ts.isoformat() if their_ts else None})
        checks.append(row)
        time.sleep(0.2)

    total = sum(len(c["fields"]) for c in checks)
    out = {
        "night": "2026-08-29",
        "session": 74,
        "what": "the bulk search endpoint checked against the per-bug XML export",
        "seed": SEED,
        "sampled": N,
        "fetched": len(checks),
        "fetch_failures": failures,
        "field_comparisons": total,
        "disagreements": disagreements,
        "verdict": ("all fields agree" if not disagreements and not failures
                    else "see disagreements"),
        "checks": checks,
    }
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "verification.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(f"{len(checks)}/{N} bugs fetched, {total} field comparisons, "
          f"{len(disagreements)} disagreements, {len(failures)} fetch failures")
    for d in disagreements[:10]:
        print("  !!", d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
