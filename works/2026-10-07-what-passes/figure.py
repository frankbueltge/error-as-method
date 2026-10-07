"""figure.svg: the 6 x 5 matrix of what passed, from results.json. python3 figure.py"""
import json
r = json.load(open("results.json")); c = r["cells"]
Q = [("R1_day", "day"), ("R2_season", "month"), ("R3_coupling", "coupling"), ("R4_irregular", "a singular day"), ("R5_peak_hour", "peak hour")]
A = [("A1", "literal"), ("A2", "slowed x4"), ("A3", "one minute"), ("A4", "day only"), ("A5", "change"), ("A6", "day only, slow")]
COL = {"right": "#9cc3a4", "wrong": "#e0937f", "silent": "#ece7dc"}
W, X0, Y0, CW, CH = 760, 170, 70, 116, 40
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Y0 + CH * 7 + 60}" font-family="Georgia, serif" font-size="14">',
     f'<rect width="100%" height="100%" fill="#f4f1ea"/>',
     '<text x="20" y="30" font-size="19" fill="#1d1c1a">What Passes: one river, one ear, six translations</text>',
     '<text x="20" y="52" font-size="12" fill="#6b665d">Merced at Happy Isles, Apr-Jul 2026 (USGS 11264500). Cells: the practice\'s answer through each translation.</text>']
for j, (k, t) in enumerate(Q):
    o.append(f'<text x="{X0 + j * CW + CW / 2}" y="{Y0 + 24}" text-anchor="middle" fill="#6b665d">{t}</text>')
o.append(f'<text x="20" y="{Y0 + CH + 26}" font-weight="bold" fill="#1d1c1a">river\'s own tool</text>')
for j, (k, t) in enumerate(Q):
    v = r["home"][k] + (":00" if k == "R5_peak_hour" else "")
    o.append(f'<text x="{X0 + j * CW + CW / 2}" y="{Y0 + CH + 26}" text-anchor="middle" font-weight="bold" fill="#1d1c1a">{v}</text>')
for i, (a, lab) in enumerate(A):
    y = Y0 + CH * (i + 2)
    o.append(f'<text x="20" y="{y + 25}" fill="#1d1c1a">{a} {lab}</text>')
    for j, (k, t) in enumerate(Q):
        cell = c[f"{a}.{k}"]; x = X0 + j * CW
        o.append(f'<rect x="{x + 2}" y="{y + 2}" width="{CW - 4}" height="{CH - 4}" fill="{COL[cell["verdict"]]}"/>')
        if not cell["forecast_hit"]:
            o.append(f'<rect x="{x + 6}" y="{y + 6}" width="{CW - 12}" height="{CH - 12}" fill="none" stroke="#1d1c1a" stroke-dasharray="4 3"/>')
        txt = "–" if cell["answer"] == "-" else cell["answer"]
        o.append(f'<text x="{x + CW / 2}" y="{y + 25}" text-anchor="middle" fill="#1d1c1a">{txt}</text>')
yb = Y0 + CH * 8 + 22
o.append(f'<text x="20" y="{yb}" font-size="12" fill="#6b665d">green: agrees with the river\'s tool · red: disagrees · grey: nothing passed · dashed: the practice forecast otherwise. 17 of 18 right; all 6 forecast misses on the singular day.</text>')
o.append("</svg>")
open("figure.svg", "w").write("\n".join(o) + "\n"); print("figure.svg")
