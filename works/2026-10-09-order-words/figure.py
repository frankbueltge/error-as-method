"""figure.py -- figure.svg: each maker's return, note by note: the blind coder's fit and what the maker did."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(H, "face-data.js")).read(); F = json.loads(src[src.index("{"):src.rindex("}") + 1])
M = F["makers"]; W, ROW = 760, 30
fillc = {"APPLIES": "#1d1b18", "PARTLY": "#b48a2c", "ABSENT": "#ffffff"}
s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d 470" font-family="Georgia, serif" font-size="13">' % W,
     '<rect width="100%%" height="100%%" fill="#f4f1ea"/>',
     '<text x="20" y="30" font-size="18" font-style="italic">Order-Words: twelve works came back</text>',
     '<text x="20" y="50" font-size="12" fill="#6b665d">Square fill: is the note visible in this work? (blind coder: black applies, ochre partly, white absent). Mark: what the maker did.</text>']
y = 80
labels = {"H": "nothing said", "S": "notes on its own picture", "X": "notes on another maker's picture"}
for a in "HSX":
    s.append('<text x="20" y="%d" font-size="14" font-weight="bold">%s</text>' % (y, labels[a])); y += 12
    for m in [m for m in M if m["ret"] == a]:
        y += ROW
        s.append('<text x="30" y="%d">%s</text>' % (y, m["title"].replace("&", "&amp;")))
        if a == "H":
            s.append('<text x="260" y="%d" fill="#6b665d" font-size="12">no notes</text>' % y)
        for i in range(len(m["notes"])):
            x = 260 + i * 34
            s.append('<rect x="%d" y="%d" width="22" height="22" fill="%s" stroke="#1d1b18"/>' % (x, y - 16, fillc[m["fit"][i]]))
            if m["codes"][i] == "ACTED":
                s.append('<path d="M%d %d l5 6 l11 -14" stroke="#2f6b4a" stroke-width="3" fill="none"/>' % (x + 3, y - 4))
            else:
                s.append('<path d="M%d %d l14 14 M%d %d l-14 14" stroke="#a8321e" stroke-width="2.5"/>' % (x + 4, y - 12, x + 18, y - 12))
        out = ("changed" if m["reopened"] else "left as it was")
        if m["pair"]: out += ", defects %d → %d" % (m["pair"]["defects_first"], m["pair"]["defects_second"])
        if m["pair"] and m["pair"]["rating"] == 3: out += " (picture identical)"
        s.append('<text x="380" y="%d" font-size="12">%s</text>' % (y, out))
    y += 22
s.append('<text x="20" y="%d" font-size="12" fill="#6b665d">✓ acted on the note   ✗ declined: "not in my work". Of 8 foreign notes the coder found absent, makers acted on 1, by translating it.</text>' % (y + 4))
s.append('</svg>')
s[0] = s[0].replace('0 0 %d 470' % W, '0 0 %d %d' % (W, y + 24))
open(os.path.join(H, "figure.svg"), "w").write("\n".join(s))
print("figure.svg", y)
