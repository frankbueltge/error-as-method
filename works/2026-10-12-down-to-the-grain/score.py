"""score.py: decides P1-P9 and S121.MARGIN from the two coders' answers exactly as PREDICTIONS.md fixed them,
writes results.json and prints a table. Run: python3 score.py"""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
plan = {p["maker"]: p["grain"] for p in json.load(open(os.path.join(H, "plan.json")))}
B = json.load(open(os.path.join(H, "coder", "B", "answers.json")))
A = json.load(open(os.path.join(H, "coder", "A", "answers.json")))
key = json.load(open(os.path.join(H, "keys", "A.json")))
Am = {key[w]: v for w, v in A.items()}
G = ["G1", "G2", "G3", "G4"]
by = {g: [m for m in sorted(plan) if plan[m] == g] for g in G}
f = lambda m, k: B[m][k]
n = lambda ms, k, v: sum(1 for m in ms if f(m, k) == v)
r = {}
r["P1"] = (n(plan, "B1_decoded", "yes"), n(plan, "B1_decoded", "yes") == 12)
r["P2"] = ({g: n(by[g], "B4_singular", "yes") for g in G}, all(n(by[g], "B4_singular", "yes") >= 2 for g in G) and n(plan, "B4_singular", "yes") >= 9)
low = by["G3"] + by["G4"]
r["P3"] = ({g: n(by[g], "B2_twice_daily", "measured") for g in G}, n(by["G1"], "B2_twice_daily", "measured") >= 2 and n(low, "B2_twice_daily", "measured") == 0)
r["P4"] = (n(low, "B2_twice_daily", "supplied"), n(low, "B2_twice_daily", "supplied") >= 2)
r["P5"] = ({g: n(by[g], "B6_category", "water") for g in G}, n(by["G1"], "B6_category", "water") >= 2 and n(by["G4"], "B6_category", "water") <= 1)
a2 = {g: sum(int(Am[m]["A2"]) for m in by[g]) / 3 for g in G}
r["P6"] = (a2, a2["G1"] >= a2["G2"] >= a2["G3"] >= a2["G4"] and a2["G4"] <= 1)
a3 = sum(1 for m in low if Am[m]["A3"] == "yes")
r["P7"] = (a3, a3 <= 1)
b5 = {g: n(by[g], "B5_second_event", "yes") for g in G}
r["P8"] = (b5, sum(b5.values()) <= 3 and b5["G4"] == 0)
a4 = sum(1 for m in plan if Am[m]["A4"] == "no")
r["P9"] = (a4, a4 >= 11)
nine = by["G2"] + by["G3"] + by["G4"]
pix = n(nine, "B8_units", "pixels")
lab = [m for m in nine if f(m, "B7_named_singular") == "yes" and f(m, "B7_outside") != "yes"]
r["S121.MARGIN"] = ({"pixels_of_9": pix, "units": {m: f(m, "B8_units") for m in nine}, "unflagged_labels": lab},
                    "falsified" if pix < 7 or lab else "held")
r["also"] = {"B3_fortnight": {g: {v: n(by[g], "B3_fortnight", v) for v in ("measured", "supplied", "no")} for g in G},
             "B8_units": {g: [f(m, "B8_units") for m in by[g]] for g in G},
             "B9_stopped": n(plan, "B9_stopped_counting", "yes"),
             "B7_named": {m: f(m, "B7_quote") for m in plan if f(m, "B7_named_singular") == "yes"},
             "A1_singular": {g: sum(1 for m in by[g] if Am[m]["A1"] == "yes") for g in G},
             "A3_yes": [m for m in plan if Am[m]["A3"] == "yes"]}
json.dump(r, open(os.path.join(H, "results.json"), "w"), indent=1, ensure_ascii=False)
for k, v in r.items(): print(k, json.dumps(v, ensure_ascii=False))
