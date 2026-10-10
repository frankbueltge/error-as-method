"""figure.py -- figure.svg from results.json, carry.json and carry_i.json: for each maker, grouped by the
preparation it was given, the blind coder's closeness to the plot (0-3) as stacked squares, its class,
its guess of the preparation, and what the page carries of the 838 values (exact matches)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda f: json.load(open(os.path.join(HERE, f)))
res, carry, ci = J("results.json"), J("carry.json"), J("carry_i.json")
rows = res["rows"]
ARMS = [("T", "given a table", "#2f5d8a"), ("P", "given sentences", "#8a3b2f"), ("I", "given the plot itself", "#4c6b2f")]
W, H = 960, 490
o = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Georgia, serif">' % (W, H, W, H),
     '<rect width="%d" height="%d" fill="#fbf8f2"/>' % (W, H),
     '<text x="30" y="40" font-size="22" fill="#1d1b18">Prepared Clay: one material, three preparations, twelve makers</text>',
     '<text x="30" y="64" font-size="13.5" fill="#6b655c">Squares: a blind coder’s closeness of each work to the plain scatter plot (0–3). Only the makers given the plot did not make it.</text>']
gx = 30
for A, label, col in ARMS:
    ms = sorted(m for m in rows if rows[m]["arm"] == A)
    o.append('<text x="%d" y="104" font-size="15" fill="%s">%s · %s</text>' % (gx, col, A, label))
    mean = sum(rows[m]["close"] for m in ms) / 4
    o.append('<text x="%d" y="122" font-size="12" fill="#6b655c">mean closeness %.2f</text>' % (gx, mean))
    for i, m in enumerate(ms):
        x = gx + i * 72; r = rows[m]
        for k in range(3):
            filled = k < r["close"]
            o.append('<rect x="%d" y="%d" width="40" height="40" fill="%s" stroke="%s" stroke-width="1"/>' % (x, 280 - k * 46, col if filled else "none", col if filled else "#d8d1c6"))
        o.append('<text x="%d" y="342" font-size="13" text-anchor="middle" fill="#1d1b18">%s</text>' % (x + 20, m))
        o.append('<text x="%d" y="362" font-size="11.5" text-anchor="middle" fill="#6b655c">%s</text>' % (x + 20, "XY" if r["class"] == "XY" else "other"))
        hit = r["guess"] == A
        o.append('<text x="%d" y="382" font-size="11.5" text-anchor="middle" fill="%s">guess %s%s</text>' % (x + 20, "#2e6b3a" if hit else "#9a2b2b", r["guess"], " ✓" if hit else ""))
        ex = ci[m]["exact"] if A == "I" else carry[m]["exact"]
        o.append('<text x="%d" y="402" font-size="11.5" text-anchor="middle" fill="#6b655c">%d exact</text>' % (x + 20, ex))
    gx += 310
o.append('<text x="30" y="436" font-size="12" fill="#6b655c">m04’s page throws a script error in a browser and shows nothing (coded 0). “exact”: of the 838 source values, how many the page carries exactly; for the plot arm, read back from the pixels.</text>')
o.append('<text x="30" y="454" font-size="12" fill="#6b655c">The coder’s three right guesses in the plot arm came from captions saying the values were “read back from a plot”, not from the forms. Data: Aono &amp; Katata via Our World in Data, CC BY 4.0.</text>')
o.append("</svg>")
open(os.path.join(HERE, "figure.svg"), "w", encoding="utf-8").write("\n".join(o))
print("ok")
