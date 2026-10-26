"""Writes face-data.js for index.html from results.json and posthoc.json (Session 159)."""
import json
from pathlib import Path
HERE = Path(__file__).parent
r = json.loads((HERE / "results.json").read_text())
ph = json.loads((HERE / "posthoc.json").read_text())
foods = []
for k in r["keys"]:
    cnt = lambda xs: [sum(1 for x in xs if x == v) for v in range(1, 10)]
    foods.append({"f": k["food"], "people": cnt(k["people_raw"]), "A": cnt([x for x in k["A_raw"] if x is not None]),
                  "m": {a: round(v, 3) for a, v in k["median"].items()},
                  "P": [round(x, 2) for x in k["Q"]["P"]], "O": [round(x, 2) for x in k["Q"]["O"]]})
data = {"foods": foods, "centre": {t: {x: v for x, v in c.items() if x != "rows"} for t, c in r["centre"].items()},
        "posthoc": ph, "predictions": r["predictions"]}
(HERE / "face-data.js").write_text("window.FACE = " + json.dumps(data, separators=(",", ":")) + ";\n")
print(len(foods), "foods")
