#!/usr/bin/env python3
"""Draw figure.svg from data.js: the 25 refused issues, three coders, as letters and as parties."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
rows = json.loads(open(os.path.join(H, "data.js")).read().split("=", 1)[1].rstrip(";\n"))
ref = [r for r in rows if r["ref"]]
LET = {"J": "#24527a", "R": "#b3261e", "B": "#6b3f8f", "X": "#e2dccd"}
PAR = {"standard": "#24527a", "submitter": "#b3261e", "neither": "#e2dccd"}
cw, ch, gap = 22, 14, 3
W = 660
Hh = 70 + len(ref) * (ch + gap) + 40
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}" font-family="Georgia,serif">',
     f'<rect width="{W}" height="{Hh}" fill="#f3f0e8"/>',
     '<text x="10" y="20" font-size="14" fill="#1c1c1e">25 issues refused as not a defect: who is wrong, by three readers</text>']
for k, (title, key, M) in enumerate((("the letter each wrote (scored)", "w", LET), ("whose term each struck (post hoc)", "p", PAR))):
    x0 = 10 + k * (3 * (cw + gap) + 130)
    o.append(f'<text x="{x0}" y="42" font-size="11" fill="#62605b">{title}</text>')
    for j, c in enumerate("PAB"):
        o.append(f'<text x="{x0 + j*(cw+gap) + cw/2}" y="60" font-size="11" text-anchor="middle" fill="#62605b">{c}</text>')
        n = 0
        for i, r in enumerate(ref):
            v = r["c"][c][key]
            n += (v == "R") if key == "w" else (v == "submitter")
            o.append(f'<rect x="{x0 + j*(cw+gap)}" y="{66 + i*(ch+gap)}" width="{cw}" height="{ch}" fill="{M[v]}"/>')
        o.append(f'<text x="{x0 + j*(cw+gap) + cw/2}" y="{66 + len(ref)*(ch+gap) + 14}" font-size="11" text-anchor="middle" fill="#b3261e">{n}</text>')
y = Hh - 8
o.append(f'<text x="10" y="{y}" font-size="10" fill="#62605b">red: the held term (left), the submitter\'s claim (right); blue: the judged term / the standard\'s wording; pale: neither. C++ Core Language Issues, seed 134.</text>')
o.append("</svg>")
open(os.path.join(H, "figure.svg"), "w").write("\n".join(o))
