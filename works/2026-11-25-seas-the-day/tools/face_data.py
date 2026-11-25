"""Write face-data.js for index.html from results.json, people/people.json and makings/.

Harbours: the people's first 60 SCORE draws (in draw order) and each arm's 60 final names.
The harbours' order on the page is fixed by seed 187 and written here, not chosen in the browser.
"""
import json, os, random, sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from features import norm  # noqa: E402

W = os.path.join(here, "..")
res = json.load(open(os.path.join(W, "results.json")))
freq = json.load(open(os.path.join(W, "people", "freq.json")))
rows = json.load(open(os.path.join(W, "people", "people.json")))["rows"][:200]

people_all = [{"n": r["name"].strip().upper(), "f": freq[norm(r["name"])]} for r in rows]
harb = {"people": people_all[:60]}
makers = sorted(res["per_maker"])
for a in "EDG":
    harb[a] = [{"n": n, "f": freq[norm(n)], "m": m} for m in makers if m.startswith(a)
               for n in res["per_maker"][m]["names"]]
order = ["people", "E", "D", "G"]
random.Random(187).shuffle(order)

paths = []
for m in makers:
    pm = res["per_maker"][m]
    paths.append({"m": m, "v1": pm["v1_median_freq"], "fin": pm["final_median_freq"], "versions": pm["versions"],
                  "v1_ge10": pm["v1_freq_ge10"], "fin_ge10": pm["freq_ge10"]})

prof = res["profiles"]
keep = ["PUN", "PERSON", "SINGLE", "FREQ1", "FREQ0", "FREQ2_9", "FREQ10_99", "FREQ100", "SEAWORD", "FOREIGN",
        "median_freq"]
data = {
    "order": order, "harbours": harb, "ladder": {"people": people_all, "E": harb["E"], "D": harb["D"], "G": harb["G"]},
    "paths": paths, "profiles": {k: {f: prof[k][f] for f in keep} for k in ["people_score", "E", "D", "G"]},
    "v1": {a: {"ge10": prof[a]["v1_FREQ_ge10"], "f0": prof[a]["v1_FREQ0"], "med": prof[a]["v1_median_freq"]}
           for a in "EDG"},
    "after": res["after_estimates_median"], "told": {"PUN": 18.5, "PERSON": 14, "SINGLE": 41, "UNIQUE": 44},
    "d_est": res["predictions"]["P3"]["D_median_estimates"],
    "serenity": {"makers": len([r for r in res["recurring_names"] if r[0] == "SERENITY"][0][1]), "f": freq["SERENITY"]},
    "frame": 176080,
}
open(os.path.join(W, "face-data.js"), "w").write("window.SEAS=" + json.dumps(data, separators=(",", ":")) + ";\n")
print("order", order)
