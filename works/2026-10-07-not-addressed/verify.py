"""verify.py -- checks for Not Addressed. Run from anywhere: python3 verify.py"""
import hashlib, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REL = "works/2026-10-07-not-addressed"
ok = True
def check(name, cond):
    global ok; ok &= bool(cond); print(("ok  " if cond else "FAIL"), name)
def first_commit(path):
    out = subprocess.run(["git", "log", "--diff-filter=A", "--format=%H %ct", "--", f"{REL}/{path}"],
                         cwd=HERE, capture_output=True, text=True).stdout.split()
    return int(out[-1]) if out else None
def order(path):  # topological position: number of commits that are ancestors
    h = subprocess.run(["git", "log", "--diff-filter=A", "--format=%H", "--", f"{REL}/{path}"], cwd=HERE, capture_output=True, text=True).stdout.split()
    return int(subprocess.run(["git", "rev-list", "--count", h[-1]], cwd=HERE, capture_output=True, text=True).stdout) if h else None
src = os.path.join(HERE, "sources", "fremont-2025.json")
check("source hash as recorded", hashlib.sha256(open(src, "rb").read()).hexdigest() == "d82accb00130a294775acac069e9cca58ebcaffa6618c063d1bd37390c206d20")
check("8760 hours in the source", len(json.load(open(src))) == 8760)
plan = json.load(open(os.path.join(HERE, "plan.json")))
check("12 makers, 2 per condition", sorted(p["condition"] for p in plan) == sorted("AABBCCDDEEFF"))
for p in plan:
    d = open(os.path.join(HERE, "makers", p["maker"], "data.js"), "rb").read()
    check(f"{p['maker']} data.js is the bytes laid out for condition {p['condition']}", hashlib.sha256(d).hexdigest() == p["data_sha256"])
    check(f"{p['maker']} orchard.txt present iff D", os.path.exists(os.path.join(HERE, "makers", p["maker"], "orchard.txt")) == (p["condition"] == "D"))
    brief = open(os.path.join(HERE, "briefs", "run", p["maker"] + ".md")).read()
    check(f"{p['maker']} brief names the title iff F", ("title is *Orchard*" in brief) == (p["condition"] == "F"))
pre, mk, rt, oc = order("PREDICTIONS.md"), order("makers/m01/index.html"), order("coder/ratings.json"), order("open.json")
check("pre-registration committed before the makers' files", pre is not None and mk is not None and pre < mk)
check("masked pictures committed before the ratings", order("coder/pictures/p01.png") < rt)
check("open coding committed after the ratings", oc is None or rt < oc)
before = open(os.path.join(HERE, "results.json")).read()
subprocess.run([sys.executable, os.path.join(HERE, "score.py")], capture_output=True)
check("score.py reproduces results.json", open(os.path.join(HERE, "results.json")).read() == before)
r = json.loads(before)
check("no take of the word in B-E", sum(r["takes_by_condition"][c] for c in "BCDE") == 0)
check("both F makers took it", r["takes_by_condition"]["F"] == 2)
print("ALL OK" if ok else "SOME CHECKS FAILED"); sys.exit(0 if ok else 1)
