"""facedata.py: Session 145. Writes face-data.js for index.html: the table, its declared types, the parent's page
and what it reads, the night's 24 mutants with their blind codes (once results.json exists), the family, the
predictions as scored."""
import json, os, re
import elements
H = os.path.dirname(os.path.abspath(__file__)); L = lambda p: json.load(open(os.path.join(H, p)))
F, MU, plan = L("fields.json"), L("mutants.json"), L("plan.json"); parent = plan["parent"]
R = L("results.json") if os.path.exists(os.path.join(H, "results.json")) else None
title = lambda r: open(os.path.join(H, "rooms", r, "NOTE.md")).readline().lstrip("# ").strip()
PT = {}
for line in open(os.path.join(H, "PREDICTIONS.md")):
    m = re.match(r"- \*\*(P\d) \(([^)]*)\)\.\*\* (.*)", line.strip())
    if m: PT[m.group(1)] = m.group(2)
row = lambda k: (R or {}).get("rows", {}).get(k, {})
yn = lambda s: None if s is None else ("yes" if s.lower().startswith("y") else "no" if s.lower().startswith("n") else "cannot")
night = [{"id": m["id"], "arm": m["arm"], "swaps": m["swaps"],
          "x": {"broken": yn(row(m["id"]).get("x_broken")), "distance": row(m["id"]).get("x_distance")} if R else None,
          "w": yn(row(m["id"]).get("w_works")), "v": yn(row(m["id"]).get("v_agrees")), "information": row(m["id"]).get("information")} for m in MU["mutants"]]
SUMMARY = ("Four fresh makers, given the table and nothing else, made one form four times: each element's liquid interval on a log kelvin scale. "
  "The night swapped columns under the drawn parent 24 times. Blind: 3 broken, 3 unchanged, 2 changed. Typed: 5 unchanged, 3 changed. Seeing: 2 broken, 1 unchanged, 5 changed. "
  "A blind coder rated no unbroken mutant further than 1 from the family. A fresh judge refused all ten that changed visibly: eight for misstating the table, two for being unreadable. "
  "Click any mutant to load its swaps into the wiring above.")
face = {"fields": F["fields"], "numeric": F["numeric"], "read": MU["read"], "elements": elements.load(),
        "parent": {"room": parent, "title": title(parent), "base": "rooms/%s/" % parent, "html": open(os.path.join(H, "rooms", parent, "index.html")).read()},
        "night": night, "family": [{"room": r, "title": title(r), "w": yn(row(r).get("w_works")), "v": yn(row(r).get("v_agrees"))} for r in ["c1", "c2", "c3", "c4"]],
        "predictions": [{"id": k, "text": PT.get(k, ""), "count": p["count"], "held": p["held"]} for k, p in (R or {}).get("predictions", {}).items()],
        "summary": SUMMARY}
open(os.path.join(H, "face-data.js"), "w").write("window.FACE = " + json.dumps(face, ensure_ascii=False) + ";\n")
print("face-data.js", os.path.getsize(os.path.join(H, "face-data.js")), "bytes")
