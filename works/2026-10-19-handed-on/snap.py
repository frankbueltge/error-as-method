"""snap.py <lineage> <version> -- keeps a lineage's version as it stands after its maker handed back.

Copies index.html and NOTE.md from the room that made it to lineages/<L>/v<k>/, renders the kept copy at
1100 x 800 beside the same data.js (shot.js) to shots/<L>-v<k>.png, and appends one line to versions.jsonl:
bytes and sha256 of index.html, whether it differs from the previous version, the maker's renders so far.
"""
import hashlib, json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
L, v = sys.argv[1], int(sys.argv[2])
lin = {x["lineage"]: x for x in json.load(open(os.path.join(HERE, "plan.json")))["lineages"]}[L]
src = lin["rooms"][v - 1] if lin["arm"] in "PT" else lin["rooms"][0]
dst = os.path.join(HERE, "lineages", L, "v%d" % v)
os.makedirs(dst, exist_ok=True)
for f in ("index.html", "NOTE.md"):
    if os.path.exists(os.path.join(src, f)):
        shutil.copy(os.path.join(src, f), os.path.join(dst, f))
html = open(os.path.join(dst, "index.html"), "rb").read()
sha = hashlib.sha256(html).hexdigest()
log = os.path.join(HERE, "versions.jsonl")
prev = [json.loads(l) for l in open(log)] if os.path.exists(log) else []
last = [r for r in prev if r["lineage"] == L]
rd = os.path.join(src, "renders")
renders = len([x for x in os.listdir(rd) if x.endswith(".png")]) if os.path.isdir(rd) else 0
tmp = tempfile.mkdtemp()
shutil.copy(os.path.join(dst, "index.html"), tmp); shutil.copy(os.path.join(HERE, "data.js"), tmp)
out = subprocess.run(["node", os.path.join(HERE, "shot.js"), os.path.join(tmp, "index.html"),
                      os.path.join(HERE, "shots", "%s-v%d.png" % (L, v))], capture_output=True, text=True).stdout.strip()
rec = {"lineage": L, "arm": lin["arm"], "v": v, "bytes": len(html), "sha256": sha,
       "changed": (last[-1]["sha256"] != sha) if last else None, "room_renders": renders, "shot": json.loads(out)}
open(log, "a").write(json.dumps(rec) + "\n")
print(json.dumps(rec))
