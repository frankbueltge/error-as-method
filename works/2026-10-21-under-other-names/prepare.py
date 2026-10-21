"""prepare.py <root> : sets up the four plain rooms c1..c4 (Session 145). Rooms are outside this repository,
each its own directory with nothing shared above it but the viewer (F-279). Each gets data/elements.js and
data/elements.csv (PubChem's file, unchanged). After the plain makers finish, `prepare.py <root> --parent`
draws the parent (seed 145) and has rebind.js make its 24 mutants."""
import json, os, random, shutil, subprocess, sys
import elements
HERE = os.path.dirname(os.path.abspath(__file__)); SEED = 145
root = os.path.abspath(sys.argv[1]); render = os.path.join(root, "viewer", "render.js")

def room(name):
    d = os.path.join(root, "rooms", name); os.makedirs(os.path.join(d, "data"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "sources", "pubchem-periodictable.csv"), os.path.join(d, "data", "elements.csv"))
    open(os.path.join(d, "data", "elements.js"), "w").write(elements.js(elements.load()))
    return d

if "--parent" not in sys.argv:
    os.makedirs(os.path.dirname(render), exist_ok=True); shutil.copy(os.path.join(HERE, "render.js"), render)
    brief = open(os.path.join(HERE, "briefs", "brief-C.md")).read()
    plan = [{"room": r, "arm": "C", "folder": room(r)} for r in ["c1", "c2", "c3", "c4"]]
    for p in plan: p["brief"] = brief.replace("{FOLDER}", p["folder"]).replace("{RENDER}", render)
    json.dump({"seed": SEED, "render": render, "rooms": plan}, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
    print("plain rooms ready")
else:
    plan = json.load(open(os.path.join(HERE, "plan.json")))
    parent = random.Random(SEED).choice(["c1", "c2", "c3", "c4"]); pd = os.path.join(root, "rooms", parent)
    mdir = os.path.join(root, "mutants"); os.makedirs(mdir, exist_ok=True)
    print(subprocess.run(["node", os.path.join(HERE, "rebind.js"), pd, mdir], capture_output=True, text=True, check=True).stdout)
    plan["parent"] = parent; json.dump(plan, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
    print("parent:", parent)
