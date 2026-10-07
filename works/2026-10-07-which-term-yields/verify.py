"""Checks for Which Term Yields. Run from anywhere: python3 works/2026-10-07-which-term-yields/verify.py"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=HERE, text=True).strip()
W = os.path.relpath(HERE, ROOT)
ok = 0
def check(cond, msg):
    global ok
    if not cond:
        print("FAIL", msg); sys.exit(1)
    ok += 1; print("ok  ", msg)
def first(path):
    out = subprocess.check_output(["git", "log", "--format=%ct %H", "--diff-filter=A", "--", path], cwd=ROOT, text=True).split()
    return (int(out[-2]), out[-1]) if out else None
def before(a, b):
    ca, cb = first(f"{W}/{a}"), first(f"{W}/{b}")
    if not ca or not cb: return False
    r = subprocess.run(["git", "merge-base", "--is-ancestor", ca[1], cb[1]], cwd=ROOT)
    return r.returncode == 0 and ca[1] != cb[1]
order = ["PREDICTIONS.md", "census.json", "readers/PROMPT.md", "readers/reader-A.json", "readers/reader-B.json"]
for a, b in zip(order, order[1:]):
    check(before(a, b), f"{a} committed before {b}")
check(before("readers/reader-B.json", "results.json") or first(f"{W}/results.json") is None,
      "results.json not committed before the readers")
census = json.load(open(os.path.join(HERE, "census.json")))["rows"]
check([r["id"] for r in census] == [f"F-{n}" for n in range(164, 193)], "census holds F-164 to F-192, in order")
check(all(r["wrong"] in "JRBX" and r["changed"] in "yn" for r in census), "every census code is J/R/B/X and y/n")
for k in "AB":
    rd = json.load(open(os.path.join(HERE, "readers", f"reader-{k}.json")))
    check([r["id"] for r in rd] == [r["id"] for r in census], f"reader {k} answered all 29 in order")
entries = open(os.path.join(HERE, "readers", "ENTRIES.md")).read()
check(all(f"## {r['id']} " in entries for r in census), "ENTRIES.md holds all 29 entries")
for r in census:
    body = entries.split(f"## {r['id']} ")[1].split("\n## ")[0]
    q = r["quote"].replace('\\"', '"')
    words = [w for w in q.replace("...", " ").split() if len(w) > 3][:4]
    check(all(w.strip('".,:;') in body for w in words), f"{r['id']} quote's words are in its entry")
res = json.load(open(os.path.join(HERE, "results.json")))
check(res["practice"] == {"J": 14, "R": 13, "B": 1, "X": 1}, "practice counts J14 R13 B1 X1")
check(res["P1"]["holds"] and res["P2"]["holds"] and res["P3"]["holds"], "P1, P2, P3 hold on the practice's codes")
check(res["readers"]["A"]["P1_under_this_reader"] is False and res["readers"]["B"]["P1_under_this_reader"] is True,
      "P1 fails under reader A, holds under reader B")
html = open(os.path.join(HERE, "index.html")).read()
check('"F-192"' in html and "src=\"http" not in html, "face carries the data and loads nothing from elsewhere")
pos = open(os.path.join(ROOT, "works", "position-2026-10-07.md")).read()
check("> **Error is a difference onto which an observer has already imposed a norm.**" in pos, "the standing sentence stands word for word")
print(f"{ok} checks pass")
