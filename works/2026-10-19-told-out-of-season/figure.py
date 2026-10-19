"""figure.py: writes figure.svg from kinds.json and plan-ordered face data: three rows (told January-March, told
October-December, told nothing), six squares each, coloured by the maker's favoured kind (coder H, grouped by
facedata.py's KIND rule)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
F = json.loads(open(os.path.join(HERE, "face-data.js"), encoding="utf-8").read()[len("window.FACE="):-2])
COL = {"stream": "#2f6a8c", "store": "#a8461c", "sun": "#b8892a", "other": "#8a867d"}
NAME = {"stream": "a melt-fed stream (true)", "store": "a store charged on a schedule", "sun": "a sun-driven temperature", "other": "something else"}
ROWS = [("C", "told 15 Jan – 16 Mar"), ("A", "told 15 Oct – 14 Dec"), ("N", "told nothing")]
o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 300" font-family="Georgia, serif">',
     '<rect width="760" height="300" fill="#f4f1ea"/>',
     '<text x="20" y="30" font-size="17" fill="#1d1c1a">One picture, eighteen makers: what each said had been measured</text>']
for r, (c, lab) in enumerate(ROWS):
    y = 60 + r * 62
    o.append('<text x="20" y="%d" font-size="14" fill="#1d1c1a">%s</text>' % (y + 28, lab))
    ms = sorted([m for m in F["makers"] if m["cell"] == c], key=lambda m: m["kind"])
    for i, m in enumerate(ms):
        o.append('<rect x="%d" y="%d" width="44" height="44" rx="3" fill="%s"><title>%s %s</title></rect>' % (200 + i * 52, y, COL[m["kind"]], m["m"], m["title"]))
for i, k in enumerate(["stream", "store", "sun", "other"]):
    x = 20 + i * 185
    o.append('<rect x="%d" y="262" width="14" height="14" rx="2" fill="%s"/><text x="%d" y="274" font-size="12" fill="#6b675f">%s</text>' % (x, COL[k], x + 20, NAME[k]))
o.append("</svg>")
open(os.path.join(HERE, "figure.svg"), "w", encoding="utf-8").write("\n".join(o))
