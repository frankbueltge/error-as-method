"""verify.py: re-derives tonight's evidence and checks the order of commits. Run from anywhere:
python3 works/2026-10-17-told-where/verify.py"""
import hashlib, json, os, subprocess, csv, collections, datetime as dt
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
    return a != b and subprocess.call(["git", "-C", TOP, "merge-base", "--is-ancestor", a, b]) == 0
man = json.load(open(os.path.join(HERE, "sources", "MANIFEST.json")))
check("61 raw daily files hashed in the manifest", len(man["files"]) == 61 and man["header"][1].split()[:3] == ["48.31", "-105.10", "634"])
acc = collections.defaultdict(list); rows = 0
for r in csv.DictReader(open(os.path.join(HERE, "sources", "fpk_dwsolar_1min_20250715_20250913.csv"))):
    rows += 1; t = dt.datetime(int(r["year"]), int(r["month"]), int(r["day"]), int(r["hour"]), int(r["min"])) - dt.timedelta(minutes=1)
    if int(r["qc_dwsolar"]) == 0 and float(r["dw_solar_wm2"]) > -9000: acc[t.replace(minute=0)].append(float(r["dw_solar_wm2"]))
hv = [sum(acc[h]) / len(acc[h]) for h in (dt.datetime(2025, 7, 15) + dt.timedelta(hours=i) for i in range(1464))]
hj = json.load(open(os.path.join(HERE, "materials", "hourly.json")))["dw_solar_wm2"]
check("hourly.json re-derived (87,840 one-minute rows -> 1,464 hourly means of QC-0 minutes)", rows == 87840 and len(hj) == 1464 and all(abs(a - round(b, 2)) < 1e-9 for a, b in zip(hj, hv)))
check("brightest hour below 1,000 W/m2 once the flagged fault is left out", max(hj) < 1000)
plan = json.load(open(os.path.join(HERE, "plan.json")))
check("six makers per cell", sorted(p["cell"] for p in plan["makers"]) == ["K"] * 6 + ["KP"] * 6 + ["N"] * 6 + ["P"] * 6)
KIND = "It is a record of the sunlight reaching the ground: the solar radiation falling on a level surface."
PL = "It was recorded at a station called Fort Peck, in north-eastern Montana, USA, 634 metres above sea level."
for p in plan["makers"]:
    t = open(os.path.join(HERE, "briefs", "run", p["maker"] + ".md"), encoding="utf-8").read()
    check("brief %s carries exactly its cell's sentences" % p["maker"], (KIND in t) == ("K" in p["cell"]) and (PL in t) == ("P" in p["cell"]))
pre, _ = first("PREDICTIONS.md"); h0, _ = first("coder/H0/answers.json"); crit, _ = first("coder/H0/CRITERION.md")
check("H0's criterion committed before its answers", before(crit, h0))
check("H0's test committed before any report", all(before(h0, first("reports/m%02d.md" % i)[0]) for i in range(1, 25)))
for m in ["m%02d" % i for i in range(1, 25)]:
    r, _ = first("reports/%s.md" % m)
    check("report %s committed after the predictions" % m, r is not None and before(pre, r))
    check("work %s present" % m, os.path.exists(os.path.join(HERE, "makers", m, "index.html")) and os.path.exists(os.path.join(HERE, "makers", m, "NOTE.md")))
ch, _ = first("coder/H/answers.json"); cd, _ = first("coder/D/answers.json"); sc, _ = first("score.py"); r24, _ = first("reports/m24.md")
check("coders' answers committed after every report", before(r24, ch) and before(r24, cd))
check("score.py committed before the coders' answers", before(sc, ch) and before(sc, cd))
res = json.load(open(os.path.join(HERE, "results.json")))
subprocess.check_call(["python3", os.path.join(HERE, "score.py")], stdout=subprocess.DEVNULL)
check("score.py reproduces results.json", json.load(open(os.path.join(HERE, "results.json"))) == res)
c = res["counts"]
check("all 24 favour sunlight", all(c[k]["favours_light"] == 6 for k in c))
check("S132.CHECKABLE void by its letter (3 of 6 P makers name the place in text)", res["S132.CHECKABLE"]["verdict"] == "void" and res["S132.CHECKABLE"]["P_mentioning"] == 3)
check("the place on 12 of 12 told pages and 0 of 12 untold", c["P"]["page_place"] + c["KP"]["page_place"] == 12 and c["N"]["page_place"] + c["K"]["page_place"] == 0)
check("the kind held apart by 1 of 12 told it", c["K"]["holds_kind_apart"] + c["KP"]["holds_kind_apart"] == 1)
check("5 of 9 predictions held", res["predictions_held"] == "5 of 9")
print("\n%d of %d" % (ok, ok + fail))
