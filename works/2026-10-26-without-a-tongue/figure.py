"""figure.svg for Without a Tongue (Session 159): the 48 foods where the machine's middle rating differs from the
people's, sorted by the people's minus the machine's. Blue: twelve instances rating (median). Orange: 59 people
(median). Green diamond: six instances describing the people (mean of stated medians)."""
import json
from pathlib import Path
HERE = Path(__file__).parent
r = json.loads((HERE / "results.json").read_text())
rows = sorted([k for k in r["keys"] if abs(k["median"]["A"] - k["median"]["people"]) >= 0.5],
              key=lambda k: k["median"]["people"] - k["median"]["A"], reverse=True)
W, LBL, L, R, TOP, RH = 760, 210, 230, 740, 64, 15
X = lambda v: L + (v - 1) * (R - L) / 8
H = TOP + RH * len(rows) + 40
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="system-ui, sans-serif" font-size="11">',
     f'<rect width="{W}" height="{H}" fill="#fcfcfb"/>',
     '<text x="20" y="24" font-size="15" font-weight="600" fill="#0b0b0b">Without a Tongue: where the machine\'s taste is not the people\'s</text>',
     '<text x="20" y="42" fill="#52514e">48 of 67 foods. Blue: 12 instances rating. Orange: 59 people. Green (above the line): 6 instances describing the people. Medians, 1–9 scale.</text>']
for v in range(1, 10):
    o.append(f'<line x1="{X(v)}" x2="{X(v)}" y1="{TOP - 8}" y2="{TOP + RH * len(rows)}" stroke="#ecebe7"/>')
    o.append(f'<text x="{X(v)}" y="{TOP + RH * len(rows) + 16}" text-anchor="middle" fill="#77756f">{v}</text>')
for i, k in enumerate(rows):
    y = TOP + i * RH + RH / 2
    m = k["median"]
    o.append(f'<text x="{LBL}" y="{y + 4}" text-anchor="end" fill="#0b0b0b">{k["food"]}</text>')
    o.append(f'<line x1="{X(m["A"])}" x2="{X(m["people"])}" y1="{y}" y2="{y}" stroke="#b9b7b0" stroke-width="2"/>')
    o.append(f'<circle cx="{X(m["people"]):.1f}" cy="{y}" r="4.5" fill="#eb6834" stroke="#fcfcfb" stroke-width="1.5"/>')
    o.append(f'<circle cx="{X(m["A"]):.1f}" cy="{y}" r="4.5" fill="#2a78d6" stroke="#fcfcfb" stroke-width="1.5"/>')
    o.append(f'<rect x="{X(m["P"]) - 3.5:.1f}" y="{y - 9.5}" width="6" height="6" transform="rotate(45 {X(m["P"]):.1f} {y - 6.5})" fill="#1baf7a" stroke="#fcfcfb" stroke-width="1"/>')
o.append(f'<text x="20" y="{H - 8}" fill="#77756f">Data: Galgani 2026, Zenodo 23296649 (CC BY 4.0); machine replies in this experiment\'s rooms/.</text>')
o.append('</svg>')
(HERE / "figure.svg").write_text("\n".join(o) + "\n")
