#!/usr/bin/env python3
"""verify.py -- the checks this night's claims rest on, run before the work was written.

A port's only warrant is that it reproduces what it ports.  A declared rule's only warrant is that
the declaration precedes the rule.  Both are checkable from the repository and both are checked
here, along with the ground truth's own arithmetic.

Exit 0 if every check passes.  Writes verification.json.
"""

import gzip
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
S88 = HERE.parent / "2026-09-12-adjacent-text"
S90 = HERE.parent / "2026-09-15-not-part-of-the-act"

checks = []


def check(name, ok, detail):
    checks.append({"check": name, "pass": bool(ok), "detail": detail})
    print("  %-4s %-52s %s" % ("PASS" if ok else "FAIL", name, detail))
    return ok


def main():
    print("verify.py -- Session 91\n")

    # 1. the reach percentages this night recomputes are Session 90's published ones
    b = json.load(open(HERE / "bounds.json"))
    published = {"base": 0.76, "narrow": 34.24, "wide": 50.91}
    got = {k: v["pct_within_36_words"] for k, v in b["lists"].items()}
    check("S90 reach reproduced from the committed corpus", got == published,
          "%s == %s" % (got, published))

    # 2. the 26 base terms are read out of Session 88, not retyped
    pat = json.load(open(S88 / "results.json"))["mechanical_ceiling"]["party_terms"]
    terms = pat[len(r"\b("):-len(r")\b")].split("|")
    check("Session 88's party terms read from its results.json", len(terms) == 26,
          "%d terms, first three %s" % (len(terms), terms[:3]))

    # 3. the ground truth's own arithmetic
    h = json.load(open(S90 / "handreading.json"))
    yes = sum(1 for r in h["rows"]
              if r["is_the_nearest_party_term_the_bearer"].strip().upper() == "YES")
    no = len(h["rows"]) - yes
    check("handreading.json 17 YES / 23 NO / precision 0.425",
          (yes, no, len(h["rows"])) == (17, 23, 40) and h["precision"] == 0.425,
          "%d YES, %d NO, %d rows, precision %s" % (yes, no, len(h["rows"]), h["precision"]))

    # 4. every hand-read row was matched against the population -- no verdict silently dropped
    r = json.load(open(HERE / "results.json"))
    a = r["against_the_reader"]
    check("all 40 verdicts matched to a population row",
          a["n_scored"] == 40 and a["unmatched_against_the_population"] == 0,
          "%d scored, %d unmatched" % (a["n_scored"], a["unmatched_against_the_population"]))
    check("the reader's base rate recomputed from the rows", a["reader_base_rate"] == 0.425,
          "%s" % a["reader_base_rate"])

    # 5. the population is Session 89's, unchanged
    occ = json.load(gzip.open(S90 / "occurrences.json.gz"))
    pop = sum(1 for x in occ if x["form"] == "B-FORM" and x["agent"] == "AGENTLESS"
              and x["register"] == "ACT")
    check("population is 660 B-FORM AGENTLESS rows of the Act", pop == 660, "%d rows" % pop)

    # 6. the declaration precedes the instrument, in the repository's own record
    def commit_of(path):
        out = subprocess.run(["git", "log", "--format=%H", "--", path],
                             cwd=HERE, capture_output=True, text=True)
        lines = [x for x in out.stdout.split() if x]
        return lines[-1] if lines else None

    pred = commit_of("PREDICTIONS.md")
    inst = commit_of("validate.py")
    if pred and inst:
        order = subprocess.run(["git", "merge-base", "--is-ancestor", pred, inst], cwd=HERE)
        ok = order.returncode == 0 and pred != inst
        detail = "%s (predictions) is an ancestor of %s (validate.py)" % (pred[:12], inst[:12])
    else:
        ok, detail = False, "validate.py not yet committed -- run again after the commit"
    check("PREDICTIONS.md was committed before validate.py", ok, detail)

    # 7. the rule literals in results.json are the ones the module holds
    import validate as V
    lits = r["rule_literals"]
    same = (lits["R1_gap_pattern"] == V.R1_GAP.pattern
            and lits["R2_nominal_pattern"] == V.R2_NOMINAL.pattern
            and lits["R2_boundary_pattern"] == V.R2_BOUNDARY.pattern
            and lits["R3_verb_alternation"] == V.R3_VERB)
    check("rule literals in results.json are byte-identical to the module's", same,
          "four literals compared")

    # 8. R1 is a special case of R2 in principle; where it is not, say so
    both = [x for x in a["rows"] if x["rules"]["R1_adjacent_subject"]
            and not x["rules"]["R2_no_competing_nominal"]]
    check("no row fires R1 without firing R2 (R1 is the stricter rule)", not both,
          "%d exceptions" % len(both))

    ok = all(c["pass"] for c in checks)
    (HERE / "verification.json").write_text(json.dumps(
        {"session": 91, "date": "2026-09-17", "all_pass": ok, "checks": checks}, indent=1) + "\n")
    print("\n  %s -- %d checks" % ("all pass" if ok else "FAILURES", len(checks)))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
