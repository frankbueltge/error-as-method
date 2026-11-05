"""Session 170: writes face-data.js for index.html from people.json, plan.json and results.json (no download needed).
Also prints the one test the face states: whether the 18 told makers lean nearer the family's own order than the 6 plain
describers do (exact permutation test on the per-maker rho with the A account, all C(24,6) splits)."""
import json, itertools, statistics as st
from pathlib import Path

HERE = Path(__file__).parent
people = json.loads((HERE / "people.json").read_text())
plan = json.loads((HERE / "plan.json").read_text())
res = json.loads((HERE / "results.json").read_text())
import re


def room_vals(mid):
    txt = (HERE / "rooms" / f"{mid}.txt").read_text()
    vals = {int(m.group(1)): float(m.group(2)) for m in re.finditer(r"^\s*(\d+)\s*:\s*(?:mean\s*)?([0-9.]+)", txt, re.M)}
    a = plan["makers"][mid]["arrangement"] - 1
    order = plan["arrangements_all"][a] if mid[0] == "A" else plan["arrangements_scored"][a]
    return {order[i - 1]: v for i, v in vals.items()}


scored = [k["id"] for k in plan["keys"] if k["role"] == "scored"]
contact = [k["id"] for k in plan["keys"] if k["role"] == "contact"]
A = {m: room_vals(m) for m in [f"A{i}" for i in range(1, 7)]}
D = {m: room_vals(m) for m in [f"D{i}" for i in range(1, 7)]}
fam = {k: st.median(A[m][k] for m in A) for k in scored + contact}
acc_d = {k: st.median(D[m][k] for m in D) for k in scored}
told_s = {c: people[plan["shuffle"]["told_S"][c]]["mean"] for c in contact}
told_v = plan["V"]["told_V"]

data = {
    "scored": [dict(id=k, text=people[k]["text"], people=round(people[k]["mean"], 2), raters=people[k]["raters"],
                    own=fam[k], account=round(acc_d[k], 2)) for k in scored],
    "contact": [dict(id=k, text=people[k]["text"], own=fam[k], true=round(people[k]["mean"], 2), shuffled=round(told_s[k], 2),
                     fitted=round(told_v[k], 2)) for k in contact],
    "makers": [dict(id=m, arm=m[0], rp=v["rho_people"], rf=v.get("rho_family"), how=v["how"]) for m, v in res["makers"].items()],
    "arms": res["arms"], "maker_means": res["maker_means"],
}

# permutation test: told makers (B, S, V) vs plain (D) on per-maker rho with the family
rf = {m: v["rho_family"] for m, v in res["makers"].items() if m[0] in "DBSV"}
ids = sorted(rf); told = [m for m in ids if m[0] != "D"]
obs = st.mean(rf[m] for m in told) - st.mean(rf[m] for m in ids if m[0] == "D")
n = ge = 0
for plain in itertools.combinations(ids, 6):
    t = [m for m in ids if m not in plain]
    d = st.mean(rf[m] for m in t) - st.mean(rf[m] for m in plain)
    n += 1; ge += d >= obs - 1e-12
data["lean_test"] = dict(observed_difference=round(obs, 4), splits=n, as_large_or_larger=ge, p=round(ge / n, 5))
(HERE / "face-data.js").write_text("window.FACE = " + json.dumps(data, ensure_ascii=False) + ";\n")
print("lean toward the family: told minus plain", round(obs, 3), "p =", ge, "/", n, "=", round(ge / n, 5))
