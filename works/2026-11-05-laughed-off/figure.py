"""Session 170: figure.svg, the 24 describing instances by agreement with the panel (x) and with the family's own taste (y)."""
import json
from pathlib import Path
HERE = Path(__file__).parent
res = json.loads((HERE / "results.json").read_text())
col = {"D": "#5b6470", "B": "#2f6b4f", "S": "#a3392b", "V": "#9a7414"}
nm = {"D": "told nothing", "B": "told the true means", "S": "told them dealt at random", "V": "told them dealt in the family's own order"}
W, H, L, B, x0, x1, y0, y1 = 720, 470, 60, 50, .3, .8, .4, .9
X = lambda v: L + (v - x0) / (x1 - x0) * (W - L - 20)
Y = lambda v: H - B - (v - y0) / (y1 - y0) * (H - B - 70)
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia, serif" font-size="12">',
     f'<rect width="{W}" height="{H}" fill="#f4f1ea"/>',
     '<text x="20" y="26" font-size="16" fill="#1d1c19">Laughed Off: 24 instances guessing a panel\'s ratings of 48 dad jokes</text>',
     '<text x="20" y="46" fill="#6a655b">No instance said the numbers it was shown did not fit. Shown any numbers, true or false, each told arm leaned further on its own taste.</text>']
g = .3
while g <= .8001:
    o.append(f'<line x1="{X(g):.1f}" x2="{X(g):.1f}" y1="70" y2="{H-B}" stroke="#d6cfbf"/><text x="{X(g):.1f}" y="{H-B+16}" text-anchor="middle" fill="#6a655b">{g:.1f}</text>'); g += .1
g = .4
while g <= .9001:
    o.append(f'<line x1="{L}" x2="{W-20}" y1="{Y(g):.1f}" y2="{Y(g):.1f}" stroke="#d6cfbf"/><text x="{L-6}" y="{Y(g)+4:.1f}" text-anchor="end" fill="#6a655b">{g:.1f}</text>'); g += .1
o.append(f'<text x="{W-20}" y="{H-12}" text-anchor="end" fill="#6a655b">Spearman ρ with the panel\'s means →</text>')
o.append(f'<text x="{L+6}" y="84" fill="#6a655b">↑ ρ with the family\'s own ratings (median of six)</text>')
for m, v in res["makers"].items():
    if m[0] in col:
        o.append(f'<circle cx="{X(v["rho_people"]):.1f}" cy="{Y(v["rho_family"]):.1f}" r="6" fill="{col[m[0]]}" fill-opacity=".85"/>')
for a in col:
    mm = res["maker_means"][a]
    o.append(f'<circle cx="{X(mm["rho_people"]):.1f}" cy="{Y(mm["rho_family"]):.1f}" r="12" fill="none" stroke="{col[a]}" stroke-width="2"/>')
for i, a in enumerate(col):
    o.append(f'<circle cx="{W-250}" cy="{H-150+i*18}" r="5" fill="{col[a]}"/><text x="{W-240}" y="{H-146+i*18}" fill="#1d1c19">{nm[a]}</text>')
o.append(f'<text x="{W-250}" y="{H-150+4*18+4}" fill="#6a655b">rings: arm means</text>')
(HERE / "figure.svg").write_text("\n".join(o) + "\n</svg>\n")
