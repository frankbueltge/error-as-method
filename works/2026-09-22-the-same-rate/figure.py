#!/usr/bin/env python3
"""figure.py -- figure.svg, complete without a line of script.

Left panel: eighty cells, forty per corpus, each one a row a reader read.  Each cell says what
happened when the rule met the reader on that row -- the rule said yes and the reader agreed, the
rule said yes and the reader did not, the rule said no and the reader had named a bearer anyway, or
both said no.  The two fire counts are almost the same height; what differs is what they are made
of, which is the whole night in one picture.

Right panel: what forty rows could have separated.  The UK arm is held at its published 13 right of
19 fires and the RFC arm is swept over every possible outcome on its 18; the curve is Fisher's
exact two-sided p, the dashed line is 0.05, and the shaded region is the only part of the axis
where a difference would have been called.  The observed point sits far outside it.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

INK = "#1b1b1b"
MUTED = "#6f6f6f"
PAPER = "#faf8f4"
BAND = "#d8d2c4"
HIT = "#a33"
AGREE = "#3c5a54"

W, H = 1180, 640
R3 = "R3_active_governor"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def cell_class(rule, reader):
    if rule and reader:
        return "tp"
    if rule and not reader:
        return "fp"
    if not rule and reader:
        return "fn"
    return "tn"


STYLE = {
    "tp": (AGREE, 1.0, "the rule fired and the reader agreed"),
    "fp": (HIT, 1.0, "the rule fired and the reader did not"),
    "fn": (HIT, 0.30, "the rule was silent where the reader named that term"),
    "tn": (BAND, 0.65, "both said no"),
}


def main():
    res = json.load(open(HERE / "results.json"))
    ins = json.load(open(HERE / "inspection.json"))
    uk = res["calibration"]["by_rule"][R3]
    rfc = res["against_the_reader"]["M1"][R3]
    sweep = ins["does_it_survive_n_40"]["what_forty_rows_could_have_separated"]

    uk_cells = [cell_class(r["R3"], r["reader"]) for r in res["calibration"]["rows"]]
    rfc_cells = [cell_class(r["rules"][R3], r["m1"]) for r in res["rows"]]

    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
         'font-family="Georgia, \'Times New Roman\', serif" fill="%s">' % (W, H, W, H, INK)]
    o.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPER))
    o.append('<text x="60" y="38" font-size="21">The same rate, and not the same decisions</text>')
    o.append('<text x="60" y="60" font-size="13" fill="%s">R3 -- does the party term nearest the '
             'obligation act in its block? -- against one reader, forty rows each. UK statute: '
             'Session 90\'s verdicts, Session 91\'s scoring, reproduced here. RFCs: read blind '
             'tonight. Session 95, 2026-09-22.</text>' % MUTED)

    # ---------------------------------------------------------------- left panel: eighty cells
    x0, y0 = 60, 108
    cw, gap, cols = 30, 6, 8
    for col, (name, cells, stats) in enumerate((
            ("UK statute — where the rule was written", uk_cells, uk),
            ("the RFC series — where it was not", rfc_cells, rfc))):
        bx = x0 + col * 300
        o.append('<text x="%d" y="%d" font-size="13">%s</text>' % (bx, y0, esc(name)))
        for i, c in enumerate(cells):
            fill, op, _ = STYLE[c]
            cx = bx + (i % cols) * (cw + gap) * 0.9
            cy = y0 + 18 + (i // cols) * (cw + gap)
            o.append('<rect x="%.1f" y="%.1f" width="%d" height="%d" fill="%s" '
                     'fill-opacity="%.2f"/>' % (cx, cy, cw, cw, fill, op))
        base = y0 + 18 + 5 * (cw + gap) + 26
        o.append('<text x="%d" y="%d" font-size="13">the rule fired on <tspan font-size="17">%d'
                 '</tspan> of 40</text>' % (bx, base, stats["fires"]))
        o.append('<text x="%d" y="%d" font-size="12" fill="%s">of those, right on %d — '
                 'precision %.4f</text>' % (bx, base + 20, MUTED, stats["tp"],
                                            stats["precision_on_yes"]))
        o.append('<text x="%d" y="%d" font-size="12" fill="%s">the reader found a bearer in reach '
                 'on %d</text>' % (bx, base + 38, MUTED, stats["tp"] + stats["fn"]))
        o.append('<text x="%d" y="%d" font-size="12" fill="%s">agreement %.2f · Cohen\'s κ %+.4f'
                 '</text>' % (bx, base + 56, MUTED, stats["agreement"], stats["cohens_kappa"]))
        if col == 1:
            o.append('<text x="%d" y="%d" font-size="12" fill="%s">in %d of the 40 the paragraph '
                     'named no bearer at all</text>'
                     % (bx, base + 74, HIT, res["reading"]["bearer_none"]))

    ly = y0 + 18 + 5 * (cw + gap) + 100
    for i, key in enumerate(("tp", "fp", "fn", "tn")):
        fill, op, label = STYLE[key]
        o.append('<rect x="%d" y="%d" width="13" height="13" fill="%s" fill-opacity="%.2f"/>'
                 % (60, ly + i * 20 - 10, fill, op))
        o.append('<text x="%d" y="%d" font-size="11.5" fill="%s">%s</text>'
                 % (80, ly + i * 20, MUTED, esc(label)))

    # ---------------------------------------------------------------- right panel: the sweep
    RX, RY, RW, RH = 700, 128, 420, 300
    o.append('<text x="%d" y="%d" font-size="13">What forty rows could have separated</text>'
             % (RX, y0))
    o.append('<text x="%d" y="%d" font-size="11.5" fill="%s">Fisher\'s exact, two-sided, UK held '
             'at 13 right of 19.</text>' % (RX, y0 + 18, MUTED))

    pts = sweep["sweep"]
    xlo, xhi = 0.0, 1.0
    px = lambda v: RX + RW * (v - xlo) / (xhi - xlo)
    py = lambda p: RY + RH - RH * min(p, 1.0)

    thresh = sweep["highest_rfc_precision_that_would_have_been_significant"]
    if thresh is not None:
        o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" fill="%s" fill-opacity="0.55"/>'
                 % (px(0.0), RY, px(thresh) - px(0.0), RH, BAND))
        o.append('<text x="%.1f" y="%.1f" font-size="11" fill="%s">only here</text>'
                 % (px(0.0) + 6, RY + 16, MUTED))

    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1" '
             'stroke-dasharray="5 4"/>' % (px(xlo), py(0.05), px(xhi), py(0.05), HIT))
    o.append('<text x="%.1f" y="%.1f" font-size="11" fill="%s" text-anchor="end">p = 0.05</text>'
             % (px(xhi), py(0.05) - 6, HIT))

    d = " ".join("%s%.1f %.1f" % ("M" if i == 0 else "L", px(p["rfc_precision"]),
                                  py(p["p_two_sided"])) for i, p in enumerate(pts))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.6"/>' % (d, AGREE))

    ox, oy = px(rfc["precision_on_yes"]), py(sweep["p_observed"])
    o.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s"/>' % (ox, oy, HIT))
    o.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="%s">observed: %.4f, p = %s</text>'
             % (ox + 10, oy - 8, INK, rfc["precision_on_yes"], sweep["p_observed"]))
    ux = px(uk["precision_on_yes"])
    o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="0.8" '
             'stroke-dasharray="2 3"/>' % (ux, RY, ux, RY + RH, MUTED))
    o.append('<text x="%.1f" y="%d" font-size="11" fill="%s" text-anchor="middle">UK %.4f</text>'
             % (ux, RY - 6, MUTED, uk["precision_on_yes"]))

    o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s"/>'
             % (px(xlo), RY + RH, px(xhi), RY + RH, INK))
    o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s"/>'
             % (px(xlo), RY, px(xlo), RY + RH, INK))
    for v in (0.0, 0.25, 0.5, 0.75, 1.0):
        o.append('<text x="%.1f" y="%d" font-size="11" fill="%s" text-anchor="middle">%.2f</text>'
                 % (px(v), RY + RH + 16, MUTED, v))
    o.append('<text x="%.1f" y="%d" font-size="11.5" fill="%s" text-anchor="middle">the rule\'s '
             'precision in the RFC series, swept</text>' % (RX + RW / 2, RY + RH + 36, MUTED))
    for v in (0.0, 0.5, 1.0):
        o.append('<text x="%.1f" y="%.1f" font-size="11" fill="%s" text-anchor="end">%.1f</text>'
                 % (px(xlo) - 8, py(v) + 4, MUTED, v))

    o.append('<text x="%d" y="%d" font-size="13">The observed gap is %.2f points. The smallest gap '
             'these forty rows could have seen is %s.</text>'
             % (RX, RY + RH + 76,
                100 * (uk["precision_on_yes"] - rfc["precision_on_yes"]),
                sweep["gap_in_points_needed"]))
    o.append('<text x="%d" y="%d" font-size="12" fill="%s">Across four traditions the fire rate '
             'itself spans 39.44 points (Session 94). The check is coarser than the thing it was '
             'brought in to check.</text>' % (RX, RY + RH + 98, MUTED))

    o.append('<text x="60" y="%d" font-size="11" fill="%s">Every number recomputable from this '
             'directory: draw.py, verdicts.json, adjudicate.py, inspect.py. No network.</text>'
             % (H - 18, MUTED))
    o.append("</svg>")
    (HERE / "figure.svg").write_text("\n".join(o) + "\n")
    print("wrote figure.svg -- %d cells left, %d sweep points right"
          % (len(uk_cells) + len(rfc_cells), len(pts)))


if __name__ == "__main__":
    main()
