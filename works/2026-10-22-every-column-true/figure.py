"""figure.py (Session 147): figure.svg, the twenty pages against the six seats. Rows: each work as made, then its four
dealt copies. A filled square is a refusal or a 'dealt' call; an open square is acceptance or a 'real' call. The
mark at the left flags the pages of K (words true of their own drawing, false to the table)."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); r = json.load(open(os.path.join(H, "results.json")))
M = {m["id"]: m for m in json.load(open(os.path.join(H, "mutants.json")))["mutants"]}
T = r["table"]; K = set(r["K"]); low = lambda s: str(s).strip().lower()
seats = [("W", "W: works?", lambda t: low(t["W"]) == "no"), ("WT", "WT: works? (has table)", lambda t: low(t["WT"]) == "no"),
         ("P", "P: words false?", lambda t: low(t["P_words"]) == "no"), ("G", "G: dealt?", lambda t: low(t["G"]).startswith("sh")),
         ("H", "the practice: dealt?", lambda t: low(t["H"]).startswith("sh")), ("V", "V: false to table?", lambda t: low(t["V"]) == "no")]
rows = [k for c in ["c1", "c2", "c3", "c4"] for k in [c] + [c + s for s in ["o1", "o2", "o3", "a"]]]
x0, y0, cw, rh = 280, 92, 112, 24; W_ = x0 + cw * len(seats) + 30; H_ = y0 + rh * len(rows) + 4 * 10 + 70
s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" font-family="Georgia,serif" font-size="13">' % (W_, H_),
     '<rect width="100%%" height="100%%" fill="#efece4"/>',
     '<text x="20" y="30" font-size="19" fill="#1d1b17">Every Column True: twenty pages, six seats</text>',
     '<text x="20" y="52" fill="#68625a">filled = refused / called dealt / called false; open = accepted / real / agrees. &#9654; = page in K (its words true of its drawing, false to the table).</text>']
for i, (_, lab, _) in enumerate(seats):
    s.append('<text x="%d" y="%d" text-anchor="middle" fill="#1d1b17" font-size="11.5">%s</text>' % (x0 + cw * i + cw / 2, y0 - 12, lab.split(":")[0]))
    s.append('<text x="%d" y="%d" text-anchor="middle" fill="#68625a" font-size="10.5">%s</text>' % (x0 + cw * i + cw / 2, y0 - 0, lab.split(":")[1].strip()))
y = y0 + 8
for n, k in enumerate(rows):
    if n and n % 5 == 0: y += 10
    t = T[k]; fam = len(k) == 2
    lab = ("%s as made" % k) if fam else ("%s dealt: %s" % (k, "every column it reads" if len(M[k]["cols"]) > 2 else ", ".join(M[k]["cols"])))
    s.append('<text x="40" y="%d" fill="%s" font-size="12">%s</text>' % (y + 13, "#1d1b17" if fam else "#68625a", lab))
    if k in K: s.append('<text x="22" y="%d" fill="#a8432b" font-size="12">&#9654;</text>' % (y + 13))
    for i, (_, _, f) in enumerate(seats):
        on = f(t); cx = x0 + cw * i + cw / 2 - 8
        col = "#a8432b" if on else "#2f6a46"
        s.append('<rect x="%d" y="%d" width="16" height="16" fill="%s" stroke="%s" stroke-width="1.5"/>' % (cx, y + 1, col if on else "none", col))
    y += rh
s.append('<text x="20" y="%d" fill="#68625a" font-size="12">W refused 9 of the 11 pages in K: by the state\'s shape (5), a named fact (2), the other versions in the packet (2).</text>' % (y + 22))
s.append('<text x="20" y="%d" fill="#68625a" font-size="12">It passed the two whose dealt column (traffic, length) neither memory nor siblings could show; WT, computing from the table, refused them.</text>' % (y + 40))
s.append('</svg>')
open(os.path.join(H, "figure.svg"), "w").write("\n".join(s))
