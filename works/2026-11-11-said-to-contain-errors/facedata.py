"""Writes face-data.js for index.html from plan.json, results.json, rooms/ and the raw USGS response."""
import json
p = json.load(open("plan.json")); r = json.load(open("results.json"))
raw = json.load(open("sources/usgs-dv-2026-10.json"))
daily = {}
for ts in raw["value"]["timeSeries"]:
    s = ts["sourceInfo"]["siteCode"][0]["value"]
    if s in ("07289000", "11264500"):
        daily[s] = [float(v["value"]) for v in ts["values"][0]["value"]]
contact = [{"name": p["names"][s], "true": p["told"]["true"][s], "rev": p["told"]["reversed"][s]} for s in p["contact"]]
scored = [{"name": p["names"][s], "true": p["true_cfs"][s],
           "arms": {a: round(10 ** r["arms"][a]["median_log"][i]) for a in "URDT"}} for i, s in enumerate(p["scored"])]
makers = {m: {"how": v["how"], "rho": v["rho_truth"]} for m, v in r["makers"].items()}
arms = {a: {k: r["arms"][a][k] for k in r["arms"][a] if k != "median_log"} for a in "URDT"}
d = {"contact": contact, "scored": scored, "makers": makers, "arms": arms, "vicksburg": daily["07289000"]}
open("face-data.js", "w").write("window.FACE = " + json.dumps(d, separators=(",", ":")) + ";\n")
