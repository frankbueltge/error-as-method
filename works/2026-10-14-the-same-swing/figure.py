"""figure.py: figure.svg. Left, the record's mean day: dissolved oxygen and water temperature from the same sonde,
each scaled to its own range (materials/hourly.json, hours in local time, UTC-4). Right, the twelve makers by cell,
each with the quantity coder B coded (B7) and the ground it gave (B7_basis). Run after score.py."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
r = json.load(open(os.path.join(H, "results.json")))["makers"]
h = json.load(open(os.path.join(H, "materials", "hourly.json")))
def prof(s):
    p = [sum(s[d * 24 + k] for d in range(61)) / 61 for k in range(24)]
    p = p[4:] + p[:4]                                                   # UTC -> local (EDT, UTC-4): local 0 h = UTC 4 h
    lo, hi = min(p), max(p); return [(v - lo) / (hi - lo) for v in p], lo, hi
do, dlo, dhi = prof(h["do_mg_l"]); wt, tlo, thi = prof(h["water_temp_c"])
W, Ht = 820, 440
s = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Georgia, serif">' % (W, Ht, W, Ht),
     '<rect width="%d" height="%d" fill="#f3f0e8"/>' % (W, Ht),
     '<text x="20" y="34" font-size="20" fill="#1b1a17">The Same Swing: the river breathed, the makers read the weather</text>']
x0, y0, pw, ph = 40, 90, 330, 220
s.append('<text x="%d" y="72" font-size="13" fill="#6b655b">the mean day, 1 July – 30 August 2025, each scaled to its range</text>' % x0)
s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#fffdf8" stroke="#d5cec0"/>' % (x0, y0, pw, ph))
X = lambda k: x0 + 10 + k / 23 * (pw - 20); Y = lambda v: y0 + ph - 15 - v * (ph - 30)
for vals, col, wdt in ((wt, "#b3261e", 2), (do, "#2f5d8a", 3)):
    s.append('<polyline fill="none" stroke="%s" stroke-width="%d" points="%s"/>' % (col, wdt, " ".join("%.1f,%.1f" % (X(k), Y(v)) for k, v in enumerate(vals))))
for k in (0, 6, 12, 18, 23):
    s.append('<text x="%.1f" y="%d" font-size="11" fill="#6b655b" text-anchor="middle">%d h</text>' % (X(k), y0 + ph + 16, k))
s.append('<text x="%d" y="%d" font-size="13" fill="#2f5d8a">dissolved oxygen, %.1f–%.1f mg/L (what was measured)</text>' % (x0, y0 + ph + 40, dlo, dhi))
s.append('<text x="%d" y="%d" font-size="13" fill="#b3261e">water temperature, %.1f–%.1f °C (same sonde, shown to no maker)</text>' % (x0, y0 + ph + 58, tlo, thi))
s.append('<text x="%d" y="%d" font-size="11" fill="#6b655b">USGS 01646500, Potomac River at Little Falls; hours in local time</text>' % (x0, y0 + ph + 76))
cells = (("F", "300 px, the day measurable"), ("U", "40 px, told “every hour”"), ("X", "40 px, told no count"))
colmap = {"temperature": "#b3261e", "oxygen": "#2f5d8a"}
for j, (c, lab) in enumerate(cells):
    y = 90 + j * 110
    s.append('<text x="410" y="%d" font-size="14" fill="#1b1a17">%s</text>' % (y, lab))
    for k, m in enumerate(sorted(m for m in r if r[m]["cell"] == c)):
        v = r[m]; q = v["B7_category"]; quote = v["B7_quote"].lower()
        word = "an oscillation" if q == "other" and "oscillation" in quote else ("tide" if q == "other" else q)
        if q == "temperature": word = "air temperature" if "air" in quote else "temperature"
        x = 410 + k * 100
        s.append('<rect x="%d" y="%d" width="92" height="58" fill="#fffdf8" stroke="%s" stroke-width="%s"/>' % (x, y + 10, colmap.get(q, "#d5cec0"), "2" if q in colmap else "1"))
        s.append('<text x="%d" y="%d" font-size="12" fill="%s" text-anchor="middle">%s</text>' % (x + 46, y + 34, colmap.get(q, "#1b1a17"), word))
        s.append('<text x="%d" y="%d" font-size="9" fill="#6b655b" text-anchor="middle">%s · %s</text>' % (x + 46, y + 54, m, "measured the day" if v["measured_day"] else ("supplied a day" if v["B3"] == "supplied" else "no day")))
s.append('<text x="410" y="420" font-size="12" fill="#6b655b">what each maker named (coder B, B7). Oxygen: 0 of 12.</text>')
open(os.path.join(H, "figure.svg"), "w").write("\n".join(s + ["</svg>"]))
print("figure.svg")
