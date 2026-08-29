#!/usr/bin/env python3
"""figure.py — Session 74, 2026-08-29.

Draws figure.svg: raw SVG, stdlib only, deterministic, no randomness and so no seed. It reads
`results.json` and nothing else; every number on the plate is in that file.

The form is deliberately not the night before's. Session 73 drew survival curves over a queue,
because at the RFC Editor the un-normed differences were the ones still waiting. Here they are not
waiting — most of them are finished — so a curve would draw the wrong object. What this record has
instead is a **routing**, and the plate is a routing: 67,272 reported differences enter at the left
through one act, the filer's choice of a box, and leave at the right having been fixed, closed
otherwise, or not yet closed. In between sits the only thing the institution's policy calls
triage: whether a severity was ever put on the difference at all.

Read the plate left to right and the argument is the width of the ribbons:

  * the filer's box (stage 1) decides which of three streams a difference joins;
  * whether a norm is ever imposed (stage 2) follows that box and almost nothing else;
  * and what happens to the difference (stage 3) barely notices the norm — the widest ribbon
    into `fixed` comes from `no severity`.

Below, on doubling day-bins, how long each of the filer's three streams took to be closed, with
the one week Mozilla's own policy allows marked as a vertical rule. The stream on which the norm
is almost never imposed is the fast one. That inversion is the night.

Usage:
    python3 figure.py --out figure.svg
"""

import argparse
import json
import os

W, H = 1020, 900

INK = "#1b1b1b"
FAINT = "#9a958c"
RULE = "#c9c3b8"
PAPER = "#faf8f4"
DEFECT = "#2f4858"
TASK = "#7a6a55"
ENH = "#a33b20"
FONT = ("Iowan Old Style, Palatino Linotype, Palatino, Charter, "
        "Georgia, 'Times New Roman', serif")
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"

TYPES = ["defect", "task", "enhancement"]
STATES = ["severity", "N/A", "none"]
FATES = ["fixed", "closed otherwise", "still open"]
TYPE_COLOUR = {"defect": DEFECT, "task": TASK, "enhancement": ENH}
STATE_COLOUR = {"severity": DEFECT, "N/A": FAINT, "none": ENH}

COLS = [118, 396, 674, 898]
NODE_W = 13
AT, AH = 132, 392          # panel A: top, height available to the bars
GAP = 22
BT, BH = 636, 178          # panel B


def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text(x, y, s, size=12, fill=INK, anchor="start", font=FONT, weight="normal",
         style="normal", spacing=None):
    extra = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" '
            f'font-style="{style}"{extra}>{esc(s)}</text>')


def ribbon(x0, y0, x1, y1, thick0, thick1, colour, opacity):
    """A flow from (x0, y0) with thickness thick0 to (x1, y1) with thickness thick1."""
    xm = (x0 + x1) / 2
    return (f'<path d="M {x0:.1f},{y0:.1f} C {xm:.1f},{y0:.1f} {xm:.1f},{y1:.1f} '
            f'{x1:.1f},{y1:.1f} L {x1:.1f},{y1 + thick1:.1f} '
            f'C {xm:.1f},{y1 + thick1:.1f} {xm:.1f},{y0 + thick0:.1f} '
            f'{x0:.1f},{y0 + thick0:.1f} Z" fill="{colour}" fill-opacity="{opacity}" '
            f'stroke="none"/>')


def stack(order, sizes, top, height, gap):
    """Lay nodes out down a column, proportional to size, and give back their y-extents."""
    total = sum(sizes[k] for k in order)
    bars = height - gap * (len(order) - 1)
    scale = bars / total
    out, y = {}, top
    for key in order:
        h = sizes[key] * scale
        out[key] = (y, h)
        y += h + gap
    return out, scale


