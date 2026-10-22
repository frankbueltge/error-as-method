"""make_packets.py <root> : Session 147, after Session 146's file. Renders c1..c4 and the 16 mutants with shoot.js
(final.png), then builds six blind packets under <root>/packets, each its own shuffle of the same 20 pages
(seed 147, one stream, in this order):
  P:  P01-P20   the coder of the page alone (broken; are its words true of its drawing?), no table;
  W:  W01-W20   the judge, without the table;
  WT: J01-J20   the judge, with data/bridges.csv beside it;
  G:  G01-G20   the guesser, told that some pages are drawn from a shuffled copy, without the table;
  V:  T01-T20   the reader of truth, with data/bridges.csv;
  H:  H01-H20   the practice's own guess, the G question, made before any key is opened.
Every picture is written with a PNG text chunk holding a random number, so that equal pictures are not equal
bytes (F-291, F-297); the pixels are untouched. Keys to coder/key.json, page errors to renders.json."""
import json, os, random, shutil, struct, subprocess, sys, zlib
HERE = os.path.dirname(os.path.abspath(__file__)); root = os.path.abspath(sys.argv[1]); SEED = 147
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
    ihdr_end = 8 + 4 + 4 + 13 + 4
    open(dst, "wb").write(b[:ihdr_end] + chunk + b[ihdr_end:])
C = ["c1", "c2", "c3", "c4"]; M = [c + s for c in C for s in ["o1", "o2", "o3", "a"]]
loc = lambda k: os.path.join(root, "rooms" if len(k) == 2 else "mutants", k)
errs = {k: shoot(loc(k), os.path.join(loc(k), "final.png")) for k in C + M}
json.dump(errs, open(os.path.join(HERE, "renders.json"), "w"), indent=1)
rng = random.Random(SEED); P = os.path.join(root, "packets"); key = {}
SEATS = [("P", "P", False), ("W", "W", False), ("WT", "J", True), ("G", "G", False), ("V", "T", True), ("H", "H", False)]
for seat, letter, table in SEATS:
    order = C + M; rng.shuffle(order); d = os.path.join(P, seat); os.makedirs(d, exist_ok=True); key[seat] = {}
    if table:
        os.makedirs(os.path.join(d, "data"), exist_ok=True)
        shutil.copy(os.path.join(root, "rooms", "c1", "data", "bridges.csv"), os.path.join(d, "data", "bridges.csv"))
    for i, k in enumerate(order, 1):
        name = "%s%02d" % (letter, i); put_png(os.path.join(loc(k), "final.png"), os.path.join(d, name + ".png")); key[seat][name] = k
json.dump(key, open(os.path.join(HERE, "coder", "key.json"), "w"), indent=1)
print("packets built; page errors:", {k: v for k, v in errs.items() if v})
