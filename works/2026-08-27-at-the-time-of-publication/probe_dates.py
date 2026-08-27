#!/usr/bin/env python3
"""probe_dates.py — Session 72, 2026-08-27.

One question, asked of a seeded random sample: the bulk dump gives 5,157 of 8,021
errata the same `update_date`, 2019-09-10, which is a database migration and not a
judgement. Does the RFC Editor's own page for those errata still show the real date
the verdict was imposed?

Three cases seen by hand said yes. This turns three into a sample.

Output: date_probe.json — errata id, the dump's date, the date the page shows, and
whether they agree. Derived metadata only; no third-party prose is written out.

Usage:
    python3 probe_dates.py --raw ../../../.raw --n 40 --seed 72
"""

import argparse
import datetime
import hashlib
import html
import json
import random
import re
import sys
import time
import urllib.request

UA = "error-as-method/night-2026-08-27 (research; contact f.bueltge@gmail.com)"
MIGRATION = "2019-09-10"
# "Date Verified:", "Date Rejected:", "Date Held for Document Update:" — the page's own
# label for the moment a norm was imposed, whatever the verdict was.
DATE_RE = re.compile(r"Date\s+(Verified|Rejected|Held for Document Update)\s*:?\s*"
                     r"(\d{4}-\d{2}-\d{2})", re.I)


def text_of(b):
    t = b.decode("utf-8", "replace")
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", t)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    return re.sub(r"[ \t]+", " ", html.unescape(t))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="../../../.raw")
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--seed", type=int, default=72)
    args = ap.parse_args()

    errata = json.load(open(f"{args.raw}/errata.json"))
    pool = [e for e in errata
            if (e.get("update_date") or "").startswith(MIGRATION)
            and e["errata_status_code"] != "Reported"]
    random.seed(args.seed)
    sample = random.sample(pool, args.n)

    rows, digests = [], []
    for e in sample:
        url = f"https://www.rfc-editor.org/errata/eid{e['errata_id']}"
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                status, body = r.status, r.read()
        except Exception as exc:
            rows.append({"id": e["errata_id"], "http": str(exc), "page_date": None})
            continue
        digests.append(hashlib.sha256(body).hexdigest())
        m = DATE_RE.search(text_of(body))
        rows.append({
            "id": e["errata_id"], "doc": e["doc-id"], "http": status,
            "status": e["errata_status_code"],
            "dump_update_date": (e.get("update_date") or "")[:10],
            "page_label": m.group(1) if m else None,
            "page_date": m.group(2) if m else None,
        })
        time.sleep(0.4)

    agree = [r for r in rows if r.get("page_date") == MIGRATION]
    differ = [r for r in rows if r.get("page_date") and r["page_date"] != MIGRATION]
    nodate = [r for r in rows if r.get("http") == 200 and not r.get("page_date")]
    out = {
        "pool_size": len(pool), "sampled": len(sample), "seed": args.seed,
        "page_carries_a_different_date": len(differ),
        "page_repeats_the_migration_date": len(agree),
        "page_shows_no_verdict_date": len(nodate),
        "median_years_lost": None,
        "aggregate_sha256_over_sorted_page_digests":
            hashlib.sha256("\n".join(sorted(digests)).encode()).hexdigest(),
        "rows": rows,
    }
    gaps = sorted((datetime.date.fromisoformat(MIGRATION)
                   - datetime.date.fromisoformat(r["page_date"])).days / 365.2425
                  for r in differ)
    if gaps:
        out["median_years_lost"] = round(gaps[len(gaps) // 2], 2)
        out["max_years_lost"] = round(gaps[-1], 2)
        out["min_years_lost"] = round(gaps[0], 2)
    json.dump(out, open("date_probe.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
