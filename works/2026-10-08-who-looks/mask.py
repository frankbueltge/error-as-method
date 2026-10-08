"""mask.py -- the two coders' folders.

coder1/ (pairs): for every maker whose final index.html differs from the html at its first look, the first
look's picture (renders/01.png) and the final picture (shots/<maker>.png) as pairNN-X.png and pairNN-Y.png.
Pair order is shuffled with seed 1170, and which of the two is X is drawn from the same generator.
coder2/ (finals): all twelve final pictures as fNN.png, shuffled with seed 1171.
The keys go to coder1/key.json and coder2/key.json, which the coders never see."""
import hashlib, json, os, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
plan = {p["maker"]: p["arm"] for p in json.load(open(os.path.join(HERE, "plan.json")))["plan"]}
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
pairs = []
for m in sorted(plan):
    first = os.path.join(HERE, "makers", m, "renders", "01.html")
    if os.path.exists(first) and sha(first) != sha(os.path.join(HERE, "makers", m, "index.html")):
        pairs.append(m)
r = random.Random(1170)
r.shuffle(pairs)
o1 = os.path.join(HERE, "coder1", "pictures"); os.makedirs(o1, exist_ok=True)
key1 = {}
for i, m in enumerate(pairs, 1):
    first_is_x = r.random() < 0.5
    a = os.path.join(HERE, "makers", m, "renders", "01.png"); b = os.path.join(HERE, "shots", m + ".png")
    x, y = (a, b) if first_is_x else (b, a)
    shutil.copy(x, os.path.join(o1, "pair%02d-X.png" % i)); shutil.copy(y, os.path.join(o1, "pair%02d-Y.png" % i))
    key1["pair%02d" % i] = {"maker": m, "arm": plan[m], "X": "first look" if first_is_x else "final", "Y": "final" if first_is_x else "first look"}
json.dump(key1, open(os.path.join(HERE, "coder1", "key.json"), "w"), indent=1)
order = sorted(plan)
random.Random(1171).shuffle(order)
o2 = os.path.join(HERE, "coder2", "pictures"); os.makedirs(o2, exist_ok=True)
key2 = {}
for i, m in enumerate(order, 1):
    shutil.copy(os.path.join(HERE, "shots", m + ".png"), os.path.join(o2, "f%02d.png" % i))
    key2["f%02d" % i] = {"maker": m, "arm": plan[m]}
json.dump(key2, open(os.path.join(HERE, "coder2", "key.json"), "w"), indent=1)
print(len(pairs), "pairs;", key1); print(key2)
