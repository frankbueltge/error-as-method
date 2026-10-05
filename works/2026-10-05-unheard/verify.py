"""Checks the record of Unheard against its claims. python3 verify.py"""
import json, re, subprocess, hashlib, os, sys
here = os.path.dirname(os.path.abspath(__file__)); os.chdir(here)
ok = True
def check(name, cond):
    global ok; ok &= bool(cond); print(("PASS " if cond else "FAIL ") + name)
def first(path):  # unix time of the commit that first added path
    out = subprocess.run(["git", "log", "--diff-filter=A", "--format=%ct %h", "--", path], capture_output=True, text=True).stdout.split("\n")
    out = [l for l in out if l]
    return (int(out[-1].split()[0]), out[-1].split()[1]) if out else (None, None)
def order(a, b):
    ta, tb = first(a), first(b)
    # same second is possible; fall back to topological order
    if ta[0] is None or tb[0] is None: return False
    if ta[1] == tb[1]: return False
    r = subprocess.run(["git", "merge-base", "--is-ancestor", ta[1], tb[1]])
    return r.returncode == 0
check("pre-registration committed before the recording", order("PREDICTIONS.md", "sources/kirkbymoorside.commons-transcode.mp3"))
check("S reading committed before any N output", order("readings/R-1-S.md", "readings/R-2-N-out-120-128.txt"))
check("N reading committed before the B picture of R", order("readings/R-2-N.md", "seen/R-B-detected-20-60.png"))
check("B reading and reconciliation before i1 exists", order("readings/R-4-reconciliation.md", "iterations/i1.json"))
for k in (1, 2, 3):
    # The promise was: the note before the next *sound*. The notes for i2 and i3 share a commit with
    # the next iteration's parameters (written after the note in the same step; disclosed in the
    # journal), so the check is against the next sound's picture, which came in a later commit.
    check(f"i{k} note committed before i{k+1} sound was rendered", order(f"iterations/i{k}-note.md", f"seen/i{k+1}-S-030-045.png"))
    check(f"i{k} picture committed before (or with) its note", order(f"seen/i{k}-S-030-045.png", f"iterations/i{k}-note.md"))
m = json.load(open("sources/MANIFEST.json"))
for s in m["sources"]:
    if s.get("committed"):
        h = hashlib.sha256(open(s["path"], "rb").read()).hexdigest()
        check(f"hash of {s['path']}", h == s["sha256"])
tally = re.search(r"\*\*S (\d+), N (\d+), B (\d+), K (\d+)\.\*\*", open("iterations/i4-note.md").read()).groups()
page = re.search(r'\["S","pictures",(\d+)\],\["N","numbers",(\d+)\],\["B","the ringers\' picture",(\d+)\],\["K","knowledge, no perceiving",(\d+)\]', open("index.html").read()).groups()
check("tally on the face equals the tally in i4-note", tally == page)
rows = json.load(open("iterations/i4.rows.json"))["rows"]
body = rows[3:64]
check("Plain Bob Minor course: 60 distinct rows between rounds", len({tuple(r) for r in body[:-1]}) == 60 and body[-1] == [1, 2, 3, 4, 5, 6])
for k in range(1, 5):
    out = open(f"iterations/i{k}-N-out.txt").read()
    full, n = map(int, re.search(r"holding all six bells (\d+) of (\d+)", out).groups())
    check(f"detector on own ringing i{k} finds whole rows in under a third of windows ({full}/{n})", full / n < 1 / 3)
for f in ["index.html", "work.md", "meta.json", "figure.svg"] + [f"audio/i{k}-30-45.mp3" for k in range(1, 5)] + ["audio/R-30-45.mp3"]:
    check("exists " + f, os.path.exists(f))
sys.exit(0 if ok else 1)
