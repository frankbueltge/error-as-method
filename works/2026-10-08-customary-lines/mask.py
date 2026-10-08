"""mask.py -- the coder's folder. Round 1's pictures go in as the reference set r1..r6 (r<k> is m0<k>);
round 2's twelve go in as p01..p12 in an order shuffled with seed 1160. The key (picture -> maker, with
arms) goes to coder/key.json, which the coder never sees."""
import json, os, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
plan = {p["maker"]: p["arm"] for p in json.load(open(os.path.join(HERE, "plan.json")))}
out = os.path.join(HERE, "coder", "pictures")
os.makedirs(out, exist_ok=True)
for k in range(1, 7):
    shutil.copy(os.path.join(HERE, "shots", "m%02d.png" % k), os.path.join(out, "r%d.png" % k))
order = ["m%02d" % i for i in range(7, 19)]
random.Random(1160).shuffle(order)
key = {}
for i, m in enumerate(order, 1):
    pid = "p%02d" % i
    shutil.copy(os.path.join(HERE, "shots", m + ".png"), os.path.join(out, pid + ".png"))
    key[pid] = {"maker": m, "arm": plan[m]}
json.dump(key, open(os.path.join(HERE, "coder", "key.json"), "w"), indent=1)
print(key)
