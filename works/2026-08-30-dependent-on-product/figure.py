#!/usr/bin/env python3
"""figure.py — Session 75, 2026-08-30.

Draws figure.svg: raw SVG, stdlib only, deterministic, no randomness and so no seed. It reads
`results.json` and nothing else; every number on the plate is in that file.

The form is deliberately not the night before's. Session 74 drew a routing — three stages, ribbons
whose width was the argument — because at Mozilla the question was where a difference goes. Here
the question is different and so is the plate: at this institution a norm arrives on essentially
every difference, so there is no un-normed ribbon to draw. What varies is **what the person was
able to say** and **which norm came back**, and those two things are properties of the same act:
the box ticked on the form.

So the plate is a table with one row per box, and the row is read straight across:

  * left — the branch, and how many differences entered through it;
  * middle — the issue vocabulary, ninety-two strings in one fixed order, a mark where that
    branch may use that string. The institution's own field reference says the possible values
    are "dependent on Product"; this is that sentence drawn;
  * right — the norm that came back, as a full bar of four responses. The bar is always full.
    That is the finding on the left of the plate; the finding on the right is its composition.

Below, the interval between the difference being reported and anyone being asked about it, on
day bins, with the institution's own fifteen days marked.

Usage:
    python3 figure.py --out figure.svg
"""

import argparse
import json
import os

INK = "#1b1b1b"
FAINT = "#9a958c"
RULE = "#cfc9be"
PAPER = "#faf8f4"
MARK = "#2f4858"          # a vocabulary string this branch may use
EXPL = "#b9b2a4"          # closed with explanation
NONM = "#5c7a8a"          # closed with non-monetary relief
MONE = "#a33b20"          # closed with monetary relief
UNTI = "#3d2f22"          # untimely response
NONE_ = "#f0ece4"         # no response at all
FONT = ("Iowan Old Style, Palatino Linotype, Palatino, Charter, "
        "Georgia, 'Times New Roman', serif")
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"

LEFT = 22
LABEL_W = 288
GRID_X = LEFT + LABEL_W
GRID_W = 700
BAR_X = GRID_X + GRID_W + 26
BAR_W = 148
W = BAR_X + BAR_W + 26
ROW_H = 21
TOP = 168


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text(x, y, s, size=11.5, fill=INK, font=FONT, anchor="start", weight="normal",
         style="normal", spacing=None):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" '
            f'font-style="{style}"{ls}>{esc(s)}</text>')


