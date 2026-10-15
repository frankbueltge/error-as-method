"""verify.py: re-derives tonight's evidence and checks the order of commits. Run from anywhere:
python3 works/2026-10-15-told-a-tide/verify.py"""
import hashlib, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REL = os.path.relpath(HERE, subprocess.check_output(["git", "-C", HERE, "rev-parse", "--show-toplevel"], text=True).strip())
ok = fail = 0
def check(name, cond):
    global ok, fail
    print(("ok   " if cond else "FAIL ") + name); ok += bool(cond); fail += (not cond)
def git(*a): return subprocess.check_output(["git", "-C", HERE] + list(a), text=True).strip()
for e in json.load(open(os.path.join(HERE, "sources", "MANIFEST.json"))):
    b = open(os.path.join(HERE, "sources", e["file"]), "rb").read()
    check("source hash " + e["file"], hashlib.sha256(b).hexdigest() == e["sha256"] and len(b) == e["bytes"])
d = json.load(open(os.path.join(HERE, "sources", "usgs_geomag_BOU_H_minute_20250702_20250901.json")))
v = d["values"][0]["values"]; rows = []
for i in range(0, 87840, 60):
    w = [x for x in v[i:i + 60] if x is not None]; rows.append(sum(w) / len(w))
hj = json.load(open(os.path.join(HERE, "materials", "hourly.json")))["h_nT"]
check("hourly.json re-derived from the minute file (1,464 values)", len(hj) == 1464 and all(abs(a - round(b, 2)) < 1e-9 for a, b in zip(hj, rows)))
plan = json.load(open(os.path.join(HERE, "plan.json")))
check("six makers per cell", sorted(p["cell"] for p in plan) == ["N"] * 6 + ["T"] * 6)
TOLD = "It is a record of the water level in a tidal harbour. "
for p in plan:
    b = open(os.path.join(HERE, "briefs", "run", p["maker"] + ".md"), encoding="utf-8").read()
    base = open(os.path.join(HERE, "briefs", "BRIEF.md"), encoding="utf-8").read()
    pth = "/tmp/claude-0/s128/mk/%s" % p["maker"]
    exp = base.replace("{FOLDER}", pth + "/work").replace("{SCRATCH}", pth + "/scratch").replace("{TOLD}", TOLD if p["cell"] == "T" else "").replace(
        "{NOTTOLD}", "You are not told where or when." if p["cell"] == "T" else "You are not told what was measured, where or when.")
    check("brief %s is the template for cell %s" % (p["maker"], p["cell"]), b == exp)
    check("work, note and report of %s committed" % p["maker"], all(os.path.exists(os.path.join(HERE, *x)) for x in
          (("makers", p["maker"], "index.html"), ("makers", p["maker"], "NOTE.md"), ("reports", p["maker"] + ".md"))))
# git order: predictions, plan and briefs committed before the first report or maker file
def first(path): return git("log", "--diff-filter=A", "--format=%ct %h", "--", os.path.join(REL, path)).splitlines()[-1].split()
pr = first("PREDICTIONS.md"); check("PREDICTIONS.md first committed in 80bdac4", pr[1].startswith("80bdac4"))
for path in ["reports/m%02d.md" % i for i in range(1, 13)] + ["coder/B/answers.json", "results.json"]:
    f = first(path); check("%s added after the predictions (%s > %s)" % (path, f[1], pr[1]), int(f[0]) >= int(pr[0]) and f[1] != pr[1])
check("PREDICTIONS.md unchanged since 80bdac4", git("log", "--format=%h", "--", os.path.join(REL, "PREDICTIONS.md")).splitlines() == [pr[1]])
# the scoring re-runs to the committed results
before = open(os.path.join(HERE, "results.json")).read()
subprocess.run([sys.executable, os.path.join(HERE, "score.py")], capture_output=True, check=True)
check("score.py reproduces results.json", open(os.path.join(HERE, "results.json")).read() == before)
R = json.loads(before)
check("S125.GIVENKIND falsified by (b): 6 rejected, 0 bent", R["S125.GIVENKIND"]["rejected"] == 6 and R["S125.GIVENKIND"]["bent"] == 0)
check("S126.SELECT holds (0 and 0)", R["S126.SELECT"]["verdict"] == "holds")
check("S124.TABLE holds by its letter on four holders", R["S124.TABLE"]["verdict"] == "holds" and len(R["S124.TABLE"]["holders_of_only_the_day"]) == 4)
check("four of nine predictions held", R["predictions_held"] == 4)
fd = open(os.path.join(HERE, "face-data.js")).read()
subprocess.run([sys.executable, os.path.join(HERE, "facedata.py")], capture_output=True, check=True)
check("facedata.py reproduces face-data.js", open(os.path.join(HERE, "face-data.js")).read() == fd)
print("%d of %d checks" % (ok, ok + fail)); sys.exit(1 if fail else 0)
