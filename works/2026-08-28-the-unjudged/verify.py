#!/usr/bin/env python3
"""verify.py — Session 73, 2026-08-28.

Asks the institution's own pages whether the dump is telling the truth about the
population this night measures. Session 72's sharpest correction came from doing
exactly this and not from the dump, so it is done again, on a different question.

For a seeded random sample of the errata that the dump calls *Reported*, plus a
few named ones the work quotes, it fetches https://www.rfc-editor.org/errata/eid<N>
and reads back the four fields that carry tonight's claims: displayed status,
displayed type, displayed date reported, and the "Source of RFC" line, which the
dump does not carry at all. Nothing is fetched twice; the pages are not committed.

Usage:
    python3 verify.py --raw ../../../.raw --sample 25 --seed 73
"""

import argparse
import datetime
import html
import json
import os
import random
import re
import time
import urllib.request

UA = "error-as-method/night-2026-08-28 (research; contact f.bueltge@gmail.com)"
NAMED = ["2016", "2017", "3917", "7000"]   # quoted in the work, or checked as controls


def plain(markup):
    text = re.sub(r"(?s)<(script|style).*?</\1>", " ", markup)
    text = re.sub(r"(?s)<[^>]+>", "\n", text)
    text = html.unescape(text)
    return re.sub(r"\n\s*\n+", "\n", text)


def field(text, label):
    m = re.search(rf"^\s*{re.escape(label)}\s*:?\s*$\n(.+)$", text, re.M)
    return m.group(1).strip() if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=os.path.join(os.path.dirname(__file__), "..", "..", "..", ".raw"))
    ap.add_argument("--sample", type=int, default=25)
    ap.add_argument("--seed", type=int, default=73)
    args = ap.parse_args()
    raw = os.path.abspath(args.raw)
    here = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(raw, "errata.json"), encoding="utf-8") as fh:
        errata = json.load(fh)
    by_id = {str(e["errata_id"]): e for e in errata}
    pending = sorted(str(e["errata_id"]) for e in errata
                     if e["errata_status_code"] == "Reported")

    rng = random.Random(args.seed)
    chosen = rng.sample(pending, args.sample)
    targets = list(dict.fromkeys(chosen + NAMED))

    checks = []
    agree = disagree = unreachable = 0
    for eid in targets:
        url = f"https://www.rfc-editor.org/errata/eid{eid}"
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                text = plain(resp.read().decode("utf-8", "replace"))
                status_code = resp.status
        except Exception as err:                                # noqa: BLE001
            checks.append({"errata_id": eid, "url": url, "http": str(err)})
            unreachable += 1
            continue
        rec = by_id.get(eid, {})
        got = {
            "errata_id": eid,
            "url": url,
            "http": status_code,
            "page_status": field(text, "Status"),
            "page_type": field(text, "Type"),
            "page_date_reported": field(text, "Date Reported"),
            "page_source_of_rfc": field(text, "Source of RFC"),
            "dump_status": rec.get("errata_status_code"),
            "dump_type": rec.get("errata_type_code"),
            "dump_submit_date": rec.get("submit_date"),
        }
        got["agrees"] = (got["page_status"] == got["dump_status"]
                         and got["page_type"] == got["dump_type"]
                         and got["page_date_reported"] == got["dump_submit_date"])
        agree += 1 if got["agrees"] else 0
        disagree += 0 if got["agrees"] else 1
        checks.append(got)
        time.sleep(0.7)

    out = {
        "when": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "seed": args.seed,
        "sample_size": args.sample,
        "sampled_from": "the 728 errata the dump calls Reported",
        "named_extra": NAMED,
        "agree": agree,
        "disagree": disagree,
        "unreachable": unreachable,
        "checks": checks,
    }
    path = os.path.join(here, "verification.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"{agree} agree, {disagree} disagree, {unreachable} unreachable -> {path}")


if __name__ == "__main__":
    main()
