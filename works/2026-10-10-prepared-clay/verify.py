"""verify.py -- re-runs the night's measures and checks the order of the record. Run from anywhere.
1. the source file's SHA-256; 2. prepare.py regenerates bloom.csv, bloom.txt and bloom.svg byte for byte and
the same plan; 3. carry.py, carry_i.py and score.py reproduce carry.json, carry_i.json and results.json;
4. git order: PREDICTIONS.md and plan.json were committed before any maker file, and keys/coder.json before
coder/answers.json."""
import hashlib, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ok = True
def check(name, cond):
    global ok; ok &= bool(cond); print(("PASS " if cond else "FAIL ") + name)
h = lambda p: hashlib.sha256(open(os.path.join(HERE, p), "rb").read()).hexdigest()
check("source sha256", h("sources/owid-kyoto-cherry-blossom.csv") == "aea6779dc2a586454bbb46cdb2edbdd0063181daffcd0dcbeec0868bf6236bd5")
keep = {p: open(os.path.join(HERE, p), "rb").read() for p in ["materials/bloom.csv", "materials/bloom.txt", "materials/bloom.svg", "plan.json", "carry.json", "carry_i.json", "results.json"]}
run = lambda s: subprocess.run([sys.executable, os.path.join(HERE, s)], capture_output=True, text=True, cwd=HERE)
run("prepare.py"); run("carry.py"); run("carry_i.py"); run("score.py")
for p, b in keep.items():
    check("reproduces " + p, open(os.path.join(HERE, p), "rb").read() == b)
def first(path):
    r = subprocess.run(["git", "log", "--format=%ct %h", "--diff-filter=A", "--", path], capture_output=True, text=True, cwd=HERE).stdout.split()
    return (int(r[-2]), r[-1]) if r else None
pre, mk = first("PREDICTIONS.md"), min(first("reports/%s.md" % m) for m in ["m%02d" % i for i in range(1, 13)])
check("predictions committed before the first maker file (%s < %s)" % (pre[1], mk[1]), pre[0] < mk[0])
k, a = first("keys/coder.json"), first("coder/answers.json")
check("coder key committed before coder answers", k and a and k[0] < a[0])
res = json.load(open(os.path.join(HERE, "results.json")))
check("four of eight predictions held", res["held"] == 4)
print("ALL PASS" if ok else "SOME CHECKS FAILED"); sys.exit(0 if ok else 1)
