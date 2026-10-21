"""figure.py: Session 145. figure.svg from results.json: the 24 mutants in their three arms, each placed by what
became of it (broken; unchanged and accepted; changed and refused for misstating the table; changed and refused
for being unreadable; changed and accepted). No mutant falls in the last column, which is where information
would sit. The category of each refusal is the practice's reading of W's sentence, listed in REFUSED below."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(H, "results.json")))["rows"]
MISSTATES = {"u3", "t3", "t8", "s1", "s2", "s3", "s5", "s7"}   # W's sentence names a wrong value, order or label
REFUSED = {k: ("misstates" if k in MISSTATES else "unreadable") for k in R}
def cat(k):
    r = R[k]
    if r["x_broken"] == "yes": return 0
    if r["x_distance"] == 0 and r["w_works"] == "yes": return 1
    if r["w_works"] == "no": return 2 if REFUSED[k] == "misstates" else 3
    return 4
cols = ["broken", "unchanged, accepted", "changed, refused: misstates the table", "changed, refused: unreadable", "far, accepted (information)"]
W, X0, CW, Y0, RH = 1000, 150, 170, 120, 70
s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d 400" font-family="Georgia, serif">' % W,
     '<rect width="100%" height="100%" fill="#eef0ea"/>',
     '<text x="20" y="36" font-size="22" fill="#16191a">Under Other Names: 24 swaps of a table under one page</text>',
     '<text x="20" y="60" font-size="14" fill="#5f6763">Blind coder X (broken, distance), fresh judge W (works or not). The last column, far and still a work, stays empty.</text>']
for i, c in enumerate(cols):
    x = X0 + i * CW; s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="#c9cec6"/>' % (x, Y0 - 10, CW - 8, 3 * RH + 10, "#fbfcf8" if i < 4 else "#f3e9e4"))
    words = c.split(": "); 
    for j, w_ in enumerate(words): s.append('<text x="%d" y="%d" font-size="12.5" fill="#5f6763">%s</text>' % (x + 6, Y0 - 36 + j * 15, w_))
names = {"U": "U · blind", "T": "T · typed", "S": "S · seeing"}
for a, arm in enumerate("UTS"):
    y = Y0 + a * RH + 34; s.append('<text x="20" y="%d" font-size="15" fill="#16191a">%s</text>' % (y, names[arm]))
    slots = {}
    for k in [arm.lower() + str(i) for i in range(1, 9)]:
        c = cat(k); n = slots.get(c, 0); slots[c] = n + 1
        cx = X0 + c * CW + 22 + (n % 5) * 30; cy = y - 12 + (n // 5) * 28
        fill = ["#9aa39d", "#2d6b4a", "#b2412a", "#6b5a7a", "#16191a"][c]
        s.append('<circle cx="%d" cy="%d" r="11" fill="%s"/><text x="%d" y="%d" font-size="10" fill="#fff" text-anchor="middle">%s</text>' % (cx, cy, fill, cx, cy + 3.5, k))
s.append('<text x="20" y="385" font-size="12" fill="#5f6763">Parent: The Liquid Interval (plain maker c4). PubChem periodic table, 118 elements. Session 145, 2026-10-21.</text></svg>')
open(os.path.join(H, "figure.svg"), "w").write("\n".join(s)); print("figure.svg")
