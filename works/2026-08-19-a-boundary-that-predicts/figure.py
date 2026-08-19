#!/usr/bin/env python3
"""Draw figure.svg from results.json + adjudication.json. One version axis; ten features,
one lane each. A filled square marks OptionalRelease (the recording field) — it never moves,
so it is one mark per lane. Open circles mark the successive values of MandatoryRelease (the
predicting field), joined by a drift arrow where it moved; a hollow diamond at the far right
marks a boundary withdrawn to None. Moves are coloured by what the adjudication says they were
for. stdlib only, deterministic; no browser, no external asset.

    python3 figure.py
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

res = json.load(open(os.path.join(HERE, "results.json")))
adj = json.load(open(os.path.join(HERE, "adjudication.json")))
verdict = {v["feature"]: v for v in adj["verdicts"]}

# The x axis: every measured release, plus 4.0 as a virtual right-hand tick (barry and the
# early annotations placeholder both point past the last shipped release).
AXIS = ["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7",
        "3.0", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7",
        "3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14", "4.0"]
XPOS = {v: i for i, v in enumerate(AXIS)}

CLASS_COLOUR = {
    "schedule": "#5b6b7a",
    "corrected-prediction": "#c05a2e",
    "joke": "#8a5cb0",
    "withdrawn-plan": "#b03a48",
}
INK = "#1a1a1a"
FAINT = "#c9c4bb"
PAPER = "#f4f1ea"

features = res["summary"]["features"]
n = len(features)

# layout
L, R, T, B = 210, 60, 96, 150
lane_h = 34
W = L + R + (len(AXIS) - 1) * 40
plot_w = W - L - R
H = T + n * lane_h + B


def x(ver):
    return L + XPOS[ver] * (plot_w / (len(AXIS) - 1))


def lane_y(i):
    return T + i * lane_h + lane_h / 2


out = []
out.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="Georgia, \'Times New Roman\', serif">')
out.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')

# title
out.append(f'<text x="{L}" y="40" font-size="21" fill="{INK}">'
           f'A boundary that predicts, and a boundary that records</text>')
out.append(f'<text x="{L}" y="64" font-size="13" fill="#555">'
           f'CPython <tspan font-style="italic">__future__</tspan>: the recording field never '
           f'moves in 22 releases; the predicting field moves in 3 of 10.</text>')

# vertical version gridlines + labels
for ver in AXIS:
    xv = x(ver)
    faint = ver == "4.0"
    dash = ' stroke-dasharray="2 3"' if faint else ''
    out.append(f'<line x1="{xv:.1f}" y1="{T-6}" x2="{xv:.1f}" y2="{T + n*lane_h}" '
               f'stroke="{FAINT}" stroke-width="1"{dash}/>')
    fill = "#999" if faint else "#444"
    out.append(f'<text x="{xv:.1f}" y="{T + n*lane_h + 20}" font-size="11" fill="{fill}" '
               f'text-anchor="middle">{ver}</text>')
# the 2->3 break marker between 2.7 and 3.0
xb = (x("2.7") + x("3.0")) / 2
out.append(f'<line x1="{xb:.1f}" y1="{T-6}" x2="{xb:.1f}" y2="{T + n*lane_h}" '
           f'stroke="#b03a48" stroke-width="1.2" stroke-dasharray="1 4"/>')
out.append(f'<text x="{xb:.1f}" y="{T-14}" font-size="10.5" fill="#b03a48" '
           f'text-anchor="middle">2 → 3 break</text>')
out.append(f'<text x="{x("4.0"):.1f}" y="{T-14}" font-size="10" fill="#999" '
           f'text-anchor="middle">(never)</text>')

for i, feat in enumerate(features):
    y = lane_y(i)
    pf = res["per_feature"][feat]
    v = verdict[feat]
    # lane baseline
    out.append(f'<line x1="{L}" y1="{y:.1f}" x2="{W-R}" y2="{y:.1f}" '
               f'stroke="{FAINT}" stroke-width="1"/>')
    # feature name
    out.append(f'<text x="{L-12}" y="{y+4:.1f}" font-size="12.5" fill="{INK}" '
               f'text-anchor="end">{feat}</text>')

    # optional debut — filled square, the fact that never moves
    ov = pf["optional_values"][0]
    if ov in XPOS:
        xo = x(ov)
        out.append(f'<rect x="{xo-4:.1f}" y="{y-4:.1f}" width="8" height="8" '
                   f'fill="{INK}"/>')

    # mandatory trajectory
    runs = [r for r in pf["mandatory_runs"]]
    colour = CLASS_COLOUR.get(v["class"], "#5b6b7a")
    pts = []
    for r in runs:
        val = r["value"]
        if val is None:
            pts.append(("none", x("4.0")))
        elif val in XPOS:
            pts.append((val, x(val)))
    # drift arrows between successive mandatory values
    for a in range(len(pts) - 1):
        (_, xa), (_, xb2) = pts[a], pts[a + 1]
        ya = y - 12
        out.append(f'<path d="M {xa:.1f} {ya:.1f} L {xb2:.1f} {ya:.1f}" '
                   f'stroke="{colour}" stroke-width="1.4" fill="none" '
                   f'marker-end="url(#arw)"/>')
    # markers
    for k, (val, xm) in enumerate(pts):
        last = k == len(pts) - 1
        if val == "none":
            # withdrawn: hollow diamond
            out.append(f'<path d="M {xm:.1f} {y-6:.1f} L {xm+6:.1f} {y:.1f} '
                       f'L {xm:.1f} {y+6:.1f} L {xm-6:.1f} {y:.1f} Z" '
                       f'fill="{PAPER}" stroke="{colour}" stroke-width="1.6"/>')
        else:
            r0 = 5.2 if last else 4
            fill = colour if last else PAPER
            out.append(f'<circle cx="{xm:.1f}" cy="{y:.1f}" r="{r0}" '
                       f'fill="{fill}" stroke="{colour}" stroke-width="1.6"/>')

# arrowhead def
out.insert(3, '<defs><marker id="arw" markerWidth="7" markerHeight="7" refX="6" refY="3" '
              'orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#555"/></marker></defs>')

# legend
ly = T + n * lane_h + 44
lx = L
out.append(f'<rect x="{lx-2:.1f}" y="{ly-9}" width="8" height="8" fill="{INK}"/>')
out.append(f'<text x="{lx+14}" y="{ly-1}" font-size="11.5" fill="#333">'
           f'OptionalRelease — records; never moved</text>')
out.append(f'<circle cx="{lx+2:.1f}" cy="{ly+20}" r="5" fill="{PAPER}" stroke="#5b6b7a" '
           f'stroke-width="1.6"/>')
out.append(f'<text x="{lx+14}" y="{ly+24}" font-size="11.5" fill="#333">'
           f'MandatoryRelease — predicts; open = superseded value, filled = current</text>')
# class swatches
cx0 = L + 430
labels = [("schedule / 2→3 break", "schedule"),
          ("corrected prediction", "corrected-prediction"),
          ("April-Fool joke", "joke"),
          ("withdrawn to None", "withdrawn-plan")]
for k, (lab, cls) in enumerate(labels):
    yy = ly - 9 + k * 15
    col = CLASS_COLOUR.get(cls, "#5b6b7a")
    out.append(f'<line x1="{cx0}" y1="{yy+4}" x2="{cx0+22}" y2="{yy+4}" stroke="{col}" '
               f'stroke-width="2.4"/>')
    out.append(f'<text x="{cx0+30}" y="{yy+8}" font-size="11" fill="#333">{lab}</text>')

out.append(f'<text x="{L}" y="{H-14}" font-size="10.5" fill="#777">'
           f'Source: CPython Lib/__future__.py at 22 released tags (2.1–3.14), PEP 236, '
           f'PEP 401, PEP 649. Zero of ten mandatory versions set by a breach.</text>')

out.append('</svg>')

with open(os.path.join(HERE, "figure.svg"), "w") as fh:
    fh.write("\n".join(out) + "\n")
print(f"figure.svg written ({W}x{H})")
