"""figure.py: figure.svg from plan.json and seasons.json -- where in the year each maker put the record, against its
true span. The bands are the practice's post hoc reading of each maker's words onto the calendar (as on the face)."""
import json, os, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "seasons.json"), encoding="utf-8"))["makers"]
D0, D1, X0, X1 = dt.date(2025, 6, 1), dt.date(2025, 12, 31), 150, 880
X = lambda m, d: X0 + (dt.date(2025, m, d) - D0).days / (D1 - D0).days * (X1 - X0)
B = {"autumn": ((9, 22), (12, 21)), "late summer": ((8, 1), (9, 22)), "late summer into autumn": ((8, 1), (10, 31))}
rows = sorted(S.items(), key=lambda kv: (kv[1]["cell"], kv[0]))
H = 60 + 18 * len(rows) + 40
o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 %d" font-family="Georgia, serif">' % H,
     '<rect width="900" height="%d" fill="#f4f1ea"/>' % H,
     '<text x="20" y="26" font-size="16" fill="#1d1c1a">Told When: where in the year twelve makers put one record</text>',
     '<rect x="%.1f" y="40" width="%.1f" height="%d" fill="#3d7a3a" opacity="0.14"/>' % (X(7, 15), X(9, 14) - X(7, 15), 18 * len(rows) + 10)]
for i, mn in enumerate(["Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
    x = X(6 + i, 1); o.append('<line x1="%.1f" x2="%.1f" y1="40" y2="%d" stroke="#d8d2c5"/><text x="%.1f" y="%d" font-size="11" fill="#6b675f">%s</text>' % (x, x, 50 + 18 * len(rows), x + 3, 64 + 18 * len(rows), mn))
for i, (m, v) in enumerate(rows):
    y = 46 + 18 * i; col = "#9a4a1c" if v["cell"] == "W" else "#2f5d7c"
    o.append('<text x="%d" y="%d" font-size="11" text-anchor="end" fill="%s">%s %s</text>' % (X0 - 8, y + 10, col, m, "told the dates" if v["cell"] == "W" else "told nothing"))
    b = ((9, 1), (10, 31)) if m == "m12" else B.get(v["class"])
    if b: o.append('<rect x="%.1f" y="%d" width="%.1f" height="11" fill="%s"/>' % (X(*b[0]), y, X(*b[1]) - X(*b[0]), col))
    else: o.append('<text x="%.1f" y="%d" font-size="10" fill="%s">dates only, no season named</text>' % (X(7, 15) + 4, y + 9, col))
o.append('<text x="20" y="%d" font-size="11" fill="#3d7a3a">shaded: the record, soil temperature at 5 cm, Starkville MS, 15 Jul to 13 Sep 2025</text>' % (H - 10))
open(os.path.join(HERE, "figure.svg"), "w", encoding="utf-8").write("\n".join(o + ["</svg>"]))
print("figure.svg")
