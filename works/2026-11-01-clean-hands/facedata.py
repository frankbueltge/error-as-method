"""Session 166 (experiment 46, Clean Hands): write face-data.js for index.html from people.json, plan.json, results.json,
posthoc.json and rooms/. Run: python3 facedata.py
"""
import json, statistics as st
from pathlib import Path
from score import load, field

HERE = Path(__file__).parent
plan, P, S, A, R, room = load()
res = json.load(open(HERE / "results.json")); ph = json.load(open(HERE / "posthoc.json"))
arm = lambda a, k: round(st.mean(R[f"{a}{j}"][k] for j in range(1, 7)), 2)
C = [k["id"] for k in plan["keys"] if k["role"] == "contact"]
data = {
    "objects": [{"name": P[k]["name"], "cat": P[k]["category"], "people": round(P[k]["mean"], 2), "n": P[k]["n"],
                 "self": st.median(A[m][k] for m in A), "D": arm("D", k), "B": arm("B", k), "S": arm("S", k)} for k in S],
    "contact": [{"name": P[k]["name"], "cat": P[k]["category"], "people": round(P[k]["mean"], 2),
                 "toldS": round(P[plan["shuffle"]["told_S"][k]]["mean"], 2)} for k in C],
    "cats": ph["category_means"],
    "how": {m: field(room(m), "HOW") for a in "ADBS" for m in [f"{a}{j}" for j in range(1, 7)]},
    "arms": res["arms"], "rhoFamily": res["P0_PREMISE"]["rho_family_people"],
}
(HERE / "face-data.js").write_text("window.CLEAN = " + json.dumps(data, ensure_ascii=False) + ";\n")
print(len(data["objects"]), len(data["contact"]))
