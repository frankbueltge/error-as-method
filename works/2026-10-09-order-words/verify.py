"""verify.py -- re-runs the night's mechanical steps and checks the record's order in git.

python3 verify.py     (from anywhere; exits non-zero on any failed check)
"""
import json, os, subprocess, hashlib, sys
H = os.path.dirname(os.path.abspath(__file__)); REL = "works/2026-10-09-order-words"
ok = True
def check(c, what):
    global ok; print(("ok   " if c else "FAIL ") + what); ok &= bool(c)
man = json.load(open(os.path.join(H, "sources", "MANIFEST.json")))
body = open(os.path.join(H, "sources", "root-zone.json"), "rb").read()
check(hashlib.sha256(body).hexdigest() == man[1]["sha256"], "root-zone.json matches its manifest hash")
check(len(json.loads(body)) == 1595 == man[0]["rows"], "1,595 domains")
plan = json.load(open(os.path.join(H, "plan.json")))["plan"]
check(sorted(p["return"] for p in plan) == list("HHHHSSSSXXXX"), "four makers per return")
check(all(p["notes_from"] != p["maker"] for p in plan if p["return"] == "X"), "no X maker got its own notes")
before = open(os.path.join(H, "results.json")).read()
subprocess.run([sys.executable, os.path.join(H, "score.py")], capture_output=True, check=True)
check(open(os.path.join(H, "results.json")).read() == before, "score.py reproduces results.json")
def first(path):
    out = subprocess.run(["git", "log", "--diff-filter=A", "--format=%ct %h", "--", REL + "/" + path], cwd=os.path.dirname(os.path.dirname(H)), capture_output=True, text=True).stdout.split()
    return int(out[-2]) if out else None
pre = first("PREDICTIONS.md")
check(pre is not None and all((first("reports/%s-first.md" % p["maker"]) or 0) >= pre for p in plan), "PREDICTIONS.md committed before every first report")
na = first("coderA/notes-as-returned.json")
check(all((first("reports/%s-second.md" % p["maker"]) or 0) >= na for p in plan), "coder A's notes committed before every second report")
for c in ("b", "c"):
    check(first("keys/coder-%s.json" % c) <= first("coder%s/answers-as-returned.json" % c.upper()), "coder %s key committed before its answers" % c.upper())
check(first("open.json") >= first("coderC/answers-as-returned.json") and first("open.json") >= first("coderB/answers-as-returned.json"), "open coding committed after both coders")
sys.exit(0 if ok else 1)
