#!/usr/bin/env python3
"""measure.py -- what a registry that never removes a name has nevertheless lost.

Offline, stdlib only, deterministic. Reads cache/, writes results.json.

WHAT IS COUNTED, AND THE CHOICES THAT DECIDE THE NUMBERS
--------------------------------------------------------
1. A *record* is one %%-separated entry in the IANA Language Subtag Registry. The whole
   file is counted, every Type: language, extlang, script, region, variant, redundant,
   grandfathered.

2. *Deprecated* means the record carries a Deprecated field. The registry has no other
   state; there is no removal, which is the thing being tested.

3. *Born deprecated* means Deprecated < Added -- a record entered into the registry with
   a death date earlier than its birth date. RFC 5646 section 3.1.6 notices these itself.

4. *Orphan* means Deprecated present and Preferred-Value absent: a name withdrawn with no
   forwarding address. RFC 5646: "a record that contains a 'Deprecated' field and no
   corresponding 'Preferred-Value' field has no replacement mapping."

5. The ISO 639-3 join is by exact three-letter code against records of Type: language
   only. Extlang records duplicate some language subtags and are excluded from the join
   so that no retirement is counted twice; the extlang set is reported separately.

6. THE FLOOR TEST is the night's measurement. RFC 5645 imported ISO 639-3 into the
   registry with Added: 2009-07-29. That date is the cut. For every ISO 639-3 retirement,
   ask only: is the retired code in the registry today, yes or no -- and did the
   retirement fall before or after the cut. The claim under test is that the cut, and
   nothing about the individual names, decides it. Exceptions are printed, not smoothed.

7. Withdrawals *by the registry itself* cannot be measured from one snapshot. They are
   established textually instead, from RFC 4646 and RFC 5646 rule 14, whose sentences are
   cut into sources/ verbatim by evidence.py. This is a weaker instrument than S54's
   36-version diff and the work says so.
"""

import collections
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")

# The date RFC 5645's bulk import of ISO 639-3 carries in the registry's Added field.
IMPORT_DATE = "2009-07-29"
# The date the initial registry (the ILSR) carries.
ILSR_DATE = "2005-10-16"
# ISO 639-3 retirement reason codes, as published by the registration authority.
REASONS = {"C": "code changed", "D": "duplicate", "N": "non-existent",
           "S": "split", "M": "merge"}


