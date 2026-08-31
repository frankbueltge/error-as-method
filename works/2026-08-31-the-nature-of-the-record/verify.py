#!/usr/bin/env python3
"""The measurement, re-derived by a decomposition the harvest never used.

F-081 (register 030): *a disagreement between two views of the same record is a claim about
your comparator until the comparator has been checked.* So the check has to be a genuinely
different route to the same two numbers, not a re-read of the same response.

Two routes:

  1. **By month.** Every branch total and every branch union is re-asked twelve times, once per
     `month=1..12`, and the twelve must sum to the one. Both numbers P1 depends on are
     re-derived from a partition the harvest never queried. A record with an unparseable month
     would break this — and if it does, that is a finding about the window and is reported as
     one, not smoothed.
  2. **Flag by flag, in the population.** For the smallest branch of the window, all 105 flags
     are asked one at a time with count-only queries and compared with the `facet=issue`
     response the harvest used. The interface test did this on `year=2024`; this does it inside
     the population, because F-087 says a limit observed once under one filter is a conjecture
     about the instrument.

Writes `verification.json` and `verify.log`.
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
    issues = h["issue_enum"]
    branches = h["branches"]

    c = Client(log=os.path.join(HERE, "verify.log"))
    V = {"route_1_by_month": {}, "route_2_flag_by_flag": {}, "disagreements": []}

    for b in sorted(branches, key=lambda x: branches[x]):
        months = {}
        for m in range(1, 13):
            base = [("limit", "0"), ("year", YEAR), ("basisOfRecord", b), ("month", str(m))]
            t = c.get(SEARCH, base)["count"]
            u = c.get(SEARCH, base + [("issue", i) for i in issues])["count"]
            months[m] = {"total": t, "union": u}
        st = sum(v["total"] for v in months.values())
        su = sum(v["union"] for v in months.values())
        row = {
            "months": months,
            "months_sum_total": st, "harvest_total": branches[b], "total_agrees": st == branches[b],
            "months_sum_union": su, "harvest_union": h["union_of_all_flags"][b],
            "union_agrees": su == h["union_of_all_flags"][b],
        }
        V["route_1_by_month"][b] = row
        if not row["total_agrees"]:
            V["disagreements"].append(f"{b}: months sum to {st}, harvest says {branches[b]}")
        if not row["union_agrees"]:
            V["disagreements"].append(f"{b}: month unions sum to {su}, harvest union {h['union_of_all_flags'][b]}")
        c._log(f"{b}: months {st:,} vs {branches[b]:,} ({row['total_agrees']}), "
               f"unions {su:,} vs {h['union_of_all_flags'][b]:,} ({row['union_agrees']})")

    smallest = min(branches, key=lambda x: branches[x])
    counted = {}
    for i in issues:
        counted[i] = c.get(SEARCH, [("limit", "0"), ("year", YEAR), ("basisOfRecord", smallest), ("issue", i)])["count"]
    facet = h["flag_incidence"][smallest]
    nonzero = {k: v for k, v in counted.items() if v}
    bad = {k: [facet.get(k, 0), nonzero.get(k, 0)] for k in set(facet) | set(nonzero)
           if facet.get(k, 0) != nonzero.get(k, 0)}
    V["route_2_flag_by_flag"] = {
        "branch": smallest, "branch_total": branches[smallest],
        "count_only_nonzero": len(nonzero), "facet_nonzero": len(facet),
        "agrees": not bad, "disagreements": bad, "count_only": counted,
    }
    if bad:
        V["disagreements"].append(f"{smallest}: facet and count-only disagree on {sorted(bad)}")
    c._log(f"{smallest}: facet {len(facet)} vs count-only {len(nonzero)} nonzero flags, agrees={not bad}")

    V["comparisons"] = 2 * 12 * len(branches) + len(issues)
    V["disagreement_count"] = len(V["disagreements"])
    with open(os.path.join(HERE, "verification.json"), "w", encoding="utf-8") as fh:
        json.dump(V, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, "sources", "MANIFEST-verify.json"), "w", encoding="utf-8") as fh:
        json.dump(c.manifest_json(
            what="Every query of the verification pass, all count-only over year=2025.",
            why="A second decomposition of the two numbers P1 depends on.",
        ), fh, indent=1, ensure_ascii=False)
    print(json.dumps({"comparisons": V["comparisons"], "disagreements": V["disagreements"]}, indent=1))


if __name__ == "__main__":
    main()
