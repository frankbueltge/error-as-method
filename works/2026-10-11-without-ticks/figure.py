"""figure.py -- figure.svg: the ledger of what each maker named (ledger.json), twelve columns by preparation, with
the unit each page carries underneath. Static, for the site page that renders work.md."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); L = json.load(open(os.path.join(H, "ledger.json")))
plan = json.load(open(os.path.join(H, "plan.json")))
cols = [p["maker"] for a in "TIL" for p in plan if p["arm"] == a]
named = list(L[cols[0]]["named"].keys())
C = {"T": "#2f5d8a", "I": "#7a5a1e", "L": "#8a3b2f"}
x0, cw, y0, rh = 230, 46, 70, 30
W, Hh = x0 + cw * 12 + 3 * 14 + 20, y0 + rh * (len(named) + 1) + 60
gx = lambda i: x0 + i * cw + (i // 4) * 14 + cw / 2
s = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Georgia, serif" font-size="14">' % (W, Hh, W, Hh),
     '<rect width="100%" height="100%" fill="#f4f1ea"/>',
     '<text x="20" y="28" font-size="17" fill="#1c1a16">What twelve makers named, by the preparation they were given</text>']
for j, a in enumerate("TIL"):
    lab = {"T": "T table", "I": "I picture, axes", "L": "L lossy picture"}[a]
    s.append('<text x="%.1f" y="56" text-anchor="middle" fill="%s">%s</text>' % ((gx(4 * j) + gx(4 * j + 3)) / 2, C[a], lab))
for r, k in enumerate(named):
    y = y0 + r * rh + rh / 2
    s.append('<text x="20" y="%.1f" fill="#1c1a16">%s</text>' % (y + 5, k.replace("&", "&amp;")))
    s.append('<line x1="20" x2="%d" y1="%.1f" y2="%.1f" stroke="#d6cfc2"/>' % (W - 20, y + rh / 2, y + rh / 2))
    for i, m in enumerate(cols):
        if L[m]["named"][k]: s.append('<circle cx="%.1f" cy="%.1f" r="7" fill="%s"/>' % (gx(i), y, C[L[m]["arm"]]))
        else: s.append('<circle cx="%.1f" cy="%.1f" r="1.6" fill="#8a8478"/>' % (gx(i), y))
y = y0 + len(named) * rh + rh / 2
s.append('<text x="20" y="%.1f" fill="#6a645a">unit carried</text>' % (y + 5))
for i, m in enumerate(cols):
    s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-family="monospace" font-size="10" fill="#6a645a">%s</text>' % (gx(i), y + 4, L[m]["unit"]))
    s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-family="monospace" font-size="10" fill="#6a645a">%s</text>' % (gx(i), y + 22, m))
s.append('<text x="20" y="%d" font-size="12" fill="#6a645a">Searched in note, report and page after makers and coder finished (ledger.py). Data: SSA via FiveThirtyEight, CC BY 4.0.</text>' % (Hh - 12))
s.append("</svg>")
open(os.path.join(H, "figure.svg"), "w", encoding="utf-8").write("\n".join(s)); print("ok")
