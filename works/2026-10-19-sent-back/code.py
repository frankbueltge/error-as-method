"""code.py <scratch-root> -- builds the two coders' packets after every maker is done (Session 139).

Coder O gets, per lineage of at least three versions, its renders copied under letters in an order shuffled with
seed 1390, lineages renamed L1.. in a shuffled order. The key goes to coder/key.json, which coder O never sees.
Coder S gets every transition vN -> vN+1 in true order: both renders and both NOTE.md files.
"""
import json, os, random, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(sys.argv[1])
vs = [json.loads(l) for l in open(os.path.join(HERE, "versions.jsonl"))]
by = {}
for r in vs:
    by.setdefault(r["maker"], []).append(r["v"])
rng = random.Random(1390)
makers = sorted(m for m in by if len(by[m]) >= 3)
rng.shuffle(makers)
key = {"O": {}, "S": {}}
for i, m in enumerate(makers, 1):
    L = "L%d" % i
    vers = sorted(by[m]); order = vers[:]; rng.shuffle(order)
    d = os.path.join(root, "O", L); os.makedirs(d, exist_ok=True)
    key["O"][L] = {"maker": m, "letters": {}}
    for j, v in enumerate(order):
        ch = "ABCDEFGH"[j]
        shutil.copy(os.path.join(HERE, "shots", "%s-v%d.png" % (m, v)), os.path.join(d, ch + ".png"))
        key["O"][L]["letters"][ch] = v
tr = []
for m in sorted(by):
    for v in sorted(by[m])[:-1]:
        tr.append((m, v))
rng.shuffle(tr)
for k, (m, v) in enumerate(tr, 1):
    T = "T%02d" % k
    d = os.path.join(root, "S", T); os.makedirs(d, exist_ok=True)
    for tag, vv in (("before", v), ("after", v + 1)):
        shutil.copy(os.path.join(HERE, "shots", "%s-v%d.png" % (m, vv)), os.path.join(d, tag + ".png"))
        n = os.path.join(HERE, "makers", m, "v%d" % vv, "NOTE.md")
        if os.path.exists(n):
            shutil.copy(n, os.path.join(d, tag + "-NOTE.md"))
    key["S"][T] = {"maker": m, "from": v, "to": v + 1}
os.makedirs(os.path.join(HERE, "coder"), exist_ok=True)
json.dump(key, open(os.path.join(HERE, "coder", "key.json"), "w"), indent=1)
print(len(makers), "lineages for O;", len(tr), "transitions for S")
