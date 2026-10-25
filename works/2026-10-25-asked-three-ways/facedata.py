"""Writes face-data.js for index.html from results.json, posthoc.json and the rooms (Session 158)."""
import json
from pathlib import Path
import score
HERE = Path(__file__).parent
r = json.loads((HERE / "results.json").read_text())
ph = json.loads((HERE / "posthoc.json").read_text())
div = {d["phrase"] for d in ph["diverging"]}
rooms = sorted(p.stem for p in (HERE / "rooms").glob("*.txt"))
parsed = {m: score.parse_room(m)[0] for m in rooms}
rows = []
for k, key in enumerate(score.keys):
    row = r["keys"][k]
    rows.append({
        "phrase": key["phrase"], "kind": key["kind"],
        "people": row["people_raw"], "A": row["A_raw"],
        "P": row["Q"]["P"], "O": row["Q"]["O"],
        "Pm": [parsed[m][k] for m in rooms if m[0] == "P"],
        "Om": [parsed[m][k] for m in rooms if m[0] == "O"],
        "medPeople": score.unscale(key["kind"], row["median"]["people"]),
        "medA": score.unscale(key["kind"], row["median"]["A"]),
        "diverging": key["phrase"] in div,
    })
rows.sort(key=lambda x: (x["kind"] != "probability", -x["medPeople"] if x["kind"] == "probability" else x["medPeople"]))
pred = r["predictions"]
(HERE / "face-data.js").write_text("window.FACE = " + json.dumps({"rows": rows, "predictions": pred,
    "posthoc": {"n": ph["n_diverging"], "P": ph["P_nearer_A"], "O": ph["O_nearer_A"], "unanimous": ph["n_unanimous_A"]}}) + ";\n")
print(len(rows))
