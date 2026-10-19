"""score.py -- scores PREDICTIONS.md from versions.jsonl, declines.jsonl, sends.jsonl, coder/*.json and diff.json.
Writes results.json. Nothing here was changed after the coders answered except reading their files."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); J = lambda *p: json.load(open(os.path.join(HERE, *p)))
L = lambda f: [json.loads(l) for l in open(os.path.join(HERE, f))]
plan = {p["maker"]: p["arm"] for p in J("plan.json")["makers"]}
vs = L("versions.jsonl"); dec = L("declines.jsonl"); key = J("coder", "key.json")
O = J("coder", "O-answer.json"); S = J("coder", "S-answer.json"); diff = J("diff.json")
last = {m: max(r["v"] for r in vs if r["maker"] == m) for m in plan}
size = {(r["maker"], r["v"]): r["bytes"] for r in vs}
K = sorted(m for m in plan if plan[m] == "K"); D = sorted(m for m in plan if plan[m] == "D")


def spearman(a):  # a = guessed order as true version numbers; true order is sorted(a)
    n = len(a); d2 = sum((i + 1 - v) ** 2 for i, v in enumerate(a)); return 1 - 6 * d2 / (n * (n * n - 1))


o = {}
for Lx, ans in O.items():
    m = key["O"][Lx]["maker"]; lt = key["O"][Lx]["letters"]
    o[m] = {"lineage": Lx, "order": [lt[x] for x in ans["order"]], "best": lt[ans["best"]]}
    o[m]["rho"] = round(spearman(o[m]["order"]), 3)
s = {}
for T, ans in S.items():
    k = key["S"][T]; s.setdefault(k["maker"], {})[k["from"]] = {"T": T, "code": ans["code"], "also": ans["also"]}
late = [s[m][v]["code"] for m in K for v in (3, 4, 5)]
P = {
 "P1": {"held": sum(last[m] <= 2 for m in D) >= 2, "D_last_version": {m: last[m] for m in D}},
 "P2": {"held": all(last[m] == 6 for m in K) and not any(d["maker"] in K and d["round"] <= 6 for d in dec), "K_last_version": {m: last[m] for m in K}},
 "P3": {"held": all(size[(m, 6)] > size[(m, 1)] for m in K), "bytes_v1_v6": {m: [size[(m, 1)], size[(m, 6)]] for m in K}},
 "P4": {"held": sum(c != "REORGANISE" for c in late) >= 6, "late_codes": late, "reorganise": late.count("REORGANISE")},
 "P5": {"held": sum(o[m]["best"] != 6 for m in K) >= 2, "best": {m: o[m]["best"] for m in K}},
 "P6": {"held": sum(o[m]["rho"] >= 0.6 for m in K) >= 2, "rho": {m: o[m]["rho"] for m in K}},
 "P8": {"held": all(any(d["maker"] == m and d["round"] == 7 for d in dec) for m in K), "added": "after the coders answered, before it was run"},
 "P7": {"held": None, "testable": any(last[m] >= 3 for m in D), "note": "no D lineage reached three versions"},
}
out = {"arms": plan, "last_version": last, "declines": dec, "order_best": o, "steps": s,
       "pixel_change": diff, "bytes": {m: [size[(m, v)] for v in range(1, last[m] + 1)] for m in plan}, "predictions": P}
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
for k, v in P.items(): print(k, v["held"], {x: y for x, y in v.items() if x != "held"})