def parse_registry(path):
    """The registry is record-jar: %%-separated records, folded continuation lines."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    head, *chunks = text.split("%%")
    file_date = ""
    for line in head.splitlines():
        if line.startswith("File-Date:"):
            file_date = line.split(":", 1)[1].strip()
    records = []
    for chunk in chunks:
        if not chunk.strip():
            continue
        rec = collections.defaultdict(list)
        key = None
        for line in chunk.strip("\n").split("\n"):
            if line.startswith("  ") and key:
                rec[key][-1] += " " + line.strip()
            elif ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                rec[key].append(val.strip())
        if rec:
            records.append(dict(rec))
    return file_date, records


def ident(rec):
    return (rec.get("Subtag") or rec.get("Tag") or ["?"])[0]


def main():
    file_date, R = parse_registry(os.path.join(CACHE, "language-subtag-registry.txt"))
    with open(os.path.join(CACHE, "iso-639-3_Retirements.tab"), encoding="utf-8") as fh:
        RET = list(csv.DictReader(fh, delimiter="\t"))

    out = {
        "measured_by": "works/2026-08-14-the-threshold/measure.py",
        "session": 55,
        "registry_file_date": file_date,
    }

    # ---- the registry as it stands -------------------------------------------------
    dep = [r for r in R if "Deprecated" in r]
    born = [r for r in dep if r["Deprecated"][0] < r["Added"][0]]
    orph = [r for r in dep if "Preferred-Value" not in r]
    out["registry"] = {
        "records": len(R),
        "by_type": dict(sorted(collections.Counter(r["Type"][0] for r in R).items())),
        "deprecated": len(dep),
        "deprecated_by_year": dict(sorted(
            collections.Counter(r["Deprecated"][0][:4] for r in dep).items())),
        "earliest_deprecation": min(r["Deprecated"][0] for r in dep),
        "earliest_added": min(r["Added"][0] for r in R),
        "latest_added": max(r["Added"][0] for r in R),
        "added_top_dates": collections.Counter(r["Added"][0] for r in R).most_common(6),
        "records_added_before_the_registry_existed": sum(
            1 for r in R if r["Added"][0] < ILSR_DATE),
        "removed_ever": 0,
        "removed_ever_basis": (
            "textual, not measured: RFC 4646 (2006) and RFC 5646 (2009) section 3.4 "
            "rule 14 -- withdrawn codes 'remain valid in language tags'. One snapshot "
            "cannot prove a negative about removals; see work.md, attack B."),
    }

    out["born_deprecated"] = {
        "count": len(born),
        "max_gap_years": max(int(r["Added"][0][:4]) - int(r["Deprecated"][0][:4]) for r in born),
        "records": [
            {"type": r["Type"][0], "id": ident(r), "description": r["Description"][0],
             "deprecated": r["Deprecated"][0], "added": r["Added"][0],
             "preferred_value": (r.get("Preferred-Value") or [None])[0]}
            for r in sorted(born, key=lambda r: r["Deprecated"][0])],
    }

    out["orphans"] = {
        "count": len(orph),
        "share_of_deprecated": round(len(orph) / len(dep), 4),
        "by_type": dict(sorted(collections.Counter(r["Type"][0] for r in orph).items())),
        "note": "Deprecated, with no Preferred-Value: a withdrawn name with nowhere to send a reference.",
        "non_language_examples": [
            {"type": r["Type"][0], "id": ident(r), "description": r["Description"][0],
             "deprecated": r["Deprecated"][0]}
            for r in orph if r["Type"][0] != "language"],
    }

    # ---- the upstream registration authority ---------------------------------------
    out["iso639_3_retirements"] = {
        "count": len(RET),
        "by_reason": {REASONS.get(k, k): v for k, v in sorted(
            collections.Counter(r["Ret_Reason"] for r in RET).items())},
        "by_year": dict(sorted(collections.Counter(r["Effective"][:4] for r in RET).items())),
        "earliest": min(r["Effective"] for r in RET),
        "latest": max(r["Effective"] for r in RET),
    }

    # ---- THE FLOOR TEST ------------------------------------------------------------
    lang = {r["Subtag"][0]: r for r in R
            if r["Type"][0] == "language" and "Subtag" in r}
    extlang = {r["Subtag"][0] for r in R if r["Type"][0] == "extlang" and "Subtag" in r}

    before = [r for r in RET if r["Effective"] < IMPORT_DATE]
    after = [r for r in RET if r["Effective"] >= IMPORT_DATE]

    def split(rows):
        return ([r for r in rows if r["Id"] in lang],
                [r for r in rows if r["Id"] not in lang])

    bp, ba = split(before)
    ap, aa = split(after)
    out["floor_test"] = {
        "cut_date": IMPORT_DATE,
        "cut_is": "the Added date RFC 5645's bulk import of ISO 639-3 carries in the registry",
        "retired_before_cut": {"total": len(before), "in_registry": len(bp), "absent": len(ba)},
        "retired_on_or_after_cut": {"total": len(after), "in_registry": len(ap), "absent": len(aa)},
        "in_registry_are_all_deprecated": all("Deprecated" in lang[r["Id"]] for r in bp + ap),
        "exceptions_before_cut_but_present": [
            {"id": r["Id"], "name": r["Ref_Name"], "effective": r["Effective"]} for r in bp],
        "exceptions_after_cut_but_absent": [
            {"id": r["Id"], "name": r["Ref_Name"], "effective": r["Effective"],
             "reason": REASONS.get(r["Ret_Reason"], r["Ret_Reason"]),
             "also_absent_as_extlang": r["Id"] not in extlang} for r in aa],
        "cut_robustness": {
            "latest_retirement_before_cut": max(r["Effective"] for r in before),
            "earliest_retirement_on_or_after_cut": min(r["Effective"] for r in after),
            "note": ("The nearest retirements on either side are almost a year apart, so any "
                     "cut date inside that gap gives the same table. The result does not "
                     "depend on picking 2009-07-29 exactly."),
        },
        "forgotten_by_reason": {REASONS.get(k, k): v for k, v in sorted(
            collections.Counter(r["Ret_Reason"] for r in ba).items())},
        "forgotten_by_year": dict(sorted(collections.Counter(r["Effective"][:4] for r in ba).items())),
    }

    # ---- names for things that were found not to exist ------------------------------
    nonexistent = [r for r in RET if r["Ret_Reason"] == "N"]
    ne_in = [r for r in nonexistent if r["Id"] in lang]
    out["non_existent_languages"] = {
        "retired_as_non_existent": len(nonexistent),
        "still_valid_subtags_today": len(ne_in),
        "never_in_the_registry": len(nonexistent) - len(ne_in),
        "note": ("A code retired because the language it named was found not to exist. "
                 "Those that were in the registry keep a permanent, valid address and no "
                 "Preferred-Value, because there is nothing to point at."),
        "examples": [
            {"id": r["Id"], "name": r["Ref_Name"], "retired": r["Effective"],
             "subtag_deprecated": lang[r["Id"]]["Deprecated"][0],
             "preferred_value": (lang[r["Id"]].get("Preferred-Value") or [None])[0]}
            for r in sorted(ne_in, key=lambda r: r["Effective"])[:10]],
    }

    # ---- the one exception, traced --------------------------------------------------
    ggr = lang.get("ggr")
    trace = {"note": "The split that the permanent registry recorded with one product missing."}
    for r in RET:
        if r["Id"] == "ggr":
            trace["upstream_split"] = {"id": "ggr", "name": r["Ref_Name"],
                                       "effective": r["Effective"], "remedy": r["Ret_Remedy"]}
        if r["Id"] == "ggm":
            trace["upstream_retirement_of_missing_product"] = {
                "id": "ggm", "name": r["Ref_Name"], "effective": r["Effective"],
                "reason": REASONS.get(r["Ret_Reason"], r["Ret_Reason"])}
    if ggr:
        trace["registry_record_of_the_split"] = {
            "subtag": "ggr", "added": ggr["Added"][0],
            "deprecated": ggr["Deprecated"][0],
            "comments": (ggr.get("Comments") or [""])[0]}
    trace["products_in_registry"] = {
        code: ({"added": lang[code]["Added"][0],
                "description": lang[code]["Description"][0]} if code in lang else "ABSENT")
        for code in ("gtu", "ggm", "ikr")}
    trace["ggm_anywhere_in_registry"] = any(ident(r) == "ggm" for r in R)
    out["the_missing_product"] = trace

    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")

    f = out["floor_test"]
    print("registry file-date        :", file_date)
    print("records / deprecated      : %d / %d" % (len(R), len(dep)))
    print("born deprecated           : %d (max gap %d years)"
          % (len(born), out["born_deprecated"]["max_gap_years"]))
    print("deprecated with no successor: %d (%.0f%% of deprecations)"
          % (len(orph), 100 * len(orph) / len(dep)))
    print("ISO 639-3 retirements     :", len(RET))
    print("  retired before %s : %d -- in registry %d, absent %d"
          % (IMPORT_DATE, f["retired_before_cut"]["total"],
             f["retired_before_cut"]["in_registry"], f["retired_before_cut"]["absent"]))
    print("  retired after  %s : %d -- in registry %d, absent %d"
          % (IMPORT_DATE, f["retired_on_or_after_cut"]["total"],
             f["retired_on_or_after_cut"]["in_registry"], f["retired_on_or_after_cut"]["absent"]))
    print("  exceptions                :", f["exceptions_before_cut_but_present"],
          f["exceptions_after_cut_but_absent"])
    print("non-existent languages still holding a valid subtag: %d of %d"
          % (out["non_existent_languages"]["still_valid_subtags_today"],
             out["non_existent_languages"]["retired_as_non_existent"]))
    print("\nwrote results.json")


if __name__ == "__main__":
    main()
