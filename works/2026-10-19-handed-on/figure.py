"""figure.py -- figure.svg: the blind coder's code for each of the 18 steps, by arm and lineage, with each
lineage's first-version title. Read from results.json, coder/key.json, coder/answer.json and face-data.js."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
key = json.load(open(os.path.join(HERE, "coder", "key.json")))
ans = json.load(open(os.path.join(HERE, "coder", "answer.json")))["pairs"]
s = open(os.path.join(HERE, "face-data.js"), encoding="utf-8").read()
face = json.loads(s[s.index("["):s.rindex("]") + 1])
title = {l["lineage"]: l["versions"][0]["title"] for l in face}
code = {(k["lineage"], k["to"]): ans[t]["code"] for t, k in key.items()}
COL = {"SCHEMA": "#b2361f", "STRIKE": "#c08a2c", "ADD": "#c9c3b6", "SAME": "#eeeae2"}
ARMS = [("P", "handed on, plain brief", ["L1", "L6"]), ("T", "handed on, with Simondon's test", ["L2", "L4"]),
        ("K", "kept, sent back", ["L3", "L5"])]
W, y = 760, 64
o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d 430" font-family="Georgia, serif" font-size="13">' % W,
     '<rect width="100%" height="100%" fill="#f6f3ec"/>',
     '<text x="20" y="30" font-size="17" fill="#1d1b18">Handed On — what a blind coder saw change at each step</text>',
     '<text x="20" y="50" font-size="12" fill="#6b665c">v1 → v2 → v3 → v4 · eighteen steps coded from the two pictures alone, lineage and arm masked</text>']
for arm, name, ls in ARMS:
    n = sum(code[(L, k)] in ("SCHEMA", "STRIKE") for L in ls for k in (2, 3, 4))
    o.append('<text x="20" y="%d" font-size="14" fill="#1d1b18">%s</text>' % (y + 16, name))
    o.append('<text x="%d" y="%d" font-size="13" fill="#b2361f" text-anchor="end">%d of 6 reorganised or struck</text>' % (W - 20, y + 16, n))
    y += 26
    for L in ls:
        o.append('<text x="20" y="%d" fill="#6b665c" font-family="monospace" font-size="12">%s</text>' % (y + 22, L))
        o.append('<text x="52" y="%d" fill="#1d1b18" font-style="italic">%s</text>' % (y + 22, title[L].replace("&", "&amp;")))
        for i, k in enumerate((2, 3, 4)):
            c = code[(L, k)]; x = 300 + i * 150
            o.append('<rect x="%d" y="%d" width="138" height="32" rx="3" fill="%s"/>' % (x, y + 4, COL[c]))
            o.append('<text x="%d" y="%d" text-anchor="middle" font-family="monospace" font-size="12" fill="%s">v%d→v%d %s</text>'
                     % (x + 69, y + 25, "#fff" if c in ("SCHEMA", "STRIKE") else "#1d1b18", k - 1, k, c.lower()))
        y += 40
    y += 12
o.append('<text x="20" y="%d" font-size="11" fill="#6b665c">Five of six first versions, made apart from one brief, drew the same form: a line from birth to prize. Data: Nobel Prize API v2.1 (CC0).</text>' % (y + 6))
o.append('</svg>')
open(os.path.join(HERE, "figure.svg"), "w", encoding="utf-8").write("\n".join(o))
print("figure.svg", y)