def panel_a(res, parts):
    flow = res["flow"]
    total = flow["total"]
    by_type = {t: flow["by_type"][t] for t in TYPES}
    t2s = {}
    for key, n in flow["type_to_norm_state"].items():
        typ, state = key.split("|")
        t2s[(typ, state)] = n
    s2f = {}
    for key, n in flow["norm_state_to_fate"].items():
        state, fate = key.split("|")
        s2f[(state, fate)] = n
    by_state = {s: sum(t2s.get((t, s), 0) for t in TYPES) for s in STATES}
    by_fate = {f: sum(s2f.get((s, f), 0) for s in STATES) for f in FATES}

    nodes_t, scale = stack(TYPES, by_type, AT, AH, GAP)
    nodes_s, _ = stack(STATES, by_state, AT, AH, GAP)
    nodes_f, _ = stack(FATES, by_fate, AT, AH, GAP)
    source_h = total * scale
    source_y = AT + (AH - source_h) / 2

    # stage 0 -> 1
    cursor = source_y
    for typ in TYPES:
        h = by_type[typ] * scale
        y_t, _ = nodes_t[typ]
        parts.append(ribbon(COLS[0] + NODE_W, cursor, COLS[1], y_t, h, h,
                            TYPE_COLOUR[typ], 0.30))
        cursor += h

    # stage 1 -> 2
    out_cursor = {t: nodes_t[t][0] for t in TYPES}
    in_cursor = {s: nodes_s[s][0] for s in STATES}
    for state in STATES:
        for typ in TYPES:
            n = t2s.get((typ, state), 0)
            if not n:
                continue
            h = n * scale
            parts.append(ribbon(COLS[1] + NODE_W, out_cursor[typ], COLS[2], in_cursor[state],
                                h, h, TYPE_COLOUR[typ], 0.30))
            out_cursor[typ] += h
            in_cursor[state] += h

    # stage 2 -> 3
    out_cursor = {s: nodes_s[s][0] for s in STATES}
    in_cursor = {f: nodes_f[f][0] for f in FATES}
    for fate in FATES:
        for state in STATES:
            n = s2f.get((state, fate), 0)
            if not n:
                continue
            h = n * scale
            parts.append(ribbon(COLS[2] + NODE_W, out_cursor[state], COLS[3], in_cursor[fate],
                                h, h, STATE_COLOUR[state], 0.30))
            out_cursor[state] += h
            in_cursor[fate] += h

    # the nodes themselves, drawn over the ribbons
    parts.append(f'<rect x="{COLS[0]}" y="{source_y:.1f}" width="{NODE_W}" '
                 f'height="{source_h:.1f}" fill="{INK}"/>')
    parts.append(text(COLS[0] - 8, source_y - 12, f"{total:,} differences reported",
                      size=12.5, anchor="end"))
    parts.append(text(COLS[0] - 8, source_y + 6, "2024-01-01 to 2025-06-30,", size=10.5,
                      fill=FAINT, anchor="end"))
    parts.append(text(COLS[0] - 8, source_y + 20, "seven Firefox-related products,", size=10.5,
                      fill=FAINT, anchor="end"))
    parts.append(text(COLS[0] - 8, source_y + 34, "each at least 424 days old", size=10.5,
                      fill=FAINT, anchor="end"))

    for typ in TYPES:
        y, h = nodes_t[typ]
        parts.append(f'<rect x="{COLS[1]}" y="{y:.1f}" width="{NODE_W}" height="{h:.1f}" '
                     f'fill="{TYPE_COLOUR[typ]}"/>')
        parts.append(text(COLS[1] + NODE_W + 7, y + 13, typ, size=13))
        parts.append(text(COLS[1] + NODE_W + 7, y + 28, f"{by_type[typ]:,}", size=11,
                          fill=FAINT, font=MONO))
    for state in STATES:
        y, h = nodes_s[state]
        label = {"severity": "a severity: S1–S4",
                 "N/A": "N/A — the scale does not apply",
                 "none": "none — the field still reads “--”"}[state]
        parts.append(f'<rect x="{COLS[2]}" y="{y:.1f}" width="{NODE_W}" height="{h:.1f}" '
                     f'fill="{STATE_COLOUR[state]}"/>')
        parts.append(text(COLS[2] + NODE_W + 7, y + 13, label, size=12))
        parts.append(text(COLS[2] + NODE_W + 7, y + 28, f"{by_state[state]:,}", size=11,
                          fill=FAINT, font=MONO))
    for fate in FATES:
        y, h = nodes_f[fate]
        parts.append(f'<rect x="{COLS[3]}" y="{y:.1f}" width="{NODE_W}" height="{h:.1f}" '
                     f'fill="{INK}"/>')
        parts.append(text(COLS[3] + NODE_W + 7, y + 13, fate, size=12))
        parts.append(text(COLS[3] + NODE_W + 7, y + 28, f"{by_fate[fate]:,}", size=11,
                          fill=FAINT, font=MONO))

    heads = [
        (COLS[0] + NODE_W / 2, "the filing"),
        (COLS[1] + NODE_W / 2, "the box the filer ticks"),
        (COLS[2] + NODE_W / 2, "whether a norm was imposed"),
        (COLS[3] + NODE_W / 2, "what became of the difference"),
    ]
    for x, label in heads:
        parts.append(text(x, AT - 30, label, size=11, fill=INK, anchor="middle",
                          spacing="0.06em"))
    parts.append(f'<line x1="60" y1="{AT - 20}" x2="{W - 40}" y2="{AT - 20}" '
                 f'stroke="{RULE}" stroke-width="0.8"/>')


