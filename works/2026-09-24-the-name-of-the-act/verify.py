#!/usr/bin/env python3
"""verify.py -- the night's order and its numbers, checked from git and from the files.

1. PREDICTIONS.md and power.py were committed before draw.py existed; draw.py and sheet.json before
   verdicts.json; verdicts.json before score.py and inspect.py.  Checked by first-commit ancestry.
2. PREDICTIONS.md and verdicts.json have not changed since their first commit.
3. draw.py, re-run, reproduces census.json and sheet.json byte for byte.
4. score.py, re-run, reproduces results.json; and its verdict on S95.NOTPARTY is FALSIFIED.
5. No measuring script imports a network module.
6. power.py's self-check (derived from math.comb, not from memory -- F-155) passes.
7. Importing Session 91's and Session 94's scripts left their published files untouched (F-154).
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
REL = HERE.relative_to(REPO).as_posix()
fails = []


def git(*a):
    return subprocess.run(["git", *a], cwd=REPO, capture_output=True, text=True).stdout.strip()


def first_commit(name):
    out = git("log", "--diff-filter=A", "--format=%H", "--", "%s/%s" % (REL, name)).split()
    return out[-1] if out else None


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        fails.append(what)


def before(a, b):
    ca, cb = first_commit(a), first_commit(b)
    if not ca or not cb:
        return False
    return ca != cb and subprocess.run(["git", "merge-base", "--is-ancestor", ca, cb], cwd=REPO).returncode == 0


check(before("PREDICTIONS.md", "draw.py"), "PREDICTIONS.md committed before draw.py")
check(before("power.py", "sheet.json"), "power.py committed before sheet.json")
check(before("sheet.json", "verdicts.json"), "sheet.json committed before verdicts.json")
check(before("verdicts.json", "score.py"), "verdicts.json committed before score.py")
check(before("verdicts.json", "inspect.py"), "verdicts.json committed before inspect.py")
for f in ("PREDICTIONS.md", "verdicts.json"):
    check(git("log", "--format=%H", "--", "%s/%s" % (REL, f)).count("\n") == 0,
          "%s has exactly one commit touching it" % f)

snap = {f: (HERE / f).read_bytes() for f in ("census.json", "sheet.json", "results.json", "power.json")}
for script in ("power.py", "draw.py", "score.py"):
    r = subprocess.run([sys.executable, script], cwd=HERE, capture_output=True, text=True)
    check(r.returncode == 0, "%s runs" % script)
for f, b in snap.items():
    check((HERE / f).read_bytes() == b, "%s reproduced byte for byte" % f)
check('"S95.NOTPARTY": "FALSIFIED"' in (HERE / "results.json").read_text(), "results say FALSIFIED")

for script in ("power.py", "draw.py", "inspect.py", "score.py", "figure.py"):
    src = (HERE / script).read_text()
    check(not any(m in src for m in ("urllib", "requests", "http.client", "socket")),
          "%s imports no network module" % script)

dirty = git("status", "--porcelain", "--", "works/2026-09-17-the-second-instrument",
            "works/2026-09-21-three-other-offices")
check(dirty == "", "earlier nights' files untouched by importing their scripts")

print("\n%d failure(s)" % len(fails))
sys.exit(1 if fails else 0)
