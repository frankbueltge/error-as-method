#!/usr/bin/env python3
"""Session 78 -- the hand-checks, kept as evidence rather than as prose.

F-087 asks that a rule's limit be tested rather than assumed, and F-100 that the
hits of a pattern be looked at before they are counted.  Both apply to the
adjacency rule this night used to find a published SQLSTATE: the word SQLSTATE,
then only whitespace and markup, then a five-character code.

Two questions are settled here, and the verdicts are mine, recorded per hit so a
reader can disagree with each one:

  1. What does the rule MISS inside ecpg.sgml?
  2. Outside ecpg.sgml the rule returns nothing.  Does the manual name SQLSTATE
     values there anyway, in a form the rule cannot see?

    python3 handcheck.py <tree> results.json hand-checks.json
"""

import json
import os
import re
import sys

# Every distinct five-character token from the vocabulary found as a bare
# literal in doc/ outside ecpg.sgml, read one by one.  The verdict says whether
# the occurrence is a SQLSTATE at all.
VERDICTS = {
    "00000": ("SQLSTATE", "plpgsql.sgml: the rule for user-chosen codes, "
                          "'other than 00000'"),
    "01000": ("not a SQLSTATE", "func.sgml: the value of a bit-string shift, "
                                "B'10001' << 3"),
    "20000": ("not a SQLSTATE", "array.sgml: a salary in the tutorial table"),
    "22003": ("SQLSTATE", "plpgsql.sgml: RAISE ... USING ERRCODE = '22003'"),
    "22012": ("SQLSTATE", "plpgsql.sgml: WHEN SQLSTATE '22012' THEN"),
    "22013": ("SQLSTATE", "btree.sgml: the code an operator class must raise"),
    "23505": ("SQLSTATE", "mvcc.sgml: 'which have SQLSTATE code 23505'"),
    "23P01": ("SQLSTATE", "mvcc.sgml: 'which have SQLSTATE code 23P01'"),
    "25000": ("not a SQLSTATE", "array.sgml: a salary in the tutorial table"),
    "27000": ("not a SQLSTATE", "array.sgml: a salary in the tutorial table"),
    "40000": ("not a SQLSTATE", "libpq.sgml: a server version number, 4.0"),
    "40001": ("SQLSTATE", "mvcc.sgml: 'an SQLSTATE value of 40001'"),
    "40P01": ("SQLSTATE", "mvcc.sgml: 'These have the SQLSTATE code 40P01'"),
    "P0001": ("not a SQLSTATE", "datatype.sgml: the timestamp "
                                "P0001-02-03T04:05:06"),
}


def main():
    tree, results, out = sys.argv[1:4]
    R = json.load(open(results, encoding="utf-8"))
    V = set(R["vocabulary"]["V"])

    bare = re.compile(r"(?<![0-9A-Za-z_])(" + "|".join(sorted(V)) + r")(?![0-9A-Za-z_])")
    hits = {}
    for dirpath, _d, files in os.walk(os.path.join(tree, "doc/src/sgml")):
        for name in files:
            if name == "ecpg.sgml":
                continue
            path = os.path.join(dirpath, name)
            try:
                text = open(path, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            for m in bare.finditer(text):
                hits.setdefault(m.group(1), []).append({
                    "file": os.path.relpath(path, tree),
                    "line": text.count("\n", 0, m.start()) + 1,
                    "context": " ".join(
                        text[max(0, m.start() - 80):m.end() + 50].split()),
                })

    outside = []
    for code in sorted(hits):
        verdict, note = VERDICTS.get(code, ("UNREAD", ""))
        outside.append({
            "code": code,
            "in_vocabulary": code in V,
            "verdict": verdict,
            "note": note,
            "n_occurrences": len(hits[code]),
            "occurrences": hits[code][:4],
        })

    real = [o for o in outside if o["verdict"] == "SQLSTATE"]
    result = {
        "question_1_what_the_rule_misses_inside_ecpg_sgml": {
            "found_by_hand": ["07002"],
            "why_the_rule_cannot_see_it": (
                "two entries read '(SQLSTATE 07001 or 07002)'. The rule takes the "
                "code adjacent to the word SQLSTATE and there is no second word "
                "SQLSTATE before 07002. The rule under-counts by one code."),
            "entries": ["-201 (ECPG_TOO_MANY_ARGUMENTS)", "-202 (ECPG_TOO_FEW_ARGUMENTS)"],
        },
        "question_2_outside_ecpg_sgml": {
            "mechanical_result_of_the_adjacency_rule": 0,
            "bare_vocabulary_literals_found_by_hand": len(outside),
            "of_those_actually_naming_a_SQLSTATE": len(real),
            "codes_naming_a_SQLSTATE": [o["code"] for o in real],
            "all_of_them_in_the_vocabulary": all(o["in_vocabulary"] for o in real),
            "reading": (
                "The manual does name SQLSTATE values in three other files "
                "-- mvcc.sgml, plpgsql.sgml, btree.sgml -- and every one "
                "of them is a code Appendix A carries. Only the ecpg listing steps "
                "outside the vocabulary. P3 loses on its own bar and the hand-check "
                "makes the loss sharper rather than softer: the second face is "
                "singular, not one of many."),
            "false_positives_reported_rather_than_dropped": [
                {"code": o["code"], "what_it_really_is": o["note"]}
                for o in outside if o["verdict"] == "not a SQLSTATE"],
            "all": outside,
        },
    }
    json.dump(result, open(out, "w", encoding="utf-8"), indent=1)
    print(f"outside ecpg.sgml: {len(outside)} vocabulary literals by hand, "
          f"{len(real)} of them genuine SQLSTATE mentions, "
          f"all in the vocabulary: {result['question_2_outside_ecpg_sgml']['all_of_them_in_the_vocabulary']}")


if __name__ == "__main__":
    main()
