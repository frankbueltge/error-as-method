"""POST-HOC, written after results.json was read (Session 159). Not a prediction; nothing here decides a row.

1. Shift: on each key where median(A) and median(people) differ by >= 0.5 (the fixed rule), how far did the
   describers' pooled median P travel from A's centre toward the people's?  s = (P - A) / (people - A);
   0 = stayed on the family's centre, 1 = reached the people's. Same for O.
2. Direction: on how many of 67 keys is median(A) below the people's, above, equal?
3. Rank agreement (Spearman, ties averaged) across the 67 foods between the people's medians and A's, P's, O's.
4. The refusal: how many arm-A makers gave one value to every food, and how many arm-O makers said in HOW that
   some instances would default to the neutral 5.
"""
import json, re
from pathlib import Path
import numpy as np
HERE = Path(__file__).parent
r = json.loads((HERE / "results.json").read_text())
K = r["keys"]
def rank(v):
    v = np.asarray(v, float); o = v.argsort(); rk = np.empty(len(v)); rk[o] = np.arange(len(v))
    for x in np.unique(v): rk[v == x] = rk[v == x].mean()
    return rk
def spearman(a, b): return float(np.corrcoef(rank(a), rank(b))[0, 1])
out = {}
div = [k for k in K if abs(k["median"]["A"] - k["median"]["people"]) >= 0.5]
for arm in "PO":
    s = [(k["median"][arm] - k["median"]["A"]) / (k["median"]["people"] - k["median"]["A"]) for k in div]
    out[f"shift_{arm}"] = {"mean": round(float(np.mean(s)), 3), "median": round(float(np.median(s)), 3),
                           "n_reached_half_way": int(sum(x >= 0.5 for x in s)), "n": len(s)}
out["direction_A_vs_people"] = {"below": sum(k["median"]["A"] < k["median"]["people"] for k in K),
                                "above": sum(k["median"]["A"] > k["median"]["people"] for k in K),
                                "equal": sum(k["median"]["A"] == k["median"]["people"] for k in K)}
pm = [k["median"]["people"] for k in K]
out["spearman_with_people"] = {a: round(spearman(pm, [k["median"][a] for k in K]), 3) for a in "APO"}
out["spearman_A_P"] = round(spearman([k["median"]["A"] for k in K], [k["median"]["P"] for k in K]), 3)
flat = [m for m in r["rooms"] if m[0] == "A" and len({k["A_raw"][int(m[1:]) - 1] for k in K}) == 1]
out["A_one_value_for_all"] = flat
out["O_HOW_mentions_default_5"] = [m for m, v in r["rooms"].items() if m[0] == "O" and re.search(r"default|disclaim", v["HOW"] or "")]
mean_people = float(np.mean([np.mean(k["people_raw"]) for k in K]))
mean_A = float(np.mean([np.mean([x for x in k["A_raw"] if x is not None]) for k in K]))
out["grand_mean"] = {"people": round(mean_people, 3), "A": round(mean_A, 3)}
(HERE / "posthoc.json").write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps(out, indent=1))
