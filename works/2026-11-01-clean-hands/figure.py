"""Session 166 (experiment 46, Clean Hands): figure.svg, the six kinds of object ranked by five voices.
Reads posthoc.json and results.json. Run: python3 figure.py
"""
import json
from pathlib import Path
HERE = Path(__file__).parent
ph = json.load(open(HERE / "posthoc.json")); res = json.load(open(HERE / "results.json"))
C = ph["category_means"]; K = list(C)
LAB = {"Fruit": "fruit", "Vegetable": "vegetables", "Kitchen Utensils": "kitchen utensils", "Office Supplies": "office supplies",
       "Toys": "toys", "Women's Accessories": "women's accessories"}
COL = {"Fruit": "#c2702a", "Vegetable": "#5c8a2e", "Kitchen Utensils": "#7a6a58", "Office Supplies": "#3f6f9c", "Toys": "#b03a6e",
       "Women's Accessories": "#7d55a8"}
A = res["arms"]
V = [("family", "machine, as itself", f"ρ {res['P0_PREMISE']['rho_family_people']:.2f}"), ("D", "describing the adults", f"ρ {A['D']['rho_people']:.2f}"),
     ("S", "told 24, shuffled", f"ρ {A['S']['rho_people']:.2f}"), ("B", "told 24, true", f"ρ {A['B']['rho_people']:.2f}"), ("people", "the Turkish adults", "")]
W, H, L, R, T, RH = 900, 400, 90, 90, 80, 52
cw = (W - L - R) / (len(V) - 1)
ranks = [sorted(K, key=lambda k: -C[k][v]) for v, _, _ in V]
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia, serif">',
     f'<rect width="{W}" height="{H}" fill="#fbfcfa"/>',
     '<text x="20" y="26" font-size="16" fill="#1a1d1b">Six kinds of object, ranked by mean perceived disease risk (riskiest at top)</text>']
for i, (v, lab, rho) in enumerate(V):
    x = L + i * cw
    o.append(f'<text x="{x:.0f}" y="54" text-anchor="middle" font-size="13" fill="#1a1d1b">{lab}</text>')
    if rho: o.append(f'<text x="{x:.0f}" y="69" text-anchor="middle" font-size="11" fill="#5f6862">48 objects: {rho} with the adults</text>')
for k in K:
    pts = " ".join(f"{L + i * cw:.0f},{T + 12 + r.index(k) * RH}" for i, r in enumerate(ranks))
    o.append(f'<polyline points="{pts}" fill="none" stroke="{COL[k]}" stroke-width="3" stroke-opacity=".75"/>')
for i, r in enumerate(ranks):
    for j, k in enumerate(r):
        x, y = L + i * cw, T + 12 + j * RH
        o.append(f'<rect x="{x-68:.0f}" y="{y-11}" width="136" height="22" rx="3" fill="#fbfcfa" stroke="{COL[k]}"/>')
        o.append(f'<text x="{x:.0f}" y="{y+4}" text-anchor="middle" font-size="12" fill="#1a1d1b">{LAB[k]}</text>')
o.append(f'<text x="20" y="{H-14}" font-size="11" fill="#5f6862">Rengiiyiler &amp; Tekozel, osf.io/9zfsu: 107 Turkish-speaking adults, 1-7. Machine: six instances per column. Experiment 46, Session 166.</text>')
o.append("</svg>")
(HERE / "figure.svg").write_text("\n".join(o) + "\n")
print("ok")
