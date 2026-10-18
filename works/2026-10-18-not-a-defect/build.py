#!/usr/bin/env python3
"""Build data.js for the face from the committed codes. Stdlib, no network.

    python3 -I build.py <entries.json from draw.py>

Takes from the drawn entries only each issue's number, title and section (the titles are short
quotations, with a link to the issue's own page); everything else from committed files.
"""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__))
L = lambda p: json.load(open(os.path.join(H, p)))
ents = json.load(open(sys.argv[1]))
codes = {c: {r["id"]: r for r in L(f)} for c, f in (("P", "practice.json"), ("A", "readers/reader-A.json"), ("B", "readers/reader-B.json"))}
party = L("party.json")["refused"]
rows = []
for i, e in enumerate(ents, 1):
    eid = f"E{i:02d}"
    ref = e["status"] == "NAD"
    row = {"id": eid, "n": e["id"], "t": e["title"], "s": e["section"], "st": e["status"], "ref": ref, "c": {}}
    for c in "PAB":
        r = codes[c][eid]
        pk = {"P": "practice", "A": "A", "B": "B"}[c]
        row["c"][c] = {"w": r["wrong"], "h": r["held"], "j": r["judged"],
                       "p": party[pk][eid] if ref else "standard"}
    rows.append(row)
open(os.path.join(H, "data.js"), "w").write("window.ROWS=" + json.dumps(rows, ensure_ascii=False) + ";\n")
print(len(rows), "rows")
