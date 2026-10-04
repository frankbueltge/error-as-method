"""Checks that the order claimed in FOLLOWING.md is the order in git, and that the scores
reproduce. Run from this directory after the night is committed."""
import subprocess, json, glob, re
def git(*a): return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout.strip()
def added(path):
    h = git("log", "--format=%H", "--diff-filter=A", "--", path).split("\n")
    assert h and h[-1], f"never added: {path}"; return h[-1]
def before(a, b): return a != b and subprocess.run(["git", "merge-base", "--is-ancestor", a, b]).returncode == 0
ok = True
def check(name, cond):
    global ok; ok &= bool(cond); print(("PASS " if cond else "FAIL ") + name)
data = added("data.js")
check("PREDICTIONS.md committed before the harvest", before(added("PREDICTIONS.md"), data))
check("the mould (iterations/0-mould.js) committed before the harvest", before(added("iterations/0-mould.js"), data))
its = {int(p.split("/")[1].split("-")[0]): p for p in glob.glob("iterations/*.js")}
for n in sorted(its):
    if n + 1 not in its: continue
    seen = added(f"seen/{n}.png")
    body = git("show", f"{seen}:works/2026-10-04-the-mould/FOLLOWING.md")
    check(f"entry {n} is in the commit that adds seen/{n}.png", re.search(rf"^## {n} ·", body, re.M))
    check(f"seen/{n}.png and entry {n} committed before iterations/{n+1} existed", before(seen, added(its[n + 1])))
for n, p in its.items():
    check(f"{p} unchanged since it was first committed", len(git("log", "--format=%H", "--", p).split("\n")) == 1)
old = json.load(open("results.json")); subprocess.run(["python3", "score.py"], capture_output=True, check=True)
check("results.json reproduces from FOLLOWING.md", json.load(open("results.json")) == old)
print("ALL PASS" if ok else "SOME CHECKS FAILED")
