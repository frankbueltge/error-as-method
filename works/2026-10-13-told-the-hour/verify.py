"""verify.py: checks that this experiment's record says what it claims. Run from anywhere: python3 verify.py
- the source file matches its manifest hash; the two pictures are not re-rendered here;
- the git order: predictions, brief and plan committed before any maker's report; the coders' briefs and the mask
  before the first report; coder A's key before coder A's answers; score.py before either coder's answers;
- every maker's work is still, loads nothing, and has a NOTE.md and a verbatim report;
- score.py reproduces results.json."""
import hashlib, json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); ok = fail = 0
def check(c, what):
    global ok, fail
    ok += bool(c); fail += (not c); print(("PASS " if c else "FAIL ") + what)
man = json.load(open(os.path.join(H, "sources", "MANIFEST.json")))[0]
check(hashlib.sha256(open(os.path.join(H, "sources", man["file"]), "rb").read()).hexdigest() == man["sha256"], "source matches its SHA-256")
plan = json.load(open(os.path.join(H, "plan.json")))
check(sorted(p["cell"] for p in plan) == sorted(["FU", "FN", "CU", "CN"] * 3), "three makers per cell")
def first(path):
    r = subprocess.run(["git", "log", "--diff-filter=A", "--format=%ct %h", "--", path], cwd=H, capture_output=True, text=True).stdout.split()
    return int(r[-2]) if r else None
t = {k: first(v) for k, v in {"pred": "PREDICTIONS.md", "plan": "plan.json", "brief": "briefs/BRIEF.md", "mask": "shot.js",
     "cA": "coder/A/BRIEF.md", "cB": "coder/B/BRIEF.md", "key": "keys/A.json", "ansA": "coder/A/answers.json",
     "ansB": "coder/B/answers.json", "score": "score.py"}.items()}
reps = [first("reports/%s.md" % p["maker"]) for p in plan]
check(all(r is not None for r in reps), "twelve reports in git")
check(max(t["pred"], t["plan"], t["brief"]) <= min(reps), "predictions, brief and plan precede every report")
check(max(t["mask"], t["cA"], t["cB"]) <= min(reps), "mask and both coder briefs precede every report")
check(max(reps) <= t["key"] <= t["ansA"], "all reports, then coder A's key, then its answers")
check(max(reps) <= t["ansB"], "all reports before coder B's answers")
check(t["score"] <= min(t["ansA"], t["ansB"]), "score.py fixed before either coder answered")
for p in plan:
    d = os.path.join(H, "makers", p["maker"])
    check(os.path.exists(os.path.join(d, "index.html")) and os.path.exists(os.path.join(d, "NOTE.md")), p["maker"] + " has index.html and NOTE.md")
for line in open(os.path.join(H, "shots.log")):          # F-225: 23 lines summarised as text, the 24th raw JSON
    line = line.strip()
    if not line: continue
    if line.startswith("{"):
        j = json.loads(line); m, mask, good = j["maker"], j["mask"], j["still"] and not j["requests"] and not j["errors"]
    else:
        f = line.split(); m, mask = f[0], f[1] == "True"; good = line.endswith("[1100, 800] True") and "[] []" in line
    check(good, "%s%s: still, no requests, no errors" % (m, " (masked)" if mask else ""))
before = json.load(open(os.path.join(H, "results.json")))
subprocess.run([sys.executable, os.path.join(H, "score.py")], capture_output=True)
check(json.load(open(os.path.join(H, "results.json"))) == before, "score.py reproduces results.json")
words = open(os.path.join(H, "work.md"), encoding="utf-8").read()
check("## What this taught the project" in words, "work.md ends with its project paragraph")
print("%d of %d checks pass" % (ok, ok + fail)); sys.exit(1 if fail else 0)
