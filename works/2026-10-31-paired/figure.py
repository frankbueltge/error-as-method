"""Session 165 (experiment 45, Paired): figure.svg, the 48 scored pictures, the people's mean across, three voices up.
Run: python3 figure.py
"""
import json
from pathlib import Path
HERE = Path(__file__).parent
d = json.loads((HERE / "face-data.js").read_text().split("=", 1)[1].rstrip().rstrip(";"))
W, H, L, R, T, B = 900, 380, 50, 20, 40, 50
panels = [("self", "as itself", "#1d1b17", True), ("D", "describing the people", "#3b6e8f", False), ("S", "after 24 false pairs", "#a07a12", False)]
pw = (W - L - R) / 3
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia, serif" font-size="12">',
       f'<rect width="{W}" height="{H}" fill="#f6f3ec"/>']
for i, (k, lab, col, hollow) in enumerate(panels):
    x0 = L + i * pw + (10 if i else 0); w = pw - 20
    px = lambda v: x0 + (v - 1) / 8 * w; py = lambda v: H - B - (v - 1) / 8 * (H - T - B)
    for v in range(1, 10):
        out.append(f'<line x1="{px(v):.1f}" x2="{px(v):.1f}" y1="{py(1):.1f}" y2="{py(9):.1f}" stroke="#d8d1c2"/>')
        out.append(f'<line x1="{px(1):.1f}" x2="{px(9):.1f}" y1="{py(v):.1f}" y2="{py(v):.1f}" stroke="#d8d1c2"/>')
    out.append(f'<line x1="{px(1):.1f}" y1="{py(1):.1f}" x2="{px(9):.1f}" y2="{py(9):.1f}" stroke="#b4432b" stroke-dasharray="4 4"/>')
    for s in d["scored"]:
        out.append(f'<circle cx="{px(s["people"]):.1f}" cy="{py(s[k]):.1f}" r="3.6" fill="{"none" if hollow else col}" stroke="{col}" fill-opacity="0.8"/>')
    rho = d["rhoFamily"] if k == "self" else d["arms"][k]["rho_people"]
    out.append(f'<text x="{x0:.1f}" y="{T-14}" font-size="14">The machine {lab} · ρ {rho:.2f}</text>')
    out.append(f'<text x="{x0 + w/2:.1f}" y="{H-14}" text-anchor="middle" fill="#6d675c">the Japanese adults’ mean kawaii rating (1–9)</text>')
out.append('</svg>')
(HERE / "figure.svg").write_text("\n".join(out))
