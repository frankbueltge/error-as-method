"""Writes face-data.js for index.html from people.json, plan.json and results.json (Session 171)."""
import json, re
from pathlib import Path
HERE = Path(__file__).parent
P = json.loads((HERE / "people.json").read_text()); plan = json.loads((HERE / "plan.json").read_text())
res = json.loads((HERE / "results.json").read_text())
scored = [k["id"] for k in plan["keys"] if k["role"] == "scored"]
words = [dict(id=k, w=P[k]["word"], es=P[k]["spanish"], l2=round(P[k]["l2"], 2), nat=round(P[k]["native"], 2),
              tail="lo" if P[k]["tail"].startswith("L2 below") else "hi",
              **{a: res["accounts"][a][k] for a in "ADBSR"}) for k in scored]
how = {a: [res["makers"][f"{a}{i}"]["how"] for i in range(1, 7)] for a in "ADBSR"}
arms = {a: dict(rho_l2=res["arms"][a]["rho_l2"], rho_nat=res["arms"][a]["rho_native"], sd=res["arms"][a]["sd_medians"],
                named=res["noticed_mine"].get(a)) for a in "ADBSR"}
quiz = ["mattress", "shelf", "jug", "fence", "definition", "revolution", "idol", "geology"]
qz = []
for w in quiz:
    k = next(x for x in P if not x.startswith("_") and P[x]["word"] == w)
    qz.append(dict(w=w, es=P[k]["spanish"], l2=round(P[k]["l2"], 2), nat=round(P[k]["native"], 2),
                   A=res["accounts"]["A"].get(k) if k in scored else None))
(HERE / "face-data.js").write_text("window.FACE = " + json.dumps(dict(words=words, how=how, arms=arms, quiz=qz,
    rho_publics=res["publics"]["rho_l2_native"]), ensure_ascii=False) + ";\n")
print("ok", len(words), [q["A"] for q in qz])
