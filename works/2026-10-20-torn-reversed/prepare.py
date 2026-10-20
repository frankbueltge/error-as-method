"""prepare.py <root> : sets up the four plain rooms c1..c4 (Session 144). Rooms are outside this repository,
each its own directory with nothing shared above it but the viewer (F-279). Each gets data/selborne.txt and
data/selborne.js (the same text as one JS string, Session 143's thread 5 / F-286). After the plain makers
finish, `prepare.py <root> --parent` draws the parent (seed 144) and sets up a1..a4 and the mutants."""
import json, os, random, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); SEED = 144
root = os.path.abspath(sys.argv[1]); txt = os.path.join(HERE, "sources", "selborne.txt")
render = os.path.join(root, "viewer", "render.js")
b = lambda n: open(os.path.join(HERE, "briefs", n)).read()

def room(name):
    d = os.path.join(root, "rooms", name); os.makedirs(os.path.join(d, "data"), exist_ok=True)
    shutil.copy(txt, os.path.join(d, "data", "selborne.txt"))
    open(os.path.join(d, "data", "selborne.js"), "w").write("const SELBORNE = " + json.dumps(open(txt).read()) + ";\n")
    return d

if "--parent" not in sys.argv:
    os.makedirs(os.path.dirname(render), exist_ok=True); shutil.copy(os.path.join(HERE, "render.js"), render)
    plan = [{"room": r, "arm": "C", "folder": room(r), "brief": b("brief-C.md")} for r in ["c1", "c2", "c3", "c4"]]
    for p in plan: p["brief"] = p["brief"].replace("{FOLDER}", p["folder"]).replace("{RENDER}", render)
    json.dump({"seed": SEED, "render": render, "rooms": plan}, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
    print("plain rooms ready")
else:
    plan = json.load(open(os.path.join(HERE, "plan.json")))
    parent = random.Random(SEED).choice(["c1", "c2", "c3", "c4"]); pd = os.path.join(root, "rooms", parent)
    for r in ["a1", "a2", "a3", "a4"]:
        d = room(r)
        for f in os.listdir(pd):  # the whole work as its maker left it, except the maker's own renders
            if f in ("renders", "data", "final.png"): continue
            src = os.path.join(pd, f); shutil.copytree(src, os.path.join(d, f)) if os.path.isdir(src) else shutil.copy(src, d)
        os.makedirs(os.path.join(d, "renders"), exist_ok=True); shutil.copy(os.path.join(pd, "final.png"), os.path.join(d, "renders", "final.png"))
        os.makedirs(os.path.join(d, "original"), exist_ok=True)
        for f in ["index.html", "NOTE.md"]: shutil.copy(os.path.join(pd, f), os.path.join(d, "original", f))
        plan["rooms"].append({"room": r, "arm": "A", "folder": d, "brief": b("brief-A.md").replace("{FOLDER}", d).replace("{RENDER}", render)})
    mdir = os.path.join(root, "mutants"); os.makedirs(mdir, exist_ok=True)
    print(subprocess.run(["node", os.path.join(HERE, "mutate.js"), os.path.join(pd, "index.html"), mdir], capture_output=True, text=True).stdout)
    for m in sorted(x for x in os.listdir(mdir) if x[1:].isdigit()):
        for f in os.listdir(pd):  # everything the parent's page could load, except its page and its renders
            if f in ("index.html", "renders", "final.png"): continue
            src = os.path.join(pd, f); dst = os.path.join(mdir, m, f)
            shutil.copytree(src, dst) if os.path.isdir(src) else shutil.copy(src, dst)
    plan["parent"] = parent; json.dump(plan, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
    print("parent:", parent)
