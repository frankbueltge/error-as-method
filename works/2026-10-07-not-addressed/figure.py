"""figure.py -- figure.svg from results.json and open.json: where the word stood, who took it, who noticed it."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
res = json.load(open(os.path.join(HERE, "results.json"))); opn = json.load(open(os.path.join(HERE, "open.json")))
LAB = [("B", "the folder's own name"), ("C", "the folder above"), ("D", "an empty file beside the data"),
       ("E", "the data's first line"), ("F", "the brief (title given)"), ("A", "nowhere (control)")]
W, H = 760, 330
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Georgia,serif" font-size="14">',
     f'<rect width="{W}" height="{H}" fill="#f3efe6"/>',
     '<text x="20" y="28" font-size="17">Not Addressed: where the word <tspan font-style="italic">orchard</tspan> stood, and what twelve makers did with it</text>']
y = 70
for c, lab in LAB:
    ms = sorted(m for m, r in res["makers"].items() if r["condition"] == c)
    o.append(f'<text x="20" y="{y+5}">{c}  {lab}</text>')
    for i, m in enumerate(ms):
        r = res["makers"][m]; x = 300 + i * 230
        took, noticed = r["M1_take"], opn[m].get("report_channel")
        fill = "#2f6b3a" if took else "none"
        stroke = "#b2401f" if noticed else ("#2f6b3a" if took else "#8a8274")
        o.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{fill}" stroke="{stroke}" stroke-width="{3 if noticed else 1.5}"/>')
        o.append(f'<text x="{x+16}" y="{y+5}" font-style="italic">{r["title"]}</text>')
    y += 40
o.append(f'<text x="20" y="{H-18}" font-size="12" fill="#6b6458">filled: took the word (title or note) · red ring: noticed it, in the report only · same brief, same data (Fremont Bridge, 2025)</text>')
o.append('</svg>')
open(os.path.join(HERE, "figure.svg"), "w").write("\n".join(o)); print("figure.svg")
