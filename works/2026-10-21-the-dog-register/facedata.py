"""facedata.py: Session 146, after Session 145's file. Writes face-data.js for index.html: the twelve columns,
their declared types, the parent's page and what it reads, the night's 24 mutants with their swaps and their
blind codes, the family, the predictions as scored. The register itself is not copied here: the face loads
rooms/c2/data/dogs.js, the parent's own table, once."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); L = lambda p: json.load(open(os.path.join(H, p)))
F, MU, plan, R = L("fields.json"), L("mutants.json"), L("plan.json"), L("results.json"); parent = plan["parent"]
title = lambda r: open(os.path.join(H, "rooms", r, "NOTE.md")).readline().lstrip("# ").strip()
PT = {}
for line in open(os.path.join(H, "PREDICTIONS.md")):
    m = re.match(r"- \*\*(P\d) \(([^)]*)\)\.\*\* (.*)", line.strip())
    if m: PT[m.group(1)] = m.group(2)
yn = lambda s: None if s is None else ("yes" if str(s).lower().startswith("y") else "no" if str(s).lower().startswith("n") else "cannot")
T = R["table"]
night = [{"id": m["id"], "arm": m["arm"], "swaps": m["swaps"], "pixeldiff": T[m["id"]]["pixeldiff"],
          "x": {"broken": yn(T[m["id"]]["X_broken"]), "distance": T[m["id"]]["X_distance"]},
          "w": yn(T[m["id"]]["W"]), "wt": yn(T[m["id"]]["WT"]), "v": yn(T[m["id"]]["V"]),
          "w_why": T[m["id"]]["W_why"], "wt_why": T[m["id"]]["WT_why"], "v_why": T[m["id"]]["V_why"],
          "pw": T[m["id"]]["practice_works"]} for m in MU["mutants"]]
fam = [{"room": r, "title": title(r), "w": yn(R["family"][r]["W"]), "wt": yn(R["family"][r]["WT"]), "v": yn(R["family"][r]["V"]),
        "w_why": R["family"][r]["W_why"], "wt_why": R["family"][r]["WT_why"], "v_why": R["family"][r]["V_why"]} for r in ["c1", "c2", "c3", "c4"]]
face = {"fields": F["fields"], "numeric": F["numeric"], "read": MU["read"],
        "parent": {"room": parent, "title": title(parent), "base": "rooms/%s/" % parent, "html": open(os.path.join(H, "rooms", parent, "index.html")).read()},
        "night": night, "family": fam, "meaning": {"W": R["P2"]["meaning"], "WT": R["P2"]["WT_meaning"]},
        "predictions": [{"id": k, "text": PT.get(k, ""), "count": R["scored"][k]["count"], "held": R["scored"][k]["held"]} for k in sorted(R["scored"])],
        "summary": R.get("summary", "")}
open(os.path.join(H, "face-data.js"), "w").write("window.FACE = " + json.dumps(face, ensure_ascii=False) + ";\n")
print("face-data.js", os.path.getsize(os.path.join(H, "face-data.js")), "bytes")
