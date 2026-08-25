#!/usr/bin/env python3
"""Draw figure.svg. Raw SVG, no libraries, deterministic, no randomness so no seed.

Three panels.

A — the three grids on one time axis, 2023-04-18 (the file's first commit) to
    2026-08-25 (tonight). 78 release tags, 94 commits, 840 patchsets. The panel
    exists to kill an assumption I nearly drew instead: the release grid is not
    sparse. Go ships a tag every fortnight. Density is not what makes the values
    below invisible.

B — the descent. Eleven values whose life is measurable: eight replaced inside a
    change that later merged, three added to master and reverted. Each is drawn
    against the interval between the minor releases that enclose it, on a log
    axis, because 8.6 h and 10,276 h do not share a linear one.

C — the arithmetic, which is the finding in four numbers per column: what each
    floor holds, at three precisions. Strict nesting, checked in both directions.

Usage: python3 figure.py    Reads grids.json, results.json, findings.json.
"""

import datetime as dt
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 980, 806
INK, CREAM, RED, GREEN, GREY = "#1b1b1b", "#f4f1ea", "#8c2f1e", "#5c6b52", "#a09a8c"
SERIF = "Iowan Old Style, Palatino, Georgia, serif"
MONO = "IBM Plex Mono, DejaVu Sans Mono, Courier New, monospace"
out = []


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text(x, y, s, size=12, fill=INK, anchor="start", font=SERIF, weight=None):
    out.append('<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s" '
               'font-family="%s"%s>%s</text>'
               % (x, y, size, fill, anchor, font,
                  ' font-weight="%s"' % weight if weight else "", esc(s)))


def line(x1, y1, x2, y2, stroke=INK, w=1, dash=None, op=None):
    out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s%s/>'
               % (x1, y1, x2, y2, stroke, w,
                  ' stroke-dasharray="%s"' % dash if dash else "",
                  ' stroke-opacity="%s"' % op if op else ""))


def rect(x, y, w, h, fill, op=None):
    out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"%s/>'
               % (x, y, w, h, fill, ' fill-opacity="%s"' % op if op else ""))


def ts(s):
    return dt.datetime.strptime(s[:19].replace("T", " "), "%Y-%m-%d %H:%M:%S")


