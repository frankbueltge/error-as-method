"""verify.py -- re-runnable checks for Customary Lines. Exit 1 on any failure."""
import hashlib, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); fails = []
def check(ok, what): print(("ok   " if ok else "FAIL ") + what); ok or fails.append(what)
J = lambda *p: json.load(open(os.path.join(HERE, *p)))
check(hashlib.sha256(open(os.path.join(HERE, "sources", "moon-2025.json"), "rb").read()).hexdigest()
      == "30d4fa685949f66921428446796f324d2c07cbeb39638c8851927006a2e02328", "source hash")
items = J("sources", "moon-2025.json")["items"]; v = [i["views"] for i in items]
check(len(v) == 365 and max(v) == 17284 and items[v.index(17284)]["timestamp"].startswith("20250907"), "365 days, peak 17,284 on 7 Sep")
plan = J("plan.json")
check([p["arm"] for p in plan].count("R") == 6 and all([p["arm"] for p in plan].count(a) == 4 for a in "DBC"), "6 R, 4 D, 4 B, 4 C")
for p in plan:
    m = p["maker"]
    check(all(os.path.exists(os.path.join(HERE, d, f)) for d, f in
              [("makers/" + m, "index.html"), ("makers/" + m, "NOTE.md"), ("reports", m + ".md"), ("shots", m + ".png"), ("briefs/run", m + ".md")]),
          m + ": work, note, report, shot, brief present")
    b = open(os.path.join(HERE, "briefs", "run", m + ".md")).read()
    check(("others/" in b) == (p["arm"] in "BC") and ("none of them" in b) == (p["arm"] == "C"), m + ": brief matches arm " + p["arm"])
key = J("coder", "key.json")
check(sorted(k["maker"] for k in key.values()) == ["m%02d" % i for i in range(7, 19)], "coder key covers round 2 exactly")
def commit_of(path):
    return subprocess.run(["git", "log", "--diff-filter=A", "--format=%ct %h", "--", path], cwd=HERE, capture_output=True, text=True).stdout.split()
order = [("PREDICTIONS.md",), ("makers/m01/index.html",), ("briefs/run/m07.md",), ("makers/m07/index.html",), ("coder/key.json",), ("coder/ratings.json",), ("open.json",)]
ts = [commit_of(p[0]) for p in order]
check(all(ts), "every staged file has an adding commit")
if all(ts):
    t = [int(x[0]) for x in ts]
    check(t == sorted(t), "git order: predictions < round 1 < round-2 briefs < round 2 < mask < ratings < open coding")
r = subprocess.run([sys.executable, os.path.join(HERE, "score.py")], capture_output=True, text=True).stdout
check(r.count("HELD") == 7 and "P5 FAILED" in r, "score.py reproduces: seven held, P5 failed")
print(f"{len(fails)} failed"); sys.exit(1 if fails else 0)
