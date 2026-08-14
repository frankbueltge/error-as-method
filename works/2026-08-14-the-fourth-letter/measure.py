#!/usr/bin/env python3
"""measure.py -- offline, deterministic, no network. Reads cache/, writes results.json.

Session 56. One upstream authority's dead, joined against three registers that stand
downstream of it or beside it, plus the authority's own three parallel namespaces.

    python3 measure.py            -> results.json
"""

import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")

# RFC 1766's normative reference for country codes: ISO 3166:1988 (E/F), 3rd edition,
# 1988-08-15. RFC 4645 rule 1 makes that date the registry's memory floor.
FLOOR = "1988-08-15"
# The day the Initial Language Subtag Registry was populated (every founding record's
# 'Added' value).
ILSR = "2005-10-16"


def read(name, binary=False):
    with open(os.path.join(CACHE, name), "rb" if binary else "r",
              **({} if binary else {"encoding": "utf-8", "errors": "replace"})) as f:
        return f.read()


def parse_registry(text):
    """The registry is RFC 2141-style records separated by %%; folded lines indent."""
    records = []
    for block in text.split("\n%%\n")[1:]:
        rec, key = {}, None
        for line in block.split("\n"):
            if line.startswith("  ") and key:
                rec[key] += " " + line.strip()
            elif ":" in line:
                k, v = line.split(":", 1)
                k, v = k.strip(), v.strip()
                rec[k] = rec[k] + " | " + v if k in rec else v
                key = k
        if rec:
            records.append(rec)
    return records


def norm_date(d):
    """ISO 3166-3 withdrawal dates are either YYYY or YYYY-MM-DD. Compare as YYYY-MM-DD."""
    return d if len(d) > 4 else d + "-12-31"


