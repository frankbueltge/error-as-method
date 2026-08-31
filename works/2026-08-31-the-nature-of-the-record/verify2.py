#!/usr/bin/env python3
"""The second verification, written because the first one disagreed and the disagreement was real.

`verify.py` re-derives every branch total and every branch union by decomposing the window into
twelve months. For `OBSERVATION` the twelve months summed to 4,318 against a branch total of
8,136 — a shortfall of 3,818 records.

F-081 says a disagreement between two views of the same record is a claim about your comparator
until the comparator has been checked. It was checked, on the interface year and not on the
population: for `year=2024 & basisOfRecord=OBSERVATION` the endpoint reports 55,702 records, the
range query `month=1,12` reports 42,114, and the twelve single-month queries sum to exactly
42,114. The three agree with each other and all disagree with the total. **The comparator is
sound and the record has a hole in it**: a record can carry an interpreted year and no
interpreted month.

Which means the month decomposition is not a partition of the window and cannot be used as one.
So this file adds a decomposition that *is* complete: `hasCoordinate` is a boolean the index
sets on every record, so `true` and `false` exhaust the branch with nothing left over. If the
two halves do not sum to the whole, the fault is the comparator's after all.

Writes `verification-2.json`.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gbif import Client  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
YEAR = "2025"
SEARCH = "occurrence/search"


def main():
    with open(os.path.join(HERE, "harvest.json"), encoding="utf-8") as fh:
        h = json.load(fh)
    issues, branches = h["issue_enum"], h["branches"]

    c = Client(log=os.path.join(HERE, "verify2.log"))
    V = {"partition": "hasCoordinate true|false — a boolean the index sets on every record",
         "by_branch": {}, "disagreements": []}

    for b in sorted(branches, key=lambda x: branches[x]):
        half = {}
        for v in ("true", "false"):
            base = [("limit", "0"), ("year", YEAR), ("basisOfRecord", b), ("hasCoordinate", v)]
            half[v] = {"total": c.get(SEARCH, base)["count"],
                       "union": c.get(SEARCH, base + [("issue", i) for i in issues])["count"]}
        st = half["true"]["total"] + half["false"]["total"]
        su = half["true"]["union"] + half["false"]["union"]
        row = {"halves": half,
               "sum_total": st, "harvest_total": branches[b], "total_agrees": st == branches[b],
               "sum_union": su, "harvest_union": h["union_of_all_flags"][b],
               "union_agrees": su == h["union_of_all_flags"][b]}
        V["by_branch"][b] = row
        if not row["total_agrees"]:
            V["disagreements"].append(f"{b}: hasCoordinate halves sum to {st}, harvest {branches[b]}")
        if not row["union_agrees"]:
            V["disagreements"].append(f"{b}: half-unions sum to {su}, harvest union {h['union_of_all_flags'][b]}")
        c._log(f"{b}: {st:,} vs {branches[b]:,} ({row['total_agrees']}), "
               f"unions {su:,} vs {h['union_of_all_flags'][b]:,} ({row['union_agrees']})")

    # the month hole, measured rather than inferred, using the range form
    V["records_with_a_year_and_no_month"] = {}
    for b in branches:
        with_month = c.get(SEARCH, [("limit", "0"), ("year", YEAR), ("basisOfRecord", b), ("month", "1,12")])["count"]
        V["records_with_a_year_and_no_month"][b] = {
            "with_month": with_month, "branch_total": branches[b],
            "without_month": branches[b] - with_month,
            "without_month_pct": 100.0 * (branches[b] - with_month) / branches[b],
        }
    V["window_records_without_month"] = sum(v["without_month"] for v in V["records_with_a_year_and_no_month"].values())
    V["comparisons"] = 4 * len(branches) + len(branches)
    V["disagreement_count"] = len(V["disagreements"])

    with open(os.path.join(HERE, "verification-2.json"), "w", encoding="utf-8") as fh:
        json.dump(V, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, "sources", "MANIFEST-verify2.json"), "w", encoding="utf-8") as fh:
        json.dump(c.manifest_json(
            what="Every query of the second verification pass, count-only over year=2025.",
            why="A complete partition of each branch, after the month partition turned out not to be one.",
        ), fh, indent=1, ensure_ascii=False)
    print(json.dumps({"comparisons": V["comparisons"], "disagreements": V["disagreements"],
                      "window_records_without_month": V["window_records_without_month"]}, indent=1))


if __name__ == "__main__":
    main()
