"""figure.py: writes figure.svg from results.json and face-data.js: for the twelve makers told where the record was
made, where the place went (on the page, and what the report did with it); for the twelve told what it records, whether
the kind was said to be given. Six makers told nothing are shown for the kind."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(H, "results.json")))
F = json.loads(open(os.path.join(H, "face-data.js"), encoding="utf-8").read()[len("window.FACE="):].rstrip().rstrip(";"))
told = [x for x in F["makers"] if x["trail"]]; c = R["counts"]
rows = [("on the page", sum(x["page_place"] for x in told), "#1f6a6a"),
        ("in the report, as given to it", sum(x["trail"] == "given" for x in told), "#c0841a"),
        ("in the report, as a station it knew", sum(x["trail"] == "memory" for x in told), "#6a3d8a"),
        ("in the report, as plain fact", sum(x["trail"] == "plain" for x in told), "#3d5266"),
        ("in the report, only as “about 48° N”", sum(x["trail"] == "latitude" for x in told), "#3d5266")]
W, Hh = 880, 420
s = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Georgia,serif">' % (W, Hh, W, Hh),
     '<rect width="%d" height="%d" fill="#f4f0e6"/>' % (W, Hh),
     '<text x="20" y="32" font-size="19" fill="#1d1d1f">Told Where: where the place went</text>',
     '<text x="20" y="54" font-size="12.5" fill="#5f5e63">Twelve makers were told “Fort Peck, Montana, 634 m”. Each square is one of them.</text>']
for j, (lab, v, col) in enumerate(rows):
    y = 80 + j * 40
    s.append('<text x="20" y="%d" font-size="14" fill="#1d1d1f">%s</text>' % (y + 16, lab))
    for i in range(12):
        s.append('<rect x="%d" y="%d" width="18" height="18" fill="%s" stroke="%s" stroke-width="1.4"/>' % (360 + i * 23, y + 2, col if i < v else "none", col))
    s.append('<text x="%d" y="%d" font-size="13" fill="#5f5e63">%d of 12</text>' % (360 + 12 * 23 + 10, y + 16, v))
y = 300
s.append('<text x="20" y="%d" font-size="14" fill="#1d1d1f">Told what (sunlight), says it was stated</text>' % (y + 16))
kg = c["K"]["holds_kind_apart"] + c["KP"]["holds_kind_apart"]
for i in range(12):
    s.append('<rect x="%d" y="%d" width="18" height="18" fill="%s" stroke="#9a5b12" stroke-width="1.4"/>' % (360 + i * 23, y + 2, "#9a5b12" if i < kg else "none"))
s.append('<text x="%d" y="%d" font-size="13" fill="#5f5e63">%d of 12</text>' % (360 + 12 * 23 + 10, y + 16, kg))
s.append('<text x="20" y="%d" font-size="14" fill="#1d1d1f">Told nothing, read sunlight anyway</text>' % (y + 56))
for i in range(6):
    s.append('<rect x="%d" y="%d" width="18" height="18" fill="%s" stroke="#3d5266" stroke-width="1.4"/>' % (360 + i * 23, y + 42, "#3d5266" if i < c["N"]["favours_light"] else "none"))
s.append('<text x="%d" y="%d" font-size="13" fill="#5f5e63">%d of 6</text>' % (360 + 6 * 23 + 10, y + 56, c["N"]["favours_light"]))
s.append('<text x="20" y="%d" font-size="11" fill="#5f5e63">Record: global solar irradiance, SURFRAD Fort Peck MT, hourly, 15 Jul to 13 Sep 2025 (NOAA GML, CC0). Coders H (reports) and D (pages); report classes drawn after reading.</text>' % (Hh - 14))
s.append("</svg>")
open(os.path.join(H, "figure.svg"), "w", encoding="utf-8").write("\n".join(s)); print([r[1] for r in rows], kg)
