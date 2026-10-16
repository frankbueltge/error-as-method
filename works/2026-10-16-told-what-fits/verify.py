"""verify.py: re-derives tonight's evidence and checks the order of commits. Run from anywhere:
python3 works/2026-10-16-told-what-fits/verify.py"""
import hashlib, json, os, subprocess, csv
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
def before(a, b):
    return subprocess.call(["git", "-C", TOP, "merge-base", "--is-ancestor", a, b]) == 0
for e in json.load(open(os.path.join(HERE, "sources", "MANIFEST.json"))):
    b = open(os.path.join(HERE, "sources", e["file"]), "rb").read()
    check("source hash " + e["file"], hashlib.sha256(b).hexdigest() == e["sha256"] and len(b) == e["bytes"])
raw = list(csv.DictReader(open(os.path.join(HERE, "sources", "pfynwald_1548_src_10min_20240709_20240907.csv"))))
hv = [sum(float(r["value_um"]) for r in raw[i:i + 6]) / 6 for i in range(0, 8784, 6)]
hj = json.load(open(os.path.join(HERE, "materials", "hourly.json")))["stem_radius_change_um"]
check("hourly.json re-derived (8,784 ten-minute rows -> 1,464 hourly means)", len(raw) == 8784 and len(hj) == 1464 and all(abs(a - round(b, 3)) < 1e-9 for a, b in zip(hj, hv)))
plan = json.load(open(os.path.join(HERE, "plan.json")))
check("six makers per cell", sorted(p["cell"] for p in plan["makers"]) == ["C"] * 6 + ["N"] * 6 + ["T"] * 6)
TOLD = {"N": None, "T": "It is a record of the radius of a tree's trunk, measured at one point on its bark.",
        "C": "It is a record of the carbon dioxide content of the air at a measuring station."}
for p in plan["makers"]:
    t = open(os.path.join(HERE, "briefs", "run", p["maker"] + ".md"), encoding="utf-8").read()
    want = TOLD[p["cell"]]
    check("brief %s carries only its cell's sentence" % p["maker"],
          (want in t if want else "You are not told what was measured" in t) and all((s not in t) for c, s in TOLD.items() if s and c != p["cell"]))
pre, _ = first("PREDICTIONS.md")
for m in ["m%02d" % i for i in range(1, 19)]:
    r, _ = first("reports/%s.md" % m)
    check("report %s committed after the predictions" % m, r is not None and before(pre, r) and pre != r)
    check("work %s present" % m, os.path.exists(os.path.join(HERE, "makers", m, "index.html")) and os.path.exists(os.path.join(HERE, "makers", m, "NOTE.md")))
cb, _ = first("coder/B/answers.json"); r18, _ = first("reports/m18.md")
check("coder B's answers committed after every report", before(r18, cb) and r18 != cb)
res = json.load(open(os.path.join(HERE, "results.json")))
subprocess.check_call(["python3", os.path.join(HERE, "score.py")], stdout=subprocess.DEVNULL)
check("score.py reproduces results.json", json.load(open(os.path.join(HERE, "results.json"))) == res)
check("S130.SOURCE holds", res["S130.SOURCE"]["verdict"] == "holds")
check("9 of 12 predictions held", res["predictions_held"] == 9)
check("told the false carbon dioxide: 6 of 6 keep it, 0 say they were told, 0 doubt it",
      res["counts"]["C5"]["C"]["carbon"] == 6 and res["counts"]["C11_said_told"]["C"] == 0 and res["counts"]["C7_yes"]["C"] == 0)
check("told the true tree: 6 of 6 keep it, 0 say they were told", res["counts"]["C5"]["T"]["tree"] == 6 and res["counts"]["C11_said_told"]["T"] == 0)
check("one untold maker reached the tree (m06)", [m for m in res["cells"]["N"] if res["per_maker"][m]["C5"] == "tree"] == ["m06"])
print("\n%d of %d" % (ok, ok + fail))
