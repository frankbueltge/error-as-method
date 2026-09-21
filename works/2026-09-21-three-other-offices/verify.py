#!/usr/bin/env python3
"""verify.py -- the checks a stranger can run against this night without trusting a sentence of it.

Eleven checks.  They do not confirm the night's argument; they confirm that its numbers come from
where it says they come from, that the rules were imported rather than rewritten, that the
pre-registration precedes the measurement in git, and that every figure quoted in work.md resolves
to a committed JSON value.

    python3 verify.py
"""

import json
import re
import subprocess
import sys
import xml.dom.minidom
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
S91 = HERE.parent / "2026-09-17-the-second-instrument"
R3B = "R3b_active_governor_own_block"

fails = []


def check(label, good, detail=""):
    print("  %s  %s%s" % ("PASS" if good else "FAIL", label, (" -- " + detail) if detail else ""))
    if not good:
        fails.append(label)


def git(*args):
    return subprocess.run(["git", "-C", str(REPO)] + list(args),
                          capture_output=True, text=True).stdout.strip()


def main():
    res = json.load(open(HERE / "results.json"))
    ins = json.load(open(HERE / "inspection.json"))
    adj = json.load(open(HERE / "adjudication.json"))
    work = (HERE / "work.md").read_text()

    # 1 -------------------------------------------------------------- the pre-registration is first
    added = git("log", "--diff-filter=A", "--format=%H", "--",
                "works/2026-09-21-three-other-offices/PREDICTIONS.md").split("\n")[-1]
    tree = git("ls-tree", "-r", "--name-only", added,
               "works/2026-09-21-three-other-offices/") if added else ""
    listed = [l for l in tree.split("\n") if l.strip()]
    check("PREDICTIONS.md was committed, and that commit carries nothing else from this work",
          bool(added) and listed == ["works/2026-09-21-three-other-offices/PREDICTIONS.md"],
          "%s: %s" % (added[:9] or "(no commit)", listed or "(empty)"))

    # 2 -------------------------------------------------------------- the rules were imported
    src = (HERE / "port.py").read_text()
    defines = re.findall(r"^def (r1|r2|r3|r3b)\b", src, re.M)
    check("port.py defines no rule of its own", not defines, ", ".join(defines) or "none")

    sys.path.insert(0, str(HERE))
    import port as P
    for fn in (P.V.r1, P.V.r2, P.V.r3, P.V.r3b):
        pass
    where = Path(P.V.r3.__code__.co_filename).resolve()
    check("r1/r2/r3/r3b are the functions in Session 91's validate.py",
          where == (S91 / "validate.py").resolve(), str(where))

    # 3 -------------------------------------------------------------- the literals are unchanged
    published = json.load(open(S91 / "results.json"))["rule_literals"]
    mine = {"R1_gap_pattern": P.V.R1_GAP.pattern,
            "R2_nominal_pattern": P.V.R2_NOMINAL.pattern,
            "R2_boundary_pattern": P.V.R2_BOUNDARY.pattern,
            "R3_verb_alternation": P.V.R3_VERB}
    check("the four rule literals are byte-identical to Session 91's published ones",
          mine == published,
          "; ".join(k for k in published if mine.get(k) != published[k]) or "all four identical")

    # 4 -------------------------------------------------------------- the calibration
    cal = res["calibration_UK_statute"]
    want = cal["session_91_published"]
    bad = []
    for l, w in want.items():
        got = cal["lists"][l]
        if got["rows_in_reach_at_word_36"] != w["in_reach"]:
            bad.append("%s reach" % l)
        for short, key in (("R1", "R1_adjacent_subject"), ("R2", "R2_no_competing_nominal"),
                           ("R3", "R3_active_governor"), ("R3b", R3B)):
            if got["by_rule"][key]["fire_rate"] != w[short]:
                bad.append("%s/%s" % (l, short))
    check("the port reproduces Session 91's three reach counts and twelve fire rates exactly",
          not bad, ", ".join(bad) or "15 of 15 agree")

    # 5 -------------------------------------------------------------- populations, recomputed
    pops = {}
    for name, spec in P.CORPORA.items():
        _, rows = spec["build"]()
        pops[name] = len(rows)
    check("the three populations recompute from the committed occurrence files",
          all(pops[n] == res["corpora"][n]["population"] for n in pops),
          "; ".join("%s %d" % (n, v) for n, v in pops.items()))

    # 6 -------------------------------------------------------------- the RFC paragraph mapping
    docs, rows = P.rfc()
    miss = sum(1 for r in rows if r["sentence"] not in docs[r["doc"]][r["block"]])
    check("every RFC obligation sits inside the paragraph tonight mapped it to",
          miss == 0, "%d of %d rows outside their block" % (miss, len(rows)))

    # 7 -------------------------------------------------------------- the verdict is the arithmetic
    band = (21.42, 41.42)
    inside = [n for n, e in res["corpora"].items()
              if band[0] <= e["lists"]["narrow"]["by_rule"][R3B]["fire_pct"] <= band[1]]
    check("the falsification verdict follows from the band and the narrow figures",
          inside == adj["S91.RULEBOUND"]["inside_the_band"]
          and (adj["S91.RULEBOUND"]["verdict"] == "FALSIFIED") == bool(inside),
          "%s -> %s" % (inside or "none", adj["S91.RULEBOUND"]["verdict"]))

    # 8 -------------------------------------------------------------- the exploratory ordering
    agree = [k for k, v in ins["agreement"].items() if v]
    check("only the subjecthood ordering reproduces the rule's own order",
          agree == ["by_subjecthood_rate"], ", ".join(agree) or "none")

    # 9 -------------------------------------------------------------- the page fetches nothing
    html = (HERE / "index.html").read_text()
    outside = re.findall(r'(?:src|href)\s*=\s*"(?!figure\.svg)(?:https?:)?//[^"]*"', html)
    apis = [w for w in ("fetch(", "XMLHttpRequest", "import(", "new Worker", "WebSocket")
            if w in html]
    check("index.html loads nothing from outside and opens no channel",
          not outside and not apis, "; ".join(outside + apis) or "clean")

    # 10 ------------------------------------------------------------- the figure parses
    xml.dom.minidom.parse(str(HERE / "figure.svg"))
    svg = (HERE / "figure.svg").read_text()
    check("figure.svg parses and states the same verdict as adjudication.json",
          adj["S91.RULEBOUND"]["verdict"] in svg, adj["S91.RULEBOUND"]["verdict"])

    # 11 ------------------------------------------------------------- work.md resolves to the JSON
    C, cl = res["corpora"], cal["lists"]
    claims = [
        ("67.59", C["EU acts"]["lists"]["narrow"]["by_rule"][R3B]["fire_pct"]),
        ("55.52", C["WHATWG standards"]["lists"]["narrow"]["by_rule"][R3B]["fire_pct"]),
        ("28.15", C["RFCs"]["lists"]["narrow"]["by_rule"][R3B]["fire_pct"]),
        ("29.62", C["RFCs"]["lists"]["wide"]["by_rule"][R3B]["fire_pct"]),
        ("49.19", C["RFCs"]["lists"]["base"]["by_rule"][R3B]["fire_pct"]),
        ("31.42", cl["narrow"]["by_rule"][R3B]["fire_pct"]),
        ("3,864", C["EU acts"]["population"]),
        ("956", C["RFCs"]["population"]),
        ("1,190", C["WHATWG standards"]["population"]),
        ("2,015", C["EU acts"]["lists"]["narrow"]["rows_in_reach_at_word_36"]),
        ("302", C["RFCs"]["lists"]["narrow"]["rows_in_reach_at_word_36"]),
        ("697", C["WHATWG standards"]["lists"]["narrow"]["rows_in_reach_at_word_36"]),
        ("52.69", round(C["EU acts"]["lists"]["wide"]["reach_pct"]
                        - C["EU acts"]["lists"]["base"]["reach_pct"], 2)),
        ("42.86", round(C["WHATWG standards"]["lists"]["wide"]["reach_pct"]
                        - C["WHATWG standards"]["lists"]["base"]["reach_pct"], 2)),
        ("19.88", round(C["RFCs"]["lists"]["wide"]["reach_pct"]
                        - C["RFCs"]["lists"]["base"]["reach_pct"], 2)),
        ("77.47", C["WHATWG standards"]["lists"]["narrow"]["carrier_in_own_block_pct"]),
        ("47.59", C["WHATWG standards"]["lists"]["base"]["carrier_in_own_block_pct"]),
        ("39.44", round(max(e["lists"]["narrow"]["by_rule"][R3B]["fire_pct"]
                            for e in C.values())
                        - min(list(e["lists"]["narrow"]["by_rule"][R3B]["fire_pct"]
                                   for e in C.values())
                              + [cl["narrow"]["by_rule"][R3B]["fire_pct"]]), 2)),
    ]
    subj = {r["corpus"].replace(" (calibration)", ""): r["subjecthood_rate_pct"]
            for r in ins["rows"]}
    claims += [("29.14", subj["EU acts"]), ("19.88", subj["WHATWG standards"]),
               ("19.07", subj["UK Acts"]), ("13.65", subj["RFCs"])]
    bad = []
    for text, value in claims:
        want = text.replace(",", "")
        got = ("%g" % value) if isinstance(value, float) else str(value)
        if want != got:
            bad.append("%s != %s" % (text, got))
        elif text not in work:
            bad.append("%s absent from work.md" % text)
    check("every headline figure in work.md is the committed value, to the digit",
          not bad, "; ".join(bad) or "%d figures checked" % len(claims))

    # 12 ------------------------------------------------------------- the tally
    check("the prediction tally in work.md matches adjudication.json",
          adj["tally"] == "3 of 7 won" and "three of seven" in work.lower(), adj["tally"])

    print("\n%s" % ("all checks pass" if not fails
                    else "%d failed: %s" % (len(fails), "; ".join(fails))))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
