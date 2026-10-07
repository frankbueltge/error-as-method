"""verify.py: re-checks What Passes. Run from this directory; exits 1 on any failure.
  carried files byte-identical with Unheard's; material hash; git order (pre-registration before
  material, material before outputs, readings in the drawn order, home.json after the last reading);
  home.json and results.json reproduce; the face's JS adapters write the WAVs' samples (if node)."""
import hashlib, json, subprocess, sys, os
ok = 0; bad = 0
def check(name, cond):
    global ok, bad
    print(("PASS " if cond else "FAIL ") + name); ok += bool(cond); bad += (not cond)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
here = os.path.dirname(os.path.abspath(__file__)); os.chdir(here)
for k, v in json.load(open("carried/CARRIED.json")).items():
    check(f"{k} identical with {v['copied_from']}", sha(k) == v["sha256"] == sha(os.path.join("../..", v["copied_from"])))
m = json.load(open("sources/MANIFEST.json"))
for f, v in m.items():
    check(f"material {f} hash", sha("sources/" + f) == v["sha256"])
def first_commit(path):
    out = subprocess.run(["git", "log", "--diff-filter=A", "--format=%H %ct", "--reverse", "--", path], capture_output=True, text=True).stdout.split()
    return out[0] if out else None
def before(a, b):
    ca, cb = first_commit(a), first_commit(b)
    if not ca or not cb: return False
    return subprocess.run(["git", "merge-base", "--is-ancestor", ca, cb]).returncode == 0 and ca != cb
seq = ["PREDICTIONS.md", "sources/merced-11264500-2026-04-01_07-31.rdb", "seen/A1-S.png",
       "readings/R-1-A1.md", "readings/R-2-A3.md", "readings/R-3-A6.md", "readings/R-4-A2.md",
       "readings/R-5-A5.md", "readings/R-6-A4.md", "home.json"]
for a, b in zip(seq, seq[1:]):
    check(f"git order: {a} before {b}", before(a, b))
for f in ["adapt.py", "home.py", "order.py", "run.sh"]:
    log = subprocess.run(["git", "log", "--format=%H", "--", f], capture_output=True, text=True).stdout.split()
    check(f"{f} unchanged since the pre-registration commit", len(log) == 1 and log[0] == first_commit("PREDICTIONS.md"))
check("reading order is seed 110's", subprocess.run([sys.executable, "order.py"], capture_output=True, text=True).stdout.split() == ["A1", "A3", "A6", "A2", "A5", "A4"])
h0, r0 = open("home.json").read(), open("results.json").read()
subprocess.run([sys.executable, "home.py"], capture_output=True); subprocess.run([sys.executable, "score.py"], capture_output=True)
check("home.json reproduces", open("home.json").read() == h0)
check("results.json reproduces", open("results.json").read() == r0)
r = json.loads(r0)
check("17 of 18 definite answers right", (r["right"], r["definite"]) == (17, 18))
check("24 of 30 forecast cells matched", r["forecast_hits"] == 24)
check("every forecast miss is on R4", all(c["forecast_hit"] or k.endswith("R4_irregular") for k, c in r["cells"].items()))
check("work.md ends with 'What this taught the project'", "## What this taught the project" in open("work.md").read())
if subprocess.run(["which", "node"], capture_output=True).returncode == 0:
    if not os.path.exists("out/A6.wav"):
        subprocess.run([sys.executable, "adapt.py", "sources/merced-11264500-2026-04-01_07-31.rdb"], capture_output=True)
    check("face adapters (adapters.js) write the WAVs' samples", subprocess.run(["node", "check_js.js"], capture_output=True).returncode == 0)
print(f"{ok} passed, {bad} failed"); sys.exit(1 if bad else 0)
