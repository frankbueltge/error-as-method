"""verify.py: checks that this experiment's record says what it claims. Run from anywhere: python3 verify.py
- every source file matches its manifest hash;
- the git order: predictions, briefs, coders' briefs, mask and plan committed before any maker's report; all reports,
  then coder A's key, then its answers; all reports before coder B's answers; score.py before either coder answered;
- every maker's work has index.html and NOTE.md; every shot is still and loads nothing; the two pages that throw an
  error are exactly the two the record names (F-226);
- score.py reproduces results.json; work.md ends with its project paragraph."""
import hashlib, json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); ok = fail = 0
def check(c, what):
    global ok, fail
    ok += bool(c); fail += (not c); print(("PASS " if c else "FAIL ") + what)
for man in json.load(open(os.path.join(H, "sources", "MANIFEST.json"))):
    check(hashlib.sha256(open(os.path.join(H, "sources", man["file"]), "rb").read()).hexdigest() == man["sha256"], man["file"] + " matches its SHA-256")
plan = json.load(open(os.path.join(H, "plan.json")))
check(sorted(p["cell"] for p in plan) == sorted(["F", "U", "X"] * 4), "four makers per cell")
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
erred = set()
for line in open(os.path.join(H, "shots.log")):            # summarised lines: maker mask textcalls bytes [errors] [requests] [w, h] still
    f = line.strip().split(" ", 4)
    if len(f) < 5: continue
    m, mask, rest = f[0], f[1] == "True", f[4]
    check(rest.endswith("[1100, 800] True") and "] [] [1100" in rest, "%s%s: still, no requests, no scroll" % (m, " (masked)" if mask else ""))
    if not rest.startswith("[]"): erred.add(m)
check(erred == {"m05", "m12"}, "the pages that throw are m05 and m12, as F-226 says")
before = json.load(open(os.path.join(H, "results.json")))
subprocess.run([sys.executable, os.path.join(H, "score.py")], capture_output=True)
check(json.load(open(os.path.join(H, "results.json"))) == before, "score.py reproduces results.json")
words = open(os.path.join(H, "work.md"), encoding="utf-8").read()
check("## What this taught the project" in words, "work.md ends with its project paragraph")
print("%d of %d checks pass" % (ok, ok + fail)); sys.exit(1 if fail else 0)
