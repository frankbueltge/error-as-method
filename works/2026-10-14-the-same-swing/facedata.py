"""facedata.py: writes face-data.js for index.html from plan.json, the makers' NOTE.md titles, coder B's answers,
results.json, the hourly record (materials/hourly.json) and the daily discharge (sources/). Run after score.py."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
plan = json.load(open(os.path.join(H, "plan.json"))); R = json.load(open(os.path.join(H, "results.json")))
W = []
for p in plan:
    m = p["maker"]; v = R["makers"][m]; q = v["B7_quote"].lower(); c = v["B7_category"]
    word = "an oscillation" if c == "other" and "oscillation" in q else ("tide" if c == "other" else c)
    if c == "temperature": word = "air temperature" if "air" in q else "temperature"
    W.append({"m": m, "cell": p["cell"], "title": open(os.path.join(H, "makers", m, "NOTE.md")).readline().strip("# \n"),
              "named": word, "day": "measured the day" if v["measured_day"] else ("supplied a day" if v["B3"] == "supplied" else "named no day"),
              "quote": v["B7_quote"][:200], "blank": m in ("m05", "m12")})
h = json.load(open(os.path.join(H, "materials", "hourly.json")))
d = json.load(open(os.path.join(H, "sources", "usgs_01646500_00060_dv_20250701_20250830.json")))
q = [round(float(x["value"])) for x in [b for b in d["value"]["timeSeries"][0]["values"] if b["value"]][0]["value"]]
P = {k: v[1] for k, v in R.items() if k.startswith("P")}
out = "const WORKS = " + json.dumps(W, ensure_ascii=False) + ";\n"
out += "const DO = " + json.dumps([round(v, 2) for v in h["do_mg_l"]]) + ";\n"
out += "const WT = " + json.dumps([round(v, 2) for v in h["water_temp_c"]]) + ";\n"
out += "const Q = " + json.dumps(q) + ";\n"
out += "const PRED = " + json.dumps(P) + ";\nconst SUPPLIED = " + json.dumps(R["S123.SUPPLIED"]) + ";\n"
open(os.path.join(H, "face-data.js"), "w").write(out); print(len(out), len(q))
