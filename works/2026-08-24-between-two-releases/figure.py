#!/usr/bin/env python3
"""Draw figure.svg. Raw SVG, no libraries, deterministic, no randomness so no seed.

Three panels, and the argument is in the arithmetic of the first one.

A — the whole life of Lib/__future__.py on one time axis, 2001-02-26 to today. Above the
    rule, the 22 grid points Session 62 sampled; below it, the 40 commits that have ever
    touched the file. The value this night is about lived 1 h 0 m 18 s, which on this axis
    is four thousandths of a pixel. It cannot be drawn. It is marked with a hairline and a
    leader, and the panel's honesty is that the mark is bigger than the thing.

B — the same interval, magnified 112,000 times: two hours of 2006-02-28, the two commits
    an hour apart, and the two nearest grid points 657 days out on either side.

C — the second blindness, which is not on the time axis at all. The boundary is a
    five-slot tuple; the move is in the fifth slot; Session 62's reduction reads the first
    two. Even a per-commit instrument that reduced the tuple to the release it names would
    have returned zero.
"""

import datetime as dt
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

INK = "#1b1b1b"
PAPER = "#f4f1ea"
MOVED = "#8c2f1e"
FAINT = "#b9b2a4"
QUIET = "#5c6b52"
FONT = "Iowan Old Style, Palatino, Georgia, serif"
MONO = "IBM Plex Mono, DejaVu Sans Mono, Courier New, monospace"

# The two commits, from results.json; kept here as the anchor the panels share.
T0 = dt.datetime(2006, 2, 28, 19, 2, 24, tzinfo=dt.timezone.utc)
T1 = dt.datetime(2006, 2, 28, 20, 2, 42, tzinfo=dt.timezone.utc)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def iso(s):
    return dt.datetime.fromisoformat(s)


