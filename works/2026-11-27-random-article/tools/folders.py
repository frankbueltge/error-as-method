"""Write each curator's draw.txt (and pool.txt for arm B) into its folder."""
import json, os, sys
base = sys.argv[1]; W = sys.argv[2]
rows = {json.loads(l)["n"]: json.loads(l) for l in open(os.path.join(W, "people/pool-160.jsonl"))}
draws = json.load(open(os.path.join(W, "people/draws.json")))["draws"]
def entry(lbl, r):
    return f"{lbl}. {r['title']}  ({r['words']} words)\n   {r['lead']}\n"
pool = "".join(entry(str(n), rows[n]) + "\n" for n in range(1, 161))
for d in draws:
    txt = "".join(entry("abcdefghijkl"[i], rows[n]) + "\n" for i, n in enumerate(d["items"]))
    for arm in "AB":
        f = os.path.join(base, f"{arm}{d['draw']}"); os.makedirs(f, exist_ok=True)
        open(os.path.join(f, "draw.txt"), "w").write(txt)
        if arm == "B": open(os.path.join(f, "pool.txt"), "w").write(pool)
print("ok")
