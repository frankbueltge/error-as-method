"""make_packets.py <root> : Session 145. Renders c1..c4 and the 24 mutants with shoot.js (final.png), then builds
three blind packets under <root>/packets, shuffles seed 145:
  X: family/F1-F4 (c1-c4 shuffled), variants/V01-V24 (the mutants shuffled);
  W: W01-W28 (c1-c4 and the mutants, shuffled);   V: T01-T28 (the same 28, shuffled again).
Keys to coder/key.json, page errors to renders.json."""
import json, os, random, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(sys.argv[1]); SEED = 145
def shoot(page_dir, out):
    try: r = subprocess.run(["node", os.path.join(HERE, "shoot.js"), out, os.path.join(page_dir, "index.html")], capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:  # a page that never yields is shown as a blank 1100 x 800 picture (declared)
        subprocess.run(["node", "-e", "require('playwright').chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).then(async b=>{const p=await b.newPage({viewport:{width:1100,height:800}});await p.screenshot({path:%r});await b.close()})" % out]); return ["timeout: page did not finish in 60 s"]
    return json.loads(r.stdout.strip().splitlines()[-1])["errors"] if r.stdout.strip() else ["shoot failed: " + r.stderr[-200:]]
C = ["c1", "c2", "c3", "c4"]; M = [a + str(i) for a in "uts" for i in range(1, 9)]
loc = lambda k: os.path.join(root, "rooms" if k.startswith("c") else "mutants", k)
errs = {k: shoot(loc(k), os.path.join(loc(k), "final.png")) for k in C + M}
json.dump(errs, open(os.path.join(HERE, "renders.json"), "w"), indent=1)
rng = random.Random(SEED); fam = C[:]; rng.shuffle(fam); var = M[:]; rng.shuffle(var)
allw = C + M; rng.shuffle(allw); allv = C + M; rng.shuffle(allv)
P = os.path.join(root, "packets"); key = {"X_family": {}, "X_variants": {}, "W": {}, "V": {}}
for d in ["X/family", "X/variants", "W", "V"]: os.makedirs(os.path.join(P, d), exist_ok=True)
def put(k, rel, slot, name): shutil.copy(os.path.join(loc(k), "final.png"), os.path.join(P, rel, name + ".png")); key[slot][name] = k
for i, k in enumerate(fam, 1): put(k, "X/family", "X_family", "F%d" % i)
for i, k in enumerate(var, 1): put(k, "X/variants", "X_variants", "V%02d" % i)
for i, k in enumerate(allw, 1): put(k, "W", "W", "W%02d" % i)
for i, k in enumerate(allv, 1): put(k, "V", "V", "T%02d" % i)
json.dump(key, open(os.path.join(HERE, "coder", "key.json"), "w"), indent=1)
print("packets built; page errors:", {k: v for k, v in errs.items() if v})
