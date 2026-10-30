"""Session 164, experiment 44: write face-data.js for index.html from plan.json, people.json, results.json, posthoc.json.
Run: python3 facedata.py
"""
import json, statistics as st
from pathlib import Path
HERE = Path(__file__).parent
plan = json.load(open(HERE / "plan.json")); P = json.load(open(HERE / "people.json"))
R = json.load(open(HERE / "results.json")); H = json.load(open(HERE / "posthoc.json"))
anch = set(R["M_anchors"]) | set(R["U_anchors"])
keys = []
for k in plan["keys"]:
    i = k["id"]; pk = R["per_key"][i]
    arm = {a: [None if x is None else round(x["mean"], 2) for x in pk[a]] for a in "DMU"}
    keys.append({"id": i, "t": k["text"], "true": k["true"], "anchor": i in anch, "hist": P[i]["hist"],
                 "pm": P[i]["mean"], "pmed": P[i]["median"], "A": pk["A"], "fam": pk["fam"], **arm})
summary = {k: R[k] for k in ("people_gap_true_minus_false", "family_gap", "gap", "mae_mean", "far_placements_beyond_one_step")}
summary.update({k: H[k] for k in ("rho_describers_vs_family", "rho_people_vs_family", "rho_describers_vs_people",
                                  "slope_describers_per_family_step", "slope_people_per_family_step")})
summary["rho_order"] = R["P5_ORDER"]["rho"]; summary["M_anchors"] = R["M_anchors"]; summary["U_anchors"] = R["U_anchors"]
(HERE / "face-data.js").write_text("window.LK=" + json.dumps({"keys": keys, "s": summary}, ensure_ascii=False) + ";\n")
print(len(keys), "keys")
