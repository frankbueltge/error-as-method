"""verify.py — Withdrawn (Session 104). Run from this directory; exits non-zero on any failure.
1. Order, from git: PREDICTIONS.md was committed before notices.json existed; hand.json before code.py.
2. The coder reproduces results.json from notices.json and hand.json.
3. The face carries every notice and the counts it prints."""
import json, subprocess, sys
D = "works/2026-10-04-withdrawn/"
def first(path):
    out = subprocess.run(["git", "log", "--diff-filter=A", "--format=%H", "--", path],
                         capture_output=True, text=True, cwd="../..").stdout.split()
    return out[-1] if out else None
def before(a, b):
    return subprocess.run(["git", "merge-base", "--is-ancestor", a, b], cwd="../..").returncode == 0 and a != b
ok = True
def check(name, cond):
    global ok; ok &= bool(cond); print(("ok   " if cond else "FAIL ") + name)
p, n, h, c = (first(D + f) for f in ("PREDICTIONS.md", "notices.json", "hand.json", "code.py"))
check("predictions committed before the harvest", p and n and before(p, n))
check("hand verdicts committed before the coder", h and c and before(h, c))
old = json.load(open("results.json"))
subprocess.run([sys.executable, "code.py"], capture_output=True, check=True)
subprocess.run([sys.executable, "correct.py"], capture_output=True, check=True)
new = json.load(open("results.json"))
check("coder reproduces results.json", old == new)
check("P1 falsified, P2 falsified, P3 holds, P4 falsified",
      [new[k] for k in ("P1", "P2", "P3", "P4")] == ["falsified", "falsified", "holds", "falsified"])
check("P5 holds on all four questions", set(new["P5"].values()) == {"holds"})
html = open("index.html").read()
check("face holds all 7,282 notices", html.count('["') >= 7282 and "7,282" in html)
check("face fetches nothing", "fetch(" not in html and "src=\"http" not in html and "@import" not in html)
sys.exit(0 if ok else 1)
