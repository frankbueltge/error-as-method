"""facedata.py: writes face-data.js for index.html from plan.json, the makers' NOTE.md titles, coder B's answers,
the two pictures' holds and the hourly record (materials/hourly.json). Run after score.py."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
plan = json.load(open(os.path.join(H, "plan.json"))); B = json.load(open(os.path.join(H, "coder", "B", "answers.json")))
W = []
for p in plan:
    m = p["maker"]; b = B[m]
    W.append({"m": m, "cell": p["cell"], "title": open(os.path.join(H, "makers", m, "NOTE.md")).readline().strip("# \n"),
              "rec": b["B2"] == "yes" and b["B5"] == "yes", "day": b["B3"], "week": b["B4"], "units": b["B10"],
              "q": b["B7_category"], "qw": b["B7_quote"][:170], "interval": b["B8"], "label": b["B9"]})
out = "const WORKS = " + json.dumps(W, indent=0, ensure_ascii=False) + ";\n"
out += "const HOLDS = " + json.dumps(json.load(open(os.path.join(H, "materials", "holds.json")))) + ";\n"
out += "const HOURLY = " + json.dumps([round(v) for v in json.load(open(os.path.join(H, "materials", "hourly.json")))]) + ";\n"
open(os.path.join(H, "face-data.js"), "w").write(out); print(len(out))
