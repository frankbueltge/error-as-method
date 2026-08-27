#!/usr/bin/env python3
"""figure.py — Session 72, 2026-08-27.

Draws figure.svg: raw SVG, stdlib only, deterministic (no randomness, so no seed).

What it draws, and why this shape rather than last night's timeline. The night's
subject is *when* a norm arrived, and the record's answer to that question has a
hole in it: 5,157 of 8,021 errata carry the same `update_date`, a database
migration in September 2019. So the figure plots each erratum at
(reported, adjudicated) and lets the hole draw itself — the diagonal is the
record working, the horizontal bar at 2019-09-10 is 64% of the record's memory of
its own judgements collapsed onto one day.

Beneath it, a second strip: the 728 errata that have no verdict at all, by the
year they were reported. Those have no y-coordinate, because no norm has been
imposed on them. Under the standing position they are not yet errors.

Binned to month × month cells so the file stays small and no point is drawn twice.

Usage:
    python3 figure.py --raw ../../.raw --out figure.svg
"""

import argparse
import collections
import datetime
import json
import sys

W, H = 980, 700
L, R, T, B = 78, 26, 58, 210          # margins; B leaves room for the pending strip
Y0, Y1 = 2000, 2027                   # axis span, years
MIGRATION = datetime.date(2019, 9, 10)
QUARANTINED = "6534"

INK = "#1b1b1b"
FAINT = "#9a958c"
RULE = "#c9c3b8"
MARK = "#2f4858"
STRIPE = "#a33b20"
PEND = "#5c6b3f"
FONT = ("Iowan Old Style, Palatino Linotype, Palatino, Charter, "
        "Georgia, 'Times New Roman', serif")
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"


def frac(d):
    """A date as a fractional year."""
    y0 = datetime.date(d.year, 1, 1)
    y1 = datetime.date(d.year + 1, 1, 1)
    return d.year + (d - y0).days / (y1 - y0).days


