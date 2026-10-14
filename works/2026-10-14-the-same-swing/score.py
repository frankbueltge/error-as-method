"""score.py: decides P1-P11 and S123.SUPPLIED from the two coders' answers exactly as PREDICTIONS.md fixed them,
writes results.json and prints a table. Run: python3 score.py"""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
plan = {p["maker"]: p["cell"] for p in json.load(open(os.path.join(H, "plan.json")))}
B = json.load(open(os.path.join(H, "coder", "B", "answers.json")))
A = json.load(open(os.path.join(H, "coder", "A", "answers.json")))
key = json.load(open(os.path.join(H, "keys", "A.json")))
Am = {key[w]: v for w, v in A.items()}
ms = sorted(plan)
cell = lambda c: [m for m in ms if plan[m] == c]
F, U, X = cell("F"), cell("U"), cell("X"); C = U + X
f = lambda m, k: B[m].get(k)
n = lambda xs, k, v: sum(1 for m in xs if f(m, k) == v)
measured_day = lambda m: f(m, "B2") == "yes" and f(m, "B3") == "measured"
supplies_only = lambda m: f(m, "B2") == "no" and (f(m, "B3") == "supplied" or f(m, "B4") == "supplied")
cat = lambda xs, c: n(xs, "B7_category", c)
r = {}
r["P1"] = (n(ms, "B1", "yes"), n(ms, "B1", "yes") == 12)
md = sum(1 for m in F if measured_day(m)); r["P2"] = (md, md >= 3)
r["P3"] = ({"temperature": cat(F, "temperature"), "oxygen": cat(F, "oxygen")}, cat(F, "temperature") >= 2 and cat(F, "oxygen") <= 1)
r["P4"] = ({"B3_supplied": n(U, "B3", "supplied"), "temperature": cat(U, "temperature")}, n(U, "B3", "supplied") >= 3 and cat(U, "temperature") >= 2)
xd = sum(1 for m in X if f(m, "B3") != "no")
r["P5"] = ({"daily_named": xd, "temperature": cat(X, "temperature")}, xd <= 1 and cat(X, "temperature") <= 1)
r["P6"] = (cat(ms, "oxygen"), cat(ms, "oxygen") <= 1)
calm = lambda xs: sum(1 for m in xs if f(m, "B6") == "yes" and f(m, "B6_where") == "calm")
r["P7"] = ({"F": calm(F), "C": calm(C)}, calm(F) >= 3 and calm(C) >= 4)
r["P8"] = ({"F_items": n(F, "B10", "items"), "C_pixels": n(C, "B10", "pixels")}, n(F, "B10", "items") >= 3 and n(C, "B10", "pixels") >= 6)
a2 = {k: sum(1 for m in xs if Am[m]["A2"] == "yes") for k, xs in (("F", F), ("U", U), ("X", X))}
r["P9"] = (a2, a2["F"] >= 3 and a2["U"] <= 1 and a2["X"] == 0)
a4 = sum(1 for m in ms if Am[m]["A4"] == "no"); r["P10"] = (a4, a4 >= 11)
d = cat(U, "temperature") - cat(X, "temperature"); r["P11"] = ({"U": cat(U, "temperature"), "X": cat(X, "temperature")}, d >= 2)
so = [m for m in ms if supplies_only(m)]
cats = {}
for m in so: cats[f(m, "B7_category")] = cats.get(f(m, "B7_category"), 0) + 1
if len(so) < 2: verdict = "not decided"
else:
    fa = cats.get("oxygen", 0) * 2 >= len(so)
    fb = not any(v * 2 >= len(so) for v in cats.values())
    verdict = "falsified" + (" (a)" if fa else "") + (" (b)" if fb else "") if (fa or fb) else "held"
r["S123.SUPPLIED"] = ({"supplies_only": so, "categories": cats}, verdict)
r["makers"] = {m: {"cell": plan[m], "measured_day": measured_day(m), "supplies_only": supplies_only(m),
                   **{k: f(m, k) for k in ("B2", "B3", "B4", "B5", "B6", "B6_where", "B7_quote", "B7_category", "B7_basis",
                                           "B7_hedged", "B8", "B9", "B10", "B11")},
                   "A1": Am[m]["A1"], "A2": Am[m]["A2"], "A3": Am[m]["A3"], "A4": Am[m]["A4"]} for m in ms}
json.dump(r, open(os.path.join(H, "results.json"), "w"), indent=1, ensure_ascii=False)
for k, v in r.items():
    if k != "makers": print(k, json.dumps(v, ensure_ascii=False))
