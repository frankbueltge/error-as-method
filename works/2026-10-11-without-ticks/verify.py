"""verify.py -- re-runs prepare/score/ledger checks and the git order of the night. Run from anywhere:
python3 verify.py. Each check prints PASS or FAIL."""
import hashlib, json, os, subprocess
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.relpath(H, subprocess.check_output(["git", "-C", H, "rev-parse", "--show-toplevel"], text=True).strip())
ok = []
def check(name, cond): ok.append(bool(cond)); print("PASS" if cond else "FAIL", name)
def first(path):  # first commit that added path
    out = subprocess.check_output(["git", "-C", H, "log", "--diff-filter=A", "--format=%ct %h", "--", ":(top)" + path], text=True).split("\n")
    out = [x for x in out if x]; return int(out[-1].split()[0]) if out else None
src = open(os.path.join(H, "sources", "US_births_2000-2014_SSA.csv"), "rb").read()
check("source hash matches manifest", hashlib.sha256(src).hexdigest() == json.load(open(os.path.join(H, "sources", "MANIFEST.json")))[0]["sha256"])
check("births.csv is the source, unchanged", open(os.path.join(H, "materials", "births.csv"), "rb").read() == src)
plan = json.load(open(os.path.join(H, "plan.json")))
check("4 makers per arm", all(sum(p["arm"] == a for p in plan) == 4 for a in "TIL"))
for p in plan:
    b = open(os.path.join(H, "briefs", "run", p["maker"] + ".md"), encoding="utf-8").read()
    check("brief %s names its own file and folders" % p["maker"], p["file"] in b and p["folder"] in b and p["scratch"] in b)
t_pred = first(os.path.join(W, "PREDICTIONS.md")); t_rep = first(os.path.join(W, "reports", "m05.md"))
t_coderbrief = first(os.path.join(W, "coder", "BRIEF.md")); t_keys = first(os.path.join(W, "keys", "coder.json"))
t_ans = first(os.path.join(W, "coder", "answers.json")); t_led = first(os.path.join(W, "ledger.py"))
check("predictions committed before the first report", t_pred and t_rep and t_pred <= t_rep)
check("coder brief committed before the first report", t_coderbrief and t_coderbrief <= t_rep)
check("masked shots and key committed before the coder's answers", t_keys and t_ans and t_keys <= t_ans)
check("M1 ledger committed after the coder's answers", t_led and t_led >= t_ans)
before = json.load(open(os.path.join(H, "results.json")))
subprocess.run(["python3", os.path.join(H, "score.py")], capture_output=True, check=True)
check("score.py reproduces results.json", json.load(open(os.path.join(H, "results.json"))) == before)
res = {k: v["held"] for k, v in before.items()}
check("verdicts as reported: P1 P3 P4 P6 P8 held; P2 P5 P7 failed", res == {"P1": True, "P2": False, "P3": True, "P4": True, "P5": False, "P6": True, "P7": False, "P8": True})
for p in plan:
    check("page and note collected for " + p["maker"], all(os.path.exists(os.path.join(H, "makers", p["maker"], f)) for f in ("index.html", "NOTE.md")))
print("%d of %d checks pass" % (sum(ok), len(ok)))
