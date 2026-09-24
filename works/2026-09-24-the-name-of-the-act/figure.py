#!/usr/bin/env python3
"""figure.py -- figure.svg from the committed JSON only.

Left: the twenty occurrences read, one row each -- the verdict as a filled or open mark, the
carrier's word distance from the modal as a bar, the comitology formula as a tick.
Right: the chance twenty rows falsify the row for each true party share (power.json), with the
coin band shaded and the observed count's interval drawn under it.
"""
import json
from pathlib import Path

H = Path(__file__).resolve().parent
power = json.load(open(H / "power.json"))
ver = {v["n"]: v["verdict"] for v in json.load(open(H / "verdicts.json"))["verdicts"]}
ins = json.load(open(H / "inspection.json"))
res = json.load(open(H / "results.json"))
dist = {int(k): v[0] for k, v in ins["sheet_word_distance"].items()}
formula = set(ins["formula"]["sheet_formula_rows"])
inside = set(ins["sheet_rows_whose_carrier_is_inside_the_obligation_sentence"])

INK, MUTE, FAINT, MARK = "#1d1d1b", "#6b6b66", "#d9d6cf", "#a3341f"
W, HT = 900, 460
o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" font-family="Georgia, serif" '
     'role="img" aria-label="Twenty occurrences of Commission, nineteen of them a party; beside it '
     'the chance twenty rows could falsify the row at each true share.">' % (W, HT),
     '<rect width="%d" height="%d" fill="#faf8f3"/>' % (W, HT)]
t = lambda x, y, s, size=12, fill=INK, anchor="start", style="": o.append(
    '<text x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="%s"%s>%s</text>'
    % (x, y, size, fill, anchor, (' font-style="%s"' % style) if style else "", s))

# ---- left panel
x0, y0, rh = 40, 70, 17
t(x0, 32, "Twenty occurrences of “Commission”, as read", 15)
t(x0, 50, "filled: a party · open: not · bar: words from the modal · F: the implementing-act formula", 11, MUTE)
scale = 1.2
for n in range(1, 21):
    y = y0 + (n - 1) * rh
    t(x0, y + 4, "%2d" % n, 10, MUTE)
    cx = x0 + 30
    if ver[n] == "YES":
        o.append('<circle cx="%d" cy="%d" r="5" fill="%s"/>' % (cx, y, INK))
    else:
        o.append('<circle cx="%d" cy="%d" r="5" fill="none" stroke="%s" stroke-width="1.6"/>' % (cx, y, MARK))
    bx = x0 + 48
    o.append('<rect x="%d" y="%d" width="%.1f" height="7" fill="%s"/>'
             % (bx, y - 4, max(1.5, dist[n] * scale), MUTE if n not in inside else INK))
    lab = "%d" % dist[n] + ("  in the sentence" if n in inside else "")
    t(bx + max(1.5, dist[n] * scale) + 5, y + 3, lab, 9, MUTE)
    if n in formula:
        t(x0 + 395, y + 4, "F", 10, MARK)
o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-dasharray="3 3"/>'
         % (x0 + 48 + 60 * scale, y0 - 10, x0 + 48 + 60 * scale, y0 + 19 * rh + 6, FAINT))
t(x0 + 48 + 60 * scale, y0 + 19 * rh + 20, "60 words: the edge of what the reader was shown", 9, MUTE, "middle")

# ---- right panel
px, py, pw, ph = 500, 90, 360, 260
t(px, 32, "What twenty rows could decide", 15)
t(px, 50, "chance the row is falsified (more than 10 of 20), by true share", 11, MUTE)
cb = power["coin_band_20_to_80_percent"]
X = lambda p: px + p * pw
Y = lambda v: py + ph - v * ph
o.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" fill="%s" opacity="0.6"/>'
         % (X(cb[0]), py, X(cb[1]) - X(cb[0]), ph, FAINT))
t((X(cb[0]) + X(cb[1])) / 2, py + 14, "coin band", 10, MUTE, "middle", "italic")
o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (px, py + ph, px + pw, py + ph, INK))
o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (px, py, px, py + ph, INK))
for p in (0, 0.25, 0.5, 0.75, 1):
    t(X(p), py + ph + 16, "%.2f" % p, 10, MUTE, "middle")
for v in (0, 0.5, 1):
    t(px - 6, Y(v) + 4, "%.1f" % v, 10, MUTE, "end")
pts = [(0.0, 0.0)] + [(float(k), v) for k, v in power["p_falsified_by_true_share"].items()] + [(1.0, 1.0)]
o.append('<polyline fill="none" stroke="%s" stroke-width="2" points="%s"/>'
         % (INK, " ".join("%.1f,%.1f" % (X(p), Y(v)) for p, v in pts)))
lo, hi = res["clopper_pearson_95"]
yy = py + ph + 36
o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="3"/>' % (X(lo), yy, X(hi), yy, MARK))
o.append('<circle cx="%.1f" cy="%d" r="4.5" fill="%s"/>' % (X(res["k_strict"] / 20), yy, MARK))
t(X(lo) - 6, yy + 4, "observed 19 of 20, 95 %% interval %.3f–%.3f" % (lo, hi), 10, MARK, "end")
t(px, yy + 34, "Only 0–5 or 15–20 of twenty exclude one half.", 11, INK)
t(px, yy + 50, "Computed before the frame existed (power.py).", 11, MUTE, style="italic")
o.append("</svg>")
(H / "figure.svg").write_text("\n".join(o) + "\n")
print("figure.svg written")
