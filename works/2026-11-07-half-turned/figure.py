"""figure.svg for Half Turned: left, told agreement against answered agreement per maker; right, the half-turned arm's 32 answers against the people's."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
res = json.loads((HERE / "results.json").read_text())
plan = json.loads((HERE / "plan.json").read_text())
people = json.loads((HERE / "people.json").read_text())["occupations"]
W, H = 900, 420
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Menlo,Consolas,monospace" font-size="11">',
     f'<rect width="{W}" height="{H}" fill="#fbfaf6"/>',
     '<text x="20" y="24" font-size="14" fill="#1d1c1a">Half Turned (Session 172): told half a reversal, six instances answered with a whole one</text>']
# left panel
l, r, t, b = 60, 420, 50, 360
gx = lambda v: l + (r - l) * (v + 1) / 2
gy = lambda v: b - (b - t) * (v + 1) / 2
o.append(f'<rect x="{l}" y="{t}" width="{r-l}" height="{b-t}" fill="none" stroke="#d3cec3"/>')
o.append(f'<line x1="{gx(-1)}" y1="{gy(-1)}" x2="{gx(1)}" y2="{gy(1)}" stroke="#66625a" stroke-dasharray="3 4"/>')
for v in (-1, -0.5, 0, 0.5, 1):
    o.append(f'<text x="{gx(v)}" y="{b+16}" text-anchor="middle" fill="#66625a">{v}</text>')
    o.append(f'<text x="{l-6}" y="{gy(v)+4}" text-anchor="end" fill="#66625a">{v}</text>')
o.append(f'<text x="{(l+r)/2}" y="{b+36}" text-anchor="middle" fill="#66625a">told numbers vs truth (Spearman rho)</text>')
o.append(f'<text x="{l+4}" y="{t+14}" fill="#66625a">each instance\'s answer vs truth</text>')
told = plan["deal_rho_with_truth"]
col = {"B": "#2f5f86", "H": "#d6a93a", "R": "#a34a3a"}
for a in "BHR":
    for i in range(1, 7):
        v = res["makers"][f"{a}{i}"]["rho_brazil"]
        o.append(f'<circle cx="{gx(told[a]) + (i-3.5)*5:.1f}" cy="{gy(v):.1f}" r="4.5" fill="{col[a]}"/>')
o.append(f'<text x="{gx(1)-8}" y="{gy(0.95)+22}" text-anchor="end">true: kept</text>')
o.append(f'<text x="{gx(-0.5)+10}" y="{gy(-0.9)-10}">half turned: answered at -0.79 to -0.95</text>')
o.append(f'<text x="{gx(-1)+10}" y="{gy(-0.96)+22}">reversed: followed</text>')
# right panel
l, r, t, b = 500, 870, 50, 360
px = lambda v: l + (r - l) * v / 100
py = lambda v: b - (b - t) * v / 100
o.append(f'<rect x="{l}" y="{t}" width="{r-l}" height="{b-t}" fill="none" stroke="#d3cec3"/>')
o.append(f'<line x1="{px(0)}" y1="{py(0)}" x2="{px(100)}" y2="{py(100)}" stroke="#66625a" stroke-dasharray="3 4"/>')
for v in (0, 50, 100):
    o.append(f'<text x="{px(v)}" y="{b+16}" text-anchor="middle" fill="#66625a">{v}</text>')
    o.append(f'<text x="{l-6}" y="{py(v)+4}" text-anchor="end" fill="#66625a">{v}</text>')
o.append(f'<text x="{(l+r)/2}" y="{b+36}" text-anchor="middle" fill="#66625a">110 people in Brazil (0 masc., 100 fem.)</text>')
o.append(f'<text x="{l+4}" y="{t+14}" fill="#66625a">half-turned arm, median of six</text>')
for occ, v in res["arms"]["H"]["medians"].items():
    x = people[occ]["brazil"]
    c = "#a34a3a" if x >= 50 else "#2f5f86"
    o.append(f'<circle cx="{px(x):.1f}" cy="{py(v):.1f}" r="4" fill="{c}"/>')
    if occ in ("rider", "childminder", "governor", "decorator", "cook"):
        o.append(f'<text x="{px(x)+7:.1f}" y="{py(v)+4:.1f}">{occ}</text>')
o.append(f'<text x="20" y="{H-12}" fill="#66625a">Material: NeFeLaE, osf.io/j86z4 (2026). rho told -0.50; answered -0.90 (arm), with the machine\'s own order -0.93.</text>')
o.append("</svg>")
(HERE / "figure.svg").write_text("\n".join(o))
