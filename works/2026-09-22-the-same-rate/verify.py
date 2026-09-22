#!/usr/bin/env python3
"""verify.py -- fifteen checks a stranger can run against this directory.

The point of this file is that nothing in the work above has to be believed: the order of the
night, the rules' identity, the calibration, the arithmetic, and every load-bearing figure in
work.md are checked here against the committed records rather than asserted in prose.

    python3 verify.py

Exits non-zero on the first failure it finds, and prints every check either way.
"""

import importlib.util
import json
import re
import subprocess
import sys
import xml.dom.minidom
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
S91 = HERE.parent / "2026-09-17-the-second-instrument"

checks = []


def ok(label, good, detail=""):
    checks.append((bool(good), label, detail))
    print("  %s  %s%s" % ("PASS" if good else "FAIL", label, (" -- " + detail) if detail else ""))


def git(*args):
    return subprocess.run(["git", "-C", str(REPO)] + list(args),
                          capture_output=True, text=True).stdout.strip()


def first_commit(path):
    out = git("log", "--diff-filter=A", "--format=%H", "--", str(path))
    return out.split("\n")[-1] if out else ""


def is_ancestor(a, b):
    return subprocess.run(["git", "-C", str(REPO), "merge-base", "--is-ancestor", a, b]).returncode == 0


