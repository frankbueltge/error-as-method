"""figure.svg: share of each kind of notice per year of last version (Session 104)."""
import json, collections
n = {r["id"]: r for r in json.load(open("notices.json"))}
by = collections.defaultdict(lambda: [0] * 5)
for c in json.load(open("coded.json")):
    k = 0 if c["bare_corrected"] else 1 if c["admin"] else 2 if c["located"] else 3 if c["error"] else 4
    by[int(n[c["id"]]["updated"][:4])][k] += 1
years = list(range(1996, 2027))  # before 1996 fewer than ten notices a year
fill = {0: "none", 1: "#9a958b", 2: "#7a1712", 3: "#c8553d", 4: "#d9c9a3"}
order = [0, 1, 4, 3, 2]
names = {0: "said nothing else", 1: "withdrawn by administrators", 4: "a reason, not an error",
         3: "an error, not where", 2: "an error, and where"}
W, H, L, T, B, bw = 760, 400, 46, 30, 300, 18
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia,serif" font-size="11">',
     f'<rect width="{W}" height="{H}" fill="#f4f1ea"/>',
     f'<text x="{L}" y="18" font-size="13" fill="#1d1b18">What 7,282 arXiv withdrawal notices say, by year of last version (share of each year)</text>']
for p in (0, 50, 100):
    y = B - (B - T) * p / 100
    o.append(f'<line x1="{L}" x2="{L + len(years) * (bw + 4)}" y1="{y}" y2="{y}" stroke="#cfc8ba" stroke-width="0.6"/>'
             f'<text x="{L - 6}" y="{y + 4}" text-anchor="end" fill="#6f6a60">{p}%</text>')
for i, yr in enumerate(years):
    v = by[yr]; tot = sum(v) or 1; x = L + i * (bw + 4); y = B
    for k in order:
        h = (B - T) * v[k] / tot; y -= h
        if k == 0:
            o.append(f'<rect x="{x + .5}" y="{y + .5}" width="{bw - 1}" height="{max(h - 1, 0)}" fill="#f4f1ea" stroke="#1d1b18" stroke-width="1"/>')
        else:
            o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" fill="{fill[k]}"/>')
    if yr % 2 == 0:
        o.append(f'<text x="{x + bw / 2}" y="{B + 14}" text-anchor="middle" fill="#6f6a60" font-size="9.5">{yr}</text>')
    o.append(f'<text x="{x + bw / 2}" y="{B + 26}" text-anchor="middle" fill="#9b958a" font-size="7.5">{sum(v)}</text>')
o.append(f'<text x="{L - 6}" y="{B + 26}" text-anchor="end" fill="#9b958a" font-size="7.5">n</text>')
lx = L
for k in [0, 4, 3, 2, 1]:
    sw = (f'<rect x="{lx + .5}" y="{H - 49.5}" width="10" height="10" fill="#f4f1ea" stroke="#1d1b18"/>' if k == 0
          else f'<rect x="{lx}" y="{H - 50}" width="11" height="11" fill="{fill[k]}"/>')
    o.append(sw + f'<text x="{lx + 16}" y="{H - 41}" fill="#1d1b18">{names[k]}</text>')
    lx += 16 + 5.6 * len(names[k]) + 12
o.append(f'<text x="{L}" y="{H - 14}" fill="#6f6a60" font-size="10">Coded by fixed rules, checked against a hand reading of 60. Source: arXiv API, search co:withdrawn, harvested 2026-10-04 (CC0). 1992-95 (24 notices) not drawn.</text></svg>')
open("figure.svg", "w").write("\n".join(o))
