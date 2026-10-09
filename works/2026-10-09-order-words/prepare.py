"""prepare.py -- builds data.js from the IANA Root Zone Database page and lays out the makers' folders.

python3 prepare.py parse <root-zone-db.html>     writes sources/root-zone.json and sources/MANIFEST.json
python3 prepare.py makers <scratch-root>          writes data.js, briefs/run/, plan.json

Twelve makers, one brief, one viewer each (the viewer of experiment 13, byte for byte). The makers
work outside this repository, in <scratch-root>/<id>/work/, so that nothing of this experiment's
name is in reach of them (F-195). Every maker gets the same brief: the viewer offered, "as often or
as little as you like" (experiment 13's arm O).

After the first hand-in each maker gets one RETURN, assigned here by seed 118, four makers each:

  H  handed back   the work comes back with nothing said about it
  S  own notes     the work comes back with a stranger's three notes written on its own picture
  X  other notes   the work comes back with a stranger's three notes written on ANOTHER maker's
                   picture, presented in exactly the words S gets

The X donor of each X maker is drawn here too (seed 118), never itself. The arms are not known to
the makers, nor to the stranger who writes the notes.
"""
import json, os, random, sys, hashlib, shutil, re, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 118
URL = "https://www.iana.org/domains/root/db"


def parse(path):
    raw = open(path, "rb").read()
    t = raw.decode("utf-8")
    rows = re.findall(r'<a href="/domains/root/db/[^"]+">([^<]+)</a></span></td>\s*<td>([^<]*)</td>\s*<td>([^<]*)</td>', t, re.S)
    items = [{"tld": H.unescape(a).strip(), "type": b.strip(), "manager": H.unescape(c).strip()} for a, b, c in rows]
    os.makedirs(os.path.join(HERE, "sources"), exist_ok=True)
    body = json.dumps(items, ensure_ascii=False, indent=0)
    open(os.path.join(HERE, "sources", "root-zone.json"), "w").write(body)
    man = [{"url": URL, "fetched": "2026-10-09", "status": 200, "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "what": "IANA Root Zone Database, the HTML table of every top-level domain with its type and TLD manager",
            "why": "the night's material; parsed into root-zone.json (domain, type, manager), which is committed. "
                   "The page itself is not committed (site chrome); re-fetch and compare the hash, or the row count.",
            "rows": len(items)},
           {"file": "root-zone.json", "sha256": hashlib.sha256(body.encode()).hexdigest(), "rows": len(items)}]
    json.dump(man, open(os.path.join(HERE, "sources", "MANIFEST.json"), "w"), indent=1, ensure_ascii=False)
    print(len(items), "rows")


def data_js():
    items = json.load(open(os.path.join(HERE, "sources", "root-zone.json")))
    return "window.ROOT = " + json.dumps({"source": "IANA Root Zone Database, " + URL + ", as of 2026-10-09",
                                         "count": len(items), "items": items},
                                        separators=(",", ":"), ensure_ascii=False) + ";\n"


def makers(root):
    body = data_js()
    open(os.path.join(HERE, "data.js"), "w").write(body)
    rng = random.Random(SEED)
    ret = ["H"] * 4 + ["S"] * 4 + ["X"] * 4
    rng.shuffle(ret)
    ids = ["m%02d" % (i + 1) for i in range(12)]
    donors = {}
    for i, mid in enumerate(ids):
        if ret[i] == "X":
            donors[mid] = rng.choice([d for d in ids if d != mid])
    t = open(os.path.join(HERE, "briefs", "brief.md")).read()
    os.makedirs(os.path.join(HERE, "briefs", "run"), exist_ok=True)
    plan = []
    for i, mid in enumerate(ids):
        folder = os.path.join(root, mid, "work")
        render = os.path.join(root, mid, "viewer", "render.js")
        os.makedirs(folder, exist_ok=True); os.makedirs(os.path.dirname(render), exist_ok=True)
        open(os.path.join(folder, "data.js"), "w").write(body)
        shutil.copy(os.path.join(HERE, "render.js"), render)
        b = t.replace("{FOLDER}", folder).replace("{RENDER}", render)
        open(os.path.join(HERE, "briefs", "run", mid + ".md"), "w").write(b)
        plan.append({"maker": mid, "return": ret[i], "notes_from": donors.get(mid, mid if ret[i] == "S" else None),
                     "folder": folder, "data_sha256": hashlib.sha256(body.encode()).hexdigest(),
                     "brief_sha256": hashlib.sha256(b.encode()).hexdigest()})
    json.dump({"seed": SEED, "plan": plan}, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
    for p in plan:
        print(p["maker"], p["return"], p["notes_from"])


if __name__ == "__main__":
    {"parse": parse, "makers": makers}[sys.argv[1]](sys.argv[2])
