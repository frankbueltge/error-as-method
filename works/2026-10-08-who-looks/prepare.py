"""prepare.py -- builds data.js from the Wikidata file and lays out the twelve makers' folders.

python3 prepare.py <scratch-root>

The makers work outside this repository, in <scratch-root>/<id>/work/, so that nothing of this
experiment's name is in reach of them (F-195, Session 114). data.js and the viewport are the same
bytes for every maker. Only the brief's {VIEWER} slot and the presence of a viewer differ by arm:

  N  no viewer       {VIEWER} empty; nothing beside the folder
  O  viewer offered  {VIEWER} names <scratch-root>/<id>/viewer/render.js, "as often or as little as you like"
  R  viewer required as O, and "Render it at least once before you finish."

The viewer (render.js) is the same file for O and R. Each call writes <folder>/renders/NN.png and a copy
of index.html as it stood at that moment (renders/NN.html), and appends a line to renders/log.jsonl.
That is how this experiment knows who looked, how often, and what changed after looking.
"""
import json, os, random, sys, hashlib, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 117
UNIT = {"Q41803": 1.0, "Q11570": 1000.0, "Q191118": 1e6}   # gram, kilogram, tonne
# Q11247037 ("ton ... varying by language and place") is left out: one record (Sericho), unit ambiguous.
VIEWER = ("\n\nBeside your folder is a viewer. Run `node {RENDER} {FOLDER}` and it renders your "
          "`index.html` at 1100 × 800 as a picture, `renders/NN.png` in your folder, which you can open and "
          "look at. It also keeps a copy of `index.html` as it was at that moment. The `renders/` folder is "
          "the viewer's; you need not touch it. Running the viewer is allowed, although it lives outside your folder.")
OFFERED = " Use it as often or as little as you like."
REQUIRED = " Render your work with it at least once before you finish."


def items():
    rows = json.load(open(os.path.join(HERE, "sources", "wikidata-meteorites-mass.json")))["results"]["bindings"]
    by = {}
    dropped = []
    for b in rows:
        q = b["m"]["value"].rsplit("/", 1)[1]
        u = b["unit"]["value"].rsplit("/", 1)[1]
        if u not in UNIT:
            dropped.append(q); continue
        g = float(b["amount"]["value"]) * UNIT[u]
        year = None
        for k in ("fell", "found"):
            if k in b:
                year = int(b[k]["value"][:5].lstrip("+")) if b[k]["value"][0] in "+-" else int(b[k]["value"][:4])
                break
        lat = lon = None
        if "coord" in b and b["coord"]["value"].startswith("Point("):
            lon, lat = (float(x) for x in b["coord"]["value"][6:-1].split())
        name = b["mLabel"]["value"]
        prev = by.get(q)
        if prev is None or g > prev["grams"]:      # several mass statements: the largest
            by[q] = {"name": name, "grams": round(g, 3), "year": year, "lat": lat, "lon": lon}
        else:
            for k in ("year", "lat", "lon"):
                if prev[k] is None and locals()[k] is not None:
                    prev[k] = locals()[k]
    out = sorted(by.values(), key=lambda r: (r["name"], r["grams"]))
    return out, sorted(set(dropped) - set(by))


def data_js(rows):
    return "window.FALLS = " + json.dumps({"source": "Wikidata, items that are meteorites and state a mass (CC0)",
                                          "unit": "gram", "count": len(rows), "items": rows},
                                         separators=(",", ":"), ensure_ascii=False) + ";\n"


def brief(folder, render, arm):
    t = open(os.path.join(HERE, "briefs", "brief.md")).read()
    v = "" if arm == "N" else VIEWER.replace("{RENDER}", render).replace("{FOLDER}", folder) + (OFFERED if arm == "O" else REQUIRED)
    return t.replace("{FOLDER}", folder).replace("{VIEWER}", v)


if __name__ == "__main__":
    root = sys.argv[1]
    rows, dropped = items()
    body = data_js(rows)
    open(os.path.join(HERE, "data.js"), "w").write(body)
    arms = ["N"] * 4 + ["O"] * 4 + ["R"] * 4
    random.Random(SEED).shuffle(arms)
    plan = []
    os.makedirs(os.path.join(HERE, "briefs", "run"), exist_ok=True)
    for i, arm in enumerate(arms):
        mid = "m%02d" % (i + 1)
        folder = os.path.join(root, mid, "work")
        os.makedirs(folder, exist_ok=True)
        open(os.path.join(folder, "data.js"), "w").write(body)
        render = os.path.join(root, mid, "viewer", "render.js")
        if arm != "N":
            os.makedirs(os.path.dirname(render), exist_ok=True)
            shutil.copy(os.path.join(HERE, "render.js"), render)
        b = brief(folder, render, arm)
        open(os.path.join(HERE, "briefs", "run", mid + ".md"), "w").write(b)
        plan.append({"maker": mid, "arm": arm, "folder": folder,
                     "data_sha256": hashlib.sha256(body.encode()).hexdigest(),
                     "brief_sha256": hashlib.sha256(b.encode()).hexdigest()})
    json.dump({"items": len(rows), "dropped_unit": dropped, "plan": plan}, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
    print(len(rows), "items; dropped for unit:", dropped)
    for p in plan:
        print(p["maker"], p["arm"], p["folder"])
