#!/usr/bin/env python3
"""figure.py — draw the twenty norms of this practice against the record's own calendar.

One row per norm, ordered as the populations were fixed: the five instruments, the nine gate
checks, the six prohibitions. The x axis is the record, from the founding day to tonight.

  filled square    the norm's own date
  hollow circle    the breakdown it answers, where one is documented
  joining rule     the interval between them
  open tail west   no parent in this repository — the norm's genesis is outside the record

The point of the drawing is the shape, not the precision: four short rules at the right-hand end,
and fifteen rows with nothing behind them. Deterministic, stdlib only, no network. Reads
adjudication.json beside it; writes figure.svg beside it.
"""

import datetime as dt
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 960, 730
L, R, T = 300, 40, 96
ROW = 22
BAND = 16

INK = "#1b1a17"
PALE = "#8d8a80"
HOT = "#a8321e"
RULE = "#d8d4c8"

START = dt.date(2026, 6, 28)
END = dt.date(2026, 8, 17)
SPAN = (END - START).days


def x_of(day):
    d = dt.date.fromisoformat(day)
    return L + (d - START).days / SPAN * (W - L - R)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def label(norm, limit=40):
    """The norm's short name: everything before the em dash, trimmed."""
    s = norm.split("—")[0].strip()
    if s.startswith("the gate: "):
        s = s[len("the gate: "):]
    return s if len(s) <= limit else s[: limit - 1] + "…"


def main():
    with open(os.path.join(HERE, "adjudication.json"), encoding="utf-8") as fh:
        adj = json.load(fh)
    rows = adj["direction_A"]

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'font-family="Iowan Old Style, Palatino, Georgia, serif">',
        f'<rect width="{W}" height="{H}" fill="#faf8f3"/>',
        f'<text x="{L - 260}" y="40" font-size="19" fill="{INK}">'
        f'The norm is younger than its breach — where it is machinery</text>',
        f'<text x="{L - 260}" y="60" font-size="12.5" fill="{PALE}">'
        f'Twenty norms of this practice, each against the breakdown it answers. '
        f'Populations complete, no sampling.</text>',
    ]

    # calendar
    ticks = ["2026-06-28", "2026-07-08", "2026-07-18", "2026-07-28", "2026-08-07", "2026-08-17"]
    for t in ticks:
        x = x_of(t)
        out.append(f'<line x1="{x:.1f}" y1="{T - 16}" x2="{x:.1f}" y2="{H - 74}" '
                   f'stroke="{RULE}" stroke-width="1"/>')
        out.append(f'<text x="{x:.1f}" y="{T - 22}" font-size="10.5" fill="{PALE}" '
                   f'text-anchor="middle">{t[5:]}</text>')

    # the fork, named because every date in the right-hand cluster is after it
    fx = x_of("2026-08-10")
    out.append(f'<line x1="{fx:.1f}" y1="{T - 16}" x2="{fx:.1f}" y2="{H - 74}" '
               f'stroke="{PALE}" stroke-width="1" stroke-dasharray="2 3"/>')
    out.append(f'<text x="{fx:.1f}" y="{H - 60}" font-size="10.5" fill="{PALE}" '
               f'text-anchor="middle">the fork</text>')

    y = T
    band_seen = None
    for r in rows:
        if r["class"] != band_seen:
            band_seen = r["class"]
            y += BAND
            out.append(f'<text x="14" y="{y + 4:.0f}" font-size="12" fill="{INK}" '
                       f'font-style="italic">{esc(band_seen)}</text>')
            y += 16

        nx = x_of(r["norm_date"])
        out.append(f'<text x="{L - 12}" y="{y + 4:.0f}" font-size="11.5" fill="{INK}" '
                   f'text-anchor="end">{esc(label(r["norm"]))}</text>')

        if r["breakdown_date"]:
            bx = x_of(r["breakdown_date"])
            lo, hi = min(bx, nx), max(bx, nx)
            # the interval is hours or days: draw it with a visible minimum so it can be seen
            hi = max(hi, lo + 7)
            out.append(f'<line x1="{lo:.1f}" y1="{y:.0f}" x2="{hi:.1f}" y2="{y:.0f}" '
                       f'stroke="{HOT}" stroke-width="2.5"/>')
            out.append(f'<circle cx="{lo:.1f}" cy="{y:.0f}" r="4" fill="#faf8f3" '
                       f'stroke="{HOT}" stroke-width="1.6"/>')
            out.append(f'<rect x="{hi - 3.5:.1f}" y="{y - 3.5:.0f}" width="7" height="7" '
                       f'fill="{HOT}"/>')
        else:
            if nx - 6 > L - 4:      # a day-zero norm has no room for a tail, and needs none
                out.append(f'<line x1="{L - 4}" y1="{y:.0f}" x2="{nx - 6:.1f}" y2="{y:.0f}" '
                           f'stroke="{PALE}" stroke-width="1" stroke-dasharray="1 4"/>')
            out.append(f'<rect x="{nx - 3.5:.1f}" y="{y - 3.5:.0f}" width="7" height="7" '
                       f'fill="{INK}"/>')
            out.append(f'<text x="{nx + 9:.1f}" y="{y + 3.5:.0f}" font-size="9.5" '
                       f'fill="{PALE}">{esc(r["verdict"])}</text>')
        y += ROW

    # legend
    ly = H - 40
    out.append(f'<circle cx="{L}" cy="{ly}" r="4" fill="#faf8f3" stroke="{HOT}" stroke-width="1.6"/>')
    out.append(f'<line x1="{L + 5}" y1="{ly}" x2="{L + 26}" y2="{ly}" stroke="{HOT}" stroke-width="2.5"/>')
    out.append(f'<rect x="{L + 24}" y="{ly - 3.5}" width="7" height="7" fill="{HOT}"/>')
    out.append(f'<text x="{L + 40}" y="{ly + 4}" font-size="11" fill="{INK}">'
               f'breakdown, then the norm it produced — 4 of 20, every one of them an instrument</text>')
    out.append(f'<line x1="{L}" y1="{ly + 18}" x2="{L + 26}" y2="{ly + 18}" stroke="{PALE}" '
               f'stroke-width="1" stroke-dasharray="1 4"/>')
    out.append(f'<rect x="{L + 24}" y="{ly + 14.5}" width="7" height="7" fill="{INK}"/>')
    out.append(f'<text x="{L + 40}" y="{ly + 22}" font-size="11" fill="{INK}">'
               f'no breakdown behind it in this record — 16 of 20 — fifteen of them texts, and one instrument that arrived by decision</text>')
    out.append(f'<text x="{L}" y="{ly + 40}" font-size="10" fill="{PALE}" font-style="italic">'
               f'Three of the four intervals are hours long and are drawn at a visible minimum '
               f'width; the drawing overstates them and the dates in adjudication.json do not.</text>')

    out.append("</svg>")
    path = os.path.join(HERE, "figure.svg")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"{len(rows)} rows -> {os.path.basename(path)}")


if __name__ == "__main__":
    main()
