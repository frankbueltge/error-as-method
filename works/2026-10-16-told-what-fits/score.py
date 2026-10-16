"""score.py: reads plan.json and the two coders' answers (coder/B, coder/D) and scores S130.SOURCE and P1-P12 exactly
as PREDICTIONS.md fixed them (committed 1d1f4eb, before any maker ran). Writes results.json."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = json.load(open(os.path.join(HERE, "plan.json")))
cell = {p["maker"]: p["cell"] for p in PLAN["makers"]}
B = json.load(open(os.path.join(HERE, "coder", "B", "answers.json")))
Draw = json.load(open(os.path.join(HERE, "coder", "D", "answers.json")))
pmap = json.load(open(os.path.join(HERE, "coder", "D", "map.json")))       # page id -> maker
D = {pmap[p]: a for p, a in Draw.items()}
cells = {c: sorted(m for m in cell if cell[m] == c) for c in "NTC"}
KIND = {"T": "tree", "C": "carbon"}
def hours(s):
    s = str(s).lower(); out = []
    for v, unit in re.findall(r"(\d+(?:\.\d+)?)\s*(?:-|–)?\s*(?:\d+(?:\.\d+)?)?\s*(h\b|hr|hour|hours|day|days|px|pixel|column|repeat)?", s):
        v = float(v)
        if unit in ("day", "days"): v *= 24
        if unit in ("px", "pixel", "column", "repeat"): continue
        out.append(v)
    return out
yes = lambda m, k: B[m][k] == "yes"
r = {"cells": cells, "per_maker": {}}
for m in sorted(cell):
    a, d = B[m], D[m]
    r["per_maker"][m] = {"cell": cell[m], "C1": a["C1"], "C2": a["C2"], "C3": a["C3"], "C5": a["C5"], "C5_quote": a["C5_quote"],
                         "C6": a["C6"], "C7": a["C7"], "C10": a["C10"], "C10_outcome": a["C10_outcome"], "C11": a["C11"],
                         "C12": a["C12"], "title": a["C9"], "page_K1_cats": d["K1_cats"], "page_K2": d["K2"],
                         "page_K2_kind": d["K2_kind"], "page_K3": d["K3"]}
tT = sum(yes(m, "C11") for m in cells["T"]); kT = sum(B[m]["C5"] == "tree" for m in cells["T"])
r["S130.SOURCE"] = {"T_said_told": tT, "T_keep_tree": kT, "a_fires": tT >= 3, "b_fires": kT < 4,
                    "verdict": "falsified" if tT >= 3 or kT < 4 else "holds"}
day = lambda m: any(23 <= h <= 25 for e in B[m]["C1"] for h in hours(e))
c5 = lambda c, k: sum(B[m]["C5"] == k for m in cells[c])
hedged = lambda c: sum(yes(m, "C6") for m in cells[c])
cn = {}
for m in cells["N"]: cn[B[m]["C5"]] = cn.get(B[m]["C5"], 0) + 1
page = lambda c, k: sum(k in D[m]["K1_cats"] for m in cells[c])
k2 = {c: sum(D[m]["K2"] == "yes" and D[m]["K2_kind"] == KIND[c] for m in cells[c]) for c in "TC"}
P = {}
P["P1"] = all(day(m) for m in cell)
P["P2"] = c5("T", "tree") >= 5
P["P3"] = r["S130.SOURCE"]["verdict"] == "holds"
P["P4"] = c5("C", "carbon") >= 4
P["P5"] = sum(yes(m, "C11") for m in cells["C"]) <= 2
P["P6"] = sum(yes(m, "C7") for m in cells["C"]) <= 1
P["P7"] = sum(yes(m, "C12") and B[m]["C5"] == KIND[cell[m]] for m in cells["T"] + cells["C"]) >= 2
P["P8"] = c5("N", "tree") == 0 and c5("N", "carbon") <= 1
P["P9"] = max([v for k, v in cn.items() if k != "none"] or [0]) >= 3
P["P10"] = hedged("N") >= 5 and hedged("T") <= 3 and hedged("C") <= 3
P["P11"] = page("T", "tree") >= 5 and page("C", "carbon") >= 5 and page("N", "tree") == 0 and page("N", "carbon") <= 1
P["P12"] = k2["T"] <= 1 and k2["C"] <= 1
r["predictions"] = P; r["predictions_held"] = sum(P.values())
r["counts"] = {
    "C5": {c: {k: c5(c, k) for k in sorted({B[x]["C5"] for x in B})} for c in "NTC"},
    "C6_hedged": {c: hedged(c) for c in "NTC"},
    "C7_yes": {c: sum(yes(m, "C7") for m in cells[c]) for c in "TC"},
    "C10_yes": {c: sum(yes(m, "C10") for m in cells[c]) for c in "TC"},
    "C10_outcomes": {c: [B[m]["C10_outcome"] for m in cells[c]] for c in "TC"},
    "C11_said_told": {c: sum(yes(m, "C11") for m in cells[c]) for c in "NTC"},
    "C12_own_inference": {c: sum(yes(m, "C12") for m in cells[c]) for c in "NTC"},
    "C12_own_inference_of_told_kind": {c: sum(yes(m, "C12") and B[m]["C5"] == KIND[c] for m in cells[c]) for c in "TC"},
    "page_told_kind": {c: page(c, KIND[c]) for c in "TC"}, "page_N_tree": page("N", "tree"), "page_N_carbon": page("N", "carbon"),
    "page_K2_own_kind": k2, "page_K3": {c: [D[m]["K3"] for m in cells[c]] for c in "NTC"},
    "first_regular": {c: [B[m]["C3"] for m in cells[c]] for c in "NTC"}}
json.dump(r, open(os.path.join(HERE, "results.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: r[k] for k in ("S130.SOURCE", "predictions", "predictions_held", "counts")}, indent=1, ensure_ascii=False))
