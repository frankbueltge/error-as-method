"""Writes face-data.js for index.html from plan.json, people.json and results.json."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
plan = json.loads((HERE / "plan.json").read_text())
people = json.loads((HERE / "people.json").read_text())["occupations"]
res = json.loads((HERE / "results.json").read_text())

contact = [{"o": o, "pt": people[o]["pt_f"], "truth": plan["deal"]["B"][k], "H": plan["deal"]["H"][k],
            "R": plan["deal"]["R"][k]} for k, o in enumerate(plan["contact"])]
scored = [{"o": o, "pt": people[o]["pt_f"], "br": people[o]["brazil"], "fr": people[o]["france"],
           "A": res["family"]["medians_scored"][o], **{a: res["arms"][a]["medians"][o] for a in "DBHR"}}
          for o in plan["scored"]]
arms = {a: {k: res["arms"][a][k] for k in ("rho_brazil", "mae_brazil", "sd_medians")} for a in "DBHR"}
arms["A"] = {"rho_brazil": res["family"]["rho_brazil"], "sd_medians": res["family"]["sd_medians"]}
how = {k: v["how"] for k, v in res["makers"].items()}
per = {a: [res["makers"][f"{a}{i}"]["rho_brazil"] for i in range(1, 7)] for a in "BHR"}
data = {"per": per, "contact": contact, "scored": scored, "arms": arms, "how": how, "told_rho": plan["deal_rho_with_truth"]}
(HERE / "face-data.js").write_text("window.HALF = " + json.dumps(data, ensure_ascii=False) + ";\n")
print("ok", len(contact), len(scored))
