#!/usr/bin/env python3
"""figure.svg: for each thing, the people's spread of six (5th-95th percentile band, median tick) and the
three arms' D, on one axis of the experiment's measure. Static, for the rendered page."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
res = json.load(open(os.path.join(HERE, "results.json")))
names = list(res["things"])
W, top, rowh, left, right = 760, 64, 30, 120, 30
H = top + rowh * len(names) + 50
X = lambda v: left + (W - left - right) * v / 0.75
col = {"S": "#1b1a17", "F": "#7a6f5a", "H": "#a3361f"}
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia, serif" font-size="13">',
     f'<rect width="{W}" height="{H}" fill="#f6f3ec"/>',
     f'<text x="{left}" y="22" fill="#1b1a17" font-size="15">How far apart six drawings of one thing lie (mean 1 − cosine, blurred ink)</text>',
     f'<text x="{left}" y="42" fill="#6f6a60">grey band: 90 % of 2,000 draws of six people · ● word alone · ◆ shown their own six · ▲ shown six people</text>']
for i, n in enumerate(names):
    r = res["things"][n]; y = top + i * rowh + 14; nl = r["people_null"]
    o.append(f'<text x="{left - 10}" y="{y + 4}" text-anchor="end" fill="#1b1a17">{n}</text>')
    o.append(f'<line x1="{left}" x2="{W - right}" y1="{y}" y2="{y}" stroke="#e3ddcf"/>')
    o.append(f'<rect x="{X(nl["p5"]):.1f}" y="{y - 7}" width="{X(nl["p95"]) - X(nl["p5"]):.1f}" height="14" fill="#d9d3c6"/>')
    o.append(f'<line x1="{X(nl["median"]):.1f}" x2="{X(nl["median"]):.1f}" y1="{y - 9}" y2="{y + 9}" stroke="#6f6a60"/>')
    D = r["D"]
    if D.get("S") is not None: o.append(f'<circle cx="{X(D["S"]):.1f}" cy="{y}" r="5" fill="{col["S"]}"/>')
    if D.get("F") is not None:
        x = X(D["F"]); o.append(f'<path d="M{x:.1f} {y-6} L{x+6:.1f} {y} L{x:.1f} {y+6} L{x-6:.1f} {y} Z" fill="{col["F"]}"/>')
    if D.get("H") is not None:
        x = X(D["H"]); o.append(f'<path d="M{x:.1f} {y-6} L{x+6:.1f} {y+5} L{x-6:.1f} {y+5} Z" fill="{col["H"]}"/>')
yb = top + rowh * len(names) + 6
for v in (0, 0.25, 0.5, 0.75):
    o.append(f'<text x="{X(v):.1f}" y="{yb + 12}" text-anchor="middle" fill="#6f6a60">{v:.2f}</text>')
o.append(f'<text x="{left}" y="{yb + 32}" fill="#6f6a60">0 = the same picture; to the left, more alike</text></svg>')
open(os.path.join(HERE, "figure.svg"), "w").write("\n".join(o))
print("figure.svg written")
