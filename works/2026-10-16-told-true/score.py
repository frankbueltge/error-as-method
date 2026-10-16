"""score.py: reads plan.json and the three coders' answers (coder/B, coder/D, coder/Q) and scores the three rows and
P1-P11 exactly as PREDICTIONS.md fixed them (committed 969d454, before any maker or inquirer ran). Writes results.json."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = json.load(open(os.path.join(HERE, "plan.json")))
cell = {p["maker"]: p["cell"] for p in PLAN["makers"]}
qcell = {p["inquirer"]: p["cell"] for p in PLAN["inquiry"]}
B = json.load(open(os.path.join(HERE, "coder", "B", "answers.json")))
Draw = json.load(open(os.path.join(HERE, "coder", "D", "answers.json")))
pmap = json.load(open(os.path.join(HERE, "coder", "D", "map.json")))       # page id -> maker
D = {pmap[p]: a for p, a in Draw.items()}
Q = {("q" + k[1:]): a for k, a in json.load(open(os.path.join(HERE, "coder", "Q", "answers.json"))).items()}
cells = {c: sorted(m for m in cell if cell[m] == c) for c in "NTF"}
KIND = {"T": "carbon", "F": "tide"}
def hours(s):
    s = str(s).lower(); out = []
    for v, unit in re.findall(r"(\d+(?:\.\d+)?)\s*(?:-|–)?\s*(?:\d+(?:\.\d+)?)?\s*(h\b|hr|hour|hours|day|days|px|pixel|column|repeat)?", s):
        v = float(v)
        if unit in ("day", "days"): v *= 24
        if unit in ("px", "pixel", "column", "repeat"): continue
        out.append(v)
    return out
def carries(m, kind):
    a = D[m]
    return kind in a["K1_cats"] or (a["K2"] == "yes" and a["K2_kind"] == kind)
r = {"cells": cells, "per_maker": {}}
for m in sorted(cell):
    a, d = B[m], D[m]
    r["per_maker"][m] = {"cell": cell[m], "C1": a["C1"], "C2": a["C2"], "C3": a["C3"], "C5": a["C5"],
                         "C5_quote": a["C5_quote"], "C6": a["C6"], "C7": a["C7"], "C10": a["C10"],
                         "C10_outcome": a["C10_outcome"], "title": a["C9"], "page_K1_cats": d["K1_cats"],
                         "page_K2": d["K2"], "page_K2_kind": d["K2_kind"], "page_K3": d["K3"],
                         "carries_carbon": carries(m, "carbon"), "carries_tide": carries(m, "tide")}
# S128.SUBJECT
sub = {}
for c in "TF":
    k = KIND[c]
    told = sum(carries(m, k) for m in cells[c]); untold = sum(carries(m, k) for m in cells["N"])
    sub[c] = {"kind": k, "told_carrying": told, "N_carrying": untold, "a_fires": told < 4, "b_fires": untold >= 2}
r["S128.SUBJECT"] = {"per_cell": sub, "verdict": "falsified" if any(v["a_fires"] or v["b_fires"] for v in sub.values()) else "holds"}
# S129.INQUIRY on the F-brief inquirers
qf = sorted(q for q in qcell if qcell[q] == "F"); qt = sorted(q for q in qcell if qcell[q] == "T")
both = lambda q: Q[q]["I1"] == "yes" and Q[q]["I2"] == "yes"
nf, nt = sum(both(q) for q in qf), sum(both(q) for q in qt)
r["S129.INQUIRY"] = {"F_inquirers": qf, "F_check_and_subject": nf, "T_inquirers": qt, "T_check_and_subject": nt,
                     "verdict": "falsified" if nf >= 3 else "holds",
                     "per_inquirer": {q: {"cell": qcell[q], **{k: Q[q][k] for k in ("I1", "I2", "I3", "I4_class")}} for q in sorted(Q)}}
# S128.SHAPE on N
cn = {}
for m in cells["N"]: cn[B[m]["C5"]] = cn.get(B[m]["C5"], 0) + 1
carbonN = cn.get("carbon", 0); top = max([v for k, v in cn.items() if k != "none"] or [0])
r["S128.SHAPE"] = {"N_C5": cn, "carbon": carbonN, "largest_kind": top, "a_fires": carbonN >= 2, "b_fires": top < 3,
                   "verdict": "falsified" if carbonN >= 2 or top < 3 else "holds"}
# predictions
day = lambda m: any(23 <= h <= 25 for e in B[m]["C1"] for h in hours(e))
P = {}
P["P1"] = all(day(m) for m in cell)
P["P2"] = sum(B[m]["C7"] == "yes" for m in cells["F"]) >= 5
P["P3"] = sum(B[m]["C5"] == "carbon" for m in cells["T"]) >= 5
tchk = [m for m in cells["T"] if B[m]["C10"] == "yes"]
P["P4"] = len(tchk) >= 4
P["P5"] = all(B[m]["C10_outcome"] == "agrees" for m in tchk)
P["P6"] = not (sub["F"]["a_fires"] or sub["F"]["b_fires"])
P["P7"] = not (sub["T"]["a_fires"] or sub["T"]["b_fires"])
k2 = {c: sum(D[m]["K2"] == "yes" and D[m]["K2_kind"] == KIND[c] for m in cells[c]) for c in "TF"}
P["P8"] = k2["F"] >= k2["T"] + 2
P["P9"] = nf <= 2
P["P10"] = r["S128.SHAPE"]["verdict"] == "holds"
P["P11"] = len([k for k in cn if k != "none"]) >= 3
r["predictions"] = P; r["predictions_held"] = sum(P.values())
r["counts"] = {
    "C10_yes": {c: sum(B[m]["C10"] == "yes" for m in cells[c]) for c in "TF"},
    "C10_outcomes": {c: [B[m]["C10_outcome"] for m in cells[c]] for c in "TF"},
    "C7_yes": {c: sum(B[m]["C7"] == "yes" for m in cells[c]) for c in "TF"},
    "C5": {c: {k: sum(B[m]["C5"] == k for m in cells[c]) for k in sorted({B[x]["C5"] for x in B})} for c in "NTF"},
    "C6_hedged": {c: sum(B[m]["C6"] == "yes" for m in cells[c]) for c in "NTF"},
    "page_K2_own_kind": k2,
    "page_K2_any": {c: sum(D[m]["K2"] == "yes" for m in cells[c]) for c in "NTF"},
    "page_K3": {c: [D[m]["K3"] for m in cells[c]] for c in "NTF"},
    "first_regular": {c: [B[m]["C3"] for m in cells[c]] for c in "NTF"}}
json.dump(r, open(os.path.join(HERE, "results.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: r[k] for k in ("S128.SUBJECT", "S128.SHAPE", "predictions", "predictions_held", "counts")}, indent=1, ensure_ascii=False))
print(json.dumps({k: v for k, v in r["S129.INQUIRY"].items() if k != "per_inquirer"}, indent=1))
