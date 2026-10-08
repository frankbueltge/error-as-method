"""score.py -- P1-P8 from looks.json, coder1/, coder2/ and open.json, by the rules in PREDICTIONS.md.
Writes results.json. Nothing here is tuned after the fact; post-hoc readings are marked as such."""
import json, os, statistics
H = os.path.dirname(os.path.abspath(__file__)); J = lambda p: json.load(open(os.path.join(H, p)))
L, c1, k1, c2, k2, oc = J("looks.json"), J("coder1/ratings.json"), J("coder1/key.json"), J("coder2/ratings.json"), J("coder2/key.json"), J("open.json")
arm = {m: r["arm"] for m, r in L.items()}
lookers = [m for m in L if L[m]["looks"] > 0]
O = [m for m in L if arm[m] == "O"]; R = [m for m in L if arm[m] == "R"]; N = [m for m in L if arm[m] == "N"]
res = {}
res["P1"] = {"O_looked": sum(L[m]["looks"] > 0 for m in O), "R_looked": sum(L[m]["looks"] > 0 for m in R)}
res["P1"]["holds"] = res["P1"]["O_looked"] >= 3 and res["P1"]["R_looked"] == 4
res["P2"] = {"N_viewed_picture": [m for m in N if oc[m]["check"] == "PICTURE"], "N_numeric_check": [m for m in N if oc[m]["check"] == "NUMERIC"]}
res["P2"]["holds"] = len(res["P2"]["N_viewed_picture"]) <= 1
looks = sorted(L[m]["looks"] for m in lookers)
res["P3"] = {"looks": {m: L[m]["looks"] for m in lookers}, "median": statistics.median(looks)}
res["P3"]["holds"] = res["P3"]["median"] <= 3
diffs = [d for p in c1.values() for d in p["differences"]]
fin = sum(d["tag"] == "FINISH" for d in diffs)
res["P4"] = {"differences": len(diffs), "FINISH": fin, "FORM": len(diffs) - fin, "share_finish": round(fin / len(diffs), 3)}
res["P4"]["holds"] = res["P4"]["share_finish"] >= 0.75
low = {k1[p]["maker"]: c1[p]["same"] for p in c1 if c1[p]["same"] <= 1}
res["P5"] = {"same_by_maker": {k1[p]["maker"]: c1[p]["same"] for p in c1}, "rated_0_or_1": low}
res["P5"]["holds"] = len(low) <= 1
dc = {k2[f]["maker"]: sum(len(v) for v in c2["defects"][f].values()) for f in k2}
mN = statistics.mean(dc[m] for m in N); mL = statistics.mean(dc[m] for m in O + R)
res["P6"] = {"defects_by_maker": dc, "mean_N": mN, "mean_O_R": mL, "mean_O": statistics.mean(dc[m] for m in O), "mean_R": statistics.mean(dc[m] for m in R)}
res["P6"]["holds"] = mN >= mL + 1.0
groups = [{"name": g["name"], "makers": [k2[f]["maker"] for f in g["members"]]} for g in c2["groups"]]
res["P7"] = {"groups": groups, "largest": max(len(g["makers"]) for g in groups)}
res["P7"]["holds"] = res["P7"]["largest"] >= 5
codes = {m: oc[m]["code"] for m in lookers}
dc_only = [m for m in lookers if codes[m] in ("DEFECT", "CONFIRM")]
res["P8"] = {"codes": codes, "defect_or_confirm": len(dc_only), "of": len(lookers), "surprise": [m for m in lookers if codes[m] == "SURPRISE"]}
res["P8"]["holds"] = len(dc_only) / len(lookers) >= 0.75 and len(res["P8"]["surprise"]) <= 1
form_makers = sorted({k1[p]["maker"] for p in c1 if any(d["tag"] == "FORM" for d in c1[p]["differences"])})
res["T1"] = {"makers_with_a_FORM_change_after_looking": form_makers, "count": len(form_makers)}
res["posthoc"] = {
 "_note": "Not predicted. Read after the scores.",
 "every_look_but_the_last_followed_by_change": all(all(L[m]["changed_after_look"][:-1]) and not L[m]["changed_after_look"][-1] for m in lookers),
 "final_equals_last_look": all(L[m]["final_equals_last_look"] for m in lookers),
 "lookers_with_coder2_defects_in_final": [m for m in lookers if dc[m] > 0],
 "code_lines_mean_N": statistics.mean(L[m]["final_lines"] for m in N),
 "code_lines_mean_lookers": statistics.mean(L[m]["final_lines"] for m in lookers),
 "stone_piles_by_coder2_groups": sum(len(g["makers"]) for g in groups if any(w in g["name"].lower() for w in ("pile", "heap", "stack")))}
res["held"] = [p for p in ["P1","P2","P3","P4","P5","P6","P7","P8"] if res[p]["holds"]]
json.dump(res, open(os.path.join(H, "results.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps(res, indent=1, ensure_ascii=False))
