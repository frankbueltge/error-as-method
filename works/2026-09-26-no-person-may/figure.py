#!/usr/bin/env python3
"""figure.py -- figure.svg from results.json only.

Left: the five traditions by subjecthood (x) and R3b (y).  The four earlier points rise together;
the box at the fifth's subjecthood is the R3b interval S94.SPREAD required of it, and the fifth
point sits thirty points under the box.
Right: the agent test in five traditions, against S86.CONSTANT's band and S90.FLOOR's 0.80 line.
"""
import json
from pathlib import Path

H = Path(__file__).resolve().parent
res = json.load(open(H / "results.json"))
pts = {k: tuple(v) for k, v in res["prior_points"].items()}
cfr = (res["S94_SPREAD"]["subjecthood"], res["S94_SPREAD"]["R3b"])
lo_r, hi_r = res["S94_SPREAD"]["R3b_interval"]
agent = {"RFCs": 0.9022, "WHATWG": 0.9010, "EU acts": 0.8095, "UK Acts": 0.7763,
         "14 CFR": res["classify"]["whole"]["agent_test"]}

INK, MUTE, FAINT, MARK, PAPER = "#1d1d1b", "#6b6b66", "#d9d6cf", "#a3341f", "#faf8f3"
W, HT = 900, 440
o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" font-family="Georgia, serif" '
     'role="img" aria-label="Left: four traditions whose R3b rises with subjecthood, and a fifth, '
     '14 CFR, whose subjecthood falls between WHATWG and EU but whose R3b is the lowest of all. '
     'Right: the agent test in five traditions, 14 CFR at 0.7849, inside the band and below 0.80.">'
     % (W, HT), '<rect width="%d" height="%d" fill="%s"/>' % (W, HT, PAPER)]


def t(x, y, s, size=12, fill=INK, anchor="start", style=""):
    o.append('<text x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="%s"%s>%s</text>'
             % (x, y, size, fill, anchor, (' font-style="%s"' % style) if style else "", s))


# ---------------------------------------------------------------- left panel
X0, X1, Y0, Y1 = 70, 470, 370, 70                 # plot box
sx = lambda v: X0 + (v - 10) / (32 - 10) * (X1 - X0)
sy = lambda v: Y0 - (v - 20) / (72 - 20) * (Y0 - Y1)
t(X0, 36, "S94.SPREAD: the order that held for four", 15)
for v in (10, 15, 20, 25, 30):
    o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s"/>' % (sx(v), Y0, sx(v), Y1, FAINT))
    t(sx(v), Y0 + 16, "%d" % v, 10, MUTE, "middle")
for v in (20, 30, 40, 50, 60, 70):
    o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s"/>' % (X0, sy(v), X1, sy(v), FAINT))
    t(X0 - 6, sy(v) + 4, "%d" % v, 10, MUTE, "end")
t((X0 + X1) / 2, Y0 + 34, "subjecthood, % of party-term occurrences followed by a verb", 11, MUTE, "middle")
o.append('<text x="22" y="%d" font-size="11" fill="%s" text-anchor="middle" '
         'transform="rotate(-90 22 %d)">R3b fire rate, %% of rows in reach</text>'
         % ((Y0 + Y1) // 2, MUTE, (Y0 + Y1) // 2))
# the required interval at the fifth's subjecthood
o.append('<rect x="%.1f" y="%.1f" width="14" height="%.1f" fill="none" stroke="%s" '
         'stroke-dasharray="3 3"/>' % (sx(cfr[0]) - 7, sy(hi_r), sy(lo_r) - sy(hi_r), MARK))
t(sx(cfr[0]) + 12, sy(hi_r) + 12, "required: %.2f to %.2f" % (lo_r, hi_r), 10, MARK)
order = sorted(pts.items(), key=lambda kv: kv[1][0])
o.append('<polyline fill="none" stroke="%s" stroke-width="1.2" points="%s"/>'
         % (MUTE, " ".join("%.1f,%.1f" % (sx(v[0]), sy(v[1])) for _, v in order)))
for name, (s, r) in pts.items():
    o.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="%s"/>' % (sx(s), sy(r), INK))
    dy = -9 if name != "UK Acts" else 16
    t(sx(s) + (6 if name != "WHATWG standards" else -6), sy(r) + dy, name, 11, INK,
      "start" if name != "WHATWG standards" else "end")
o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>'
         % (sx(cfr[0]), sy(lo_r), sx(cfr[0]), sy(cfr[1]) - 6, MARK))
o.append('<circle cx="%.1f" cy="%.1f" r="5.5" fill="none" stroke="%s" stroke-width="2"/>'
         % (sx(cfr[0]), sy(cfr[1]), MARK))
t(sx(cfr[0]) + 10, sy(cfr[1]) + 4, "14 CFR  %.2f, %.2f" % cfr, 11, MARK)

# ---------------------------------------------------------------- right panel
A0, A1 = 560, 860
ay = lambda v: Y0 - (v - 0.70) / (0.95 - 0.70) * (Y0 - Y1)
t(A0, 36, "S90.FLOOR: the agent test, five readings", 15)
o.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="%s" opacity="0.55"/>'
         % (A0, ay(0.95), A1 - A0, ay(0.75) - ay(0.95), FAINT))
t(A0 + 4, ay(0.95) + 14, "S86.CONSTANT band 0.75-0.95", 10, MUTE)
o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-dasharray="5 3"/>'
         % (A0, ay(0.80), A1, ay(0.80), MARK))
t(A1, ay(0.80) - 5, "0.80", 10, MARK, "end")
for v in (0.70, 0.75, 0.80, 0.85, 0.90, 0.95):
    t(A0 - 6, ay(v) + 4, "%.2f" % v, 10, MUTE, "end")
step = (A1 - A0) / len(agent)
for i, (name, v) in enumerate(sorted(agent.items(), key=lambda kv: -kv[1])):
    x = A0 + step * (i + 0.5)
    col = MARK if name == "14 CFR" else INK
    o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"/>'
             % (x, Y0, x, ay(v), col, 2 if name == "14 CFR" else 1))
    o.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="%s"/>' % (x, ay(v), col))
    t(x, ay(v) - 9, "%.4f" % v, 10, col, "middle")
    t(x, Y0 + 16, name, 10, col, "middle")
t(A0, Y0 + 50, "Falsified only if three new readings all reach 0.80. The first is 0.7849.", 11, MUTE,
  style="italic")
t(X0, Y0 + 50, "Five points; the fifth breaks the order. No coefficient is drawn.", 11, MUTE,
  style="italic")
o.append("</svg>")
(H / "figure.svg").write_text("\n".join(o) + "\n")
print("wrote figure.svg")
