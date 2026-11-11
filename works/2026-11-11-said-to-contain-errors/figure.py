"""figure.svg: per-instance rho with the truth by arm, against experiment 51's reversed arm; and how many doubted the list."""
import json
r = json.load(open("results.json")); r51 = json.load(open("../2026-11-08-read-backwards/results.json"))
W, H = 920, 380; X0, X1, Y0, Y1 = 60, 590, 40, 320
Y = lambda v: Y1 - (v + 1) / 2 * (Y1 - Y0)
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="system-ui,sans-serif" font-size="13">',
     '<rect width="100%" height="100%" fill="#f4f2ec"/>',
     '<text x="20" y="24" font-size="15" fill="#1c1d1f">Each instance\'s agreement with the truth (Spearman ρ) on the 32 places it was not told</text>']
for v in (-1, -0.5, 0, 0.5, 1):
    o.append(f'<line x1="{X0}" x2="{X1}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="#d5d2c9"/><text x="{X0-8}" y="{Y(v)+4:.1f}" text-anchor="end" fill="#676a6e">{v:+.1f}</text>')
cols = [("51 R", "exp. 51: pageviews,\nreversed, as fact", "#7a4b8c", [m for m in r51["makers"] if m.startswith("R")], r51),
        ("R", "rivers: reversed,\nas fact", "#b4380f", None, r), ("D", "rivers: reversed,\n‘may contain errors’", "#c88a12", None, r),
        ("T", "rivers: true,\n‘may contain errors’", "#2d7a5a", None, r), ("U", "rivers:\ntold nothing", "#6b6f75", None, r)]
for k, (a, lab, col, ms, src) in enumerate(cols):
    cx = X0 + 40 + k * 104
    ms = ms or [m for m in src["makers"] if m.startswith(a)]
    for j, m in enumerate(sorted(ms)):
        v = src["makers"][m]["rho_truth"] if "rho_truth" in src["makers"][m] else src["makers"][m]["rho"]
        o.append(f'<circle cx="{cx - 15 + j * 6}" cy="{Y(v):.1f}" r="5" fill="{col}" fill-opacity=".85"/>')
    for i, line in enumerate(lab.split("\n")):
        o.append(f'<text x="{cx}" y="{Y1 + 22 + i * 15}" text-anchor="middle" fill="#1c1d1f" font-size="11">{line}</text>')
BX = 640
o.append(f'<text x="{BX}" y="70" fill="#1c1d1f">Said the told list was wrong</text>')
for i, (lab, n, col) in enumerate([("51 R (pageviews, reversed)", 0, "#7a4b8c"), ("R (reversed, as fact)", 6, "#b4380f"),
                                    ("D (reversed, may err)", 6, "#c88a12"), ("T (true, may err)", 5, "#2d7a5a")]):
    y = 100 + i * 52
    o.append(f'<text x="{BX}" y="{y}" fill="#676a6e" font-size="12">{lab}</text>')
    for j in range(6):
        o.append(f'<rect x="{BX + j * 34}" y="{y + 8}" width="28" height="18" rx="3" fill="{col if j < n else "none"}" stroke="{col}"/>')
    o.append(f'<text x="{BX + 212}" y="{y + 22}" fill="#1c1d1f">{n} of 6</text>')
o.append(f'<text x="{BX}" y="330" fill="#676a6e" font-size="11">Experiment 51 blamed the list 0 of 6 (both coders);</text>')
o.append(f'<text x="{BX}" y="345" fill="#676a6e" font-size="11">tonight 17 of 18, both coders agreeing on all 18.</text>')
o.append("</svg>")
open("figure.svg", "w").write("\n".join(o))
