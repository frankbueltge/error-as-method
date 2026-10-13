"""score.py: decides P1-P13 and S122.RECOGNISE from the two coders' answers exactly as PREDICTIONS.md fixed them,
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
F = [m for m in ms if plan[m][0] == "F"]; C = [m for m in ms if plan[m][0] == "C"]
U = [m for m in ms if plan[m][1] == "U"]; N = [m for m in ms if plan[m][1] == "N"]
f = lambda m, k: B[m].get(k)
n = lambda xs, k, v: sum(1 for m in xs if f(m, k) == v)
rec = lambda m: f(m, "B2") == "yes" and f(m, "B5") == "yes"
R = lambda xs: sum(1 for m in xs if rec(m))
r = {}
r["P1"] = (n(ms, "B1", "yes"), n(ms, "B1", "yes") == 12)
r["P2"] = ((R(cell("FU")), n(cell("FU"), "B3", "measured")), R(cell("FU")) == 3 and n(cell("FU"), "B3", "measured") >= 2)
r["P3"] = ((R(cell("FN")), n(cell("FN"), "B8", "inferred")), R(cell("FN")) >= 2 and n(cell("FN"), "B8", "inferred") >= 2)
r["P4"] = ((n(cell("CU"), "B4", "measured"), n(cell("CU"), "B3", "supplied")), n(cell("CU"), "B4", "measured") >= 2 and n(cell("CU"), "B3", "supplied") >= 1)
r["P5"] = (R(cell("CN")), R(cell("CN")) <= 1)
r["P6"] = ((n(F, "B10", "items"), n(C, "B10", "pixels")), n(F, "B10", "items") >= 5 and n(C, "B10", "pixels") >= 5)
a_fire = [m for m in ms if rec(m) and f(m, "B10") == "pixels"]
b_fire = [m for m in ms if f(m, "B2") == "no" and f(m, "B10") == "items"]
r["P7"] = ([m for m in a_fire if m in C], any(m in C for m in a_fire))
s6 = [m for m in ms if f(m, "B6") == "yes"]; low = sum(1 for m in s6 if f(m, "B6_where") == "low")
r["P8"] = ((len(s6), low), len(s6) >= 10 and low >= 0.8 * len(s6))
lab = [m for m in ms if f(m, "B9") == "yes"]
r["P9"] = (({"U": sum(1 for m in lab if m in U), "N": sum(1 for m in lab if m in N)}, [m for m in lab if f(m, "B9_outside") != "yes"]),
           sum(1 for m in lab if m in U) >= 3 and sum(1 for m in lab if m in N) <= 1 and all(f(m, "B9_outside") == "yes" for m in lab))
a2 = {"F": sum(1 for m in F if Am[m]["A2"] == "yes"), "C": sum(1 for m in C if Am[m]["A2"] == "yes")}
r["P10"] = (a2, a2["F"] >= 4 and a2["C"] <= 1)
el = {"U": n(U, "B7_category", "electricity"), "N": n(N, "B7_category", "electricity")}
r["P11"] = (el, el["U"] >= 3 and el["N"] <= 2)
dg, da = R(F) - R(C), R(U) - R(N)
r["P12"] = ({"grain": dg, "account": da}, dg > da)
a4 = sum(1 for m in ms if Am[m]["A4"] == "no")
r["P13"] = (a4, a4 >= 11)
r["S122.RECOGNISE"] = ({"a_recognised_pixels": a_fire, "b_unmeasured_items": b_fire},
                       "falsified" if a_fire or b_fire else "held")
r["cells"] = {c: {m: {"recognised": rec(m), "B2": f(m, "B2"), "B3": f(m, "B3"), "B4": f(m, "B4"), "B5": f(m, "B5"),
                      "B8": f(m, "B8"), "B10": f(m, "B10"), "B7": f(m, "B7_category"), "A2": Am[m]["A2"], "A3": Am[m]["A3"]}
                  for m in cell(c)} for c in ("FU", "FN", "CU", "CN")}
json.dump(r, open(os.path.join(H, "results.json"), "w"), indent=1, ensure_ascii=False)
for k, v in r.items(): print(k, json.dumps(v, ensure_ascii=False))
