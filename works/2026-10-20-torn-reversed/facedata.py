"""facedata.py: builds face-data.js for index.html from results.json, mutants.json, pixdiff.json and the rooms' notes."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); L = lambda p: json.load(open(os.path.join(H, p)))
R, MU, PX = L("results.json"), {m["id"]: m for m in L("mutants.json")["mutants"]}, L("pixdiff.json")
def title(k):
    if k.startswith("m"): return None
    t = open(os.path.join(H, "rooms", k, "NOTE.md")).read().splitlines()[0]; return re.sub(r"^#\s*", "", t).strip("* ")
items = []
for k, r in R["rows"].items():
    d = {"id": k, "arm": r["arm"], "title": title(k), "img": ("rooms/mutants/%s/final.png" if k.startswith("m") else "rooms/%s/final.png") % k,
         "page": ("rooms/mutants/%s/index.html" if k.startswith("m") else "rooms/%s/index.html") % k,
         "broken": r["x_broken"], "nearest": r["x_nearest"], "distance": r["x_distance"], "works": r["w_works"], "why": r["w_why"],
         "practice": r["practice"], "information": r["information"], "pixels": PX.get(k)}
    if k in MU: d["op"], d["n"], d["did"] = MU[k]["op"], MU[k]["n"], MU[k]["did"]
    items.append(d)
P = {k: {"held": v["held"], "count": v["count"]} for k, v in R["predictions"].items()}
open(os.path.join(H, "face-data.js"), "w").write("const FACE = " + json.dumps({"parent": R["parent"], "meaning": R["w_meaning"], "items": items, "predictions": P}, ensure_ascii=False) + ";\n")
print(len(items), "items")
