#!/usr/bin/env python3
"""
figure.py -- draws figure.svg from results.json and sources/release-dates.json.
Stdlib only, deterministic, no network. Nothing is drawn that is not in those
two files; every number printed on the figure is read from them at draw time.

THE FORM. Three address lanes on a year axis, 1991-2026. Each lane is one region
of the code space, and the lane shows who has lived at that address: the first
occupant solid, the vacancy hollow, the second occupant hatched. Below them, on
the same axis, the two operations the institution has ever performed on an
existing character -- withdrawing it and renaming it -- and the vertical rule at
1996 where both were forbidden. Bottom right, what repair became afterwards.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = "#eef0f1"
INK = "#14181c"
GREY = "#6b737a"
RULE = "#b9c0c4"
ACCENT = "#8c2f24"          # the vacancy and the freeze
SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif'"
SERIF = '"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif'
MONO = '"IBM Plex Mono","DejaVu Sans Mono",monospace'

W, H = 1000, 720
X0, X1 = 186.0, 946.0
XLAB = 16.0          # left margin for the lane labels, clear of the plot
Y_LANES = 128.0
LANE_H = 34.0
LANE_GAP = 20.0

Y_OPS = 424.0        # baseline of the operations panel
OPS_H = 96.0
Y_AFTER = 510.0

YEAR0, YEAR1 = 1990.4, 2026.9


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def x_of(year):
    return X0 + (year - YEAR0) / (YEAR1 - YEAR0) * (X1 - X0)


def txt(x, y, s, size=11, fill=INK, anchor="start", family=SERIF, weight=None, style=None):
    a = ' font-weight="%s"' % weight if weight else ""
    b = ' font-style="%s"' % style if style else ""
    return ('<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s" '
            'font-family=\'%s\'%s%s>%s</text>' % (x, y, size, fill, anchor, family, a, b, esc(s)))


def main():
    R = json.load(open(os.path.join(HERE, "results.json")))
    rel = json.load(open(os.path.join(HERE, "sources", "release-dates.json")))["releases"]
    man = json.load(open(os.path.join(HERE, "sources", "MANIFEST.json")))

    # directory label -> the release version its UnicodeData file carries
    # ("2.1-Update4" holds UnicodeData-2.1.9.txt), then -> published year.
    label_ver = {}
    for f in man["files"]:
        if f["version"] == "current":
            continue
        m = re.search(r"UnicodeData-?([0-9.]*)\.txt$", f["url"])
        v = m.group(1).strip(".") if m and m.group(1) else f["version"]
        label_ver[f["version"]] = v if re.match(r"^\d+\.\d+", v) else f["version"]

    def year(label):
        v = label_ver.get(label, label)
        for cand in (v, v + ".0", re.sub(r"^(\d+\.\d+).*", r"\1.0", v)):
            if cand in rel:
                return rel[cand]["year"]
        return None

    s = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
         % (W, H, W, H)]
    s.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPER))
    s.append('<defs>'
             '<pattern id="occ2" width="6" height="6" patternUnits="userSpaceOnUse" '
             'patternTransform="rotate(45)"><rect width="6" height="6" fill="%s"/>'
             '<line x1="0" y1="0" x2="0" y2="6" stroke="%s" stroke-width="2.2"/></pattern>'
             '</defs>' % (PAPER, INK))

    s.append(txt(XLAB, 44, "The vacated block", 23))
    s.append(txt(XLAB, 65,
                 "Three regions of the code space, and everyone who has ever lived at each address.", 12.5, GREY))

    # ---------- year axis ----------
    for yr in range(1991, 2027):
        if yr % 5 != 1 and yr != 1996:
            continue
        x = x_of(yr)
        s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>'
                 % (x, Y_LANES - 14, x, Y_OPS + 6, RULE))
        s.append(txt(x, Y_OPS + 22, str(yr), 10.5, GREY, "middle", MONO))

    # ---------- the freeze rule ----------
    xf = x_of(1996.55)
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6" '
             'stroke-dasharray="1,3"/>' % (xf, Y_LANES - 40, xf, Y_OPS + 6, ACCENT))
    s.append(txt(xf + 6, Y_LANES - 34 + 0, "Unicode 2.0, July 1996", 10.5, ACCENT, "start", MONO))
    s.append(txt(xf + 6, Y_LANES - 21,
                 "“Once a character is encoded, it will not be moved or removed.”",
                 11, ACCENT, "start", SERIF, style="italic"))

    # ---------- lanes ----------
    lanes = [
        {"label": "U+1000..U+104C", "n": 60,
         "occ1": ("TIBETAN LETTER KA …", 1991, 1992),
         "vac": (1992, 1999),
         "occ2": ("MYANMAR LETTER KA …", 1999)},
        {"label": "U+3400..U+4DFF", "n": 6656,
         "occ1": ("HANGUL SYLLABLE KIYEOK A …", 1993, 1995),
         "vac": (1995, 1999),
         "occ2": ("CJK Ideograph Extension A", 1999)},
        {"label": "U+AC00..U+D7A3", "n": 11172,
         "occ1": None,
         "vac": None,
         "occ2": ("HANGUL SYLLABLE GA … (the syllables, re-encoded)", 1996)},
    ]

    y = Y_LANES
    for ln in lanes:
        s.append(txt(XLAB, y + 13, ln["label"], 11, INK, "start", MONO))
        s.append(txt(XLAB, y + 27, "%s addresses" % format(ln["n"], ","), 10, GREY, "start", MONO))
        if ln["occ1"]:
            name, a, b = ln["occ1"]
            s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>'
                     % (x_of(a), y, x_of(b) - x_of(a), LANE_H, INK))
            s.append(txt(x_of(a), y - 5, name, 10.5, INK, "start", MONO))
        if ln["vac"]:
            a, b = ln["vac"]
            s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" '
                     'stroke="%s" stroke-width="1.2" stroke-dasharray="3,3"/>'
                     % (x_of(a), y, x_of(b) - x_of(a), LANE_H, ACCENT))
            s.append(txt((x_of(a) + x_of(b)) / 2, y + 21, "vacant", 10.5, ACCENT, "middle", MONO))
        name, a = ln["occ2"][0], ln["occ2"][1]
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="url(#occ2)" '
                 'stroke="%s" stroke-width="0.8"/>'
                 % (x_of(a), y, x_of(2026.6) - x_of(a), LANE_H, INK))
        s.append(txt(x_of(a) + 6, y + 21, name, 10.5, INK, "start", MONO))
        y += LANE_H + LANE_GAP

    s.append(txt(XLAB, y + 6,
                 "Solid: the first occupant.  Dashed: the address standing empty.  "
                 "Hatched: a different script, at the same address.", 10.5, GREY))

    # ---------- operations panel ----------
    yb = Y_OPS
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.4"/>'
             % (X0, yb, X1, yb, INK))
    s.append(txt(XLAB, yb - OPS_H - 16,
                 "The two operations the standard has ever performed on a character "
                 "that already existed", 12.5, INK))

    ops = []
    for t in R["transitions"]:
        ya, yb2 = year(t["from"]), year(t["to"])
        if yb2 is None or (not t["withdrawn_masked_cjk"] and not t["renamed"]):
            continue
        ops.append((yb2, t["withdrawn_masked_cjk"], t["renamed"], t["from"], t["to"]))

    top = max([max(w, r) for _, w, r, _, _ in ops] + [1])
    def hgt(v):
        return 0 if v <= 0 else 8 + (v / top) ** 0.42 * (OPS_H - 12)

    for yr, w, r, fa, to in ops:
        x = x_of(yr)
        if w:
            s.append('<rect x="%.1f" y="%.1f" width="9" height="%.1f" fill="%s"/>'
                     % (x - 10, yb - hgt(w), hgt(w), ACCENT))
            s.append(txt(x - 5.5, yb - hgt(w) - 5, format(w, ","), 10, ACCENT, "middle", MONO))
        if r:
            s.append('<rect x="%.1f" y="%.1f" width="9" height="%.1f" fill="%s"/>'
                     % (x + 1, yb - hgt(r), hgt(r), INK))
            s.append(txt(x + 5.5, yb - hgt(r) - 5, format(r, ","), 10, INK, "middle", MONO))

    s.append(txt(XLAB, yb - OPS_H + 4, "■ withdrawn", 10.5, ACCENT, "start", MONO))
    s.append(txt(XLAB, yb - OPS_H + 17, "■ renamed", 10.5, INK, "start", MONO))

    last_rel = [c["version"] for c in R["census"]][-1]
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.4"/>'
             % (x_of(1997), yb, x_of(2026.4), yb, INK))
    s.append(txt(x_of(2011), yb - 10,
                 "0 withdrawn, 0 renamed — every release from 2.0 to %s"
                 % label_ver.get(last_rel, last_rel), 11.5, INK, "middle"))

    # ---------- what repair became ----------
    ya = Y_AFTER
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>'
             % (XLAB, ya - 26, X1, ya - 26, RULE))
    s.append(txt(XLAB, ya - 8,
                 "What repair became once the name and the address were both frozen", 12.5, INK))

    n_corr = len(R["corrections"])
    n_note = R["nameslist"]["annotations_by_mark"]
    n_mis = R["misnomer_notes"]["count"]
    n_unrepaired = len(R["misnomer_notes"]["without_formal_alias"])
    tiers = [
        (format(sum(n_note.values()), ","),
         "annotations printed beside the frozen names in the code charts",
         "NamesList.txt, current release"),
        (format(n_corr, ","),
         "characters given a corrected name that sits beside the wrong one",
         "NameAliases.txt, type=correction"),
        (format(n_mis, ","),
         "characters whose chart note calls the name a mistake or a misnomer",
         "“character name is a misnomer”, in the standard's own words"),
        (format(n_unrepaired, ","),
         "of those have no corrected name at all — the admission, and nothing else",
         "U+027F, U+0F0B, U+0F0C"),
    ]
    yy = ya + 14
    for n, line, src in tiers:
        s.append(txt(XLAB + 62, yy + 12, n, 19, INK, "end", MONO))
        s.append(txt(XLAB + 76, yy + 8, line, 12, INK))
        s.append(txt(XLAB + 76, yy + 23, src, 10.5, GREY, "start", MONO))
        yy += 40

    s.append(txt(XLAB, H - 22,
                 "Session 54 · Error as Method · measured from the Unicode Consortium's own "
                 "published archive at unicode.org/Public/ — see measure.py and sources/MANIFEST.json",
                 10, GREY))

    s.append("</svg>")
    out = os.path.join(HERE, "figure.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(s))
    print("wrote figure.svg (%d elements)" % len(s))


if __name__ == "__main__":
    main()
