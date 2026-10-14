#!/usr/bin/env python3
"""Checks for Whose Account. Stdlib only; uses git for order. Exits non-zero on any failure."""
import json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(H, "..", ".."))
REL = os.path.relpath(H, ROOT); ok = True
def check(c, m):
    global ok; print(("ok   " if c else "FAIL ") + m); ok &= bool(c)
def order(p):
    out = subprocess.run(["git", "log", "--diff-filter=A", "--format=%H", "--", f"{REL}/{p}"], cwd=ROOT,
                         capture_output=True, text=True).stdout.split()
    if not out: return None
    return int(subprocess.run(["git", "rev-list", "--count", out[-1]], cwd=ROOT, capture_output=True, text=True).stdout)
seq = ["PREDICTIONS.md", "sort.json", "practice.json", "readers/reader-A.json"]
for a, b in zip(seq, seq[1:]):
    check(order(a) and order(b) and order(a) < order(b), f"{a} committed before {b}")
check(order("readers/PROMPT.md") < order("readers/reader-A.json"), "prompt committed before the readers answered")
check(order("order.json") <= order("PREDICTIONS.md"), "walk order committed with the pre-registration")
srt = json.load(open(os.path.join(H, "sort.json")))["sort"]
check(len(srt) == 500, "500 entries walked and sorted (the cap)")
sel = json.load(open(os.path.join(H, "selected.json")))
check(sum(len(v) for v in sel["cells"].values()) == 57 and not sel["full"], "57 taken, quotas not all full")
ent = json.load(open(os.path.join(H, "entries.json")))["rows"]
check(all(srt[r["eid"]]["group"] == r["group"] for r in ent), "every entry's group is its committed sort")
for k in "AB":
    rd = json.load(open(os.path.join(H, "readers", f"reader-{k}.json")))
    check(len(rd) == 57 and all(r["wrong"] in "JRBX" for r in rd), f"reader {k}: 57 valid codes")
r = subprocess.run([sys.executable, "-I", os.path.join(H, "score.py")], capture_output=True, text=True)
check(r.returncode == 0, "score.py runs")
res = json.load(open(os.path.join(H, "results.json")))
check(res["testable"] and res["verdict"] == "falsified", "S120.ACCOUNT: testable, falsified")
check(res["pooled"]["A"]["splits"] == 0 and res["pooled"]["S"]["splits"] == 0, "no side-split in either group")
for f in ["draw.py", "walk.py", "quota.py", "addsort.py", "entries.py", "score.py", "build.py"]:
    src = open(os.path.join(H, f)).read()
    check("urllib" not in src and "requests" not in src and "socket" not in src, f"{f} touches no network")
page = open(os.path.join(H, "index.html")).read()
check('src="http' not in page and "<link" not in page, "the face loads nothing from another host")
sys.exit(0 if ok else 1)
