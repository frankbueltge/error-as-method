"""Session 163, experiment 43 (Unheard): write face-data.js for index.html from people.json, plan.json and rooms/.
Run: python3 facedata.py"""
import json, statistics as st
from pathlib import Path
HERE = Path(__file__).parent
src = (HERE / "score.py").read_text().split("res = {")[0]
exec(src)
PP = {k["id"]: k for k in json.load(open(HERE / "people.json"))}
D, C = arm_p50("D"), arm_p50("C")
A = {m: rooms[m][0] for m in rooms if m[0] == "A"}
def src_of(t):
    for pre, n in (("small", "small drone"), ("large", "large drone"), ("single", "car"),
                   ("helicopter", "helicopter"), ("propeller", "propeller aircraft"), ("jet", "jet airliner")):
        if t.startswith(pre): return n
rows = []
for k in keys:
    p = PP[k]
    hist = [p["ratings"].count(v) for v in range(11)]
    rows.append({"id": k, "text": p["text"], "src": src_of(p["text"]), "Lmax": p["LASmax"], "people": P[k],
                 "hist": hist, "fam": fam[k], "A": [A[m][k] for m in sorted(A)],
                 "D": [D[m][k] for m in sorted(D)], "C": [C[m][k] for m in sorted(C) if k in C[m]],
                 "anchor": k in ANCH, "far": k in far, "split": k in split})
(HERE / "face-data.js").write_text("window.UNHEARD=" + json.dumps(rows, separators=(",", ":")) + ";\n")
print(len(rows), "rows")
