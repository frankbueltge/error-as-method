"""Session 164, experiment 44: figure.svg, the 56 scored statements: the people's mean (filled) and the eighteen
describers' mean (rings) against the family's own median, with least-squares lines. Run: python3 figure.py
"""
import json, statistics as st
from pathlib import Path
HERE = Path(__file__).parent
R = json.load(open(HERE / "results.json"))
S = [k for k, v in R["per_key"].items() if k not in set(R["M_anchors"]) | set(R["U_anchors"])]
pk = R["per_key"]
W, H = 720, 470
X = lambda v: 70 + (v - 1) * 120
Y = lambda v: 410 - (v - 1) * 64
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="system-ui,sans-serif" font-size="13">',
     f'<rect width="{W}" height="{H}" fill="#fcfcfb"/>',
     '<text x="20" y="26" font-size="15" font-weight="600" fill="#0b0b0b">Lesser Known: how true 56 statements were found</text>',
     '<text x="20" y="44" fill="#52514e">filled: 30 people (mean); rings: eighteen instances saying where the people stood; across: the machine itself</text>']
for v in range(1, 7):
    o.append(f'<line x1="50" x2="{X(6)+20}" y1="{Y(v)}" y2="{Y(v)}" stroke="#e6e4de"/>')
    o.append(f'<text x="40" y="{Y(v)+4}" text-anchor="end" fill="#52514e">{v}</text>')
    o.append(f'<text x="{X(v)}" y="{H-26}" text-anchor="middle" fill="#52514e">{v}</text>')
o.append(f'<text x="{X(3.5)}" y="{H-8}" text-anchor="middle" fill="#52514e">how true the machine found it, as itself (median of six)</text>')
xs, yp, yd = [], [], []
for i, k in enumerate(S):
    d = st.mean(x["mean"] for a in "DMU" for x in pk[k][a]); p = pk[k]["people_mean"]; f = pk[k]["fam"]
    jx = X(f) + ((i * 37) % 23 - 11) * 2.4
    xs.append(f); yp.append(p); yd.append(d)
    o.append(f'<line x1="{jx:.1f}" x2="{jx:.1f}" y1="{Y(p):.1f}" y2="{Y(d):.1f}" stroke="#dddbd5"/>')
    o.append(f'<circle cx="{jx:.1f}" cy="{Y(p):.1f}" r="5" fill="#eb6834"/>')
    o.append(f'<circle cx="{jx:.1f}" cy="{Y(d):.1f}" r="5" fill="none" stroke="#1baf7a" stroke-width="1.8"/>')
def fit(ys):
    mx, my = st.mean(xs), st.mean(ys); b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return b, my - b * mx
for ys, c, dash, lab in ((yp, "#eb6834", "", "people"), (yd, "#1baf7a", ' stroke-dasharray="6 4"', "account")):
    b, a = fit(ys)
    o.append(f'<line x1="{X(1)}" x2="{X(6)}" y1="{Y(a+b):.1f}" y2="{Y(a+6*b):.1f}" stroke="{c}" stroke-width="2.5"{dash}/>')
    ty = Y(a + 3.2 * b) - 14 if lab == "people" else Y(a + 3.2 * b) + 26
    o.append(f'<text x="{X(3.2)}" y="{ty - (a + 6 * b - (a + 3.2 * b)) * 0:.1f}" text-anchor="middle" fill="{c}">{lab} {b:.2f}/step</text>')
o.append('</svg>')
(HERE / "figure.svg").write_text("\n".join(o) + "\n")
print("ok")
