#!/usr/bin/env python3
"""figure.py -- draw the shape of a permanent registry's memory.

One mark per ISO 639-3 retirement, 2005-2026, placed by the date the upstream authority
retired the code. Marks rise above the line if the retired code is in the IANA Language
Subtag Registry today, deprecated and permanently valid. Marks fall below the line if it
is not there at all. The registry has never removed a name, so nothing below the line was
ever taken out -- it was never let in.

Deterministic: same results.json, same SVG. Reads results.json and sources/floor-test.csv,
writes figure.svg. No network, no dependencies.
"""

import csv
import datetime
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1000, 640
BG, INK, MUTE, RULE = "#eef0f1", "#14181c", "#6b737a", "#b9c0c4"
SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif"
MONO = "'IBM Plex Mono','DejaVu Sans Mono',monospace"

X0, X1 = 92.0, 952.0
BASE = 300.0            # the line the marks stand on
# Marks are packed into per-year blocks, PER_ROW wide, growing away from the baseline.
# One mark is one retirement; nothing is aggregated away.
MW, MH, MGX, MGY, PER_ROW = 5.0, 5.6, 1.9, 2.2, 5
T0 = datetime.date(2005, 1, 1)
T1 = datetime.date(2026, 12, 31)
CUT = datetime.date(2009, 7, 29)


def x_of(d):
    return X0 + (X1 - X0) * ((d - T0).days / (T1 - T0).days)


def mark_xy(year, n, upward):
    """Position of the n-th mark (0-based) in a year's block."""
    x0 = x_of(datetime.date(year, 1, 1)) + 3.0
    col, row = n % PER_ROW, n // PER_ROW
    x = x0 + col * (MW + MGX)
    if upward:
        y = BASE - 5 - (row + 1) * (MH + MGY)
    else:
        y = BASE + 5 + row * (MH + MGY)
    return x, y


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=12, fill=INK, anchor="start", family=SERIF, extra=""):
    return ("<text x='%.1f' y='%.1f' font-size='%s' fill='%s' text-anchor='%s' "
            "font-family=\"%s\"%s>%s</text>" % (x, y, size, fill, anchor, family, extra, esc(s)))


def main():
    res = json.load(open(os.path.join(HERE, "results.json")))
    with open(os.path.join(HERE, "sources", "floor-test.csv")) as fh:
        rows = list(csv.DictReader(fh))

    p = ["<svg xmlns='http://www.w3.org/2000/svg' width='%d' height='%d' viewBox='0 0 %d %d'>"
         % (W, H, W, H),
         "<rect width='%d' height='%d' fill='%s'/>" % (W, H, BG)]

    p.append(text(X0 - 76, 46, "The threshold", 23))
    p.append(text(X0 - 76, 68,
                  "Every code the upstream authority has retired since 2005, and whether the "
                  "permanent registry below it kept the name.", 12.5, MUTE))

    # year gridlines
    for yr in range(2005, 2027, 2):
        x = x_of(datetime.date(yr, 1, 1))
        p.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                 % (x, 112, x, 566, RULE))
        p.append(text(x + 3, 584, str(yr), 10.5, MUTE, "start", MONO))

    # the baseline
    p.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.4'/>"
             % (X0 - 14, BASE, X1 + 8, BASE, INK))

    # one mark per retirement, packed into its year's block
    up, down = {}, {}
    ggm_pos = None
    for r in sorted(rows, key=lambda r: (r["retired_effective"], r["iso639_3_code"])):
        d = datetime.date(*map(int, r["retired_effective"].split("-")))
        if d < T0 or d > T1:
            continue
        kept = r["in_subtag_registry"] == "yes"
        col = up if kept else down
        n = col.get(d.year, 0)
        col[d.year] = n + 1
        x, y = mark_xy(d.year, n, kept)
        if kept:
            p.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>"
                     % (x, y, MW, MH, INK))
        else:
            p.append("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='none' "
                     "stroke='%s' stroke-width='1'/>" % (x, y, MW, MH, MUTE))
        if r["iso639_3_code"] == "ggm":
            ggm_pos = (x, y)

    # the cut
    xc = x_of(CUT)
    p.append("<line x1='%.1f' y1='112' x2='%.1f' y2='566' stroke='%s' stroke-width='1.6' "
             "stroke-dasharray='5 4'/>" % (xc, xc, INK))
    p.append(text(xc + 8, 126, "2009-07-29", 11, INK, "start", MONO))
    p.append(text(xc + 8, 142, "the import: ISO 639-3 enters the registry, and", 11.5, INK))
    p.append(text(xc + 8, 157, "everything it had already retired stays out", 11.5, INK))
    p.append(text(xc - 8, 126, "the registry was not yet", 11.5, MUTE, "end"))
    p.append(text(xc - 8, 141, "remembering", 11.5, MUTE, "end"))

    ft = res["floor_test"]
    kept_n = ft["retired_before_cut"]["in_registry"] + ft["retired_on_or_after_cut"]["in_registry"]
    lost_n = ft["retired_before_cut"]["absent"] + ft["retired_on_or_after_cut"]["absent"]

    p.append(text(X0 - 76, BASE - 30, "%d kept" % kept_n, 13, INK))
    p.append(text(X0 - 76, BASE - 16, "deprecated in the", 11, MUTE))
    p.append(text(X0 - 76, BASE - 4, "registry, and valid", 11, MUTE))
    p.append(text(X0 - 76, BASE + 8, "in a tag for ever", 11, MUTE))
    p.append(text(X0 - 76, BASE + 34, "%d absent" % lost_n, 13, MUTE))
    p.append(text(X0 - 76, BASE + 48, "no record of any", 11, MUTE))
    p.append(text(X0 - 76, BASE + 60, "kind, anywhere", 11, MUTE))
    p.append(text(X0 - 76, BASE + 72, "in the registry", 11, MUTE))

    # the one exception
    if ggm_pos:
        gx, gy = ggm_pos
        cy = gy + MH / 2
        p.append("<circle cx='%.1f' cy='%.1f' r='10' fill='none' stroke='%s' stroke-width='1.3'/>"
                 % (gx + MW / 2, cy, INK))
        p.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
                 % (gx + MW / 2, cy + 10, gx + MW / 2, 492, INK))
        p.append(text(gx + MW / 2, 508, "ggm", 11, INK, "middle", MONO))
        p.append(text(gx + MW / 2 + 22, 508,
                      "'Gugu Mini' — retired as non-existent in 2014, five years inside the", 11.5, INK))
        p.append(text(gx + MW / 2 + 22, 523,
                      "period the registry does remember, and missing all the same: never", 11.5, INK))
        p.append(text(gx + MW / 2 + 22, 538,
                      "added at all, on a tip that it was going to be retired.", 11.5, INK))

    p.append("<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1'/>"
             % (X0 - 76, 92, X1, 92, RULE))
    reg = res["registry"]
    p.append(text(X0 - 76, 606,
                  "Registry file-date %s: %s records, %s deprecated, none ever removed."
                  % (res["registry_file_date"], reg["records"], reg["deprecated"]),
                  11.5, MUTE, family=MONO))
    p.append(text(X0 - 76, 622,
                  "The %d absences are not removals. The names were never entered." % lost_n,
                  11.5, MUTE, family=MONO))

    p.append("</svg>")
    out = os.path.join(HERE, "figure.svg")
    with open(out, "w") as fh:
        fh.write("\n".join(p) + "\n")
    print("wrote figure.svg  (%d marks up, %d down)" % (sum(up.values()), sum(down.values())))


if __name__ == "__main__":
    main()
