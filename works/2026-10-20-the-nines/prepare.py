"""prepare.py <root> <material>: draws the arms of the twelve rooms (seed 143), copies the material into
each room's data/ and writes the briefs into plan.json. Rooms are outside this repository under neutral
names (r01..r12). Each room is its own directory with nothing shared above it but the viewer (F-279)."""
import json, os, random, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); SEED = 143
root = os.path.abspath(sys.argv[1]); material = os.path.abspath(sys.argv[2]); rng = random.Random(SEED)
arms = ["P"] * 6 + ["E"] * 6; rng.shuffle(arms)
rooms = ["r%02d" % i for i in range(1, 13)]
os.makedirs(os.path.join(root, "viewer"), exist_ok=True)
render = os.path.join(root, "viewer", "render.js"); shutil.copy(os.path.join(HERE, "render.js"), render)
b = lambda n: open(os.path.join(HERE, "briefs", n)).read()
brief, extra, extra_note = b("brief.md"), b("extra-E.md"), b("extra-E-note.md")
plan = []
for r, a in zip(rooms, arms):
    d = os.path.join(root, "rooms", r); os.makedirs(os.path.join(d, "data"), exist_ok=True)
    shutil.copy(material, os.path.join(d, "data", "46026h2024.txt"))
    t = brief.replace("{FOLDER}", d).replace("{RENDER}", render)
    t = t.replace("{EXTRA}", extra if a == "E" else "").replace("{EXTRA_NOTE}", extra_note if a == "E" else "")
    plan.append({"room": r, "arm": a, "folder": d, "brief": t})
json.dump({"seed": SEED, "render": render, "rooms": plan}, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
print([(p["room"], p["arm"]) for p in plan])