def parse_day(s):
    try:
        return datetime.date.fromisoformat((s or "").strip()[:10])
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="../../.raw")
    ap.add_argument("--out", default="figure.svg")
    args = ap.parse_args()
    errata = json.load(open(f"{args.raw}/errata.json"))

    plot_w = W - L - R
    plot_h = H - T - B

    def px(yr):
        return L + (yr - Y0) / (Y1 - Y0) * plot_w

    def py(yr):
        return T + plot_h - (yr - Y0) / (Y1 - Y0) * plot_h

    cells = collections.Counter()
    pending = collections.Counter()
    n_plotted = n_pending = n_off = 0
    for e in errata:
        if e["errata_id"] == QUARANTINED:
            n_off += 1
            continue
        s = parse_day(e["submit_date"])
        u = parse_day(e.get("update_date"))
        if not s:
            n_off += 1
            continue
        if e["errata_status_code"] == "Reported" or not u:
            pending[(s.year, s.month)] += 1
            n_pending += 1
            continue
        cells[((s.year, s.month), (u.year, u.month))] += 1
        n_plotted += 1

    def mid(ym):
        return frac(datetime.date(ym[0], ym[1], 15))

    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
             f'width="{W}" height="{H}" font-family="{FONT}">')
    o.append(f'<rect width="{W}" height="{H}" fill="#faf8f4"/>')

    # frame and year rules
    o.append(f'<rect x="{L}" y="{T}" width="{plot_w}" height="{plot_h}" fill="none" '
             f'stroke="{RULE}" stroke-width="1"/>')
    for y in range(Y0, Y1 + 1, 5):
        o.append(f'<line x1="{px(y):.1f}" y1="{T}" x2="{px(y):.1f}" y2="{T+plot_h}" '
                 f'stroke="{RULE}" stroke-width=".5"/>')
        o.append(f'<line x1="{L}" y1="{py(y):.1f}" x2="{L+plot_w}" y2="{py(y):.1f}" '
                 f'stroke="{RULE}" stroke-width=".5"/>')
        o.append(f'<text x="{px(y):.1f}" y="{T+plot_h+16}" font-size="11" fill="{FAINT}" '
                 f'text-anchor="middle" font-family="{MONO}">{y}</text>')
        o.append(f'<text x="{L-8}" y="{py(y)+4:.1f}" font-size="11" fill="{FAINT}" '
                 f'text-anchor="end" font-family="{MONO}">{y}</text>')

    # the impossible half-plane: a verdict cannot precede its report
    o.append(f'<line x1="{px(Y0):.1f}" y1="{py(Y0):.1f}" x2="{px(Y1):.1f}" y2="{py(Y1):.1f}" '
             f'stroke="{FAINT}" stroke-width="1" stroke-dasharray="4 4"/>')
    o.append(f'<text x="{px(2006.2):.1f}" y="{py(2005.5):.1f}" font-size="11" fill="{FAINT}" '
             f'transform="rotate(-45 {px(2006.2):.1f} {py(2005.5):.1f})">'
             f'judged the day it was reported</text>')

    # the migration stripe, drawn before the marks so the marks sit on it
    my = py(frac(MIGRATION))
    o.append(f'<line x1="{L}" y1="{my:.1f}" x2="{L+plot_w}" y2="{my:.1f}" '
             f'stroke="{STRIPE}" stroke-width="1.6" opacity=".55"/>')

    mx = max(cells.values())
    for (s, u), n in sorted(cells.items()):
        x, y = px(mid(s)), py(mid(u))
        op = 0.30 + 0.62 * (min(n, 40) / 40) ** 0.5
        col = STRIPE if (u == (2019, 9)) else MARK
        o.append(f'<rect x="{x-1.7:.1f}" y="{y-1.7:.1f}" width="3.4" height="3.4" '
                 f'fill="{col}" opacity="{op:.2f}"/>')

    # pending strip
    sy = T + plot_h + 46
    sh = 74
    o.append(f'<rect x="{L}" y="{sy}" width="{plot_w}" height="{sh}" fill="none" '
             f'stroke="{RULE}" stroke-width="1"/>')
    pmax = max(pending.values()) if pending else 1
    for ym, n in sorted(pending.items()):
        x = px(mid(ym))
        h = (n / pmax) * (sh - 10)
        o.append(f'<rect x="{x-1.7:.1f}" y="{sy+sh-h:.1f}" width="3.4" height="{h:.1f}" '
                 f'fill="{PEND}" opacity=".8"/>')
    o.append(f'<text x="{L}" y="{sy-8}" font-size="12" fill="{INK}">'
             f'{n_pending} reports on which no norm has been imposed, by the month they were '
             f'made — they have no second date, so they cannot be plotted above</text>')
    o.append(f'<text x="{L+plot_w}" y="{sy+sh+16}" font-size="11" fill="{FAINT}" '
             f'text-anchor="end" font-family="{MONO}">tallest bar: {pmax} in one month</text>')

    # labels
    o.append(f'<text x="{L}" y="26" font-size="16" fill="{INK}">'
             f'8,021 reported differences, and when a norm was imposed on each</text>')
    o.append(f'<text x="{L}" y="44" font-size="12" fill="{FAINT}">'
             f'RFC Errata, fetched 2026-08-27 · x: reported · y: adjudicated, as the '
             f'machine-readable record gives it</text>')
    o.append(f'<text x="{L-58}" y="{T+plot_h/2:.1f}" font-size="12" fill="{FAINT}" '
             f'text-anchor="middle" transform="rotate(-90 {L-58} {T+plot_h/2:.1f})">'
             f'adjudicated</text>')
    lx = px(2000.4)
    o.append(f'<text x="{lx:.1f}" y="{my-10:.1f}" font-size="12" fill="{STRIPE}">'
             f'2019-09-10 — 5,157 verdicts on one day: a database migration, not a judgement.</text>')
    o.append(f'<text x="{lx:.1f}" y="{my+18:.1f}" font-size="12" fill="{STRIPE}">'
             f'Nothing below this line: the record holds no adjudication date earlier than it.</text>')
    o.append(f'<text x="{lx:.1f}" y="{my+36:.1f}" font-size="12" fill="{FAINT}">'
             f'The overwritten dates are still shown on each erratum&#8217;s own page — '
             f'29 of 40 sampled, a median of 7.7 years earlier.</text>')

    o.append(f'<text x="{L}" y="{H-16}" font-size="11" fill="{FAINT}" font-family="{MONO}">'
             f'{n_plotted} plotted · {n_pending} pending · {n_off} off every axis '
             f'(eid 6534, reported 9999-04-13, held for document update 2021-04-13) · '
             f'densest cell {mx}</text>')
    o.append("</svg>")

    open(args.out, "w").write("\n".join(o) + "\n")
    print(f"  {args.out}: {n_plotted} plotted, {n_pending} pending, {n_off} off-axis",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
