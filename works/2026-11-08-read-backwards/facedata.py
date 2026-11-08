"""Session 173: write face-data.js from plan.json and results.json."""
import json, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
plan = json.load(open(os.path.join(HERE, "plan.json")))
res = json.load(open(os.path.join(HERE, "results.json")))
P = json.load(open(os.path.join(HERE, "sources/pageviews-2026-10.json")))
logs = [math.log10(r["views"]) for r in P]
face = {
    "el": [{"z": r["z"], "name": r["element"], "views": r["views"]} for r in P],
    "contact": plan["contact"], "scored": plan["scored"],
    "deals": plan["deals"], "rho": {"H": plan["rho_half_vs_true"]},
    "lo": math.floor(min(logs) * 10) / 10, "hi": math.ceil(max(logs) * 10) / 10,
    "arms": {},
}
for arm in "UBHR":
    a = res["arms"][arm]
    face["arms"][arm] = {
        "rho": a["rho_truth"],
        "med": dict(zip(plan["scored"], a["medians_log10"])),
        "makers": [{"id": f"{arm}{n}", "rho": res["makers"][f"{arm}{n}"]["rho"], "how": res["makers"][f"{arm}{n}"]["how"]}
                   for n in range(1, 7)],
    }
open(os.path.join(HERE, "face-data.js"), "w").write("window.FACE=" + json.dumps(face, ensure_ascii=False) + ";\n")
print("ok", face["lo"], face["hi"])
