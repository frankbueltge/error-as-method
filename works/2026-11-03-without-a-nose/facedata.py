"""Session 168: write face-data.js for index.html from plan.json, people.json, results.json and rooms/. Run after score.py."""
import json, re
from pathlib import Path
H = Path(__file__).parent
plan = json.load(open(H / "plan.json")); P = json.load(open(H / "people.json")); R = json.load(open(H / "results.json"))
name = {k["id"]: k["name"] for k in plan["keys"]}
contact = [k["id"] for k in plan["keys"] if k["role"] == "contact"]
told = plan["shuffle"]["told_S"]
how = lambda m: re.search(r"^HOW:\s*(.+)$", (H / "rooms" / f"{m}.txt").read_text(), re.M).group(1).strip()
mean = lambda xs: round(sum(xs) / len(xs), 3)
data = {
    "contact": [{"name": name[k], "true": round(P[k]["mean"], 2), "shuffled": round(P[told[k]]["mean"], 2)} for k in contact],
    "scored": [{"name": v["name"], "people": round(v["people_mean"], 2), "family": v["fam"],
                "D": mean(v["D"]), "B": mean(v["B"]), "S": mean(v["S"])} for v in R["per_key"].values()],
    "how": {m: how(m) for m in [f"{a}{i}" for a in "BS" for i in range(1, 7)]},
    "arms": R["arms"], "rho_family_people": R["P0_PREMISE"]["rho_family_people"],
}
(H / "face-data.js").write_text("window.FACE = " + json.dumps(data, ensure_ascii=False) + ";\n")
print(len(data["contact"]), len(data["scored"]))
