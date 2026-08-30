#!/usr/bin/env python3
"""verify.py — Session 75, 2026-08-30.

The numbers P1, P2 and P3 rest on come from one place: the `company_response` and `timely` facets
of one faceted query per branch. A facet is a single number computed by the far end and handed over;
if the far end computes it wrongly, or if this night reads the wrong node of the response, nothing
inside `measure.py` would notice, because `measure.py` never sees the record.

So this script re-derives the same distributions by a different decomposition: one count-only query
per (branch × response value) and per (branch × timeliness value), each an independently issued
request whose answer is a total rather than a bucket. It then checks that the counts sum to the
branch total, and — for the largest branch — that eighteen monthly counts sum to it as well.

A disagreement between two views of one record is a claim about the comparator until the comparator
has been cleared (F-081, Session 74). If the first run disagrees, the work says so.

Usage:
    python3 verify.py --out verification.json
"""

import argparse
import json
import os
import time
import urllib.parse
import urllib.request

UA = "error-as-method/night-2026-08-30 (research; contact f.bueltge@gmail.com)"
API = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"
DELAY = 0.12

RESPONSES = ["Closed with explanation", "Closed with non-monetary relief",
             "Closed with monetary relief", "Untimely response", "In progress"]
TIMELY = ["Yes", "No"]


def count(window, **params):
    q = {"date_received_min": window["date_received_min"],
         "date_received_max": window["date_received_max"],
         "no_aggs": "true", "size": 0}
    q.update(params)
    url = API + "?" + urllib.parse.urlencode(q)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read().decode("utf-8"))
    time.sleep(DELAY)
    return d["hits"]["total"]["value"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="verification.json")
    args = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    H = json.load(open(os.path.join(here, "harvest.json")))
    window = H["window"]
    by = H["by_product"]
    branches = sorted(by, key=lambda p: -by[p]["total_from_aggs_query"])

    out = {"night": "2026-08-30", "session": 75, "window": window,
           "method": "one count-only query per (branch, value), compared with the facet bucket "
                     "the argument actually used; a second route to the same number.",
           "comparisons": 0, "disagreements": [], "branches": {}}

    for p in branches:
        facet_resp = dict(by[p]["company_response"])
        facet_tim = dict(by[p]["timely"])
        n = by[p]["total_from_aggs_query"]
        row = {"n": n, "response": {}, "timely": {}}
        got = 0
        for v in RESPONSES:
            c = count(window, product=p, company_response=v)
            f = facet_resp.get(v, 0)
            row["response"][v] = {"count_query": c, "facet": f}
            out["comparisons"] += 1
            got += c
            if c != f:
                out["disagreements"].append({"branch": p, "field": "company_response",
                                             "value": v, "count_query": c, "facet": f})
        for v in TIMELY:
            c = count(window, product=p, timely=v)
            f = facet_tim.get(v, 0)
            row["timely"][v] = {"count_query": c, "facet": f}
            out["comparisons"] += 1
            if c != f:
                out["disagreements"].append({"branch": p, "field": "timely", "value": v,
                                             "count_query": c, "facet": f})
        row["responses_sum"] = got
        row["unaccounted_for"] = n - got
        out["branches"][p] = row
        print(f"  {p[:44]:44s} n={n:>9,}  responses sum {got:>9,}  "
              f"unaccounted {n - got:>6,}")

    # a third decomposition, on the largest branch only: eighteen months must sum to the whole
    big = branches[0]
    months, tot = [], 0
    y, m = 2023, 1
    while (y, m) <= (2024, 6):
        nm_y, nm_m = (y, m + 1) if m < 12 else (y + 1, 1)
        c = count({"date_received_min": f"{y:04d}-{m:02d}-01",
                   "date_received_max": f"{nm_y:04d}-{nm_m:02d}-01"}, product=big)
        # the max bound is inclusive, so the first day of the next month is counted twice over
        # a naive sum; take it off by counting that single day and subtracting it.
        edge = count({"date_received_min": f"{nm_y:04d}-{nm_m:02d}-01",
                      "date_received_max": f"{nm_y:04d}-{nm_m:02d}-01"}, product=big)
        months.append({"month": f"{y:04d}-{m:02d}", "count": c - edge, "next_day_edge": edge})
        tot += c - edge
        y, m = nm_y, nm_m
    out["monthly_decomposition"] = {
        "branch": big, "months": months, "sum": tot,
        "branch_total": by[big]["total_from_aggs_query"],
        "agrees": tot == by[big]["total_from_aggs_query"],
    }
    out["comparisons"] += 1
    if not out["monthly_decomposition"]["agrees"]:
        out["disagreements"].append({"branch": big, "field": "monthly decomposition",
                                     "count_query": tot,
                                     "facet": by[big]["total_from_aggs_query"]})

    json.dump(out, open(os.path.join(here, args.out), "w"), indent=1)
    print(f"\n{out['comparisons']} comparisons, {len(out['disagreements'])} disagreements")
    for d in out["disagreements"][:20]:
        print("  ", d)


if __name__ == "__main__":
    main()
