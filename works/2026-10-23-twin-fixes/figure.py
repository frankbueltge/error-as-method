"""Experiment 36, Twin Fixes: the figure. Reads results.json, results2.json; writes figure.svg. Standard library only."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
r1 = json.load(open(os.path.join(HERE, "results.json"), encoding="utf8"))
r2 = json.load(open(os.path.join(HERE, "results2.json"), encoding="utf8"))
hand = {c: sum(1 for x in r1["pins"] if x["cond"] == c and (x["town_hit"] or x["answer"].startswith("Shearia"))) for c in "EDT"}
pts = [("own string", hand["E"]), ("rewritten", hand["D"]), ("twin 0.6 km", hand["T"]),
       ("2 km", r2["summary"]["S2"]["orig"]), ("8 km", r2["summary"]["S8"]["orig"]), ("30 km", r2["summary"]["S30"]["orig"])]
W, H, L, T, B = 640, 340, 60, 40, 270
xs = [L + i * 100 for i in range(len(pts))]
y = lambda v: B - (B - T) * v / 100
s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" font-family="Georgia, serif" font-size="12">' % (W, H),
     '<rect width="%d" height="%d" fill="#f4f1ea"/>' % (W, H)]
for v in (0, 25, 50, 75, 100):
    s.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="#cfc7b8" stroke-width="0.6"/>' % (L - 10, xs[-1] + 20, y(v), y(v)))
    s.append('<text x="%d" y="%.1f" text-anchor="end" fill="#6d665c">%d%%</text>' % (L - 14, y(v) + 4, v))
pp = " ".join("%d,%.1f" % (x, y(100 * v / 72)) for x, (_, v) in zip(xs, pts))
s.append('<polyline points="%s" fill="none" stroke="#1f5f8b" stroke-width="2"/>' % pp)
for x, (lab, v) in zip(xs, pts):
    s.append('<circle cx="%d" cy="%.1f" r="4" fill="#1f5f8b"/>' % (x, y(100 * v / 72)))
    s.append('<text x="%d" y="%.1f" text-anchor="middle" fill="#1d1b18">%d of 72</text>' % (x, y(100 * v / 72) - 10, v))
    s.append('<text x="%d" y="%d" text-anchor="middle" fill="#6d665c">%s</text>' % (x, B + 20, lab))
s.append('<polyline points="%d,%.1f %d,%.1f" fill="none" stroke="#7a2e3a" stroke-width="2" stroke-dasharray="5 3"/>' % (xs[0], y(27.8), xs[2], y(12.5)))
s.append('<text x="%d" y="%.1f" fill="#7a2e3a">colour names, exact hex to twin (experiment 35): 27.8%% to 12.5%%</text>' % (xs[0] + 6, y(27.8) + 22))
s.append('<text x="%d" y="22" fill="#1d1b18" font-size="14">Towns named from a pin, by how far the pin was moved from the gazetteer\'s point</text>' % (L - 10))
s.append('<text x="%d" y="%d" fill="#6d665c">Nine fresh makers per round, three answers per pin and step. Counted by hand (Shearia = Sh\'īarīah). Round 2: 2, 8, 30 km.</text>' % (L - 10, B + 50))
s.append("</svg>")
open(os.path.join(HERE, "figure.svg"), "w", encoding="utf8").write("\n".join(s))
print(pts)
