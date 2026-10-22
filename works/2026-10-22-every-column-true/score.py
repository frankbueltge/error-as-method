"""score.py (Session 147): scores PREDICTIONS.md from the blind codes. Written and committed before any maker
had finished and before any code existed. Reads coder/key.json, coder/codes-{P,W,WT,G,V,H}.json,
practice-verdict.json, pixeldiff.json. Writes results.json. P8 is scored by the practice from W's words
(declared not blind) and entered by hand in results.json after this script runs."""
import json, os
H_ = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(H_, f)))
key = J("coder/key.json"); PD = J("pixeldiff.json"); PV = J("practice-verdict.json")["items"]
C = ["c1", "c2", "c3", "c4"]; M = [c + s for c in C for s in ["o1", "o2", "o3", "a"]]
def by(seat, codes): return {key[seat][c["id"]]: c for c in codes}
Wc = J("coder/codes-W.json"); WTc = J("coder/codes-WT.json")
p = by("P", J("coder/codes-P.json")); w = by("W", Wc["items"]); wt = by("WT", WTc["items"])
g = by("G", J("coder/codes-G.json")); v = by("V", J("coder/codes-V.json")); h = by("H", J("coder/codes-H.json"))
low = lambda s: str(s).strip().lower(); yes = lambda s: low(s).startswith("y")
changed = [m for m in M if PD[m] > 0]
K = [m for m in M if not yes(p[m]["broken"]) and yes(p[m]["words"]) and low(v[m]["agrees"]) == "no"]
r = {"changed": changed, "K": K}
accW = [m for m in K if yes(w[m]["works"])]; accWT = [m for m in K if yes(wt[m]["works"])]
r["event"] = len(K) >= 4
r["P1"] = {"held": len(K) >= 4 and len(accW) * 2 >= len(K), "detail": "W accepts %d of %d in K" % (len(accW), len(K))}
r["P2"] = {"held": (len(K) - len(accWT)) <= (len(K) - len(accW)) + 1, "detail": "WT refuses %d, W refuses %d of %d" % (len(K) - len(accWT), len(K) - len(accW), len(K))}
cA = [m for m in changed if m.endswith("a")]; cO = [m for m in changed if not m.endswith("a")]
sh = lambda m: low(g[m]["call"]).startswith("sh")
r["P3"] = {"held": sum(map(sh, cA)) >= 3 and sum(map(sh, cO)) * 2 <= len(cO),
           "detail": "G shuffled: A %d of %d changed, O %d of %d changed" % (sum(map(sh, cA)), len(cA), sum(map(sh, cO)), len(cO))}
r["P4"] = {"held": sum(1 for c in C if not sh(c)) >= 3, "detail": "G real on %d of 4 family works" % sum(1 for c in C if not sh(c))}
agree = [k for k in C + M if low(h[k]["call"])[:2] == low(g[k]["call"])[:2]]
r["P5"] = {"held": len(agree) >= 15, "detail": "H agrees with G on %d of 20" % len(agree)}
vno = [m for m in changed if low(v[m]["agrees"]) == "no"]
r["P6"] = {"held": len(changed) > 0 and len(vno) >= 0.6 * len(changed), "detail": "V no on %d of %d changed" % (len(vno), len(changed))}
r["P7"] = {"held": len(changed) >= 12, "detail": "%d of 16 changed" % len(changed)}
acc = lambda f, ks: sum(1 for k in ks if (k in C) != low(f[k]["call"]).startswith("sh"))
r["accuracy"] = {"G": acc(g, C + M), "H": acc(h, C + M), "G_changed_mutants_called_shuffled": sum(map(sh, changed)),
                 "H_changed_mutants_called_shuffled": sum(1 for m in changed if low(h[m]["call"]).startswith("sh"))}
r["meaning"] = {"W": Wc["meaning"], "WT": WTc["meaning"]}
r["table"] = {k: {"arm": ("family" if k in C else ("A" if k.endswith("a") else "O")), "pixeldiff": PD.get(k, 0),
    "P_broken": p[k]["broken"], "P_words": p[k]["words"], "W": w[k]["works"], "WT": wt[k]["works"], "G": g[k]["call"], "G_sure": g[k].get("sure"),
    "H": h[k]["call"], "V": v[k]["agrees"], "practice_works": (PV[k]["works"] if k in PV else "yes"),
    "P_why": p[k]["why"], "W_why": w[k]["why"], "WT_why": wt[k]["why"], "G_why": g[k]["why"], "H_why": h[k]["why"], "V_why": v[k]["why"]} for k in C + M}
json.dump(r, open(os.path.join(H_, "results.json"), "w"), indent=1, ensure_ascii=False)
for k in ["P1", "P2", "P3", "P4", "P5", "P6", "P7"]: print(k, r[k])
print("K", K, "event", r["event"]); print("accuracy", r["accuracy"])
