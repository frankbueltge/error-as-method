"""build.py -- face-data.js for index.html, from plan.json, looks.json, coder1/, coder2/, open.json and the
makers' NOTE.md titles. Only derived numbers and verbatim quotes; nothing is written by hand here."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); J = lambda p: json.load(open(os.path.join(H, p)))
L, c1, k1, c2, k2, oc, res = J("looks.json"), J("coder1/ratings.json"), J("coder1/key.json"), J("coder2/ratings.json"), J("coder2/key.json"), J("open.json"), J("results.json")
pair = {v["maker"]: c1[p] for p, v in k1.items()}
fin = {v["maker"]: c2["defects"][f] for f, v in k2.items()}
grp = {m: g["name"] for g in res["P7"]["groups"] for m in g["makers"]}
rows = []
for m in sorted(L):
    t = open(os.path.join(H, "makers", m, "NOTE.md")).read().strip().splitlines()[0].lstrip("# ").strip()
    o = oc[m]
    rows.append({"m": m, "arm": L[m]["arm"], "title": t, "looks": L[m]["looks"], "changed": L[m]["changed_after_look"],
                 "same": pair[m]["same"] if m in pair else None,
                 "form": [d["text"] for d in pair[m]["differences"] if d["tag"] == "FORM"] if m in pair else [],
                 "defects": [x for k in ("overlap", "clipped", "illegible", "blank") for x in fin[m][k]],
                 "group": grp[m], "code": o.get("code") or o.get("check"), "quote": o["quote"]})
open(os.path.join(H, "face-data.js"), "w").write("window.ROWS = " + json.dumps(rows, ensure_ascii=False) + ";\n")
print(len(rows))
