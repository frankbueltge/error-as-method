#!/usr/bin/env python3
"""Session 78 -- scoring, hand-checks, and the correction against Session 77.

Usage:  python3 adjudicate.py <tree> results.json ../2026-09-01-.../results.json out.json

Three things happen here and they are kept apart on purpose.

1. **Scoring.**  Each prediction of PREDICTIONS.md is scored against the
   mechanical number its bar names.  Nothing is rewritten (F-059).

2. **The hand-check every prediction owes, win or lose (F-099).**  This rule
   was filed on 2026-09-01 and has never been applied by a night that did not
   write it.  Tonight is its first application.  For each prediction the
   members the bar selected are read one by one and the population is compared
   with the population the claim is about.  Where they differ, the corrected
   figure is reported beside the mechanical one and neither replaces the other.

3. **The recomputation of Session 77's headline** under the unit tonight's
   instrument check forced -- the code rather than the row.  Session 77's own
   committed results file is the input; its per-row site counts are taken as
   given and only the aggregation changes.
"""

import json
import os
import re
import sys


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    tree, mine_path, s77_path, out = sys.argv[1:5]
    R = load(mine_path)
    S77 = load(s77_path)

    V = set(R["vocabulary"]["V"])
    E = set(R["ecpg_face"]["E"])
    entries = R["ecpg_face"]["entries"]

    # ---------------------------------------------------------------- P1
    # Mechanical: 6.  Hand-check: the rule takes the code adjacent to the word
    # SQLSTATE and therefore cannot take the second code of "(SQLSTATE 07001 or
    # 07002)".  07002 is offered to a reader in exactly the same way as 07001.
    p1_mech = sorted(E - V)
    p1_hand = sorted(set(p1_mech) | {"07002"})
    or_form = [e for e in entries if " or " in e["text"] and "SQLSTATE" in e["text"]]

    # ---------------------------------------------------------------- P6
    # Mechanical: 2, {00000, YE002}.  Hand-check: ecpg does impose 00000 -- as
    # five character constants in sqlca_init, not as a string literal.  YE002
    # survives the check: it occurs nowhere in the tree outside doc/.
    p6_mech = sorted(R["ecpg_implementation"]
                     ["codes_with_no_literal_under_src_interfaces_ecpg"])
    p6_hand = [c for c in p6_mech if c != "00000"]

    # -------------------------------------------------------- the severity face
    # errcodes.txt gives every code a severity, E/W/S.  The ecpg list gives every
    # SQLCODE a sign and a name.  Where the two disagree about the same code, the
    # reader is holding two classifications from one publisher.
    warn_terms = [e for e in entries if e["term"] and "WARNING" in e["term"]]
    severity = R["vocabulary"]["severity_by_code"]
    severity_conflict = []
    for e in warn_terms:
        for c in e["codes"]:
            if c in V and severity[c] == ["E"]:
                severity_conflict.append({
                    "sqlstate": c,
                    "vocabulary_severity": "E (error)",
                    "ecpg_term": e["term"],
                    "ecpg_line": e["line"],
                    "ecpg_text": e["text"][:200],
                })

    # ------------------------------------------------- the YE002 / YE000 pair
    ye002_entries = [
        {"term": e["term"], "line": e["line"], "text": e["text"][:160]}
        for e in entries if "YE002" in e["codes"]
    ]
    conditions = sorted({
        re.search(r"\((ECPG_[A-Z_]+)\)", e["term"]).group(1)
        for e in ye002_entries if re.search(r"\((ECPG_[A-Z_]+)\)", e["term"])
    })
    # every site in the tree at which one of those conditions is raised, and
    # which SQLSTATE constant travels with it
    sites = []
    raise_re = re.compile(
        r"ecpg_raise\s*\(\s*[^,]+,\s*(" + "|".join(conditions) + r")\s*,\s*"
        r"([A-Za-z0-9_]+)", re.S)
    for dirpath, _dirs, files in os.walk(os.path.join(tree, "src/interfaces/ecpg")):
        for name in files:
            if not name.endswith((".c", ".h")):
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
            for m in raise_re.finditer(text):
                sites.append({
                    "file": os.path.relpath(path, tree),
                    "line": text.count("\n", 0, m.start()) + 1,
                    "condition": m.group(1),
                    "sqlstate_constant": m.group(2),
                })

    # -------------------------------------------- Session 77's headline, recomputed
    rows = S77["rows"]
    by = {}
    for r in rows:
        by.setdefault(r["sqlstate"], []).append(r)
    rows_zero = [r for r in rows if r["sites_b"] == 0]
    codes_zero = sorted(c for c, rs in by.items() if all(r["sites_b"] == 0 for r in rs))
    rescued_by_another_row = sorted(
        {r["sqlstate"] for r in rows_zero} - set(codes_zero))
    # rule C of Session 77 rescued two codes through a live string route; only
    # those of them still in the code-level set count here
    rule_c = [x["sqlstate"] for x in S77["rows"] and
              load(os.path.join(os.path.dirname(s77_path), "string-routes.json"))
              ["P1_correction"]["rescued"]]
    rule_c_still = [c for c in rule_c if c in codes_zero]
    corrected = [c for c in codes_zero if c not in rule_c_still]
    xx000 = [c for c in corrected if c.endswith("000")]

    result = {
        "instrument_check": {
            "P5": "LOST",
            "expected": {"n_codes": 268, "n_with_condition_name": 262, "n_classes": 43},
            "measured": {
                "n_rows": R["vocabulary"]["n_rows"],
                "n_codes": R["vocabulary"]["n_V"],
                "n_codes_with_condition_name": R["vocabulary"]["n_A"],
                "n_rows_with_condition_name": R["vocabulary"]["n_A_rows"],
                "n_classes": R["vocabulary"]["n_classes"],
            },
            "reading": ("268 is the number of ROWS in errcodes.txt, not the number of "
                        "codes. Six SQLSTATEs carry two rows each, with two macro names. "
                        "43 classes agree. Every one of the 262 codes carries a condition "
                        "name, so no code is missing from Appendix A -- Session 77's "
                        "'six codes with no condition name' are six second rows."),
            "duplicates": R["vocabulary"]["duplicate_codes"],
        },
        "predictions": {
            "P1": {"bar": 3, "mechanical": len(p1_mech), "members": p1_mech,
                   "hand_checked": len(p1_hand), "members_after_hand_check": p1_hand,
                   "verdict": "WON",
                   "hand_check": ("every member read in its entry; all are offered to a "
                                  "reader as a SQLSTATE the library may return. The rule "
                                  "UNDER-counts: it cannot take the second code of "
                                  "'(SQLSTATE 07001 or 07002)'."),
                   "entries_of_the_or_form": [e["term"] for e in or_form]},
            "P2": {"bar": 5, "measured": R["session_77_seven"]["n_in_doc"],
                   "verdict": "WON",
                   "unpublished_remainder": [
                       c for c in R["session_77_seven"]["codes"]
                       if not R["session_77_seven"]["in_doc_sources"][c]]},
            "P3": {"bar": 1,
                   "measured": R["manual_face"]["outside_ecpg"]["n_minus_V"],
                   "verdict": "LOST"},
            "P4": {"bar": 1, "measured": len(severity_conflict), "verdict":
                   "WON" if severity_conflict else "LOST",
                   "conflicts": severity_conflict},
            "P6": {"bar": 1, "mechanical": len(p6_mech), "members": p6_mech,
                   "hand_checked": len(p6_hand), "members_after_hand_check": p6_hand,
                   "verdict": "WON",
                   "hand_check": ("00000 is a FALSE member: ecpg imposes it in "
                                  "src/interfaces/ecpg/ecpglib/misc.c, in sqlca_init, as "
                                  "five character constants rather than as a string "
                                  "literal. The bar selected 'codes with no five-character "
                                  "literal'; the claim was about 'codes ecpg cannot set'.")},
        },
        "ye002": {
            "documented_conditions": conditions,
            "entries": ye002_entries,
            "raise_sites": sites,
            "n_sites": len(sites),
            "sqlstate_constants_actually_passed":
                sorted({s["sqlstate_constant"] for s in sites}),
        },
        "session_77_headline_recomputed": {
            "unit_used_by_session_77": "row",
            "unit_forced_by_tonight": "code",
            "rows_with_no_site": len(rows_zero),
            "codes_with_no_site_on_any_row": len(codes_zero),
            "counted_siteless_as_a_row_but_imposed_through_the_other_row":
                rescued_by_another_row,
            "session_77_rule_C_rescues": rule_c,
            "rule_C_rescues_still_applying_at_code_level": rule_c_still,
            "corrected_headline": len(corrected),
            "session_77_published_headline": 73,
            "corrected_headline_without_class_generic_xx000": len(corrected) - len(xx000),
            "session_77_published_without_xx000": 59,
            "n_xx000_in_corrected_set": len(xx000),
            "codes": corrected,
        },
    }

    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1)

    print("P5 instrument check: LOST -- 268 rows over 262 codes,",
          R["vocabulary"]["n_duplicate_codes"], "codes with two rows")
    for k, v in result["predictions"].items():
        print(f"  {k}: {v['verdict']}  bar={v['bar']} "
              f"measured={v.get('measured', v.get('mechanical'))}"
              + (f" hand-checked={v['hand_checked']}" if "hand_checked" in v else ""))
    print("YE002:", len(ye002_entries), "documented conditions,", len(sites),
          "raise sites, constants passed:",
          result["ye002"]["sqlstate_constants_actually_passed"])
    h = result["session_77_headline_recomputed"]
    print(f"S77 headline 73 -> {h['corrected_headline']}; "
          f"59 -> {h['corrected_headline_without_class_generic_xx000']}; "
          f"rescued by a second row: {h['counted_siteless_as_a_row_but_imposed_through_the_other_row']}")


if __name__ == "__main__":
    main()
