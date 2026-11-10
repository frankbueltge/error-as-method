"""figure.svg for Read Backwards: left, told agreement against answered agreement per maker; right, the reversed arm's 32 median answers against the true October 2026 views (log10)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
res = json.loads((HERE / "results.json").read_text())
plan = json.loads((HERE / "plan.json").read_text())
P = {r["element"]: r["views"] for r in json.loads((HERE / "sources/pageviews-2026-10.json").read_text())}
import math
W, H = 900, 420
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Menlo,Consolas,monospace" font-size="11">',
     f'<rect width="{W}" height="{H}" fill="#fbfaf6"/>',
     '<text x="20" y="24" font-size="14" fill="#1d1c1a">Read Backwards (Session 173): a count has no label to flip, and the instances flipped it anyway</text>']
l, r, t, b = 60, 420, 50, 360
gx = lambda v: l + (r - l) * (v + 1) / 2
gy = lambda v: b - (b - t) * (v + 1) / 2
o.append(f'<rect x="{l}" y="{t}" width="{r-l}" height="{b-t}" fill="none" stroke="#d3cec3"/>')
o.append(f'<line x1="{gx(-1)}" y1="{gy(-1)}" x2="{gx(1)}" y2="{gy(1)}" stroke="#66625a" stroke-dasharray="3 4"/>')
for v in (-1, -0.5, 0, 0.5, 1):
    o.append(f'<text x="{gx(v)}" y="{b+16}" text-anchor="middle" fill="#66625a">{v}</text>')
    o.append(f'<text x="{l-6}" y="{gy(v)+4}" text-anchor="end" fill="#66625a">{v}</text>')
o.append(f'<text x="{(l+r)/2}" y="{b+36}" text-anchor="middle" fill="#66625a">told counts vs truth (Spearman rho)</text>')
o.append(f'<text x="{l+4}" y="{t+14}" fill="#66625a">each instance\'s 32 answers vs truth</text>')
told = {"B": 1.0, "H": plan["rho_half_vs_true"], "R": plan["rho_rev_vs_true"]}
col = {"B": "#2f5f86", "H": "#d6a93a", "R": "#a34a3a"}
for a in "BHR":
    for i in range(1, 7):
        v = res["makers"][f"{a}{i}"]["rho"]
        o.append(f'<circle cx="{gx(told[a]) + (i-3.5)*5:.1f}" cy="{gy(v):.1f}" r="4.5" fill="{col[a]}"/>')
o.append(f'<text x="{gx(1)-8}" y="{gy(0.89)+22}" text-anchor="end">true: kept</text>')
o.append(f'<text x="{gx(-0.6)+12}" y="{gy(0.7)+4}">half turned: 2 shrank</text>')
o.append(f'<text x="{gx(-0.6)+12}" y="{gy(-0.89)+4}">4 inverted</text>')
o.append(f'<text x="{gx(-1)+12}" y="{gy(-0.88)+22}">reversed: 6 followed</text>')
l, r, t, b = 500, 870, 50, 360
lo, hi = 3.9, 4.8
px = lambda v: l + (r - l) * (v - lo) / (hi - lo)
py = lambda v: b - (b - t) * (v - lo) / (hi - lo)
o.append(f'<rect x="{l}" y="{t}" width="{r-l}" height="{b-t}" fill="none" stroke="#d3cec3"/>')
o.append(f'<line x1="{px(lo)}" y1="{py(lo)}" x2="{px(hi)}" y2="{py(hi)}" stroke="#66625a" stroke-dasharray="3 4"/>')
for v, lab in ((4.0, "10k"), (4.3, "20k"), (4.6, "40k")):
    o.append(f'<text x="{px(v)}" y="{b+16}" text-anchor="middle" fill="#66625a">{lab}</text>')
    o.append(f'<text x="{l-6}" y="{py(v)+4}" text-anchor="end" fill="#66625a">{lab}</text>')
o.append(f'<text x="{(l+r)/2}" y="{b+36}" text-anchor="middle" fill="#66625a">true views, October 2026 (log)</text>')
o.append(f'<text x="{l+4}" y="{t+14}" fill="#66625a">reversed arm, median of six</text>')
for el, v in zip(plan["scored"], res["arms"]["R"]["medians_log10"]):
    x = math.log10(P[el])
    o.append(f'<circle cx="{px(x):.1f}" cy="{py(v):.1f}" r="4" fill="#a34a3a"/>')
    if el in ("Hydrogen", "Silver", "Copper", "Scandium"):
        o.append(f'<text x="{px(x)+7:.1f}" y="{py(v)+4:.1f}">{el.lower()}</text>')
o.append(f'<text x="20" y="{H-12}" fill="#66625a">Material: Wikimedia REST API, en.wikipedia user pageviews, Oct 2026 (CC0). Told nothing: rho 0.89. Told reversed: -0.88.</text>')
o.append("</svg>")
(HERE / "figure.svg").write_text("\n".join(o))
