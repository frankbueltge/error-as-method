#!/usr/bin/env python3
"""The night's harvest: one closed window of a data registry, read as counts only.

Population: every occurrence record GBIF's index returns for `year=2025`, as answered on
2026-08-31. Nothing here fetches a record. Every query is `limit=0` — the endpoint returns a
count and an empty result list — so this night reads 339 million records' worth of
classification without downloading one of them.

What is harvested, in this order:

  1. the window total;
  2. the branch set: `facet=basisOfRecord`, read off the window and not carried from anywhere
     (F-086);
  3. per branch, the **union of all 105 flags** — the `issue` parameter repeated 105 times,
     which the interface test on `year=2024` showed to be a union — so that
     `total - union` is exactly the count of records carrying no flag at all;
  4. per branch, the full flag incidence: `facet=issue&facetLimit=200`, shown by the same
     interface test to agree exactly with 105 count-only queries;
  5. where the records whose box could not be read have landed;
  6. who fills each branch: the five largest publishing organisations per branch, with their
     names resolved — F-082, *before comparing the branches of a classification, ask who fills
     each*, and in the same pass rather than afterwards.

Writes `harvest.json`, `harvest.log` and `sources/MANIFEST.json`. Cache-first: a resumed run
asks the endpoint for nothing it has already been told.
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
    c = Client(log=os.path.join(HERE, "harvest.log"))
    issues = c.get("enumeration/basic/OccurrenceIssue", [])
    out = {
        "population": {
            "endpoint": "https://api.gbif.org/v1/occurrence/search",
            "filter": "year=2025",
            "harvested_utc": None,
            "note": (
                "year is an INTERPRETED field. A record whose date GBIF could not read carries "
                "no year and is not in this population. The window is drawn with the instrument "
                "being measured; this is stated, not repaired."
            ),
        },
        "issue_enum_size": len(issues),
        "issue_enum": issues,
    }

    out["window_total"] = c.get(SEARCH, [("limit", "0"), ("year", YEAR)])["count"]
    c._log(f"window total {out['window_total']:,}")

    d = c.get(SEARCH, [("limit", "0"), ("year", YEAR), ("facet", "basisOfRecord"), ("facetLimit", "40")])
    branches = {x["name"]: x["count"] for x in d["facets"][0]["counts"]}
    out["branches"] = branches
    c._log(f"branch set of this window: {len(branches)} — {sorted(branches)}")

    out["union_of_all_flags"] = {}
    out["flag_incidence"] = {}
    for b in branches:
        u = c.get(SEARCH, [("limit", "0"), ("year", YEAR), ("basisOfRecord", b)]
                  + [("issue", i) for i in issues])["count"]
        out["union_of_all_flags"][b] = u
        f = c.get(SEARCH, [("limit", "0"), ("year", YEAR), ("basisOfRecord", b),
                           ("facet", "issue"), ("facetLimit", "200")])
        out["flag_incidence"][b] = {x["name"]: x["count"] for x in f["facets"][0]["counts"]}
        c._log(f"{b}: total {branches[b]:,}  union {u:,}  distinct flags {len(out['flag_incidence'][b])}")

    d = c.get(SEARCH, [("limit", "0"), ("year", YEAR), ("issue", "BASIS_OF_RECORD_INVALID"),
                       ("facet", "basisOfRecord"), ("facetLimit", "40")])
    out["basis_of_record_invalid"] = {
        "window_total": d["count"],
        "by_branch": {x["name"]: x["count"] for x in d["facets"][0]["counts"]},
    }

    # F-082 — who fills each branch
    out["publishers"] = {}
    names = {}
    for b in branches:
        d = c.get(SEARCH, [("limit", "0"), ("year", YEAR), ("basisOfRecord", b),
                           ("facet", "publishingOrg"), ("facetLimit", "5")])
        top = [(x["name"], x["count"]) for x in d["facets"][0]["counts"]]
        for key, _ in top:
            if key not in names:
                try:
                    names[key] = c.get(f"organization/{key}", [])["title"]
                except Exception as err:                      # noqa: BLE001
                    names[key] = f"<unresolved: {err}>"
        out["publishers"][b] = [{"key": k, "title": names[k], "records": n} for k, n in top]

    import time
    out["population"]["harvested_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    with open(os.path.join(HERE, "harvest.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, "sources", "MANIFEST.json"), "w", encoding="utf-8") as fh:
        json.dump(c.manifest_json(
            what="Every GBIF API query the harvest made, all of them count-only over year=2025.",
            why=("The night's population and its whole measurement. GBIF's responses are "
                 "re-fetchable by anyone without a key; the SHA-256 is the warrant."),
        ), fh, indent=1, ensure_ascii=False)
    c._log(f"done. {c.requests_made} requests, {c.cache_hits} cache hits, "
           f"{len(c.waits)} throttles, {len(c.resets)} resets.")


if __name__ == "__main__":
    main()