def main():
    g = json.load(open(os.path.join(HERE, "grids.json")))
    res = json.load(open(os.path.join(HERE, "results.json")))
    fnd = json.load(open(os.path.join(HERE, "findings.json")))

    out.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
               'viewBox="0 0 %d %d" font-family="%s">' % (W, H, W, H, SERIF))
    rect(0, 0, W, H, CREAM)

    text(40, 40, "Under the commit", 21)
    text(40, 60, "src/internal/godebugs/table.go read at three nested sampling units — "
                 "the release, the commit, and the patchset", 12.5, GREEN)

    # ---------------------------------------------------------------- panel A
    text(40, 104, "A", 13, RED, font=MONO)
    text(58, 104, "three grids, one axis: the release grid is not sparse", 13)

    L, R = 150.0, 930.0
    t0, t1 = ts("2023-04-01 00:00:00"), ts("2026-09-01 00:00:00")
    span = (t1 - t0).total_seconds()

    def X(d):
        return L + (R - L) * ((ts(d) - t0).total_seconds() / span)

    lanes = [("release", 78, 148.0), ("commit", 94, 190.0), ("patchset", 840, 232.0)]
    dates = {"release": [p["cdate"] for p in g["points"] if p["grid"] == "release"],
             "commit": [p["cdate"] for p in g["points"] if p["grid"] == "commit"],
             "patchset": [p["created"] for p in g["points"] if p["grid"] == "patchset"]}
    for name, n, y in lanes:
        line(L, y + 16, R, y + 16, GREY, 0.8)
        for d in dates[name]:
            x = X(d)
            if L <= x <= R:
                line(x, y - 8, x, y + 14, INK, 0.7, op=0.55)
        text(L - 12, y + 12, "%s  %d" % (name, n), 11.5, INK, anchor="end", font=MONO)

    # the eleven values, in the lane of the floor that alone can see them
    lane_y = {"review": 232.0, "commit": 190.0}
    for d in fnd["descent"]:
        y = lane_y[d["floor"]]
        x = X(d["start"])
        line(x, y - 12, x, y + 18, RED, 1.6)
    for yr in (2023, 2024, 2025, 2026):
        x = X("%d-01-01 00:00:00" % yr)
        line(x, 258, x, 264, INK, 0.9)
        text(x, 275, str(yr), 10.5, INK, anchor="middle", font=MONO)

    text(L, 296, "red: the eleven values of panel B, each drawn in the lane of the floor "
                 "that alone can see it — and in no lane above it.", 11, RED)

    # ---------------------------------------------------------------- panel B
    text(40, 340, "B", 13, RED, font=MONO)
    text(58, 340, "the descent — how long each value lived, against the interval "
                  "between the minor releases enclosing it", 13)

    BL, BR = 340.0, 830.0
    lo, hi = math.log10(4.0), math.log10(20000.0)

    def Xh(hours):
        return BL + (BR - BL) * ((math.log10(max(hours, 4.0)) - lo) / (hi - lo))

    for h, lab in ((8, "8 h"), (24, "1 day"), (168, "1 week"), (720, "1 month"),
                   (4380, "6 months"), (17520, "2 years")):
        x = Xh(h)
        line(x, 362, x, 620, GREY, 0.7, dash="2 4")
        text(x, 356, lab, 10, GREY, anchor="middle", font=MONO)

    y = 378.0
    for d in fnd["descent"]:
        life = d["lifetime_seconds"] / 3600.0
        gap = d["enclosing_release_interval"]["gap_seconds"] / 3600.0
        rect(Xh(4), y - 7, Xh(gap) - Xh(4), 14, GREEN, op=0.22)
        rect(Xh(4), y - 4, Xh(life) - Xh(4), 8, RED)
        tag = d["name"] + ("" if not d["changed"] else "  Changed: %d" % d["changed"])
        text(BL - 12, y + 4, tag, 11, INK, anchor="end", font=MONO)
        text(BR + 14, y + 4, "1 : %d" % round(gap / life), 10.5, GREEN, font=MONO)
        text(40, y + 4, d["floor"], 10, RED if d["floor"] == "review" else INK, font=MONO)
        if d["name"] == "x509keypairleaf":
            out.append('<circle cx="%.1f" cy="%.1f" r="3.2" fill="%s"/>'
                       % (BL - 8, y, RED))
        y += 22.5

    text(40, y + 14, "green: the interval between the minor releases that enclose the value.   "
                     "red: the value's whole life.   Every one of the eleven fits inside one "
                     "release interval.", 10.5, GREEN)
    text(40, y + 32, "\u25cf  x509keypairleaf, Changed: 32 — 19 h 27 m 19 s in patch set 1 of "
                     "CL 585856, a boundary naming Go 1.32, a release that does not exist.",
         10.5, RED)

    # ---------------------------------------------------------------- panel C
    text(40, 706, "C", 13, RED, font=MONO)
    text(58, 706, "what each floor holds — strict nesting, checked in both directions", 13)

    cols = [("names", "names"), ("(name, Changed) pairs", "pairs"),
            ("full six-field tuples", "tuples")]
    x0 = 150.0
    for ci, (label, key) in enumerate(cols):
        cx = x0 + ci * 270
        text(cx, 734, label, 11, GREEN, font=MONO)
        for ri, grid in enumerate(("release", "commit", "patchset")):
            v = res["grid_sizes"][grid][key]
            text(cx + ri * 62, 760, str(v), 20, INK if ri < 2 else RED, font=MONO)
            if ri < 2:
                text(cx + ri * 62 + 32, 760, "\u2282", 14, GREY, font=MONO)
        text(cx, 778, "release   commit   patchset", 9.5, GREY, font=MONO)

    text(40, H - 8, "Session 70 · 2026-08-25 · Ulysses (the nightly line) · "
                    "drawn from grids.json, results.json, findings.json", 10, GREY)

    out.append("</svg>")
    open(os.path.join(HERE, "figure.svg"), "w").write("\n".join(out) + "\n")
    print("figure.svg:", sum(len(s) for s in out), "bytes of markup")


if __name__ == "__main__":
    main()
