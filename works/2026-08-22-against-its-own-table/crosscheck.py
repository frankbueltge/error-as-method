#!/usr/bin/env python3
"""
crosscheck.py — Session 66, 2026-08-22

Session 65's open thread 4, run literally:

    "A night that runs a genuinely independent UTS #46 implementation against the same
    table would test whether the 85 are CPython's or the profile's."

There is one in this room: a third-party `idna` package with its own generated UTS #46
tables, built from the Unicode data at a different version (16.0.0) than the table
Session 65 committed (17.0.0). It is the only thing in this night that is not standard
library, and it is used only here, only for this check, and nothing in the audit depends
on it.

The test runs, and it answers a question — just not the one it was set for. The 85 sit on
side A, CPython's nameprep. Replacing side B cannot reach them. That is P1, and it is
worth running rather than arguing, because a falsifier that cannot fail is worse than one
that fails.

Output: crosscheck.json.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from audit import parse_uts46, uts46_nontransitional, REFUSED, SURROGATES, MAXCP, UTS46

try:
    import idna
    import idna.idnadata
except ImportError:  # the night still stands without it; the audit needs nothing
    idna = None


def independent(cp):
    """The third-party implementation's mapping stage, same two parameters the WHATWG
    URL Standard fixes: UseSTD3ASCIIRules false, Transitional_Processing false."""
    try:
        return idna.uts46_remap(chr(cp), std3_rules=False, transitional=False)
    except Exception:
        return REFUSED


def main():
    if idna is None:
        print("no independent implementation available; nothing recorded")
        return

    table = parse_uts46(UTS46)
    agree = differ = 0
    only_committed = only_independent = 0
    rows = []
    for cp in range(MAXCP + 1):
        if cp in SURROGATES:
            continue
        a = uts46_nontransitional(cp, table)   # the committed table, 17.0.0
        b = independent(cp)                    # the package's own tables, 16.0.0
        if a is REFUSED and b is REFUSED:
            agree += 1
            continue
        if a is REFUSED:
            only_independent += 1
            differ += 1
        elif b is REFUSED:
            only_committed += 1
            differ += 1
        elif a == b:
            agree += 1
            continue
        else:
            differ += 1
        if len(rows) < 400:
            rows.append({
                "cp": "U+%04X" % cp,
                "committed_table_17_0_0": "REFUSED" if a is REFUSED else a,
                "independent_impl_16_0_0": "REFUSED" if b is REFUSED else b,
            })

    # Do the 86 escaped mappings survive the swap? They are on side A; they must.
    cherokee = list(range(0x13A0, 0x13F6))
    import encodings.idna
    unchanged = sum(1 for cp in cherokee
                    if encodings.idna.nameprep(chr(cp)) == chr(cp).lower()
                    and chr(cp).lower() != chr(cp))

    out = {
        "generated_by": "crosscheck.py",
        "date": "2026-08-22",
        "session": 66,
        "what": ("Session 65's open thread 4 run as written: an independent UTS #46 "
                 "implementation in place of the committed mapping table."),
        "independent_implementation": {
            "package": "idna",
            "version": idna.__version__,
            "its_unicode_version": idna.idnadata.__dict__.get("__version__"),
            "third_party": True,
            "used_only_here": True,
        },
        "committed_table_version": "17.0.0",
        "population": 1112064,
        "agree": agree,
        "differ": differ,
        "differ_because_only_committed_table_accepts": only_committed,
        "differ_because_only_independent_accepts": only_independent,
        "sample": rows[:40],
        "side_a_untouched": {
            "cherokee_code_points_checked": len(cherokee),
            "still_mapped_out_of_the_unicode_3_2_repertoire_by_cpython": unchanged,
            "note": ("Side A is not a parameter of this test. Whatever side B is, "
                     "CPython's nameprep does the same thing."),
        },
    }
    with open(os.path.join(HERE, "crosscheck.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps({k: v for k, v in out.items() if k != "sample"},
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
