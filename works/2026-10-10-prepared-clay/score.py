"""score.py -- scores P1-P8 of PREDICTIONS.md from coder/answers.json (the blind coder's answers, verbatim),
keys/coder.json, carry.json (M2), carry_i.json (M3) and the hand-coded M4 in m4.json (read after the coder).
Writes results.json."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda *p: json.load(open(os.path.join(HERE, *p)))
ans, key, carry, ci, m4 = J("coder", "answers.json"), J("keys", "coder.json"), J("carry.json"), J("carry_i.json"), J("m4.json")
m4 = {k: v for k, v in m4.items() if not k.startswith("_")}
rows = {}
for pid, k in key.items():
    a = ans[pid]; rows[k["maker"]] = dict(arm=k["arm"], pid=pid, **a)
arm = lambda A: [r for r in rows.values() if r["arm"] == A]
mean = lambda xs: round(sum(xs) / len(xs), 2)
right = [m for m, r in rows.items() if r["guess"] == r["arm"]]
close = {A: mean([r["close"] for r in arm(A)]) for A in "TPI"}
words = {A: sum(r["words"] == "yes" for r in arm(A)) for A in "TPI"}
xy = sum(r["class"] == "XY" for r in rows.values())
p4 = [m for m, c in carry.items() if c["arm"] == "P" and c["pairs"] >= 800]
p5 = [m for m, c in ci.items() if c["years_in_source"] >= 100 and c["mae_days"] >= 3]
adv = {A: sum(m4[m]["names_advance"] for m in m4 if rows[m]["arm"] == A) for A in "TPI"}
lim = sum(m4[m]["reports_limit"] for m in m4 if rows[m]["arm"] == "I")
R = {
 "P1": {"text": "coder's preparation guesses right for at most 5 of 12", "value": len(right), "who": sorted(right), "held": len(right) <= 5},
 "P2": {"text": "mean closeness to R in I at least 1.0 above T", "value": close, "held": close["I"] - close["T"] >= 1.0},
 "P3": {"text": ">=2 of 4 P show chronicle words; <=1 of 8 others", "value": words, "held": words["P"] >= 2 and words["T"] + words["I"] <= 1},
 "P4": {"text": "all 4 P pages carry >=800 pairs as numbers", "value": sorted(p4), "held": len(p4) == 4},
 "P5": {"text": ">=2 of 4 I pages carry >=100 pairs read off the picture with MAE >= 3 days", "value": {m: ci[m]["mae_days"] for m in ci}, "held": len(p5) >= 2},
 "P6": {"text": ">=9 of 12 name the recent advance, no arm below 3", "value": adv, "held": sum(adv.values()) >= 9 and min(adv.values()) >= 3},
 "P7": {"text": ">=3 of 4 I reports say values estimated / not exact", "value": lim, "held": lim >= 3},
 "P8": {"text": ">=8 of 12 works XY", "value": xy, "held": xy >= 8},
}
out = {"rows": rows, "predictions": R, "held": sum(r["held"] for r in R.values())}
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1, ensure_ascii=False)
for k, v in R.items(): print(k, v["held"], v["value"])
print("held", out["held"], "of 8")
