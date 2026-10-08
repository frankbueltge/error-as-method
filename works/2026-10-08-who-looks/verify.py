"""verify.py -- re-runnable checks for Who Looks. Exit 1 on any failure."""
import hashlib, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); fails = []
def check(ok, what): print(("ok   " if ok else "FAIL ") + what); ok or fails.append(what)
J = lambda *p: json.load(open(os.path.join(HERE, *p)))
sha = lambda p: hashlib.sha256(open(os.path.join(HERE, p), "rb").read()).hexdigest()
check(sha("sources/wikidata-meteorites-mass.json") == "698df4bbfe04be10a3ba38dca7866ef62605d8fa743e78c2b036bd6e2e7254d2", "source hash")
P = J("plan.json")
check(P["items"] == 568 and P["dropped_unit"] == ["Q103875199"], "568 items; one dropped for an ambiguous unit")
plan = P["plan"]
check(sorted(p["arm"] for p in plan) == ["N"] * 4 + ["O"] * 4 + ["R"] * 4, "4 N, 4 O, 4 R")
for p in plan:
    m, a = p["maker"], p["arm"]
    check(all(os.path.exists(os.path.join(HERE, x)) for x in ["makers/%s/index.html" % m, "makers/%s/NOTE.md" % m, "reports/%s.md" % m, "shots/%s.png" % m, "briefs/run/%s.md" % m]), m + ": work, note, report, shot, brief")
    b = open(os.path.join(HERE, "briefs", "run", m + ".md")).read()
    check(("viewer" in b) == (a != "N") and ("at least once" in b) == (a == "R") and ("as often or as little" in b) == (a == "O"), m + ": brief matches arm " + a)
    check(hashlib.sha256(b.encode()).hexdigest() == p["brief_sha256"], m + ": brief hash")
    check(sha("makers/%s/data.js" % m) == p["data_sha256"], m + ": data.js unchanged")
    check(os.path.exists(os.path.join(HERE, "makers", m, "renders")) == (a != "N"), m + ": renders exist only where a viewer was given")
check(all(sha("render.js") == hashlib.sha256(open(os.path.join(os.path.dirname(p["folder"]), "viewer", "render.js"), "rb").read()).hexdigest() for p in plan if p["arm"] != "N") if os.path.exists(os.path.dirname(plan[0]["folder"])) else True, "viewer byte-identical for O and R (when the scratch tree exists)")
def added(path):
    o = subprocess.run(["git", "log", "--diff-filter=A", "--format=%ct", "--", path], cwd=HERE, capture_output=True, text=True).stdout.split()
    return int(o[-1]) if o else None
seq = ["PREDICTIONS.md", "makers/m04/index.html", "makers/m08/index.html", "coder1/key.json", "coder1/ratings.json", "coder2/ratings.json", "open.json", "results.json"]
ts = [added(p) for p in seq]
check(all(ts), "every staged file has an adding commit")
if all(ts):
    check(ts == sorted(ts), "git order: predictions < first maker < last maker < masks < coder 1 < coder 2 < open coding < scores")
subprocess.run([sys.executable, os.path.join(HERE, "looks.py")], capture_output=True)
subprocess.run([sys.executable, os.path.join(HERE, "score.py")], capture_output=True)
r = J("results.json")
check(r["held"] == ["P1", "P2", "P4", "P7", "P8"], "score.py reproduces: P1, P2, P4, P7, P8 held; P3, P5, P6 failed")
check(r["posthoc"]["every_look_but_the_last_followed_by_change"] and r["posthoc"]["final_equals_last_look"], "every look but the last was followed by a change; every final is its last look")
print(f"{len(fails)} failed"); sys.exit(1 if fails else 0)
