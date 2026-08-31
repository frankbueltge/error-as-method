#!/usr/bin/env python3
"""The interface, tested on a window this night does not predict over.

F-084 (register 030): *test an interface on data outside the population you are about to
predict over.* F-085 (register 031), filed the next night because F-084 was read and broken
inside a day: *before touching the object, re-read the rules of the last three registers and
write down which apply.*

The population of this night is `year=2025`. Every query in this file is `year=2024`.

Three things are in question and none of them is a fact about 2025:

  1. Does a `facet=issue` response list *every* issue type that occurs, or does it truncate?
     (F-087: a limit observed once under one filter is a conjecture about the instrument.)
  2. Does repeating the `issue` parameter give the union of the flags, so that
     `total - union` is exactly the number of records carrying no flag at all?
  3. Where does a record land when the box itself cannot be read — is
     `BASIS_OF_RECORD_INVALID` confined to one branch?

Output: `interface-test.json`, committed, so that the answers this night relies on can be
checked without re-running it.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gbif import Client  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
YEAR = "2024"          # the interface year: NOT the population
BRANCH = "FOSSIL_SPECIMEN"   # the smallest branch, so the count-only cross-check is affordable


def main():
    c = Client(log=os.path.join(HERE, "interface-test.log"))
    issues = c.get("enumeration/basic/OccurrenceIssue", [])
    out = {
        "interface_year": YEAR,
        "population_year_this_does_not_touch": "2025",
        "issue_enum_size": len(issues),
        "issue_enum": issues,
    }

    total = c.get("occurrence/search", [("limit", "0"), ("year", YEAR), ("basisOfRecord", BRANCH)])["count"]
    out["branch_total"] = {"branch": BRANCH, "count": total}

    # 1. facet completeness, at three declared facetLimits
    facets = {}
    for lim in ("10", "105", "300"):
        d = c.get("occurrence/search", [("limit", "0"), ("year", YEAR), ("basisOfRecord", BRANCH),
                                        ("facet", "issue"), ("facetLimit", lim)])
        facets[lim] = {x["name"]: x["count"] for x in d["facets"][0]["counts"]}
    out["facet_sizes_by_facetLimit"] = {k: len(v) for k, v in facets.items()}

    # the reference: one count-only query per issue type, all 105
    counted = {}
    for i in issues:
        counted[i] = c.get("occurrence/search",
                           [("limit", "0"), ("year", YEAR), ("basisOfRecord", BRANCH), ("issue", i)])["count"]
    nonzero = {k: v for k, v in counted.items() if v}
    out["count_only_nonzero"] = len(nonzero)
    out["count_only"] = counted

    ref = facets["105"]
    out["facet_105_agrees_with_count_only"] = (ref == nonzero)
    out["facet_105_disagreements"] = {k: [ref.get(k, 0), nonzero.get(k, 0)]
                                      for k in set(ref) | set(nonzero) if ref.get(k, 0) != nonzero.get(k, 0)}

    # 2. the union trick
    union = c.get("occurrence/search",
                  [("limit", "0"), ("year", YEAR), ("basisOfRecord", BRANCH)] + [("issue", i) for i in issues])["count"]
    out["union_of_all_issues"] = union
    out["union_bounds_hold"] = (max(counted.values()) <= union <= sum(counted.values()) and union <= total)
    out["max_single_issue"] = max(counted.values())
    out["sum_of_single_issues"] = sum(counted.values())
    out["records_with_no_flag"] = total - union

    # 3. where an unreadable box lands
    d = c.get("occurrence/search", [("limit", "0"), ("year", YEAR), ("issue", "BASIS_OF_RECORD_INVALID"),
                                    ("facet", "basisOfRecord"), ("facetLimit", "40")])
    out["basis_of_record_invalid"] = {
        "window_total": d["count"],
        "by_branch": {x["name"]: x["count"] for x in d["facets"][0]["counts"]},
    }

    with open(os.path.join(HERE, "interface-test.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, "sources", "MANIFEST-interface-test.json"), "w", encoding="utf-8") as fh:
        json.dump(c.manifest_json(
            what="Every GBIF API query made by the interface test, all of them on year=2024.",
            why="F-084: the instrument is tested outside the population it will be used on.",
        ), fh, indent=1, ensure_ascii=False)

    print(json.dumps({k: v for k, v in out.items() if k not in ("issue_enum", "count_only")}, indent=1))


if __name__ == "__main__":
    main()
