"""facedata.py: writes face-data.js for index.html from materials/hourly.json, plan.json, results.json and coder B's
answers. Each maker's sentence about what was measured is copied verbatim from its report (reports/mNN.md); the
assert below checks it is there."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
J = lambda *p: json.load(open(os.path.join(H, *p)))
rows = J("materials", "hourly.json")["stem_radius_change_um"]; plan = J("plan.json"); R = J("results.json")
B = J("coder", "B", "answers.json")
QUOTE = {
 "m01": "I think the tree is taking water in and giving it out, rather than visibly growing.",
 "m02": "I think it is most likely a water level or flow: a small stream's discharge or stage, or a shallow water table.",
 "m03": "I think it is a point dendrometer on a living tree during a warm season, possibly a fairly dry one.",
 "m04": "My best candidate is near-ground relative humidity. Close alternatives are tree-stem diameter or a stream or groundwater level affected by evaporation.",
 "m05": "I think this is a band or sensor on the trunk recording the daily \"breathing\" of the stem, over about two months of mostly dry weather broken by rain.",
 "m06": "This looks most like a tree-stem dendrometer in summer: the stem shrinks while it loses water through the day, refills at night, shrinks further over weeks of drought, and swells back during rainy spells.",
 "m07": "I think this is a station on land with plants growing nearby, during the growing season, near the ground or a low inlet.",
 "m08": "My best guess:** outdoor relative humidity.",
 "m09": "That matches carbon dioxide building up at night from plant and soil respiration in still air, then being drawn down by photosynthesis and daytime mixing.",
 "m10": "CO₂ near the ground at a site surrounded by growing plants, recorded in the growing season.",
 "m11": "I think this is a dendrometer on a living tree's stem, recording a dry season broken by a few rain events.",
 "m12": "I think this is CO2 near the ground at a site with plants and soil, but that is my interpretation, not something the file proves.",
 "m13": "hourly relative humidity at an outdoor site.",
 "m14": "It looks like a dendrometer (a gauge for small changes in trunk size) recording a trunk swelling and shrinking with its water content during a growing season.",
 "m15": "Relative humidity is my best guess; fuel or surface moisture would fit the same way.",
 "m16": "carbon dioxide close to the ground at a station with plants around it, during the growing season.",
 "m17": "That fits CO2 building up at night from plant respiration under calm air, then being drawn down in daylight as the air mixes and plants photosynthesise.",
 "m18": "It looks like a stem shrinking by day and swelling by night during a dry spell in the growing season, broken by a few rain events.",
}
for m, q in QUOTE.items():
    assert q in open(os.path.join(H, "reports", m + ".md"), encoding="utf-8").read(), m
QUOTE["m08"] = "My best guess: outdoor relative humidity."
TOLD = {"N": "", "T": "It is a record of the radius of a tree's trunk, measured at one point on its bark.",
        "C": "It is a record of the carbon dioxide content of the air at a measuring station."}
makers = []
for p in plan["makers"]:
    m = p["maker"]; pm = R["per_maker"][m]
    makers.append({"m": m, "cell": p["cell"], "told": TOLD[p["cell"]], "title": B[m]["C9"], "kind": B[m]["C5"],
                   "said_told": B[m]["C11"] == "yes", "own": B[m]["C12"] == "yes", "hedged": B[m]["C6"] == "yes", "quote": QUOTE[m]})
days = [rows[i:i + 24] for i in range(0, 1464, 24)]
out = {"daily_max": [round(max(d), 1) for d in days], "daily_min": [round(min(d), 1) for d in days], "makers": makers,
       "source": R["S130.SOURCE"]["verdict"], "held": R["predictions_held"], "counts": R["counts"]}
open(os.path.join(H, "face-data.js"), "w", encoding="utf-8").write("window.FACE=" + json.dumps(out, ensure_ascii=False) + ";\n")
print(len(makers), out["source"], out["held"])
