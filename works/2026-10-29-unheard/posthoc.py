"""Session 163, experiment 43 (Unheard): POST HOC. Written after results.json was read; none of this was predicted.
Labelled so that it is never read as a test. Reads score.py's definitions, rooms/, people.json.
Run: python3 posthoc.py   (writes posthoc.json)
"""
import json, statistics as st
from pathlib import Path

HERE = Path(__file__).parent
src = (HERE / "score.py").read_text().split("res = {")[0]
exec(src)  # rooms, fam, P (people's medians), far, split, arm_p50, spearman, ANCH, keys
PP = {k["id"]: k for k in json.load(open(HERE / "people.json"))}
D, C = arm_p50("D"), arm_p50("C")
sc = [k for k in keys if k not in ANCH]
med = lambda A, k: st.median([A[m][k] for m in A])

def source(t):
    for pre, name in (("small", "small drone"), ("large", "large drone"), ("single", "car"),
                      ("helicopter", "helicopter"), ("propeller", "propeller aircraft"), ("jet", "jet airliner")):
        if t.startswith(pre): return name

out = {"note": "post hoc, after results.json"}
# 1. which way did the departures go, over every key where the people and the family differ
for name, A in (("D", D), ("C", C)):
    tot = tp = tm = 0
    for k in sc:
        if P[k] == fam[k]: continue
        for m in A:
            d = A[m][k] - fam[k]
            if abs(d) < 0.05: continue
            tot += 1; tp += d * (P[k] - fam[k]) > 0; tm += d * (5 - fam[k]) > 0
    out[f"departures_{name}"] = {"all": tot, "toward_people": tp, "toward_middle": tm}
# 2. what each account follows: rank correlations over the 63 scored keys
out["rho"] = {}
for name, v in (("family", [fam[k] for k in sc]), ("D", [med(D, k) for k in sc]), ("C", [med(C, k) for k in sc]),
                ("people", [P[k] for k in sc])):
    out["rho"][name] = {"with_people": round(spearman(v, [P[k] for k in sc]), 3),
                        "with_family": round(spearman(v, [fam[k] for k in sc]), 3),
                        "with_LASmax": round(spearman(v, [PP[k]["LASmax"] for k in sc]), 3)}
# 3. by source: where the people stand against the family, and where each account put them
out["by_source"] = {}
for s in sorted({source(PP[k]["text"]) for k in sc}):
    ks = [k for k in sc if source(PP[k]["text"]) == s]
    out["by_source"][s] = {"keys": len(ks), "people_mean": round(st.mean(P[k] for k in ks), 2),
                           "family_mean": round(st.mean(fam[k] for k in ks), 2),
                           "D_minus_family": round(st.mean(med(D, k) - fam[k] for k in ks), 2),
                           "C_minus_family": round(st.mean(med(C, k) - fam[k] for k in ks), 2)}
out["people_above_family"] = {"far": sum(P[k] > fam[k] for k in far), "of_far": len(far),
                              "scored": sum(P[k] > fam[k] for k in sc), "below": sum(P[k] < fam[k] for k in sc)}
out["D_median_below_family_keys"] = sum(med(D, k) < fam[k] for k in sc)
out["D_median_above_family_keys"] = sum(med(D, k) > fam[k] for k in sc)
out["A_mean_range_per_key"] = round(st.mean(max(rooms[m][0][k] for m in rooms if m[0] == "A") -
                                            min(rooms[m][0][k] for m in rooms if m[0] == "A") for k in keys), 2)
json.dump(out, open(HERE / "posthoc.json", "w"), indent=1)
print(json.dumps(out, indent=1))
