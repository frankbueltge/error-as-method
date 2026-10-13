"""figure.py: figure.svg, the twelve makers in the 2 x 2 of grain and account. A filled disc: the maker measured a
cycle and named what makes it (coder B: B2 yes and B5 yes). An open ring: it did not. The letter under each: P draws
the picture's pixels, V draws values fitted back (B10). Run after score.py."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
r = json.load(open(os.path.join(H, "results.json")))["cells"]
W, Ht = 760, 420
s = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Georgia, serif">' % (W, Ht, W, Ht),
     '<rect width="%d" height="%d" fill="#f3f0e8"/>' % (W, Ht),
     '<text x="20" y="34" font-size="20" fill="#1b1a17">Told the Hour: the grain decided, the sentence did not</text>',
     '<text x="250" y="78" font-size="14" fill="#6b655b" text-anchor="middle">told “one value every hour”</text>',
     '<text x="560" y="78" font-size="14" fill="#6b655b" text-anchor="middle">told “at equal intervals”</text>']
for j, (g, lab) in enumerate((("F", "300 × 90 px"), ("C", "40 × 12 px"))):
    y = 150 + j * 150
    s.append('<text x="20" y="%d" font-size="14" fill="#1b1a17">%s</text>' % (y + 5, lab))
    for i, a in enumerate("UN"):
        cx0 = 190 + i * 310
        s.append('<rect x="%d" y="%d" width="240" height="120" fill="#fffdf8" stroke="#d5cec0"/>' % (cx0 - 50, y - 55))
        for k, (m, v) in enumerate(sorted(r[g + a].items())):
            cx = cx0 + k * 60 + 10
            if v["recognised"]: s.append('<circle cx="%d" cy="%d" r="16" fill="#2f5d8a"/>' % (cx, y - 10))
            else: s.append('<circle cx="%d" cy="%d" r="15" fill="none" stroke="#7a5a1e" stroke-width="2"/>' % (cx, y - 10))
            s.append('<text x="%d" y="%d" font-size="13" fill="#1b1a17" text-anchor="middle">%s</text>' % (cx, y + 25, "V" if v["B10"] == "items" else "P"))
            s.append('<text x="%d" y="%d" font-size="11" fill="#6b655b" text-anchor="middle">%s</text>' % (cx, y + 42, m))
s.append('<text x="20" y="400" font-size="12" fill="#6b655b">filled: measured a cycle and named what makes it · ring: measured none · P: draws the pixels · V: draws values fitted back (coder B)</text>')
open(os.path.join(H, "figure.svg"), "w").write("\n".join(s + ["</svg>"]))
