"""prepare.py <root> : sets up the four plain rooms c1..c4 (Session 147, after Session 146's file). Rooms are
outside this repository, each its own directory with nothing shared above it but the viewer (F-279). Each gets
data/bridges.js and data/bridges.csv (the twelve kept columns, bridges.py). After the plain makers finish,
`prepare.py <root> --mutants` has shuffle.js make the 16 mutants (four of each work; no parent is drawn tonight)."""
import json, os, shutil, subprocess, sys
import bridges
HERE = os.path.dirname(os.path.abspath(__file__)); SEED = 147
root = os.path.abspath(sys.argv[1]); render = os.path.join(root, "viewer", "render.js")
def room(name):
    d = os.path.join(root, "rooms", name); os.makedirs(os.path.join(d, "data"), exist_ok=True)
    rows = bridges.load()
    open(os.path.join(d, "data", "bridges.csv"), "w", encoding="utf-8").write(bridges.csv_text(rows))
    open(os.path.join(d, "data", "bridges.js"), "w", encoding="utf-8").write(bridges.js(rows))
    return d
if "--mutants" not in sys.argv:
    os.makedirs(os.path.dirname(render), exist_ok=True); shutil.copy(os.path.join(HERE, "render.js"), render)
    brief = open(os.path.join(HERE, "briefs", "brief-C.md")).read()
    plan = [{"room": r, "arm": "C", "folder": room(r)} for r in ["c1", "c2", "c3", "c4"]]
    for p in plan: p["brief"] = brief.replace("{FOLDER}", p["folder"]).replace("{RENDER}", render)
    json.dump({"seed": SEED, "render": render, "rooms": plan}, open(os.path.join(HERE, "plan.json"), "w"), indent=1, ensure_ascii=False)
    print("plain rooms ready")
else:
    mdir = os.path.join(root, "mutants"); os.makedirs(mdir, exist_ok=True)
    print(subprocess.run(["node", os.path.join(HERE, "shuffle.js"), os.path.join(root, "rooms"), mdir], capture_output=True, text=True, check=True).stdout)
    shutil.copy(os.path.join(mdir, "mutants.json"), os.path.join(HERE, "mutants.json"))
