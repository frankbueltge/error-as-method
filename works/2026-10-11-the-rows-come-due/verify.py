#!/usr/bin/env python3
"""Checks for The Rows Come Due. Stdlib only; uses git for order. Exits non-zero on any failure."""
import json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(H, "..", ".."))
REL = os.path.relpath(H, ROOT); ok = True
def check(c, m):
    global ok; print(("ok   " if c else "FAIL ") + m); ok &= bool(c)
def first(p):
    out = subprocess.run(["git", "log", "--diff-filter=A", "--format=%ct", "--", f"{REL}/{p}"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    return int(out[-1]) if out else None
def order(p):
    out = subprocess.run(["git", "log", "--diff-filter=A", "--format=%H", "--", f"{REL}/{p}"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    if not out: return None
    return int(subprocess.run(["git", "rev-list", "--count", out[-1]], cwd=ROOT, capture_output=True, text=True).stdout)
pre = ["PREDICTIONS.md", "census.json", "readers/PROMPT.md", "readers/ENTRIES.md", "uses.json"]
for p in pre:
    for q in ["readers/reader-A.json", "readers/reader-B.json", "readers/reader-uses.json"]:
        if order(p) and order(q):
            check(order(p) < order(q), f"{p} committed before {q}")
if order("uses-practice.json") and order("readers/reader-uses.json"):
    check(order("uses-practice.json") < order("readers/reader-uses.json"), "practice's use codes committed before the uses reader's")
check(len(json.load(open(os.path.join(H, "uses.json")))["uses"]) == 109, "109 uses")
check(len(json.load(open(os.path.join(H, "census.json")))["rows"]) == 21, "21 entries coded")
for f in ["extract_entries.py", "extract_uses.py", "count.py", "score.py", "build.py"]:
    src = open(os.path.join(H, f)).read()
    check("urllib" not in src and "requests" not in src and "socket" not in src, f"{f} touches no network")
r = subprocess.run([sys.executable, "-I", os.path.join(H, "count.py")], capture_output=True, text=True)
check(r.returncode == 0, "count.py reconciles every quote")
res = json.load(open(os.path.join(H, "results.json")))
check(res["S113_SIDE_a_fires"] and not res["S113_SIDE_b_fires"], "S113.SIDE: (a) fires, (b) does not")
ru = json.load(open(os.path.join(H, "results-uses.json")))
check(not ru["S99_JOIN_b_fires_by_rule"] and ru["reader_T"] == ["U084", "U106"], "S99.JOIN (b): practice 0 T, reader T on U084 and U106")
page = open(os.path.join(H, "index.html")).read()
check("<script src=" not in page and "http://" not in page, "the face loads nothing from another host")
sys.exit(0 if ok else 1)
