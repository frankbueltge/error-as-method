"""build.py -- writes face-data.js (window.FACE) from results.json, coder/key.json and plan.json.
The face shows the coder's order first (p01..p12, the order mask.py drew) and the arms only on request."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda *p: json.load(open(os.path.join(HERE, *p)))
res, key = J("results.json"), J("coder", "key.json")
rows = res["rows"]
works = []
for m, r in sorted(rows.items()):
    works.append({"m": m, "arm": r["arm"], "title": r["title"], "rating": r.get("M2_rating"),
                  "group": r.get("M3_group"), "words": r.get("M2_words"), "overlap": r.get("M1_overlap")})
order = [key["p%02d" % i]["maker"] for i in range(1, 13)]
face = {"works": works, "order": order, "means": res["means"], "pair": res["pair_rate"],
        "held": res["held"], "failed": res["failed"],
        "predictions": {k: v["why"] for k, v in res["predictions"].items()}}
open(os.path.join(HERE, "face-data.js"), "w").write("window.FACE = " + json.dumps(face, ensure_ascii=False) + ";\n")
print(len(works), "works;", "order", order)
