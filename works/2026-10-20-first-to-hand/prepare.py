"""prepare.py <root>: draws the arms of the twelve rooms (seed 142) and writes the briefs into plan.json.
Rooms are outside this repository under neutral names (r01..r12), empty, beside one viewer."""
import json, os, random, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); SEED = 142
root = os.path.abspath(sys.argv[1]); rng = random.Random(SEED)
arms = ["N"] * 6 + ["L"] * 6; rng.shuffle(arms)
rooms = ["r%02d" % i for i in range(1, 13)]
os.makedirs(os.path.join(root, "viewer"), exist_ok=True)
render = os.path.join(root, "viewer", "render.js"); shutil.copy(os.path.join(HERE, "render.js"), render)
brief = open(os.path.join(HERE, "briefs", "brief.md")).read(); extra = open(os.path.join(HERE, "briefs", "extra-L.md")).read()
plan = []
for r, a in zip(rooms, arms):
    d = os.path.join(root, "rooms", r); os.makedirs(d, exist_ok=True)
    plan.append({"room": r, "arm": a, "folder": d,
                 "brief": brief.replace("{FOLDER}", d).replace("{RENDER}", render).replace("{EXTRA}", extra if a == "L" else "")})
json.dump({"seed": SEED, "render": render, "rooms": plan}, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
print([(p["room"], p["arm"]) for p in plan])
