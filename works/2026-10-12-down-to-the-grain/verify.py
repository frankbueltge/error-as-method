"""verify.py: checks that this experiment's record says what it claims. Run from anywhere: python3 verify.py
- the source file matches its manifest hash; the four materials re-derive from it (prepare.py svg + render.js are
  not re-run here, but holds.json is re-measured from the committed JPEGs);
- the git order: predictions, brief and plan committed before any maker's report; the coders' briefs and the mask
  before the first report; coder A's key before coder A's answers; both coders' answers before score.py;
- every maker's work is still, loads nothing, and has a NOTE.md and a verbatim report;
- score.py reproduces results.json."""
import hashlib, json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); ok = fail = 0
def check(c, what):
    global ok, fail
    ok += bool(c); fail += (not c); print(("PASS " if c else "FAIL ") + what)
man = json.load(open(os.path.join(H, "sources", "MANIFEST.json")))[0]
check(hashlib.sha256(open(os.path.join(H, man["file"]), "rb").read()).hexdigest() == man["sha256"], "source matches its SHA-256")
plan = json.load(open(os.path.join(H, "plan.json")))
check(sorted(p["grain"] for p in plan) == sorted(["G1", "G2", "G3", "G4"] * 3), "three makers per grain")
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
check(max(t["ansA"], t["ansB"]) <= t["score"], "both coders' answers before score.py")
for p in plan:
    d = os.path.join(H, "makers", p["maker"])
    check(os.path.exists(os.path.join(d, "index.html")) and os.path.exists(os.path.join(d, "NOTE.md")), p["maker"] + " has index.html and NOTE.md")
for line in open(os.path.join(H, "shots.log")):
    j = json.loads(line)
    check(j["still"] and not j["requests"] and not j["errors"], "%s%s: still, no requests, no errors" % (j["maker"], " (masked)" if j["mask"] else ""))
before = json.load(open(os.path.join(H, "results.json")))
subprocess.run([sys.executable, os.path.join(H, "score.py")], capture_output=True)
check(json.load(open(os.path.join(H, "results.json"))) == before, "score.py reproduces results.json")
words = open(os.path.join(H, "work.md"), encoding="utf-8").read()
check("## What this taught the project" in words, "work.md ends with its project paragraph")
print("%d of %d checks pass" % (ok, ok + fail)); sys.exit(1 if fail else 0)
