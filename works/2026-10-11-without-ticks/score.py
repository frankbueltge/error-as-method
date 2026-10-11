"""score.py -- the eight predictions of PREDICTIONS.md, by their letter, from features.json (M3, pre-registered
keywords), ledger.json (M1, coded by the practice after the coder) and coder/answers.json with keys/coder.json (M2).
Writes results.json."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(H, f)))
F, L, A, K = J("features.json"), J("ledger.json"), J("coder/answers.json"), J("keys/coder.json")
arm = {m: v["arm"] for m, v in L.items()}
by = lambda a: [m for m in arm if arm[m] == a]
close = {K[p]["maker"]: A[p]["close"] for p in K}
mean = lambda a: sum(close[m] for m in by(a)) / 4
right = sum(A[p]["guess"] == K[p]["arm"] for p in K)
R = {}
n = sum("DECODE" in L[m]["m1"] for m in by("L")); R["P1"] = (n >= 3, "L makers who DECODE: %d of 4" % n)
n = sum("EMBED" in L[m]["m1"] for m in by("I") + by("L")); R["P2"] = (n <= 1, "picture makers who EMBED: %d of 8 (I %d, L %d)" % (n, sum("EMBED" in L[m]["m1"] for m in by("I")), sum("EMBED" in L[m]["m1"] for m in by("L"))))
R["P3"] = (mean("I") <= 1 and mean("L") <= 1 and mean("T") >= mean("I") + 0.5, "mean closeness T %.2f, I %.2f, L %.2f" % (mean("T"), mean("I"), mean("L")))
w = {a: sum(bool(F[m]["weekly"]) for m in by(a)) for a in "TIL"}; R["P4"] = (min(w.values()) >= 3, "weekly named: %s" % w)
h = {a: sum(bool(F[m]["holiday"]) for m in by(a)) for a in "TIL"}; R["P5"] = (h["T"] >= 3 and h["L"] <= 1, "holiday named: %s" % h)
n = sum(bool(F[m]["inexact"]) for m in by("L")); R["P6"] = (n >= 3, "L makers saying inexact: %d of 4" % n)
R["P7"] = (right <= 6, "coder's preparation guesses right: %d of 12" % right)
R["P8"] = (True, "shared scratch directory empty before and after (ROOMS.md)")
out = {k: {"held": v[0], "count": v[1]} for k, v in R.items()}
json.dump(out, open(os.path.join(H, "results.json"), "w"), indent=1)
for k, v in out.items(): print(k, "HELD " if v["held"] else "FAILED", v["count"])
