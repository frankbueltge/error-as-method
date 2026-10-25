"""figure.svg: for the 11 phrases where the family's centre differs from the people's (posthoc.json),
the people's median, the answering instances' median and the median the describers gave the people. Session 158."""
import json, math
from pathlib import Path
HERE = Path(__file__).parent
ph = json.loads((HERE / "posthoc.json").read_text())
rows = ph["diverging"]
W, top, rh, L, R = 760, 76, 46, 170, 720
H = top + rh * len(rows) + 50
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia, serif" font-size="13">',
     f'<rect width="{W}" height="{H}" fill="#f6f3ec"/>',
     '<text x="20" y="28" font-size="16" fill="#1f1d1a">Asked to describe the people, the family gives them its own centre</text>',
     '<text x="20" y="48" fill="#6b665d">11 phrases where the answering instances\' median differs from the 46 people\'s. Each row on its own scale.</text>']
for i, d in enumerate(rows):
    y = top + i * rh + 16
    vals = [d["people"], d["A"], d["P"]]
    lo, hi = min(vals), max(vals)
    pad = (hi - lo) * 0.35 or 1
    lo, hi = lo - pad, hi + pad
    f = lambda v: L + (R - L) * (v - lo) / (hi - lo)
    num = abs(d["people"]) < 3 or d["phrase"] in ("A lot", "Several", "Many", "Fractions of", "Scores of")
    lab = (lambda v: f"{10**v:.3g}") if num else (lambda v: f"{v:.3g}%")
    o.append(f'<text x="20" y="{y+4}" fill="#1f1d1a">{d["phrase"]}</text>')
    o.append(f'<line x1="{L}" x2="{R}" y1="{y}" y2="{y}" stroke="#d8d2c4"/>')
    o.append(f'<circle cx="{f(d["people"]):.1f}" cy="{y}" r="6" fill="#3d6b8f"/>')
    o.append(f'<rect x="{f(d["A"])-5:.1f}" y="{y-5}" width="10" height="10" fill="#c2551f"/>')
    o.append(f'<line x1="{f(d["P"]):.1f}" x2="{f(d["P"]):.1f}" y1="{y-10}" y2="{y+10}" stroke="#2f7d62" stroke-width="3"/>')
    o.append(f'<text x="{f(d["people"]):.1f}" y="{y+20}" text-anchor="middle" font-size="10" fill="#3d6b8f">{lab(d["people"])}</text>')
    o.append(f'<text x="{f(d["A"]):.1f}" y="{y-9}" text-anchor="middle" font-size="10" fill="#c2551f">{lab(d["A"])}</text>')
ly = H - 22
o += [f'<circle cx="30" cy="{ly}" r="6" fill="#3d6b8f"/><text x="42" y="{ly+4}" fill="#1f1d1a">46 people, median</text>',
      f'<rect x="185" y="{ly-5}" width="10" height="10" fill="#c2551f"/><text x="202" y="{ly+4}" fill="#1f1d1a">12 instances answering, median</text>',
      f'<line x1="420" x2="420" y1="{ly-10}" y2="{ly+10}" stroke="#2f7d62" stroke-width="3"/><text x="430" y="{ly+4}" fill="#1f1d1a">6 instances describing the people: median they stated</text>', '</svg>']
(HERE / "figure.svg").write_text("\n".join(o) + "\n")
