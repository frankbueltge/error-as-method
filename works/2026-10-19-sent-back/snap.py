"""snap.py <maker> <version> -- after each round, keeps the maker's folder as it stands.

Copies index.html and NOTE.md from the maker's room to makers/<maker>/v<version>/, renders the copy at
1100 x 800 (shot.js) to shots/<maker>-v<version>.png, and appends one line to versions.jsonl: bytes and
sha256 of index.html, whether it differs from the previous version, the maker's own render count so far.
"""
import hashlib, json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
m, v = sys.argv[1], int(sys.argv[2])
plan = {p["maker"]: p for p in json.load(open(os.path.join(HERE, "plan.json")))["makers"]}
src = plan[m]["folder"]
dst = os.path.join(HERE, "makers", m, "v%d" % v)
os.makedirs(dst, exist_ok=True)
for f in ("index.html", "NOTE.md"):
    if os.path.exists(os.path.join(src, f)):
        shutil.copy(os.path.join(src, f), os.path.join(dst, f))
html = open(os.path.join(dst, "index.html"), "rb").read()
sha = hashlib.sha256(html).hexdigest()
log = os.path.join(HERE, "versions.jsonl")
prev = [json.loads(l) for l in open(log)] if os.path.exists(log) else []
last = [r for r in prev if r["maker"] == m]
renders = len([x for x in os.listdir(os.path.join(src, "renders")) if x.endswith(".png")]) if os.path.isdir(os.path.join(src, "renders")) else 0
tmp = tempfile.mkdtemp()  # the kept copy is rendered beside the same data.js the maker had
shutil.copy(os.path.join(dst, "index.html"), tmp); shutil.copy(os.path.join(HERE, "data.js"), tmp)
out = subprocess.run(["node", os.path.join(HERE, "shot.js"), os.path.join(tmp, "index.html"),
                      os.path.join(HERE, "shots", "%s-v%d.png" % (m, v))], capture_output=True, text=True).stdout.strip()
rec = {"maker": m, "arm": plan[m]["arm"], "v": v, "bytes": len(html), "sha256": sha,
       "changed": (last[-1]["sha256"] != sha) if last else None, "maker_renders": renders, "shot": json.loads(out)}
open(log, "a").write(json.dumps(rec) + "\n")
print(json.dumps(rec))