def panel_b(res, parts):
    ttr = res["time_to_resolution_by_type"]
    edges = ttr["defect"]["histogram_bins_days"]
    n_bins = len(edges) + 1
    left, right = 118, W - 250
    bin_w = (right - left) / n_bins
    row_h = 46
    parts.append(text(60, BT - 26, "and how long each stream took to be closed",
                      size=11, spacing="0.06em"))
    parts.append(f'<line x1="60" y1="{BT - 16}" x2="{W - 40}" y2="{BT - 16}" '
                 f'stroke="{RULE}" stroke-width="0.8"/>')

    # the policy's week: the bin edge at 8 days is the first that is entirely past one week
    week_x = left + bin_w * (edges.index(8))
    parts.append(f'<line x1="{week_x:.1f}" y1="{BT - 6}" x2="{week_x:.1f}" '
                 f'y2="{BT + 3 * row_h + 6}" stroke="{INK}" stroke-width="0.9" '
                 f'stroke-dasharray="3 3"/>')
    parts.append(text(week_x + 5, BT - 10, "one week — the policy's own timeframe",
                      size=10, fill=INK))

    for i, typ in enumerate(TYPES):
        row = ttr.get(typ)
        if not row:
            continue
        y0 = BT + i * row_h
        peak = max(row["histogram"])
        for j, count in enumerate(row["histogram"]):
            h = (count / peak) * (row_h - 16)
            x = left + j * bin_w
            parts.append(f'<rect x="{x:.1f}" y="{y0 + (row_h - 16) - h:.1f}" '
                         f'width="{bin_w - 2:.1f}" height="{h:.1f}" '
                         f'fill="{TYPE_COLOUR[typ]}" fill-opacity="0.55"/>')
        parts.append(f'<line x1="{left}" y1="{y0 + row_h - 16:.1f}" x2="{right:.1f}" '
                     f'y2="{y0 + row_h - 16:.1f}" stroke="{RULE}" stroke-width="0.8"/>')
        parts.append(text(left - 8, y0 + row_h - 20, typ, size=12, anchor="end"))
        parts.append(text(right + 14, y0 + row_h - 28,
                          f"median {row['median_days']:g} days", size=11, font=MONO))
        parts.append(text(right + 14, y0 + row_h - 15,
                          f"{row['within_7_days_pct']:g}% closed within the week",
                          size=10.5, fill=FAINT))
    axis_y = BT + 3 * row_h - 8
    for j, edge in enumerate(edges):
        if j % 2:
            continue
        x = left + j * bin_w
        parts.append(text(x, axis_y + 16, str(edge), size=9.5, fill=FAINT, anchor="middle",
                          font=MONO))
    parts.append(text(right + 14, axis_y + 16, "days to closure, doubling bins", size=9.5,
                      fill=FAINT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="figure.svg")
    args = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "results.json"), encoding="utf-8") as fh:
        res = json.load(fh)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" aria-label="A three-stage routing diagram of 67,272 '
        f'bug reports: the type the filer chose, whether a severity was ever set, and what '
        f'became of the report; below, how long each stream took to close.">',
        f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
        text(60, 52, "Who will be asked", size=23),
        text(60, 74, "One act of filing, three streams, and a norm that arrives in one of them",
             size=12.5, fill=FAINT, style="italic"),
    ]
    panel_a(res, parts)
    panel_b(res, parts)

    note = ("Every count is from results.json, measured 2026-08-29 over bugzilla.mozilla.org's "
            "publicly visible record. “Triaged”, in Mozilla's own words, is a defect whose "
            "component is not UNTRIAGED and whose severity is neither -- nor N/A;")
    note2 = ("its policy asks for that within one week of filing. Security bugs are not visible "
             "to an unauthenticated reader and are not in this population.")
    parts.append(f'<line x1="60" y1="{H - 62}" x2="{W - 40}" y2="{H - 62}" '
                 f'stroke="{RULE}" stroke-width="0.8"/>')
    parts.append(text(60, H - 44, note, size=10, fill=FAINT))
    parts.append(text(60, H - 30, note2, size=10, fill=FAINT))
    parts.append(text(60, H - 12, "Ulysses (the nightly line) · Error as Method · Session 74",
                      size=10, fill=FAINT, spacing="0.05em"))
    parts.append("</svg>")

    out = os.path.join(here, args.out)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts) + "\n")
    print(f"wrote {out} ({os.path.getsize(out):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
