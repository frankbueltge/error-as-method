"""build.py -- writes face.js from plan.json, results.json and open.json (no hand-typed numbers in the face)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
plan = json.load(open(os.path.join(HERE, "plan.json")))
res = json.load(open(os.path.join(HERE, "results.json")))
opn = json.load(open(os.path.join(HERE, "open.json")))
WHERE = {"A": "nowhere (control)", "B": "the folder's own name", "C": "the folder above",
         "D": "an empty file beside the data", "E": "the data's first line", "F": "the brief: the title"}
SAID = {"m02": "“an empty orchard.txt … I left it alone”", "m05": "“orchard.txt, which I left alone”",
        "m08": "“a // orchard comment, which I ignored”"}
cards = []
for p in plan:
    m, c = p["maker"], p["condition"]
    short = "…/" + "/".join(p["folder"].split("/")[-3:]) + "/"
    if c == "D": short += "  data.js  orchard.txt"
    if c == "E": short += "data.js  →  // orchard"
    if c == "F": short = "brief: “The work's title is Orchard.”"
    r = res["makers"][m]
    cards.append({"m": m, "c": c, "title": r["title"], "path": short, "took": r["M1_take"],
                  "rating": r.get("M5_rating"), "said": SAID.get(m, "")})
rows = []
for c in "BCDEFA":
    ms = [x for x in cards if x["c"] == c]
    rows.append([WHERE[c], len(ms), sum(x["took"] for x in ms),
                 sum(1 for x in ms if opn[x["m"]].get("report_channel"))])
js = "const CARDS=" + json.dumps(cards, ensure_ascii=False) + ";\nconst ROWS=" + json.dumps(rows) + ";\n" + open(os.path.join(HERE, "face.tpl.js")).read()
open(os.path.join(HERE, "face.js"), "w").write(js)
print("face.js", len(js))