def main():
    res = json.load(open(os.path.join(HERE, "results.json")))
    commits = json.load(open(os.path.join(HERE, "commits.json")))

    cdates = [iso(c["author_date"]) for c in commits["commits"]]
    rels = [r for r in commits["releases"] if r.get("tag_date")]

    lo = min(cdates)
    hi = dt.datetime(2026, 8, 24, tzinfo=dt.timezone.utc)
    span = (hi - lo).total_seconds()

    W, H = 980, 772
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="{FONT}">',
         f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']

    def text(x, y, s, size=12, fill=INK, anchor="start", font=FONT, style=""):
        o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
                 f'text-anchor="{anchor}" font-family="{font}" {style}>{esc(s)}</text>')

    # ---------------------------------------------------------------- title
    text(40, 40, "A value between two releases", 21)
    text(40, 60,
         "Lib/__future__.py — every commit that has ever touched it, against the "
         "grid of releases an earlier night read it on", 12.5, QUIET)

    # ---------------------------------------------------------------- panel A
    AX0, AX1, AY = 60, W - 60, 196
    aw = AX1 - AX0

    def ax(t):
        return AX0 + aw * ((t - lo).total_seconds() / span)

    text(40, 104, "A", 13, MOVED, font=MONO)
    text(58, 104, "twenty-five years, six months, on one axis", 13)

    o.append(f'<line x1="{AX0}" y1="{AY}" x2="{AX1}" y2="{AY}" stroke="{INK}" '
             f'stroke-width="1"/>')

    # releases above
    for r in rels:
        x = ax(iso(r["tag_date"]))
        out_of_order = r["ref_kind"] == "tag" and r["series"] == "2.3"
        col = MOVED if out_of_order else INK
        o.append(f'<line x1="{x:.1f}" y1="{AY - 26}" x2="{x:.1f}" y2="{AY}" '
                 f'stroke="{col}" stroke-width="1.4"/>')
        if r["series"] in ("2.1", "2.5", "3.0", "3.7", "3.14", "2.3"):
            text(x, AY - 32, r["series"], 10.5,
                 col, "middle", MONO)
    text(AX0, 126, "22 release states — Session 62's grid", 11.5, QUIET)
    text(AX1, 126, "red: the one grid point that is not a release (C2)", 11.5,
         MOVED, "end")

    # commits below
    for d in cdates:
        x = ax(d)
        o.append(f'<line x1="{x:.1f}" y1="{AY}" x2="{x:.1f}" y2="{AY + 16}" '
                 f'stroke="{FAINT}" stroke-width="1.2"/>')
    text(AX0, AY + 34, "40 commit states — tonight's", 11.5, QUIET)

    # the sliver
    xs = ax(T0)
    o.append(f'<line x1="{xs:.1f}" y1="{AY - 62}" x2="{xs:.1f}" y2="{AY + 22}" '
             f'stroke="{MOVED}" stroke-width="0.9" stroke-dasharray="2 3"/>')
    o.append(f'<circle cx="{xs:.1f}" cy="{AY}" r="3.2" fill="{MOVED}"/>')
    text(xs + 8, AY + 56, "2006-02-28 · with_statement.OptionalRelease", 11.5, MOVED)
    text(xs + 8, AY + 71,
         "(2, 5, 0, \"alpha\", 2)  →  (2, 5, 0, \"alpha\", 1)", 11.5, INK, font=MONO)
    text(xs + 8, AY + 87,
         "lifetime 1 h 0 m 18 s — 0.0039 px at this scale. The mark is 233 times "
         "wider than the thing.", 11, QUIET)

    # ---------------------------------------------------------------- panel B
    BY = 424
    BX0, BX1 = 60, W - 60
    bw = BX1 - BX0
    blo = dt.datetime(2006, 2, 28, 18, 30, tzinfo=dt.timezone.utc)
    bhi = dt.datetime(2006, 2, 28, 20, 30, tzinfo=dt.timezone.utc)
    bspan = (bhi - blo).total_seconds()

    def bx(t):
        return BX0 + bw * ((t - blo).total_seconds() / bspan)

    text(40, BY - 66, "B", 13, MOVED, font=MONO)
    text(58, BY - 66, "the same interval, magnified 112,000 times: two hours", 13)

    o.append(f'<rect x="{bx(T0):.1f}" y="{BY - 24}" width="{bx(T1) - bx(T0):.1f}" '
             f'height="48" fill="{MOVED}" fill-opacity="0.11"/>')
    o.append(f'<line x1="{BX0}" y1="{BY}" x2="{BX1}" y2="{BY}" stroke="{INK}" '
             f'stroke-width="1"/>')
    for h in range(19, 21):
        t = dt.datetime(2006, 2, 28, h, 0, tzinfo=dt.timezone.utc)
        x = bx(t)
        o.append(f'<line x1="{x:.1f}" y1="{BY}" x2="{x:.1f}" y2="{BY + 7}" '
                 f'stroke="{FAINT}" stroke-width="1"/>')
        text(x, BY + 21, f"{h:02d}:00 UTC", 10.5, QUIET, "middle", MONO)

    for t, sha, who, val, dy in (
            (T0, "34aa7ba1", "Thomas Wouters", '(2, 5, 0, "alpha", 2)', -1),
            (T1, "91934912", "Neal Norwitz", '(2, 5, 0, "alpha", 1)', 1)):
        x = bx(t)
        o.append(f'<line x1="{x:.1f}" y1="{BY - 24}" x2="{x:.1f}" y2="{BY + 24}" '
                 f'stroke="{MOVED}" stroke-width="1.4"/>')
        o.append(f'<circle cx="{x:.1f}" cy="{BY}" r="3.4" fill="{MOVED}"/>')
        yy = BY - 40 if dy < 0 else BY + 46
        anchor = "start" if dy < 0 else "end"
        ox = x + 9 if dy < 0 else x - 9
        text(ox, yy, f'{t.strftime("%H:%M:%S")}  {sha}  {who}', 11, INK, anchor)
        text(ox, yy + 15, val, 11, MOVED, anchor, MONO)

    text(BX0, BY - 40, "← v2.4", 11, QUIET)
    text(BX0, BY - 26, "455 days", 10.5, QUIET)
    text(BX1, BY - 40, "v2.5 →", 11, QUIET, "end")
    text(BX1, BY - 26, "201 days", 10.5, QUIET, "end")
    text(BX0, BY + 92,
         "The nearest two points on Session 62's grid are 657 days apart. Nothing that "
         "lives inside them is reachable from it,", 11.5, INK)
    text(BX0, BY + 108,
         "at any sampling density that grid is capable of — the difference is not "
         "between its points, it is between its units.", 11.5, INK)

    # ---------------------------------------------------------------- panel C
    CY = 626
    text(40, CY - 52, "C", 13, MOVED, font=MONO)
    text(58, CY - 52,
         "the second blindness, and it is not on the time axis at all", 13)

    slots = [("2", 0), ("5", 0), ("0", 0), ('"alpha"', 0), ("2 → 1", 1)]
    sx, sw = 96, 96
    for i, (label, moved) in enumerate(slots):
        x = sx + i * sw
        col = MOVED if moved else INK
        o.append(f'<rect x="{x}" y="{CY}" width="{sw - 12}" height="34" fill="none" '
                 f'stroke="{col}" stroke-width="{1.6 if moved else 1}"/>')
        text(x + (sw - 12) / 2, CY + 22, label, 12.5, col, "middle", MONO)
        text(x + (sw - 12) / 2, CY + 50,
             ["major", "minor", "micro", "level", "serial"][i], 10, QUIET, "middle")

    o.append(f'<path d="M {sx} {CY - 12} L {sx} {CY - 20} L {sx + 2 * sw - 12} {CY - 20} '
             f'L {sx + 2 * sw - 12} {CY - 12}" fill="none" stroke="{QUIET}" '
             f'stroke-width="1"/>')
    text(sx + sw - 6, CY - 26, "what Session 62's instrument read — \"2.5\"",
         11, QUIET, "middle")

    text(sx + 5 * sw + 8, CY + 14,
         "before: 2.5", 11.5, QUIET, "start", MONO)
    text(sx + 5 * sw + 8, CY + 30,
         "after:  2.5", 11.5, QUIET, "start", MONO)
    text(sx + 5 * sw + 8, CY + 46,
         "moves:  0", 11.5, MOVED, "start", MONO)

    text(60, CY + 84,
         "Two alignments, not one. The instrument took the object's unit of time (the "
         "release) and the object's unit of precision", 11.5, INK)
    text(60, CY + 100,
         "(the release a tuple names). Either one alone hides this move. Only "
         "de-aligning both makes it visible.", 11.5, INK)

    n_hits = len(res["P1_tuple_values_never_released"])
    text(W - 60, H - 26,
         f"40 commit states · 22 release states · 10 features · "
         f"{n_hits} value no release ever carried", 10.5, QUIET, "end")

    o.append("</svg>")
    with open(os.path.join(HERE, "figure.svg"), "w") as fh:
        fh.write("\n".join(o) + "\n")
    print(f"figure.svg written, {os.path.getsize(os.path.join(HERE, 'figure.svg'))} bytes")


if __name__ == "__main__":
    main()
