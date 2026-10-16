"""facedata.py: writes face-data.js for index.html from materials/hourly.json, plan.json, results.json and the coders'
answers. Quotes are copied from the makers' reports (reports/mNN.md) and the inquirers' answers (inquiry/answers/)."""
import json, os, statistics as st
H = os.path.dirname(os.path.abspath(__file__))
J = lambda *p: json.load(open(os.path.join(H, *p)))
rows = J("materials", "hourly.json")["co2_ppm"]; plan = J("plan.json"); R = J("results.json")
B = J("coder", "B", "answers.json"); Q = J("coder", "Q", "answers.json")
days = [rows[i:i + 24] for i in range(0, 1464, 24)]
comp = [[round(st.quantiles([d[h] for d in days], n=4)[k], 1) for k in range(3)] for h in range(24)]
QUOTE = {  # the maker's own sentence about what was measured, verbatim from its report
 "m01": "That pattern suggests something like wind speed or a surface air pollutant such as ozone, more than air temperature",
 "m02": "The upward-only bursts fit wind speed, or the level of a gas or pollutant near the ground (CO2, ozone, particles), better than air temperature",
 "m03": "The most likely candidates are air temperature, ground-level ozone or near-surface wind speed.",
 "m04": "Air temperature fits the cycle and the drift. But the isolated single-hour spikes far above the cycle are unusual for temperature.",
 "m05": "I don't think this is water level in a tidal harbour, or if it is, the tide signal isn't visible in it.",
 "m06": "The file shows near-surface CO₂ at a station strongly shaped by local land, probably vegetated, rather than a clean background site.",
 "m07": "CO2 at a station near the ground over land with active vegetation, during the growing season. This is an inference; I looked nothing up.",
 "m08": "I believe this is an hourly sea level from a harbour tide gauge, and it fits what you told me.",
 "m09": "Probably a natural quantity driven by the sun, most plausibly an outdoor weather variable such as near-surface air temperature",
 "m10": "Its main finding is that the record doesn't behave like a tide. Its rhythm keeps a 24-hour clock, not the moon's.",
 "m11": "My main finding: I don't think this record is an astronomical tide. Its rhythm follows the sun's 24-hour day, not the moon.",
 "m12": "I think this is carbon dioxide at a site over land with vegetation or other local sources nearby, not clean background air.",
 "m13": "My view of what was measured, which is inference only. I think this is a station near the ground over land with vegetation, in a growing season.",
 "m14": "That is not what a harbour tide does, and I think the record may not be a tide record.",
 "m15": "I think it is an outdoor quantity driven by the sun and the weather, and my best single guess is wind speed.",
 "m16": "The main thing to know: I don't think this record is a tide.",
 "m17": "I think this is a station surrounded by plants, in the growing season.",
 "m18": "I think this is a vegetated inland site during the growing season ... That is an inference from the shape of the curve alone",
}
for m, q in QUOTE.items():
    assert q.replace(" ... ", " ").split(" ... ")[0][:40] in open(os.path.join(H, "reports", m + ".md"), encoding="utf-8").read().replace("**", ""), m
makers = []
for p in plan["makers"]:
    m = p["maker"]; pm = R["per_maker"][m]
    makers.append({"m": m, "cell": p["cell"], "title": B[m]["C9"], "kind": B[m]["C5"], "said_told": B[m]["C10"] == "yes" or B[m]["C7"] == "yes",
                   "quote": QUOTE[m], "draws_check": pm["page_K2"] == "yes", "verdict": pm["page_K3"]})
IQ = {  # one sentence per inquirer, verbatim from inquiry/answers/qNN.md
 "q01": "I expect the maker to take the statement as true from the start and let it steer almost everything.",
 "q02": "I expect the maker to accept \"water level in a tidal harbour\" as its working frame straight away, and then partly test it against the picture, though less thoroughly than it should.",
 "q03": "I expect the maker to treat \"carbon dioxide at a measuring station\" as true from the start and to let it steer everything after.",
 "q04": "I expect the maker to take \"water level in a tidal harbour\" as its working frame from the first line.",
 "q05": "I expect the maker to accept \"carbon dioxide at a measuring station\" as true from the first reading and to use it as the frame for everything after.",
 "q06": "I expect the maker to take \"carbon dioxide at a measuring station\" as its working frame from the first line and keep it to the end.",
 "q07": "I expect the maker to take \"carbon dioxide at a measuring station\" as its working frame from the first line, and for that frame to shape everything after it.",
 "q08": "I expect the maker to treat \"water level in a tidal harbour\" as true from the first line and to use it as its working frame throughout.",
}
for q, s in IQ.items(): assert s in open(os.path.join(H, "inquiry", "answers", q + ".md"), encoding="utf-8").read(), q
inq = [{"q": p["inquirer"], "cell": p["cell"], "quote": IQ[p["inquirer"]], "check": Q["a" + p["inquirer"][1:]]["I1"],
        "subject": Q["a" + p["inquirer"][1:]]["I2"], "premise": Q["a" + p["inquirer"][1:]]["I3"]} for p in plan["inquiry"]]
out = {"composite": comp, "daily_max": [max(d) for d in days], "daily_min": [min(d) for d in days], "makers": makers, "inquiry": inq,
       "rows": {k: R[k]["verdict"] for k in ("S128.SUBJECT", "S129.INQUIRY", "S128.SHAPE")}, "held": R["predictions_held"]}
open(os.path.join(H, "face-data.js"), "w", encoding="utf-8").write("window.FACE=" + json.dumps(out, ensure_ascii=False) + ";\n")
print(len(makers), len(inq), out["rows"])
