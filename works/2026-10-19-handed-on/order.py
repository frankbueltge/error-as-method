"""order.py <out-dir> -- lays out the blind coder's eighteen pairs. Each transition v(k-1)->v(k) of each lineage gets a
label T01..T18 in an order drawn with seed 140; before/after are the kept renders (shots/). The key goes to
coder/key.json and is not in the coder's folder."""
import json, os, random, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
out = os.path.abspath(sys.argv[1]); os.makedirs(out, exist_ok=True)
plan = json.load(open(os.path.join(HERE, "plan.json")))
tr = [(L["lineage"], k) for L in plan["lineages"] for k in (2, 3, 4)]
random.Random(140).shuffle(tr)
key = {}
for i, (L, k) in enumerate(tr, 1):
    t = "T%02d" % i
    shutil.copy(os.path.join(HERE, "shots", "%s-v%d.png" % (L, k - 1)), os.path.join(out, t + "-before.png"))
    shutil.copy(os.path.join(HERE, "shots", "%s-v%d.png" % (L, k)), os.path.join(out, t + "-after.png"))
    key[t] = {"lineage": L, "to": k, "arm": next(x["arm"] for x in plan["lineages"] if x["lineage"] == L)}
json.dump(key, open(os.path.join(HERE, "coder", "key.json"), "w"), indent=1)
print(len(key), "pairs in", out)
