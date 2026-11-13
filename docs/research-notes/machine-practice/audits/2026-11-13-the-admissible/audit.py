#!/usr/bin/env python3
"""audit.py -- Session 176 (the seventh night), 2026-11-13. Post hoc, labelled.

Reads only files already committed. Three parts:

  A. The told arms of experiments 48 to 52: what each arm was told, how many of six named a misfit
     (the practice's own coding, coding/mine.json), and where the arm's answer stands against the
     family's own order and against the truth or the public (results.json). No number is computed
     here that the works did not already publish, except the summary over the fifteen arms.
  B. The spread over the seven operations, read off the Experiments table of PROJECT.md, in every
     window of ten consecutive experiments (the fifth failure criterion, Session 138, F-269).
  C. Whether an experiment's briefs asked its instances to make anything (a work, a page, a
     drawing), for experiments 35 to 52, by a fixed word screen over briefs/.

    python3 docs/research-notes/machine-practice/audits/2026-11-13-the-admissible/audit.py
"""

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
W = ROOT / "works"


def load(d, f):
    return json.loads((W / d / f).read_text())


def named(code):
    """Normalise the five different coding formats to True/False."""
    if isinstance(code, bool):
        return code
    if isinstance(code, str):
        return code.upper() == "YES"
    if isinstance(code, list):
        return code[0].upper() == "YES"
    if isinstance(code, dict):
        return code.get("named", "NO").upper() == "YES"
    raise ValueError(code)


def coded(d):
    m = load(d, "coding/mine.json")
    if "codes" in m:
        m = m["codes"]
    return {k: named(v) for k, v in m.items() if not k.startswith("_") and k != "coder"}


# Each told arm: (experiment, dir, arm, what it was told, key for rho with own order,
# key for rho with truth/public). "own" is the family's own order on the scored keys: the arm that
# answered as itself (48 A, 49 A, 50 family) or, for quantities of the world, the arm told nothing (51 U, 52 U).
ARMS = [
    (48, "2026-11-05-laughed-off", "B", "true values", "rho_family", "rho_people"),
    (48, "2026-11-05-laughed-off", "S", "random deal", "rho_family", "rho_people"),
    (48, "2026-11-05-laughed-off", "V", "true values in the family's order", "rho_family", "rho_people"),
    (49, "2026-11-06-second-tongue", "B", "true values", "rho_family", "rho_l2"),
    (49, "2026-11-06-second-tongue", "S", "random deal", "rho_family", "rho_l2"),
    (49, "2026-11-06-second-tongue", "R", "reversed (believable)", "rho_family", "rho_l2"),
    (50, "2026-11-07-half-turned", "B", "true values", "rho_family", "rho_brazil"),
    (50, "2026-11-07-half-turned", "H", "half turned (believable)", "rho_family", "rho_brazil"),
    (50, "2026-11-07-half-turned", "R", "reversed (believable)", "rho_family", "rho_brazil"),
    (51, "2026-11-08-read-backwards", "B", "true values", "rho_with_U", "rho_truth"),
    (51, "2026-11-08-read-backwards", "H", "half turned (believable)", "rho_with_U", "rho_truth"),
    (51, "2026-11-08-read-backwards", "R", "reversed (believable)", "rho_with_U", "rho_truth"),
    (52, "2026-11-11-said-to-contain-errors", "R", "reversed (unbelievable), as fact", "rho_with_U", "rho_truth"),
    (52, "2026-11-11-said-to-contain-errors", "D", "reversed (unbelievable), may contain errors", "rho_with_U", "rho_truth"),
    (52, "2026-11-11-said-to-contain-errors", "T", "true (one month atypical), may contain errors", "rho_with_U", "rho_truth"),
]


def part_a():
    rows = []
    for exp, d, arm, told, kown, ktrue in ARMS:
        r = load(d, "results.json")["arms"][arm]
        c = coded(d)
        n = sum(1 for k, v in c.items() if k.startswith(arm) and k[len(arm):].isdigit() and v)
        rows.append({"exp": exp, "arm": arm, "told": told, "named_of_6": n,
                     "rho_own": r[kown], "rho_truth_or_public": r[ktrue]})
    return rows


OPS = ["choosing material", "finding a form", "iterating", "varying", "perceiving", "judging", "erring"]


def experiments_table():
    text = (ROOT / "docs/research-notes/machine-practice/PROJECT.md").read_text()
    out = []
    for ln in text.splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|[^|]*\|\s*\[\*\*[^]]*\*\*\]\(\.\./\.\./works/([^)/]+)/?\)\s*\|([^|]*)\|", ln)
        if m:
            ops_text = m.group(3).lower()
            ops = {o for o in OPS if o in ops_text}
            out.append((int(m.group(1)), m.group(2), ops))
    return out


def part_b(table):
    windows = []
    for i in range(len(table) - 9):
        win = table[i:i + 10]
        used = set().union(*(w[2] for w in win))
        idle = [o for o in OPS if o not in used]
        windows.append({"from": win[0][0], "to": win[-1][0], "unexercised": idle, "fires": len(idle) >= 4})
    return windows


MAKE = re.compile(r"make one work|make a work|\bindex\.html\b|\bdraw (it|the|each|a)\b|as strokes", re.I)


def part_c(table):
    out = []
    for n, d, _ in table:
        if n < 35:
            continue
        b = W / d / "briefs"
        files = sorted(p for p in b.rglob("*") if p.is_file()) if b.exists() else []
        hits = [p.name for p in files if MAKE.search(p.read_text(errors="replace"))]
        out.append({"exp": n, "dir": d, "briefs": len(files), "briefs_asking_to_make": len(hits)})
    return out


def main():
    a = part_a()
    table = experiments_table()
    b = part_b(table)
    c = part_c(table)
    lines = ["A. Told arms, experiments 48-52 (named: the practice's own coding)", ""]
    lines.append("  exp arm  named  rho_own  rho_truth  told")
    for r in a:
        lines.append("  %3d %-3s  %d/6   %+6.3f   %+6.3f    %s" % (
            r["exp"], r["arm"], r["named_of_6"], r["rho_own"], r["rho_truth_or_public"], r["told"]))
    absown = sorted(abs(r["rho_own"]) for r in a)
    neg = [("%d%s" % (r["exp"], r["arm"])) for r in a if r["rho_own"] < 0]
    lines += ["", "  |rho_own| over %d arms: min %.3f, median %.3f, max %.3f" % (
        len(a), absown[0], absown[len(absown) // 2], absown[-1]),
        "  arms whose answer stands on the family's order with the sign changed: %s" % ", ".join(neg), ""]
    lines.append("B. Operations over windows of ten experiments (fires = four or more unexercised)")
    lines.append("")
    for w in b:
        if w["fires"] or w["to"] >= 45:
            lines.append("  %2d-%2d  %-5s  unexercised: %s" % (
                w["from"], w["to"], "FIRES" if w["fires"] else "ok", ", ".join(w["unexercised"]) or "-"))
    lines += ["", "C. Briefs that ask an instance to make something (experiments 35-52)", ""]
    for r in c:
        lines.append("  %2d  %2d of %2d  %s" % (r["exp"], r["briefs_asking_to_make"], r["briefs"], r["dir"]))
    txt = "\n".join(lines) + "\n"
    (HERE / "audit.txt").write_text(txt)
    (HERE / "results.json").write_text(json.dumps({"told_arms": a, "windows": b, "making": c}, indent=1) + "\n")
    print(txt)


if __name__ == "__main__":
    main()
