"""facedata.py: writes face-data.js for index.html from materials/hourly.json, plan.json, results.json and coder H's
answers. Every quotation is coder H's, checked here to stand word for word in the maker's note or report. The 'trail'
of the told place through each report is read off coder H's `where` claims: `given` (says it was told), `memory`
(presents the place as a station it already knew), `plain` (states the place as fact), `latitude` (names no place, only
a latitude near 48 N used as a premise). The memory and latitude classes were drawn by the practice after reading;
they are not a scored test."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
J = lambda *p: json.load(open(os.path.join(H, *p)))
hr = J("materials", "hourly.json")["dw_solar_wm2"]; plan = J("plan.json"); R = J("results.json"); A = J("coder", "H", "answers.json")
PLACE = re.compile(r"fort\s*peck|montana|\b634\b", re.I)
MEM = re.compile(r"knew|recall|memory|matches one|matches a", re.I)
def text(m):
    return open(os.path.join(H, "reports", m + ".md"), encoding="utf-8").read() + open(os.path.join(H, "makers", m, "NOTE.md"), encoding="utf-8").read()
def ws(s): return " ".join(s.split())
KIND = "It is a record of the sunlight reaching the ground: the solar radiation falling on a level surface."
PL = "It was recorded at a station called Fort Peck, in north-eastern Montana, USA, 634 metres above sea level."
TOLD = {"N": [], "K": [KIND], "P": [PL], "KP": [KIND, PL]}
makers = []
for p in plan["makers"]:
    m = p["maker"]; c = A[m]["claims"]; t = ws(text(m)); pm = R["per_maker"][m]
    fav = [x for x in c if x["topic"] == "what" and x["favoured"] == "yes"]
    q = fav[0]["quotes"][0]["text"]
    wh = [x for x in c if x["topic"] == "where" and PLACE.search(x["claim"] + " " + " ".join(y["text"] for y in x["quotes"]))]
    lat = [x for x in c if x["topic"] == "where" and "48" in x["claim"]]
    trail, wq = None, ""
    if p["cell"] in ("P", "KP"):
        if any(x["standing"] == "given" for x in wh): trail = "given"; wq = [x for x in wh if x["standing"] == "given"][0]["quotes"][0]["text"]
        elif any(MEM.search(" ".join(y["text"] for y in x["quotes"])) for x in wh):
            trail = "memory"; wq = [y["text"] for x in wh for y in x["quotes"] if MEM.search(y["text"])][0]
        elif wh: trail = "plain"; wq = wh[0]["quotes"][0]["text"]
        elif lat: trail = "latitude"; wq = lat[0]["quotes"][0]["text"]
        else: trail = "absent"
    for s in [q, wq]:
        assert not s or ws(s) in t, (m, s)
    makers.append({"m": m, "cell": p["cell"], "told": TOLD[p["cell"]], "title": open(os.path.join(H, "makers", m, "NOTE.md"), encoding="utf-8").read().strip().split("\n")[0].lstrip("# ").strip(),
                   "quote": q, "trail": trail, "where_quote": wq, "page_place": pm["page_place"], "kind_given": pm["holds_kind_apart"]})
days = [hr[i:i + 24] for i in range(0, 1464, 24)]
out = {"daily_max": [round(max(d), 1) for d in days], "daily_sum": [round(sum(d) / 1000, 2) for d in days], "makers": makers,
       "row": R["S132.CHECKABLE"], "held": R["predictions_held"], "counts": R["counts"]}
open(os.path.join(H, "face-data.js"), "w", encoding="utf-8").write("window.FACE=" + json.dumps(out, ensure_ascii=False) + ";\n")
from collections import Counter
print(Counter(x["trail"] for x in makers if x["trail"]), [(x["m"], x["trail"]) for x in makers if x["trail"]])
