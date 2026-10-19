#!/usr/bin/env python3
"""Write figure.svg from face-data.js's source answers. Stdlib.

    python3 -I figure.py
"""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(H, "face-data.js")).read()
rows = [r for r in json.loads(src[src.index("{"):src.rindex("}") + 1])["rows"] if r["status"] == "NAD"]
lanes = [("no roles declared (Session 134, read by hand, not scored)", ["134A", "134B"]),
         ("declared: the standard is judged", ["D1", "D2"]),
         ("declared: the standard is held", ["O1", "O2"])]
W, cw, ch, gap, x0 = 760, 24, 40, 4, 20
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 520" font-family="Georgia, serif">',
       '<rect width="100%" height="100%" fill="#f3f0e8"/>',
       '<text x="20" y="34" font-size="20" fill="#1c1c1e">Twenty-five refusals, six readers: whose term is wrong</text>']
y = 64
for title, pair in lanes:
    out.append(f'<text x="{x0}" y="{y + 14}" font-size="14" fill="#62605b">{title}</text>')
    y += 22
    for r in pair:
        n = 0
        for j, row in enumerate(rows):
            p = row["cells"][r][0]
            x = x0 + j * (cw + gap)
            if p == "submitter":
                n += 1
                out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="2" fill="#b3261e"/>')
            elif p == "standard":
                out.append(f'<rect x="{x + 1}" y="{y + 1}" width="{cw - 2}" height="{ch - 2}" rx="2" fill="#fbf9f3" stroke="#24527a" stroke-width="2"/>')
            else:
                out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="2" fill="#e2dccd"/>')
        out.append(f'<text x="{x0 + 25 * (cw + gap) + 6}" y="{y + 26}" font-size="15" fill="#1c1c1e">{n}</text>')
        y += ch + 6
    y += 18
out.append(f'<text x="{x0}" y="{y + 6}" font-size="13" fill="#62605b">red: the submitter is wrong · outlined: the standard is wrong · pale: neither · number: submitter struck, of 25</text>')
out.append('</svg>')
open(os.path.join(H, "figure.svg"), "w").write("\n".join(out))
