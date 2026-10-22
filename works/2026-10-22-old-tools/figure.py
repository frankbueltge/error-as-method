"""figure.py: figure.svg, the sixteen choices (rows, grouped by instrument) against the five shelves
(columns), coloured by coder A's code. Read from results.json."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); res = json.load(open(os.path.join(H, "results.json")))
cols = ["PLOT", "CYCLES", "GAPS", "DIGITS", "GENERAL28"]; head = ["PLOT", "CYCLES", "GAPS", "FIRST DIGITS", "exp. 28 general"]
order = ["PLOT", "CYCLES", "GAPS", "DIGITS"]
rooms = sorted(res["rooms"], key=lambda r: (order.index(res["rooms"][r]["arm"]), r))
C = {"SAME": "#a3341f", "KIN": "#d9a441", "OFF": "#e6e1d6"}
W, x0, y0, cw, rh = 900, 330, 110, 110, 26
s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" font-family="Georgia, serif">' % (W, y0 + rh * 16 + 70),
     '<rect width="100%" height="100%" fill="#f7f4ee"/>',
     '<text x="20" y="34" font-size="20" fill="#1b1b1b">Old Tools: which shelf each maker chose from</text>',
     '<text x="20" y="58" font-size="13" fill="#555">rows: 16 makers, grouped by the instrument they held · columns: shelves named before any maker ran · blind codes</text>']
for j, h in enumerate(head):
    s.append('<text x="%d" y="%d" font-size="13" text-anchor="middle" fill="#1b1b1b">%s</text>' % (x0 + j * cw + cw / 2, y0 - 12, h))
for i, r in enumerate(rooms):
    x = res["rooms"][r]; y = y0 + i * rh
    if i % 4 == 0 and i: s.append('<line x1="20" x2="%d" y1="%d" y2="%d" stroke="#999"/>' % (W - 20, y - 1, y - 1))
    s.append('<text x="20" y="%d" font-size="12.5" fill="#1b1b1b">%s · %s · %s</text>' % (y + 17, x["arm"].replace("DIGITS", "FIRST DIGITS"), r, x["item"]))
    for j, c in enumerate(cols):
        code = x["codes"][c]; own = c == x["arm"]
        s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"%s/>' % (x0 + j * cw + 6, y + 3, cw - 12, rh - 6, C[code],
                 ' stroke="#1b1b1b" stroke-width="2"' if own else ""))
y = y0 + rh * 16 + 30
for k, (lab, c) in enumerate([("same dataset", "#a3341f"), ("same phenomenon", "#d9a441"), ("off", "#e6e1d6")]):
    s.append('<rect x="%d" y="%d" width="18" height="14" fill="%s"/><text x="%d" y="%d" font-size="12.5">%s</text>' % (20 + k * 170, y, c, 44 + k * 170, y + 12, lab))
s.append('<text x="540" y="%d" font-size="12.5">outlined: the maker\'s own instrument</text>' % (y + 12))
s.append("</svg>")
open(os.path.join(H, "figure.svg"), "w").write("\n".join(s))
