"""make_packets.py <root> : Session 146, after Session 145's file. Renders c1..c4 and the 24 mutants with shoot.js
(final.png), then builds four blind packets under <root>/packets, shuffles seed 146:
  X:  family/F1-F4 (c1-c4 shuffled), variants/V01-V24 (the mutants shuffled);
  W:  W01-W28 (c1-c4 and the mutants, shuffled);                 the judge, without the table;
  WT: J01-J28 (the same 28, shuffled again), and data/dogs.csv;   the judge, with the table beside it;
  V:  T01-T28 (shuffled again), and data/dogs.csv;                the reader of truth, with the table.
Every picture is written with a PNG text chunk holding a random number, so that equal pictures are not equal
bytes (F-291, F-297); the pixels are untouched. Keys to coder/key.json, page errors to renders.json."""
import json, os, random, shutil, struct, subprocess, sys, zlib
HERE = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(sys.argv[1]); SEED = 146
def shoot(page_dir, out):
    try: r = subprocess.run(["node", os.path.join(HERE, "shoot.js"), out, os.path.join(page_dir, "index.html")], capture_output=True, text=True, timeout=90)
    except subprocess.TimeoutExpired:  # a page that never yields is shown as a blank 1100 x 800 picture (declared; F-298's fix)
        subprocess.run(["node", "-e", "require('playwright').chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).then(async b=>{const p=await b.newPage({viewport:{width:1100,height:800}});await p.screenshot({path:%r});await b.close()})" % out]); return ["timeout: page did not finish in 90 s"]
    return json.loads(r.stdout.strip().splitlines()[-1])["errors"] if r.stdout.strip() else ["shoot failed: " + r.stderr[-200:]]
nonce_rng = random.SystemRandom()
def put_png(src, dst):
    b = open(src, "rb").read(); assert b[:8] == b"\x89PNG\r\n\x1a\n"
    data = b"nonce\x00" + str(nonce_rng.getrandbits(64)).encode()
    chunk = struct.pack(">I", len(data)) + b"tEXt" + data + struct.pack(">I", zlib.crc32(b"tEXt" + data) & 0xffffffff)
    ihdr_end = 8 + 4 + 4 + 13 + 4   # signature, then the IHDR chunk; the text chunk goes right after it
    open(dst, "wb").write(b[:ihdr_end] + chunk + b[ihdr_end:])
C = ["c1", "c2", "c3", "c4"]; M = [a + str(i) for a in "uts" for i in range(1, 9)]
loc = lambda k: os.path.join(root, "rooms" if k.startswith("c") else "mutants", k)
errs = {k: shoot(loc(k), os.path.join(loc(k), "final.png")) for k in C + M}
json.dump(errs, open(os.path.join(HERE, "renders.json"), "w"), indent=1)
rng = random.Random(SEED); fam = C[:]; rng.shuffle(fam); var = M[:]; rng.shuffle(var)
allw = C + M; rng.shuffle(allw); allj = C + M; rng.shuffle(allj); allv = C + M; rng.shuffle(allv)
P = os.path.join(root, "packets"); key = {"X_family": {}, "X_variants": {}, "W": {}, "WT": {}, "V": {}}
for d in ["X/family", "X/variants", "W", "WT/data", "V/data"]: os.makedirs(os.path.join(P, d), exist_ok=True)
for d in ["WT", "V"]: shutil.copy(os.path.join(root, "rooms", "c1", "data", "dogs.csv"), os.path.join(P, d, "data", "dogs.csv"))
def put(k, rel, slot, name): put_png(os.path.join(loc(k), "final.png"), os.path.join(P, rel, name + ".png")); key[slot][name] = k
for i, k in enumerate(fam, 1): put(k, "X/family", "X_family", "F%d" % i)
for i, k in enumerate(var, 1): put(k, "X/variants", "X_variants", "V%02d" % i)
for i, k in enumerate(allw, 1): put(k, "W", "W", "W%02d" % i)
for i, k in enumerate(allj, 1): put(k, "WT", "WT", "J%02d" % i)
for i, k in enumerate(allv, 1): put(k, "V", "V", "T%02d" % i)
json.dump(key, open(os.path.join(HERE, "coder", "key.json"), "w"), indent=1)
print("packets built; page errors:", {k: v for k, v in errs.items() if v})
