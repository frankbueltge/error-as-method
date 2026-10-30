"""Session 164, experiment 44: choose arm U's anchors from arm A's committed ratings, and write the U briefs.

Run only after rooms/A1..A6.txt are committed. The rule was committed in PREDICTIONS.md before any maker ran:
the true key and the false key on which the family's six answers spread most (inclusive IQR of A's six ratings),
M's anchors excluded; ties by the larger range (max - min), then by the family median nearer 3.5, then by key id.
U is told the people's results on those two keys: the places where the practice, without asking anyone, can see
that it is unsure of itself.
Run: python3 anchors_u.py <path to IT_ES_EN_data_final.RData>
"""
import json, statistics as st, sys
from pathlib import Path
import prepare as PR
from score import parse_ratings

HERE = Path(__file__).parent
plan = json.load(open(HERE / "plan.json"))
A = {f"A{j}": parse_ratings((HERE / "rooms" / f"A{j}.txt").read_text(), plan["shown"][f"A{j}"]) for j in range(1, 7)}

def q(v, p):
    return float(st.quantiles(v, n=100, method="inclusive")[p - 1])

stat = {}
for k in plan["keys"]:
    v = [A[m][k["id"]] for m in A]
    stat[k["id"]] = {"iqr": q(v, 75) - q(v, 25), "range": max(v) - min(v), "fam": st.median(v), "true": k["true"]}

def pick(t):
    c = [k for k, s in stat.items() if s["true"] == t and k not in plan["M_anchors"]]
    return min(c, key=lambda k: (-stat[k]["iqr"], -stat[k]["range"], abs(stat[k]["fam"] - 3.5), k))

U = [pick(True), pick(False)]
for j in range(1, 7):
    text, ids = PR.brief(f"U{j}", U)
    (HERE / "briefs" / f"U{j}.txt").write_text(text)
    plan["shown"][f"U{j}"] = ids
plan["U_anchors"] = U
plan["U_anchor_stats"] = {k: stat[k] for k in U}
json.dump(plan, open(HERE / "plan.json", "w"), indent=1, ensure_ascii=False)
print("U anchors", U, {k: stat[k] for k in U})
