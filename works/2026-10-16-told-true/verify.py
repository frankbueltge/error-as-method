"""verify.py: re-derives tonight's evidence and checks the order of commits. Run from anywhere:
python3 works/2026-10-16-told-true/verify.py"""
import hashlib, json, os, subprocess, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
TOP = subprocess.check_output(["git", "-C", HERE, "rev-parse", "--show-toplevel"], text=True).strip()
REL = os.path.relpath(HERE, TOP)
ok = fail = 0
def check(name, cond):
    global ok, fail
    print(("ok   " if cond else "FAIL ") + name); ok += bool(cond); fail += (not cond)
def first(path):
    out = subprocess.check_output(["git", "-C", TOP, "log", "--diff-filter=A", "--format=%H %ct", "--", os.path.join(REL, path)], text=True).split()
    return (out[-2], int(out[-1])) if out else (None, None)
def before(a, b):  # commit a is an ancestor of (or equal to) commit b
    return subprocess.call(["git", "-C", TOP, "merge-base", "--is-ancestor", a, b]) == 0
for e in json.load(open(os.path.join(HERE, "sources", "MANIFEST.json"))):
    b = open(os.path.join(HERE, "sources", e["file"]), "rb").read()
    check("source hash " + e["file"], hashlib.sha256(b).hexdigest() == e["sha256"] and len(b) == e["bytes"])
V = {}
for line in open(os.path.join(HERE, "sources", "noaa_gml_co2_wbi_tower_hourly_20190715_20190913.txt")):
    if line.startswith("#") or line.startswith("site_code"): continue
    p = line.split()
    if float(p[18]) == 31.0 and p[-1][0] == ".": V[dt.datetime(int(p[1]), int(p[2]), int(p[3]), int(p[4]))] = float(p[10])
ts = [dt.datetime(2019, 7, 15) + dt.timedelta(hours=i) for i in range(1464)]
hj = json.load(open(os.path.join(HERE, "materials", "hourly.json")))["co2_ppm"]
check("hourly.json re-derived (1,464 values, 2 interpolated)", len(hj) == 1464 and sum(t not in V for t in ts) == 2 and
      all(abs(hj[i] - round(V[t], 3)) < 1e-9 for i, t in enumerate(ts) if t in V))
plan = json.load(open(os.path.join(HERE, "plan.json")))
check("six makers per cell", sorted(p["cell"] for p in plan["makers"]) == ["F"] * 6 + ["N"] * 6 + ["T"] * 6)
check("four inquirers per told brief", sorted(p["cell"] for p in plan["inquiry"]) == ["F"] * 4 + ["T"] * 4)
TOLD = {"N": None, "T": "It is a record of the carbon dioxide content of the air at a measuring station.",
        "F": "It is a record of the water level in a tidal harbour."}
for p in plan["makers"]:
    t = open(os.path.join(HERE, "briefs", "run", p["maker"] + ".md"), encoding="utf-8").read()
    want = TOLD[p["cell"]]
    check("brief %s carries only its cell's sentence" % p["maker"],
          (want in t if want else True) and all((s not in t) for c, s in TOLD.items() if s and c != p["cell"]))
pre, _ = first("PREDICTIONS.md"); ans, _ = first("inquiry/answers/q01.md"); qc, _ = first("coder/Q/answers.json")
check("predictions committed before the inquiry answers", before(pre, ans) and pre != ans)
check("inquiry answers committed before coder Q's coding", before(ans, qc) and ans != qc)
for m in ["m%02d" % i for i in range(1, 19)]:
    r, _ = first("reports/%s.md" % m)
    check("report %s committed after coder Q" % m, r is not None and before(qc, r) and qc != r)
    check("work %s present" % m, os.path.exists(os.path.join(HERE, "makers", m, "index.html")) and os.path.exists(os.path.join(HERE, "makers", m, "NOTE.md")))
res = json.load(open(os.path.join(HERE, "results.json")))
subprocess.check_call(["python3", os.path.join(HERE, "score.py")], stdout=subprocess.DEVNULL)
check("score.py reproduces results.json", json.load(open(os.path.join(HERE, "results.json"))) == res)
check("rows as reported", res["S128.SUBJECT"]["verdict"] == "holds" and res["S129.INQUIRY"]["verdict"] == "holds" and res["S128.SHAPE"]["verdict"] == "holds")
check("8 of 11 predictions held", res["predictions_held"] == 8)
check("told-true makers who say they were told: 0", res["counts"]["C10_yes"]["T"] == 0 and all(res["per_maker"][m]["C7"] == "n/a" for m in res["cells"]["T"]))
print("\n%d of %d" % (ok, ok + fail))
