"""facedata.py: writes face-data.js for index.html from materials/hourly.json, materials/holds.json, plan.json,
coder/B/answers.json and results.json. Nothing in it is typed by hand except the short labels of the kinds."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
h = json.load(open(os.path.join(HERE, "materials", "hourly.json")))
holds = json.load(open(os.path.join(HERE, "materials", "holds.json")))
plan = json.load(open(os.path.join(HERE, "plan.json")))
A = json.load(open(os.path.join(HERE, "coder", "B", "answers.json")))
R = json.load(open(os.path.join(HERE, "results.json")))
def label(m):
    q = A[m]["C5_quote"].lower()
    if "humid" in q: return "relative humidity?"
    if "biological" in q or "body temperature" in q: return "an animal's body clock?"
    if A[m]["C5"] == "none": return "cannot tell"
    return A[m]["C5"]
makers = [{"m": p["maker"], "cell": p["cell"], "title": A[p["maker"]]["C9"], "named": label(p["maker"]),
           "period": A[p["maker"]]["C2"], "doubted": A[p["maker"]]["C7"] == "yes",
           "kindWords": R["post_hoc"]["per_maker"][p["maker"]]["kind_words_in_page_or_note"],
           "tideClock": R["post_hoc"]["per_maker"][p["maker"]]["draws_or_names_the_tide_clock_in_page"]} for p in plan]
out = {"h": h["h_nT"], "start": h["start_utc"], "amp": holds["record_amp_nT"], "makers": makers,
       "rows": {k: R[k]["verdict"] for k in ("S124.TABLE", "S125.GIVENKIND", "S126.SELECT")},
       "pred": R["predictions"]}
open(os.path.join(HERE, "face-data.js"), "w").write("window.FACE = " + json.dumps(out, separators=(",", ":")) + ";\n")
print(len(out["h"]), [ (x["m"], x["cell"], x["named"]) for x in makers])