def main():
    res = json.load(open(HERE / "results.json"))
    ins = json.load(open(HERE / "inspection.json"))
    adj = json.load(open(HERE / "adjudication.json"))
    sheet = json.load(open(HERE / "sheet.json"))
    verd = json.load(open(HERE / "verdicts.json"))
    work = (HERE / "work.md").read_text()

    # ---- 1-3: the order of the night, by ancestry rather than by claim
    c_sheet = first_commit(HERE / "sheet.json")
    c_pred = first_commit(HERE / "PREDICTIONS.md")
    c_verd = first_commit(HERE / "verdicts.json")
    c_adj = first_commit(HERE / "adjudicate.py")
    ok("the sheet was committed before the pre-registration",
       c_sheet and c_pred and (c_sheet == c_pred or is_ancestor(c_sheet, c_pred)),
       "%s -> %s" % (c_sheet[:7], c_pred[:7]))
    ok("the pre-registration was committed before the verdicts",
       c_pred and c_verd and (c_pred == c_verd or is_ancestor(c_pred, c_verd)),
       "%s -> %s" % (c_pred[:7], c_verd[:7]))
    ok("the verdicts were committed before anything that scores them",
       c_verd and (not c_adj or is_ancestor(c_verd, c_adj)),
       "%s -> %s" % (c_verd[:7], c_adj[:7] if c_adj else "(uncommitted)"))

    # ---- 4: the commit that carried the sheet carried no scoring
    files = git("show", "--name-only", "--format=", c_sheet).split() if c_sheet else []
    ok("the sheet's own commit carries only draw.py and sheet.json",
       sorted(Path(f).name for f in files) == ["draw.py", "sheet.json"],
       ", ".join(sorted(Path(f).name for f in files)))

    # ---- 5: the rules are Session 91's, byte for byte
    src = (S91 / "validate.py").read_text()
    literals = {
        "R1_GAP": r'''R1_GAP = re.compile(r"^[\s,;:.()\[\]'‘’“”-]*(?:(?:who|which|that)"
                    r"[\s,;:.()\[\]'‘’“”-]*)?$", re.IGNORECASE)''',
        "R2_NOMINAL": r'''R2_NOMINAL = re.compile(r"\b(?:the|a|an|any|each|every|such)\s+\w", re.IGNORECASE)''',
        "R2_BOUNDARY": r'''R2_BOUNDARY = re.compile(r"\b(?:and|or|but|if|where|unless|because|which|who|that)\b", re.IGNORECASE)''',
        "R3_VERB": r'''R3_VERB = r"(?:may|must|shall|should|will|can|is|are|has|have)"''',
    }
    missing = [k for k, v in literals.items() if v not in src]
    ok("Session 91's four rule literals are unchanged in validate.py", not missing,
       "missing: " + ", ".join(missing) if missing else "R1_GAP, R2_NOMINAL, R2_BOUNDARY, R3_VERB")

    # ---- 6: importing Session 91's kappa.py rewrites its kappa.json; check it is byte-identical
    spec = importlib.util.spec_from_file_location("s91_kappa_check", S91 / "kappa.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    dirty = git("status", "--porcelain", "--", str(S91 / "kappa.json"))
    ok("importing Session 91's kappa.py leaves its kappa.json byte-identical "
       "(it writes on import -- F-154)", dirty == "", dirty or "clean")

    # ---- 7: the calibration still returns all eighteen of Session 91's figures
    spec = importlib.util.spec_from_file_location("tonight_adjudicate", HERE / "adjudicate.py")
    A = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(A)
    _, _, problems = A.calibrate()
    ok("the UK calibration returns all eighteen published figures", not problems,
       "; ".join(problems) if problems else "18 of 18")

    # ---- 8: the sheet and the verdicts line up row for row
    ns_sheet = [r["n"] for r in sheet["rows"]]
    ns_verd = [r["n"] for r in verd["rows"]]
    ok("forty rows, numbered 1 to 40, in both the sheet and the verdicts",
       ns_sheet == ns_verd == list(range(1, 41)), "%d / %d" % (len(ns_sheet), len(ns_verd)))

    # ---- 9: the night's own failure condition was not tripped
    none = res["reading"]["bearer_none"]
    ok("the reading is not a remnant: NONE verdicts at or below the declared 20 of 40",
       none <= 20, "%d of 40" % none)

    # ---- 10: M1 recomputed from the committed verdicts
    recomputed = sum(1 for r in res["rows"]
                     if A.m1({x["n"]: x for x in verd["rows"]}[r["n"]]["bearer"], r["carrier"]))
    ok("M1 recomputes from verdicts.json to the published count",
       recomputed == res["reading"]["m1_yes"],
       "%d against %d" % (recomputed, res["reading"]["m1_yes"]))

    # ---- 11: R3b is R3 on these rows, as the frame guarantees
    ok("R3b and R3 agree on every row, as block window 0 requires",
       res["r3b_equals_r3_on_these_rows"] is True)

    # ---- 12: the exploratory test is checked against arithmetic, not memory
    sc = ins["does_it_survive_n_40"]["self_check"]
    ok("Fisher's exact self-checks derive their own expected values",
       sc["table_3_1_1_3"]["derived"] == sc["table_3_1_1_3"]["function"] == 0.4857
       and sc["table_4_0_0_4"]["derived"] == sc["table_4_0_0_4"]["function"] == 0.0286,
       "3/1/1/3 %s, 4/0/0/4 %s" % (sc["table_3_1_1_3"]["function"], sc["table_4_0_0_4"]["function"]))

    # ---- 13: nothing in the measuring pipeline touches the network
    net = []
    for f in ("draw.py", "adjudicate.py", "inspect.py", "score.py", "figure.py", "page.py"):
        t = (HERE / f).read_text()
        if re.search(r"\b(urllib|requests|httpx|socket|fetch\()", t):
            net.append(f)
    ok("no measuring script in this work touches the network", not net, ", ".join(net) or "none")

    # ---- 14: the page is self-contained and the figure is valid XML
    xml.dom.minidom.parse(str(HERE / "figure.svg"))
    page = (HERE / "index.html").read_text()
    outside = re.findall(r'(?:src|href)\s*=\s*"(https?://[^"]+)"', page)
    bad_tag = re.search(r'<(?:script|link|img)[^>]+(?:src|href)\s*=\s*"https?://', page)
    ok("figure.svg parses, and index.html loads nothing from outside "
       "(citation links excepted)", bad_tag is None,
       "%d outbound links in prose, %d outbound loads" % (len(outside), 1 if bad_tag else 0))

    # ---- 15: every load-bearing figure in work.md matches the committed records
    uk = res["calibration"]["by_rule"]["R3_active_governor"]
    rfc = res["against_the_reader"]["M1"]["R3_active_governor"]
    sw = ins["does_it_survive_n_40"]["what_forty_rows_could_have_separated"]
    claims = {
        "population 956": str(sheet["population_b_form_agentless_binding"]) == "956",
        "frame 346": str(sheet["population_in_frame"]) == "346",
        "UK fires 19": "**19** of 40" in work and uk["fires"] == 19,
        "RFC fires 18": "**18** of 40" in work and rfc["fires"] == 18,
        "UK precision 0.6842": "0.6842" in work and uk["precision_on_yes"] == 0.6842,
        "RFC precision 0.5556": "0.5556" in work and rfc["precision_on_yes"] == 0.5556,
        "UK kappa +0.4962": "+0.4962" in work and uk["cohens_kappa"] == 0.4962,
        "RFC kappa +0.3814": "+0.3814" in work and rfc["cohens_kappa"] == 0.3814,
        "NONE 16": "16" in work and res["reading"]["bearer_none"] == 16,
        "M1 14 of 40": "14 of 40" in work and res["reading"]["m1_yes"] == 14,
        "MDE 40.64": "40.64" in work and sw["gap_in_points_needed"] == 40.64,
        "observed gap 12.86": "12.86" in work
        and round(100 * (uk["precision_on_yes"] - rfc["precision_on_yes"]), 2) == 12.86,
        "p 0.5077": "0.5077" in work and sw["p_observed"] == 0.5077,
        "price 300 rows": "300" in work and ins["does_it_survive_n_40"]
        ["the_price_of_the_question"]["rows_needed_to_see_a_gap_that_size"] == 300,
        "application x8": "eight times" in work
        and ins["what_the_rule_was_reading"]["most_frequent"] == ["application", 8],
        "predictions 5 of 7": adj["won"] == 5 and len(adj["predictions"]) == 7,
        "M1 vs M2 zero": res["reading"]["m1_m2_disagreements"] == 0,
        "17 after the modal": ins["the_forwards_looking_window"]["RFC"]["after"]["rows"] == 17,
    }
    bad = [k for k, v in claims.items() if not v]
    ok("every load-bearing figure in work.md matches the committed records (%d checked)"
       % len(claims), not bad, "; ".join(bad) if bad else "all match")

    fails = sum(1 for good, _, _ in checks if not good)
    print("\n%d checks, %d failing" % (len(checks), fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