def main():
    reg_text = read("language-subtag-registry.txt")
    records = parse_registry(reg_text)
    file_date = re.search(r"File-Date:\s*(\S+)", reg_text).group(1)
    regions = [r for r in records if r.get("Type") == "region"]
    alpha2 = {r["Subtag"]: r for r in regions if len(r["Subtag"]) == 2 and r["Subtag"].isalpha()}
    numeric = [r for r in regions if r["Subtag"].isdigit()]

    iso3 = json.load(open(os.path.join(CACHE, "iso_3166-3.json")))["3166-3"]
    iso1 = json.load(open(os.path.join(CACHE, "iso_3166-1.json")))["3166-1"]
    live2 = {r["alpha_2"]: r for r in iso1}
    live3 = {r["alpha_3"]: r for r in iso1}

    cldr = read("cldr-supplementalMetadata.xml")
    aliases = dict(
        (m.group(1), (m.group(2), m.group(3)))
        for m in re.finditer(
            r'<territoryAlias type="([^"]+)" replacement="([^"]*)" reason="([^"]*)"/>', cldr)
    )

    rows = []
    for e in sorted(iso3, key=lambda x: (norm_date(x["withdrawal_date"]), x["alpha_4"])):
        a2, a3, a4 = e["alpha_2"], e["alpha_3"], e["alpha_4"]
        wd = norm_date(e["withdrawal_date"])
        rec = alpha2.get(a2)
        # Is the two-letter address in the registry, and does it hold THIS entity?
        # The matcher is deliberately crude and stated here rather than hand-curated: the
        # registry's Description and ISO 3166-3's name are held to name the same entity if
        # either one's first word occurs in the other. It gets all 31 rows right except
        # 'BY' (Belarus / Byelorussian SSR), which it calls a different entity; that one
        # case is argued in the work rather than legislated here.
        if rec is None:
            iana = "absent"
        else:
            desc = (rec.get("Description") or "").lower()
            nm = e["name"].lower()
            head_d = desc.split()[0].strip(",") if desc else ""
            head_n = nm.split()[0].strip(",")
            same = bool(head_d and (head_d in nm or head_n in desc))
            if same:
                iana = "deprecated-as-itself" if rec.get("Deprecated") else "live-as-itself"
            else:
                iana = "address-held-by-another"
        rows.append({
            "alpha_4": a4,
            "alpha_2": a2,
            "alpha_3": a3,
            "name": e["name"],
            "withdrawal_date": e["withdrawal_date"],
            "before_floor": wd < FLOOR,
            "iana": iana,
            "iana_description": rec.get("Description") if rec else None,
            "iana_added": rec.get("Added") if rec else None,
            "iana_deprecated": rec.get("Deprecated") if rec else None,
            "iana_preferred": rec.get("Preferred-Value") if rec else None,
            "iana_comments": rec.get("Comments") if rec else None,
            "cldr_alias": aliases.get(a2, (None, None))[0],
            "alpha_2_live_now": live2.get(a2, {}).get("name"),
            "alpha_3_live_now": live3.get(a3, {}).get("name"),
            "alpha_4_suffix": a4[2:],
            "alpha_4_suffix_is_live_code": a4[2:] in live2,
        })

    pre = [r for r in rows if r["before_floor"]]
    post = [r for r in rows if not r["before_floor"]]

    def tally(group):
        return dict(Counter(r["iana"] for r in group))

    results = {
        "session": 56,
        "date": "2026-08-14",
        "registry_file_date": file_date,
        "registry_records": len(records),

        "iso_3166_3": {
            "entries": len(rows),
            "oldest_withdrawal": rows[0]["withdrawal_date"],
            "newest_withdrawal": rows[-1]["withdrawal_date"],
            "withdrawn_before_the_register_existed": sum(
                1 for r in rows if norm_date(r["withdrawal_date"]) < "1999-01-01"),
            "note": "ISO 3166-3 was first published as ISO 3166-3:1999; every entry older than "
                    "that was imported, not observed.",
        },

        "the_floor": {
            "date": FLOOR,
            "source": "RFC 1766's normative reference, ISO 3166:1988 (E/F), 3rd edition, "
                      "1988-08-15, made the starting date by RFC 4645 rule 1.",
            "dead_before_floor": len(pre),
            "dead_after_floor": len(post),
            "latest_withdrawal_before_floor": max(
                norm_date(r["withdrawal_date"]) for r in pre),
            "earliest_withdrawal_after_floor": min(
                norm_date(r["withdrawal_date"]) for r in post),
            "clearance_years": round((int(min(norm_date(r["withdrawal_date"]) for r in post)[:4])
                                      - int(max(norm_date(r["withdrawal_date"])
                                                for r in pre)[:4])), 1),
        },

        "iana_registry": {
            "region_subtags": len(regions),
            "two_letter": len(alpha2),
            "numeric": len(numeric),
            "deprecated_region_subtags": sum(1 for r in regions if r.get("Deprecated")),
            "before_floor": tally(pre),
            "after_floor": tally(post),
            "czechoslovakia_in_registry": "Czechoslovak" in reg_text,
            "numeric_subtags_that_are_countries": [
                r["Subtag"] for r in numeric
                if r["Subtag"] in {c.get("numeric") for c in iso1}],
            "numeric_subtag_descriptions": sorted(r.get("Description", "") for r in numeric),
        },

        "cldr": {
            "territory_aliases": len(aliases),
            "dead_codes_aliased": sum(1 for r in rows if r["cldr_alias"]),
            "dead_codes_aliased_before_floor": sum(
                1 for r in rows if r["cldr_alias"] and r["before_floor"]),
            "aliased_but_absent_from_iana": sorted(
                r["alpha_2"] for r in rows if r["cldr_alias"] and r["iana"] == "absent"),
            "cs_alias": aliases.get("CS", (None, None))[0],
        },

        "recycling": {
            "alpha_2_reassigned": sorted(
                (r["alpha_2"], r["name"], r["alpha_2_live_now"])
                for r in rows if r["alpha_2_live_now"]),
            "alpha_3_reassigned": sorted(
                (r["alpha_3"], r["name"], r["alpha_3_live_now"])
                for r in rows if r["alpha_3_live_now"]),
            "alpha_4_reassigned": [],  # by construction: an alpha-4 is never an ISO 3166-1 code
            "space": {
                "alpha_2": {"possible": 26 ** 2, "assigned": len(iso1)},
                "alpha_3": {"possible": 26 ** 3, "assigned": len(iso1)},
                "alpha_4": {"possible": 26 ** 4, "assigned": len(rows)},
            },
        },

        "alpha_4_construction": {
            "suffix_is_a_live_alpha_2": sum(1 for r in rows if r["alpha_4_suffix_is_live_code"]),
            "suffix_classes": dict(Counter(
                r["alpha_4_suffix"] if not r["alpha_4_suffix_is_live_code"] else "<live code>"
                for r in rows)),
            "note": "Observation, not the published rule: ISO states only that the structure "
                    "'depends on the reason why the country name was removed'.",
        },

        # Does the registry's Deprecated date equal the date the upstream withdrew the code?
        # S55 measured this on the ISO 639-3 side and found the registry always late. Here the
        # answer splits by whether the registry existed yet.
        "date_agreement": {
            "rows_compared": 0, "exact": 0, "late": 0, "lag_days": {},
        },

        "rows": rows,
    }

    import datetime

    def d(s):
        return datetime.date(*map(int, s.split("-")))

    da = results["date_agreement"]
    for r in rows:
        if r["iana"] != "deprecated-as-itself" or not r["iana_deprecated"]:
            continue
        if len(r["withdrawal_date"]) < 10:
            continue
        da["rows_compared"] += 1
        lag = (d(r["iana_deprecated"]) - d(r["withdrawal_date"])).days
        da["lag_days"][r["alpha_4"]] = lag
        if lag == 0:
            da["exact"] += 1
        elif lag > 0:
            da["late"] += 1
    da["exact_are_all_pre_registry"] = all(
        r["withdrawal_date"] < ILSR
        for r in rows if da["lag_days"].get(r["alpha_4"]) == 0)
    da["late_are_all_post_registry"] = all(
        r["withdrawal_date"] > ILSR
        for r in rows if da["lag_days"].get(r["alpha_4"], 0) > 0)

    # Two identities the argument rests on. Computed, not asserted: if either goes false
    # on a later registry file, the work's central claim is wrong and this says so.
    not_aliased = {r["alpha_2"] for r in rows if not r["cldr_alias"]}
    live_again = {r["alpha_2"] for r in rows if r["alpha_2_live_now"]}
    absent = {r["alpha_2"] for r in rows if r["iana"] == "absent"}
    before = {r["alpha_2"] for r in rows if r["before_floor"]}
    results["derived_identities"] = {
        "cldr_gaps_are_exactly_the_recycled_codes": sorted(not_aliased) == sorted(live_again),
        "iana_gaps_are_exactly_the_pre_floor_dead_that_were_not_recycled":
            absent == (before - live_again),
        "cldr_holds_every_code_iana_never_admitted":
            sorted(absent) == sorted(results["cldr"]["aliased_but_absent_from_iana"]),
        "distinct_deprecated_records_for_the_13_post_floor_dead":
            len({r["alpha_2"] for r in rows if r["iana"] == "deprecated-as-itself"}),
    }

    # Occupancy, computed rather than asserted.
    for k, v in results["recycling"]["space"].items():
        v["occupancy"] = round(v["assigned"] / v["possible"], 6)

    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(results, f, indent=2, sort_keys=False)
        f.write("\n")

    # Console summary -- the numbers the work quotes.
    print("registry File-Date %s, %d records, %d region subtags"
          % (file_date, len(records), len(regions)))
    print("ISO 3166-3: %d entries, %s .. %s; %d withdrawn before the register existed"
          % (len(rows), rows[0]["withdrawal_date"], rows[-1]["withdrawal_date"],
             results["iso_3166_3"]["withdrawn_before_the_register_existed"]))
    print("floor %s: %d dead before, %d after; clearance %s years"
          % (FLOOR, len(pre), len(post), results["the_floor"]["clearance_years"]))
    print("IANA before floor: %s" % tally(pre))
    print("IANA after  floor: %s" % tally(post))
    print("Czechoslovakia anywhere in the registry: %s"
          % results["iana_registry"]["czechoslovakia_in_registry"])
    print("numeric region subtags that are countries: %s"
          % results["iana_registry"]["numeric_subtags_that_are_countries"])
    print("CLDR: %d of %d dead codes aliased, %d of them before the floor"
          % (results["cldr"]["dead_codes_aliased"], len(rows),
             results["cldr"]["dead_codes_aliased_before_floor"]))
    print("CLDR alias for CS: %s" % results["cldr"]["cs_alias"])
    print("reassigned alpha-2: %s" % [x[0] for x in results["recycling"]["alpha_2_reassigned"]])
    print("reassigned alpha-3: %s" % [x[0] for x in results["recycling"]["alpha_3_reassigned"]])
    print("dates: %d compared, %d exact, %d late; exact all pre-registry: %s; late all post: %s"
          % (results["date_agreement"]["rows_compared"], results["date_agreement"]["exact"],
             results["date_agreement"]["late"],
             results["date_agreement"]["exact_are_all_pre_registry"],
             results["date_agreement"]["late_are_all_post_registry"]))
    print("occupancy: %s" % {k: v["occupancy"] for k, v in results["recycling"]["space"].items()})
    return 0


if __name__ == "__main__":
    sys.exit(main())
