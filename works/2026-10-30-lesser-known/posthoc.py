"""Session 164, experiment 44: POST HOC reading, written after results.json existed. Nothing here was predicted.
Run: python3 posthoc.py   (writes posthoc.json)
"""
import json, statistics as st
from pathlib import Path
from score import spearman
HERE = Path(__file__).parent
R = json.load(open(HERE / "results.json")); plan = json.load(open(HERE / "plan.json"))
TEXT = {k["id"]: k["text"] for k in plan["keys"]}
S = [k for k in R["per_key"] if k not in set(R["M_anchors"]) | set(R["U_anchors"])]
pk = R["per_key"]
D = {k: st.mean(x["mean"] for x in pk[k]["D"]) for k in S}
DM = {k: st.mean(x["mean"] for a in "DMU" for x in pk[k][a]) for k in S}
P = {k: pk[k]["people_mean"] for k in S}
err = sorted(S, key=lambda k: DM[k] - P[k])
out = {"describers_all_arms_mean_by_key": {k: round(DM[k], 2) for k in S}}
out["most_below_people"] = [(k, TEXT[k], pk[k]["true"], round(P[k], 2), round(DM[k], 2)) for k in err[:6]]
out["most_above_people"] = [(k, TEXT[k], pk[k]["true"], round(P[k], 2), round(DM[k], 2)) for k in err[-6:]]
# how far the describers' account follows the family's own belief, and the people's
fam = {k: pk[k]["fam"] for k in S}
out["rho_describers_vs_family"] = round(spearman([DM[k] for k in S], [fam[k] for k in S]), 3)
out["rho_people_vs_family"] = round(spearman([P[k] for k in S], [fam[k] for k in S]), 3)
out["rho_describers_vs_people"] = round(spearman([DM[k] for k in S], [P[k] for k in S]), 3)
# slope: describers' mean per step of the family's median, against the people's
def slope(y):
    xs = [fam[k] for k in S]; mx, my = st.mean(xs), st.mean(y[k] for k in S)
    return sum((fam[k] - mx) * (y[k] - my) for k in S) / sum((x - mx) ** 2 for x in xs)
out["slope_describers_per_family_step"] = round(slope(DM), 3)
out["slope_people_per_family_step"] = round(slope(P), 3)
# keys the describers pushed lowest (mean < 3): were the people low there?
low = [k for k in S if DM[k] < 3.0]
out["describers_below_3"] = {"n": len(low), "people_mean_there": round(st.mean(P[k] for k in low), 2) if low else None,
                             "people_mean_elsewhere": round(st.mean(P[k] for k in S if k not in low), 2)}
out["sd_of_key_means"] = {"people": round(st.pstdev(P.values()), 3), "describers": round(st.pstdev(DM.values()), 3),
                          "family": round(st.pstdev(fam.values()), 3)}
json.dump(out, open(HERE / "posthoc.json", "w"), indent=1, ensure_ascii=False)
for k, v in out.items():
    if k != "describers_all_arms_mean_by_key": print(k, v)
