"""mask.py -- the coder's folder. The arm-I material goes in as R.png; the twelve screenshots go in as
p01..p12 in an order shuffled with seed 1191. The key goes to keys/coder.json, which the coder never sees."""
import json, os, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
plan = {p["maker"]: p["arm"] for p in json.load(open(os.path.join(HERE, "plan.json")))}
out = "/tmp/claude-0/s119/coder"
os.makedirs(out, exist_ok=True)
shutil.copy(os.path.join(HERE, "materials", "bloom.png"), os.path.join(out, "R.png"))
order = sorted(plan)
random.Random(1191).shuffle(order)
key = {}
for i, m in enumerate(order, 1):
    pid = "p%02d" % i
    shutil.copy(os.path.join(HERE, "shots", m + ".png"), os.path.join(out, pid + ".png"))
    key[pid] = {"maker": m, "arm": plan[m]}
os.makedirs(os.path.join(HERE, "keys"), exist_ok=True)
json.dump(key, open(os.path.join(HERE, "keys", "coder.json"), "w"), indent=1)
print(sorted(os.listdir(out)))
