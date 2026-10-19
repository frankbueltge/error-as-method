"""figure.py -- figure.svg: the six makers by round. A filled square is a version made, marked with coder S's code for
the step into it; a dashed square is "finished", nothing changed. Right: share of pixels changed from v1 to the last."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
S = json.loads(open(os.path.join(HERE, "face-data.js")).read()[len("window.SENT = "):-2])
C = {"ADD": "#2f5d8a", "TRIM": "#7a8f5a", "REORGANISE": "#c0721f", None: "#555"}
W, H, x0, y0, c = 900, 405, 210, 70, 70
o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" font-family="Georgia,serif" font-size="13">' % (W, H),
     '<rect width="100%%" height="100%%" fill="#f4f1ea"/>',
     '<text x="20" y="30" font-size="18">Sent Back: six makers, sent back with one sentence</text>',
     '<text x="20" y="50" fill="#6b665c" font-size="12">K: "Make the next version of your work." D: the same, "or, if you judge the work finished, say so and change nothing." K got the D sentence at round 7.</text>']
for r in range(1, 8):
    o.append('<text x="%d" y="%d" text-anchor="middle" fill="#6b665c" font-size="11">round %d</text>' % (x0 + (r - 1) * c + 28, y0 + 6, r))
for i, m in enumerate(S):
    y = y0 + 20 + i * 46
    o.append('<text x="20" y="%d">%s</text><text x="20" y="%d" font-size="11" fill="%s">%s · %s</text>' % (
        y + 15, m["title"], y + 30, "#2f5d8a" if m["arm"] == "K" else "#a2412b", m["arm"], m["maker"]))
    for x in m["rounds"]:
        X = x0 + (x["r"] - 1) * c
        if x["made"]:
            o.append('<rect x="%d" y="%d" width="56" height="36" fill="%s"/>' % (X, y, C[x["code"]] if x["r"] > 1 else "#222"))
            o.append('<text x="%d" y="%d" text-anchor="middle" fill="#fff" font-size="10">%s</text>' % (X + 28, y + 22, ("v%d" % x["v"]) + ("" if not x["code"] else " " + x["code"][:3].lower())))
        else:
            o.append('<rect x="%d" y="%d" width="56" height="36" fill="none" stroke="#a2412b" stroke-dasharray="3 2"/>' % (X, y))
            o.append('<text x="%d" y="%d" text-anchor="middle" fill="#a2412b" font-size="10">finished</text>' % (X + 28, y + 22))
    p = m["pixel"]["first_to_last"]
    if p is not None:
        o.append('<rect x="%d" y="%d" width="%.1f" height="10" fill="#e0157a"/><text x="%d" y="%d" font-size="11" fill="#6b665c">%.1f %%</text>' % (
            x0 + 7 * c + 4, y + 13, p * 600, x0 + 7 * c + 8 + p * 600, y + 22, p * 100))
o.append('<text x="%d" y="%d" font-size="11" fill="#6b665c">pixels v1→last</text>' % (x0 + 7 * c + 4, y0 + 6))
o.append('<text x="20" y="%d" font-size="11" fill="#6b665c">Step codes by a blind coder: add (blue), trim (green), reorganise (orange). Source: results.json, face-data.js.</text>' % (H - 14))
o.append('</svg>')
open(os.path.join(HERE, "figure.svg"), "w").write("\n".join(o))
