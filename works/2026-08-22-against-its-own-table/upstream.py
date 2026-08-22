#!/usr/bin/env python3
"""
upstream.py — Session 66, 2026-08-22

The audit measured this interpreter against RFC 3454 and found 684 deviating code
points. Halfway through the night a web search for the mechanism returned a CPython
issue: gh-155292, "stringprep and IDNA 2003 incorrectly handles some characters",
opened 2026-08-06, and merged as PR #155293, "Don't consider Unicode codepoint
attributes outside RFC 3454". The defect this night measured was reported sixteen days
before the measurement and fixed before it began.

That is not a reason to hide the measurement. It is a reason to check it against theirs,
which is a better test than either instrument alone: two parties who did not talk to each
other, with different methods, over the same specification.

This compares the exception table in the fixed `Lib/stringprep.py` on CPython's default
branch (committed here as sources/cpython-Lib-stringprep-main.py, fetched 2026-08-22 and
hashed in the manifest) against the deviating set audit.py computed here.

Three questions, in order:

  1. Is every code point this audit found also in the upstream fix? A code point in mine
     and not theirs would mean the shipped fix is incomplete. A code point in theirs and
     not mine means my instrument is narrower than theirs, which is expected: they fixed
     `map_table_b3`, this audit measures the mapping stage, and the two normalisation
     passes in `map_table_b2` wash some differences out.
  2. Where both name a code point, do they prescribe the same output? Their exception
     value against RFC 3454's enumerated Table B.3 entry.
  3. What does the fix leave standing? Run their fixed function over the whole space and
     compare it to Table B.3 again.

Output: upstream.json. Offline: both inputs are committed.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from audit import parse_rfc3454, MAXCP

RFC = os.path.join(HERE, "sources", "rfc3454.txt")
FIXED = os.path.join(HERE, "sources", "cpython-Lib-stringprep-main.py")
DEVIATIONS = os.path.join(HERE, "deviations.json")


def upstream_exceptions(path):
    """Read the b3_exceptions dict out of the fixed file without importing it.

    The file is a module named after a standard-library module; importing it would
    shadow the one the audit runs against. It is read as text and the single literal is
    evaluated on its own.
    """
    src = open(path, encoding="utf-8").read()
    m = re.search(r"^b3_exceptions = \{.*?^\}", src, re.S | re.M)
    if not m:
        raise ValueError("no b3_exceptions literal in %s" % path)
    return eval(m.group(0).split("=", 1)[1])  # a dict literal, nothing else


def main():
    import stringprep  # the interpreter in this room, unfixed

    spec = parse_rfc3454(RFC)
    b3 = spec["B.3"]["map"]
    b2 = spec["B.2"]["map"]
    fixed = upstream_exceptions(FIXED)
    here = stringprep.b3_exceptions

    added = set(fixed) - set(here)
    removed = set(here) - set(fixed)
    changed = {k for k in set(here) & set(fixed) if here[k] != fixed[k]}

    mine = {int(r["cp"][2:], 16)
            for r in json.load(open(DEVIATIONS, encoding="utf-8"))["rows"]}

    # 2. Do we prescribe the same thing where we overlap?
    disagreements = [{"cp": "U+%04X" % k, "upstream": fixed[k],
                      "rfc3454_table_b3": b3.get(k, chr(k))}
                     for k in sorted(mine & set(fixed))
                     if fixed[k] != b3.get(k, chr(k))]

    # 3. What does the fix leave standing against Table B.3?
    def fixed_b3(ch):
        r = fixed.get(ord(ch))
        return r if r is not None else ch.lower()

    residue = [cp for cp in range(MAXCP + 1)
               if fixed_b3(chr(cp)) != b3.get(cp, chr(cp))]
    residue_is_b2 = sum(1 for cp in residue if fixed_b3(chr(cp)) == b2.get(cp))

    out = {
        "generated_by": "upstream.py",
        "date": "2026-08-22",
        "session": 66,
        "upstream": {
            "issue": "python/cpython#155292, opened 2026-08-06",
            "pull_request": "python/cpython#155293",
            "news_entry": ("Change the stringprep module and encodings.idna codec to "
                           "not consider Unicode codepoint attributes beyond those "
                           "defined in RFC 3454."),
            "file": "sources/cpython-Lib-stringprep-main.py",
        },
        "exception_table": {
            "in_this_interpreter": len(here),
            "in_the_fix": len(fixed),
            "added_by_the_fix": len(added),
            "removed_by_the_fix": len(removed),
            "changed_by_the_fix": len(changed),
        },
        "against_this_audit": {
            "deviating_code_points_found_here": len(mine),
            "found_here_and_missing_from_the_fix": sorted("U+%04X" % c
                                                          for c in mine - added),
            "in_the_fix_and_not_found_here": len(added - mine),
            "why_the_fix_is_wider": ("the fix repairs map_table_b3; this audit measures "
                                     "the mapping stage, where map_table_b2's two NFKC "
                                     "passes absorb some of the difference"),
            "prescription_disagreements": disagreements,
        },
        "what_the_fix_leaves_standing": {
            "code_points_where_fixed_map_table_b3_differs_from_table_B_3": len(residue),
            "of_which_are_table_B_2_additional_foldings": residue_is_b2,
            "reading": ("Not a defect and not claimed as one. map_table_b3 is the inner "
                        "half of map_table_b2 and carries B.2's additional foldings by "
                        "design. It is at odds with the function's own documentation "
                        "('according to table B.3'), and it has no consequence for "
                        "nameprep, which calls map_table_b2."),
        },
    }
    with open(os.path.join(HERE, "upstream.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
