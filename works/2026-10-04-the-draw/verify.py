"""Checks the night's order in git, the draw's arithmetic, the harvest's hash, and that the
counts reproduce. Run from this directory after the night is committed."""
import subprocess, json, hashlib, re
W = "works/2026-10-04-the-draw/"
def git(*a): return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout.strip()
def added(p):
    h = git("log", "--format=%H", "--diff-filter=A", "--", p).split("\n"); assert h[-1], p; return h[-1]
def anc(a, b): return subprocess.run(["git", "merge-base", "--is-ancestor", a, b]).returncode == 0
def before(a, b): return a != b and anc(a, b)
def show(c, p):
    r = subprocess.run(["git", "show", f"{c}:{W}{p}"], capture_output=True, text=True); return r.stdout if r.returncode == 0 else ""
ok = True
def check(n, c):
    global ok; ok &= bool(c); print(("PASS " if c else "FAIL ") + n)
pre, log = added("PREDICTIONS.md"), added("draw-log.json")
check("PREDICTIONS.md and draw.py committed together, before the draw log", pre == added("draw.py") and before(pre, log))
d = json.load(open("draw-log.json"))
check("the draw log names the pre-registration commit", d["commit"] == pre)
check("first index = first 8 hex digits of that commit mod the count", int(pre[:8], 16) % d["count_at_draw"] == d["first_index"])
check("candidates are consecutive from the first index", [c["index"] for c in d["candidates"]] == list(range(d["first_index"], d["first_index"] + len(d["candidates"]))))
check("only the last candidate is admitted", [c["verdict"] == "admitted" for c in d["candidates"]] == [False] * (len(d["candidates"]) - 1) + [True])
check("every refusal offered no admitted format", all(all(f.endswith("/HTML") for f in c["formats"]) for c in d["candidates"][:-1]))
exp, csv = added("EXPECT.md"), added("sources/45211-0013_00.csv")
check("EXPECT.md committed after the draw and before the harvest", before(log, exp) and before(exp, csv))
m = json.load(open("sources/MANIFEST.json"))
check("harvested CSV matches its manifest hash", hashlib.sha256(open("sources/45211-0013_00.csv", "rb").read()).hexdigest() == m["sha256"])
check("draw.py was changed only in commits that name F-171 or F-172",
      all(re.search(r"F-17[12]", git("log", "-1", "--format=%s", c)) for c in git("log", "--format=%H", "--", "draw.py").split("\n")[:-1]))
for n in range(1, 6):
    s = added(f"seen/{n}.png")
    check(f"seen/{n}.png committed before its entry was written", not re.search(rf"^## {n} ·", show(s, "MAKING.md"), re.M))
    e = next(c for c in reversed(git("log", "--format=%H", "--", "MAKING.md").split("\n")) if re.search(rf"^## {n} ·", show(c, "MAKING.md"), re.M))
    nxt = added(f"seen/{n + 1}.png")
    if n == 1: check("entry 1 committed with, not before, iteration 2 (disclosed)", anc(e, nxt))
    else: check(f"entry {n} committed before seen/{n + 1}.png existed", before(e, nxt))
old = json.load(open("results.json")); subprocess.run(["python3", "score.py"], capture_output=True, check=True)
check("results.json reproduces from MAKING.md and the draw logs", json.load(open("results.json")) == old)
print("ALL PASS" if ok else "SOME CHECKS FAILED")
