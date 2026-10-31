"""Session 165 (experiment 45, Paired): write face-data.js for index.html from people.json, plan.json, results.json and rooms/.
Run: python3 facedata.py
"""
import json, statistics as st
from pathlib import Path
from score import load, field

HERE = Path(__file__).parent
plan, P, S, A, R, room = load()
res = json.load(open(HERE / "results.json"))
C = [k["id"] for k in plan["keys"] if k["role"] == "contact"]
told_S = plan["shuffle"]["told_S"]
arm = lambda a, k: round(st.mean(R[f"{a}{j}"][k]["mean"] for j in range(1, 7)), 2)
data = {
    "scored": [{"id": k, "species": P[k]["species"], "url": P[k]["url"], "people": round(P[k]["mean"], 2), "n": P[k]["n"],
                "self": st.median(A[m][k] for m in A), "selfAll": [A[m][k] for m in A],
                "D": arm("D", k), "B": arm("B", k), "S": arm("S", k)} for k in S],
    "contact": [{"id": k, "species": P[k]["species"], "url": P[k]["url"], "people": round(P[k]["mean"], 2),
                 "toldS": round(P[told_S[k]]["mean"], 2)} for k in C],
    "how": {m: field(room(m), "HOW") for m in ["S1", "S2", "S3", "S4", "S5", "S6", "B2", "D1"]},
    "arms": res["arms"], "rhoFamily": res["rho_family_people"],
}
(HERE / "face-data.js").write_text("window.PAIRED = " + json.dumps(data, ensure_ascii=False) + ";\n")
print(len(data["scored"]), len(data["contact"]))
