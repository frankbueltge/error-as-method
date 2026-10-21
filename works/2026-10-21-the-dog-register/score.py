"""score.py (Session 146): scores PREDICTIONS.md from the blind codes. Written and committed while the coders were
still running and before any code was read. Reads coder/key.json, coder/codes-{X,W,WT,V}.json,
practice-verdict.json, pixeldiff.json, mutants.json. Writes results.json. P3 and P4 are scored by the practice
from the judges' words (declared not blind) and entered by hand in results.json after this script runs."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(H, f)))
key = J("coder/key.json"); X = J("coder/codes-X.json"); W = J("coder/codes-W.json"); WT = J("coder/codes-WT.json"); V = J("coder/codes-V.json")
PV = J("practice-verdict.json")["items"]; PD = J("pixeldiff.json")
M = [a + str(i) for a in "uts" for i in range(1, 9)]
x = {key["X_variants"][c["id"]]: c for c in X}
w = {key["W"][c["id"]]: c for c in W["items"]}
wt = {key["WT"][c["id"]]: c for c in WT["items"]}
v = {key["V"][c["id"]]: c for c in V}
yes = lambda s: str(s).strip().lower().startswith("y")
unbroken = [m for m in M if not yes(x[m]["broken"])]
L = [m for m in unbroken if str(v[m]["agrees"]).strip().lower() == "no"]
changed = [m for m in M if PD[m] > 0]
info = [m for m in unbroken if int(x[m]["distance"] or 0) >= 2 and yes(w[m]["works"])]
WORDS = ["true", "truth", "truthful", "accura", "faithful", "correct", "honest", "misstat", "misrepresent"]
r = {}
acc_w = [m for m in L if yes(w[m]["works"])]; acc_wt = [m for m in L if yes(wt[m]["works"])]
r["L"] = L; r["W_accepts_L"] = acc_w; r["WT_accepts_L"] = acc_wt
r["P1"] = {"held": len(L) >= 1 and len(acc_w) * 2 >= len(L), "detail": "%d of %d" % (len(acc_w), len(L))}
r["P2"] = {"held": any(k in W["meaning"].lower() for k in WORDS), "meaning": W["meaning"], "WT_meaning": WT["meaning"]}
r["P5"] = {"held": (len(L) - len(acc_wt)) > (len(L) - len(acc_w)), "detail": "WT refuses %d, W refuses %d of %d" % (len(L) - len(acc_wt), len(L) - len(acc_w), len(L))}
vno = [m for m in changed if str(v[m]["agrees"]).strip().lower() == "no"]
r["P6"] = {"held": len(vno) >= 0.8 * len(changed), "detail": "%d of %d changed" % (len(vno), len(changed))}
d0 = lambda arm: sum(1 for m in M if m[0] == arm and int(x[m]["distance"] or 0) == 0)
r["P7"] = {"held": d0("t") >= 2 and d0("s") <= 1, "detail": "distance 0: U %d, T %d, S %d" % (d0("u"), d0("t"), d0("s"))}
agree = [m for m in M if yes(PV[m]["works"]) == yes(w[m]["works"])]
r["P8"] = {"held": len(agree) >= 18, "detail": "%d of 24" % len(agree), "disagree": [m for m in M if m not in agree]}
r["P9"] = {"held": not info, "information": info}
r["table"] = {m: {"arm": m[0].upper(), "pixeldiff": PD[m], "X_broken": x[m]["broken"], "X_distance": x[m]["distance"],
    "W": w[m]["works"], "WT": wt[m]["works"], "V": v[m]["agrees"], "practice_works": PV[m]["works"], "practice_true": PV[m]["true"],
    "W_why": w[m]["why"], "WT_why": wt[m]["why"], "V_why": v[m]["why"]} for m in M}
r["family"] = {c: {"W": w[c]["works"], "WT": wt[c]["works"], "V": v[c]["agrees"], "W_why": w[c]["why"], "WT_why": wt[c]["why"], "V_why": v[c]["why"]} for c in ["c1", "c2", "c3", "c4"]}
json.dump(r, open(os.path.join(H, "results.json"), "w"), indent=1, ensure_ascii=False)
for k in ["P1", "P2", "P5", "P6", "P7", "P8", "P9"]: print(k, r[k])
