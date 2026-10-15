"""figure.py: figure.svg -- the record folded on the sun's day and on the moon's day (mean of 48 bins, all days as
faint lines), and beneath, the twelve makers by cell with what each named. From materials/hourly.json and results.json."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
h = json.load(open(os.path.join(HERE, "materials", "hourly.json")))["h_nT"]
R = json.load(open(os.path.join(HERE, "results.json")))
A = json.load(open(os.path.join(HERE, "coder", "B", "answers.json")))
lo, hi = min(h), max(h)
W, H = 900, 470
o = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Georgia,serif">' % (W, H, W, H),
     '<rect width="%d" height="%d" fill="#f4f1ea"/>' % (W, H)]
def fold(x0, period, shift, title):
    w, hh, y0 = 400, 220, 40
    o.append('<text x="%d" y="28" font-size="15" fill="#1d1f22">%s</text>' % (x0, title))
    o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#fbf9f4" stroke="#d8d2c4"/>' % (x0, y0, w, hh))
    lines, cur, prev = [], [], -1
    for i, v in enumerate(h):
        t = i + 0.5 + shift; turn = int(t // period); ph = (t - turn * period) / period
        pt = "%.1f,%.1f" % (x0 + 6 + ph * (w - 12), y0 + 6 + (hi - v) / (hi - lo) * (hh - 12))
        if turn != prev and cur: lines.append(cur); cur = []
        cur.append(pt); prev = turn
    lines.append(cur)
    for l in lines:
        if len(l) > 1: o.append('<polyline points="%s" fill="none" stroke="#1d1f22" stroke-opacity="0.13" stroke-width="0.8"/>' % " ".join(l))
    B = 48; s = [0.0] * B; k = [0] * B
    for i, v in enumerate(h):
        b = int((((i + 0.5 + shift) / period) % 1) * B); s[b] += v; k[b] += 1
    pts = " ".join("%.1f,%.1f" % (x0 + 6 + (b + .5) / B * (w - 12), y0 + 6 + (hi - s[b] / k[b]) / (hi - lo) * (hh - 12)) for b in range(B) if k[b])
    o.append('<polyline points="%s" fill="none" stroke="#a4471f" stroke-width="2.4"/>' % pts)
fold(30, 24.0, 24 - 7.02, "folded on the sun's day, 24 h")
fold(470, 24.8412, 0, "folded on the moon's day, 24 h 50 min (a tide's clock)")
y = 300
for cx, cell, head in ((30, "T", 'told: "a record of the water level in a tidal harbour"'), (470, "N", "told nothing")):
    o.append('<text x="%d" y="%d" font-size="14" fill="%s">%s</text>' % (cx, y, "#a4471f" if cell == "T" else "#2d5470", head))
    for j, m in enumerate(R["cells"][cell]):
        q = A[m]["C5_quote"].lower()
        name = "relative humidity?" if "humid" in q else ("an animal's body clock?" if "biolog" in q else "cannot tell")
        verdict = "  - not a tide" if A[m]["C7"] == "yes" else ""
        o.append('<text x="%d" y="%d" font-size="12.5" fill="#1d1f22">%s  %s  (%s h)%s</text>' % (cx, y + 24 + j * 22, A[m]["C9"].replace("&", "&amp;"), "→ " + name, A[m]["C2"], verdict))
o.append('<text x="30" y="%d" font-size="12" fill="#5c5f66">The record: Earth\'s magnetic field (H) at Boulder, Colorado, hourly, 2 Jul - 31 Aug 2025 (USGS). No maker named it.</text>' % (H - 14))
o.append("</svg>")
open(os.path.join(HERE, "figure.svg"), "w", encoding="utf-8").write("\n".join(o))
print("figure.svg", sum(len(x) for x in o))
