"""make_packets.py <root> shoot-c | packets : Session 144.
shoot-c   renders c1..c4 with shoot.js to rooms/cN/final.png (the parent's picture for the A makers).
packets   renders a1..a4 and m01..m12, then builds two blind packets under <root>/packets:
          X: family/F1-F4 (c1-c4 shuffled), variants/V01-V16 (a1-a4, m01-m12 shuffled);
          W: W01-W20 (all twenty shuffled). Shuffles seed 144. Keys to coder/key.json, page errors to renders.json."""
import json, os, random, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(sys.argv[1]); SEED = 144
def shoot(page_dir, out):
    r = subprocess.run(["node", os.path.join(HERE, "shoot.js"), out, os.path.join(page_dir, "index.html")], capture_output=True, text=True)
    return json.loads(r.stdout.strip().splitlines()[-1])["errors"] if r.stdout.strip() else ["shoot failed: " + r.stderr[-200:]]
C = ["c1", "c2", "c3", "c4"]; A = ["a1", "a2", "a3", "a4"]; M = ["m%02d" % i for i in range(1, 13)]
loc = lambda k: os.path.join(root, "mutants" if k.startswith("m") else "rooms", k)
if sys.argv[2] == "shoot-c":
    print({c: shoot(loc(c), os.path.join(loc(c), "final.png")) for c in C})
else:
    errs = json.load(open(os.path.join(HERE, "renders.json"))) if os.path.exists(os.path.join(HERE, "renders.json")) else {}
    for k in A + M: errs[k] = shoot(loc(k), os.path.join(loc(k), "final.png"))
    for c in C: errs.setdefault(c, shoot(loc(c), os.path.join(loc(c), "final.png")))
    json.dump(errs, open(os.path.join(HERE, "renders.json"), "w"), indent=1)
    rng = random.Random(SEED); fam = C[:]; rng.shuffle(fam); var = A + M; rng.shuffle(var); allw = C + A + M; rng.shuffle(allw)
    px = os.path.join(root, "packets", "X"); pw = os.path.join(root, "packets", "W")
    for d in [os.path.join(px, "family"), os.path.join(px, "variants"), pw]: os.makedirs(d, exist_ok=True)
    key = {"X_family": {}, "X_variants": {}, "W": {}}
    for i, k in enumerate(fam, 1): shutil.copy(os.path.join(loc(k), "final.png"), os.path.join(px, "family", "F%d.png" % i)); key["X_family"]["F%d" % i] = k
    for i, k in enumerate(var, 1): shutil.copy(os.path.join(loc(k), "final.png"), os.path.join(px, "variants", "V%02d.png" % i)); key["X_variants"]["V%02d" % i] = k
    for i, k in enumerate(allw, 1): shutil.copy(os.path.join(loc(k), "final.png"), os.path.join(pw, "W%02d.png" % i)); key["W"]["W%02d" % i] = k
    json.dump(key, open(os.path.join(HERE, "coder", "key.json"), "w"), indent=1)
    print("packets built; page errors:", {k: v for k, v in errs.items() if v})