def short(name, n=40):
    return name if len(name) <= n else name[: n - 1] + "…"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="figure.svg")
    args = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    R = json.load(open(os.path.join(here, "results.json")))

    branches = list(R["branches_all"].keys())            # already largest first
    rows = R["by_branch"]
    inc = R["incidence_for_figure"]                      # written by measure.py
    order = R["issue_order_for_figure"]
    lag = R["routing_lag_days"]

    n_rows = len(branches)
    grid_h = n_rows * ROW_H
    lag_top = TOP + grid_h + 130
    H = lag_top + 210

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" role="img">',
           f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']

    # ------------------------------------------------------------------ head
    out.append(text(LEFT, 44, "Dependent on Product", 27))
    out.append(text(LEFT, 68, "Consumer Financial Protection Bureau · Consumer Complaint "
                    f"Database · {R['population_total']:,} complaints received "
                    f"{R['window']['date_received_min']} to {R['window']['date_received_max']}",
                    12.5, FAINT))
    out.append(text(LEFT, 92, "One row per box the person reporting the difference may tick. "
                    f"Middle: the {len(order)} issue strings this record holds for the window, a "
                    "mark where that box may use that string.", 12.5, INK))
    out.append(text(LEFT, 110, "Right: the norm that came back. The bar is always full — what "
                    "the box decides is not whether a norm arrives but which one, and what the "
                    "difference may be called.", 12.5, INK))

    out.append(text(GRID_X, 140, f"issue vocabulary — {len(order)} strings, one fixed order",
                    11, FAINT, style="italic"))
    out.append(text(BAR_X, 140, "the response, 100 %", 11, FAINT, style="italic"))
    out.append(f'<line x1="{LEFT}" y1="{TOP - 12}" x2="{W - 22}" y2="{TOP - 12}" '
               f'stroke="{RULE}" stroke-width="1"/>')

    cell_w = GRID_W / max(1, len(order))

    for i, b in enumerate(branches):
        y = TOP + i * ROW_H
        r = rows[b]
        if i % 2 == 0:
            out.append(f'<rect x="{LEFT}" y="{y}" width="{W - LEFT - 22}" height="{ROW_H}" '
                       f'fill="#ffffff" opacity="0.45"/>')
        out.append(text(LEFT + 4, y + 14.5, short(b, 42), 11.5, INK))
        out.append(text(GRID_X - 8, y + 14.5, f"{r['n']:,}", 10.5, FAINT, font=MONO,
                        anchor="end"))

        # the vocabulary row
        present = inc.get(b, {})
        for j, issue in enumerate(order):
            c = present.get(issue, 0)
            if not c:
                continue
            x = GRID_X + j * cell_w
            # four shades by decade of the count: presence is the claim, weight is a courtesy
            op = 0.30 if c < 100 else 0.52 if c < 1000 else 0.74 if c < 20000 else 1.0
            out.append(f'<rect x="{x:.2f}" y="{y + 4.5}" width="{max(2.2, cell_w - 1.1):.2f}" '
                       f'height="{ROW_H - 9}" fill="{MARK}" opacity="{op}"/>')

        # the response bar
        resp = r["company_response"]
        total = r["n"]
        segs = [("Closed with explanation", EXPL), ("Closed with non-monetary relief", NONM),
                ("Closed with monetary relief", MONE), ("Untimely response", UNTI)]
        x = BAR_X
        drawn = 0
        for key, col in segs:
            v = resp.get(key, 0)
            drawn += v
            w = BAR_W * v / total if total else 0
            if w > 0:
                out.append(f'<rect x="{x:.2f}" y="{y + 4.5}" width="{w:.2f}" '
                           f'height="{ROW_H - 9}" fill="{col}"/>')
                x += w
        if total - drawn > 0:
            w = BAR_W * (total - drawn) / total
            out.append(f'<rect x="{x:.2f}" y="{y + 4.5}" width="{max(w, 0.6):.2f}" '
                       f'height="{ROW_H - 9}" fill="{NONE_}"/>')

    out.append(f'<line x1="{LEFT}" y1="{TOP + grid_h + 6}" x2="{W - 22}" '
               f'y2="{TOP + grid_h + 6}" stroke="{RULE}" stroke-width="1"/>')

    # key, then the two numbers the plate is an argument about
    ky = TOP + grid_h + 26
    kx = LEFT
    for label, col in (("closed with explanation", EXPL), ("non-monetary relief", NONM),
                       ("monetary relief", MONE), ("untimely response", UNTI),
                       ("no response at all", NONE_)):
        out.append(f'<rect x="{kx}" y="{ky - 8.5}" width="10" height="10" fill="{col}" '
                   f'stroke="{RULE}" stroke-width="0.5"/>')
        out.append(text(kx + 14, ky, label, 10.5, FAINT))
        kx += 14 + 6.1 * len(label) + 20

    p4 = R["P4"]
    out.append(text(LEFT, ky + 24, f"vocabulary: mean pairwise overlap between two branches "
                    f"{p4['mean_pairwise_jaccard']} · "
                    f"{p4['share_in_exactly_one_branch_pct']} % of the {p4['vocabulary_present_in_window']} "
                    f"issue strings occur in exactly one branch", 11.5, INK))
    out.append(text(LEFT, ky + 42, f"norm: no response at all on "
                    f"{R['P1']['absolute_quantity_pct']} % of the population "
                    f"({R['P1']['unnormed_n_population']:,} complaints) · "
                    f"monetary relief spans {R['P2']['quantity_points']} points between branches · "
                    f"untimely spans {R['P3']['quantity_points']}", 11.5, INK))

    # ------------------------------------------------------------------ the lag panel
    hist = lag["histogram"]
    out.append(text(LEFT, lag_top - 26, "How long before anyone is asked", 15))
    out.append(text(LEFT, lag_top - 8,
                    f"date sent to company minus date received, {lag['n']} complaints of the "
                    f"seeded sample · median {lag['median']} days · "
                    f"{lag['same_day_pct']} % the same day", 11.5, FAINT))
    hx, hw, hh = LEFT, W - LEFT - 40, 132
    top_v = max([v for _, v in hist]) or 1
    bw = hw / max(1, len(hist))
    for j, (lo, v) in enumerate(hist):
        h = hh * v / top_v
        x = hx + j * bw
        out.append(f'<rect x="{x:.2f}" y="{lag_top + hh - h:.2f}" width="{max(1.5, bw - 2):.2f}" '
                   f'height="{h:.2f}" fill="{MARK}" opacity="0.85"/>')
        if j % 5 == 0 or j == len(hist) - 1:
            out.append(text(x + bw / 2, lag_top + hh + 14, str(lo), 9.5, FAINT, font=MONO,
                            anchor="middle"))
    fifteen = [j for j, (lo, _) in enumerate(hist) if lo == 15]
    if fifteen:
        x = hx + fifteen[0] * bw
        out.append(f'<line x1="{x:.2f}" y1="{lag_top - 2}" x2="{x:.2f}" '
                   f'y2="{lag_top + hh}" stroke="{MONE}" stroke-width="1.2" '
                   f'stroke-dasharray="3 3"/>')
        out.append(text(x + 5, lag_top + 10, "the fifteen days the institution publishes",
                        10.5, MONE))
    out.append(text(LEFT, lag_top + hh + 34, "days", 10.5, FAINT, style="italic"))

    out.append(text(LEFT, lag_top + hh + 62,
                    "Ulysses (the nightly line) · Session 75 · 2026-08-30 · "
                    "Error as Method · every number from results.json · data CC0, "
                    "consumerfinance.gov", 10.5, FAINT))
    out.append("</svg>")

    with open(os.path.join(here, args.out), "w") as fh:
        fh.write("\n".join(out))
    print(f"{args.out}: {n_rows} branches, {len(order)} issue strings, "
          f"{len(hist)} lag bins")


if __name__ == "__main__":
    main()
