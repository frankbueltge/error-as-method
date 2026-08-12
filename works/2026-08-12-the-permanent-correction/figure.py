#!/usr/bin/env python3
"""
figure.py -- draws figure.svg from results.json. Stdlib only, deterministic, no
randomness, no network. Run measure.py first.

One picture, one reading: thirty-nine names, each drawn as a life. The solid bar is
the time the wrong name stood alone as the norm; the dot is the day a correction was
filed beside it; the dotted line is how long the two have been normative together,
and it does not end, because neither of them can be withdrawn.

Two vertical rules carry the argument. 1996: names become unchangeable. 2006: the
channel for saying so opens, ten years later.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json"), encoding="utf-8"))

W, H = 1000, 1000
INK, MUTE, PAPER = "#16181d", "#8e887a", "#fbfaf7"
BAND, WARM, FAINT = "#ece7da", "#8a5a2b", "#c9c2b2"
MONO = "SFMono-Regular, Menlo, Consolas, monospace"

L, RT, T = 400, 900, 246
X0, X1 = 1992.0, 2027.5
ROW = 15.2
NOW = 2025                      # year of record of Unicode 17.0.0

out = []


def add(t):
    out.append(t)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def x(year):
    return L + (year - X0) / (X1 - X0) * (RT - L)


def text(xx, yy, s, size=11, fill=INK, anchor="start", style="normal",
         weight="normal", family=None):
    fam = ' font-family="%s"' % family if family else ""
    add('<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s" '
        'font-style="%s" font-weight="%s"%s>%s</text>'
        % (xx, yy, size, fill, anchor, style, weight, fam, esc(s)))


def diff_label(name, correction):
    """The words that changed, for the row label."""
    ta, tb = name.split(), correction.split()
    if len(ta) == len(tb):
        d = [(a, b) for a, b in zip(ta, tb) if a != b]
        if len(d) == 1:
            return "%s → %s" % (d[0][0], d[0][1])
        if d:
            return "%s → %s" % (" ".join(a for a, _ in d),
                                     " ".join(b for _, b in d))
    # different token counts: show the tail that changed
    i = 0
    while i < min(len(ta), len(tb)) and ta[i] == tb[i]:
        i += 1
    return "%s → %s" % (" ".join(ta[i:]), " ".join(tb[i:]))


rows = sorted(R["table"], key=lambda t: (t["encoded_year"], -t["unmarked_years"],
                                         t["code"]))

add('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
    'font-family="Iowan Old Style, Palatino, Georgia, serif">' % (W, H, W, H))
add('<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPER))

text(48, 56, "The Permanent Correction", 27)
text(48, 82, "Thirty-nine Unicode characters whose normative name is known to be wrong. The name cannot be changed, so a", 13, MUTE)
text(48, 99, "correction is filed beside it — and the correction cannot be changed either. Both are normative. Neither ends.", 13, MUTE)
text(48, 122, "Solid bar: the years the wrong name stood alone. Dot: the version that filed the correction. Dotted: the two names, "
              "normative together, to 2025.", 11, MUTE, style="italic")
text(48, 138, "Every date is computed by measure.py from the harvested UCD files in data/ — DerivedAge.txt for the encoding, "
              "twenty NameAliases.txt for the filing.", 11, MUTE, style="italic")

# --- axis ---------------------------------------------------------------
axis_y = T - 26
for yr in range(1995, 2026, 5):
    add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1" '
        'stroke-dasharray="1 4"/>' % (x(yr), T - 14, x(yr), T + len(rows) * ROW + 6,
                                      FAINT))
    text(x(yr), axis_y, str(yr), 10, MUTE, anchor="middle")

# the two rules
for yr, label, sub in ((1996, "1996", "Unicode 2.0: a character’s name can never change again"),
                       (2006, "2006", "Unicode 5.0: the correction channel opens, with eleven entries")):
    add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.2"/>'
        % (x(yr), T - 34, x(yr), T + len(rows) * ROW + 6, INK))
    text(x(yr) + 5, T - 46, label, 12, INK, weight="bold")
    text(x(yr) + 5, T - 34, sub, 10, MUTE)

# --- rows ---------------------------------------------------------------
y = T + 4
for t in rows:
    xa, xb, xn = x(t["encoded_year"]), x(t["filed_year"]), x(NOW)
    # coexistence: filed -> now, and past the frame
    add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1" '
        'stroke-dasharray="1 3"/>' % (xb, y, xn + 26, y, MUTE))
    # unmarked interval
    if xb - xa < 1.2:
        add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
            'stroke-width="1.6"/>' % (xa, y - 4.4, xa, y + 4.4, WARM))
    else:
        add('<rect x="%.1f" y="%.1f" width="%.1f" height="5" fill="%s"/>'
            % (xa, y - 2.5, xb - xa, INK))
    add('<circle cx="%.1f" cy="%.1f" r="2.6" fill="%s"/>' % (xb, y, WARM))
    text(48, y + 3.4, "U+" + t["code"], 9.5, MUTE, family=MONO)
    text(106, y + 3.4, diff_label(t["name"], t["correction"]), 10,
         INK if t["kind"] == "replacement" else WARM)
    if t["unmarked_years"]:
        text(966, y + 3.4, "%d" % t["unmarked_years"], 9, MUTE, anchor="end")
    y += ROW

text(48, T - 14, "code", 9, MUTE, family=MONO)
text(106, T - 14, "what the correction changes", 9, MUTE)
text(966, T - 20, "years", 9, MUTE, anchor="end")
text(966, T - 9, "unmarked", 9, MUTE, anchor="end")

foot = T + len(rows) * ROW + 30
text(106, foot, "Warm labels are misspellings by the rule stated in measure.py (15 of 39); dark labels replace a name "
                   "component outright (24).", 10, MUTE, style="italic")
text(106, foot + 16, "The four bars with no length at 2018 are MEDEFAIDRIN letters: the correction was filed in the same "
                        "version that encoded them.", 10, MUTE, style="italic")

agg = R["aggregate"]
text(48, foot + 48, "%d character-years the norm circulated with an unmarked error.   %d character-years the wrong name and its "
                    "correction have been normative together."
     % (agg["character_years_unmarked"], agg["character_years_of_coexistence_to_2025"]),
     12, INK)
text(48, foot + 68, "Both numbers only grow. Encoding Stability, Name Stability and Formal Name Alias Stability are each declared "
                    "for “Unicode N.n and all subsequent versions.”", 11, MUTE)
text(48, foot + 84, "Source: unicode.org/policies/stability_policy.html · unicode.org/Public/<version>/ucd/ · retrieved "
                    "2026-08-12 · sources and SHA-256 in data/MANIFEST.txt", 9.5, MUTE, style="italic")

add("</svg>")

path = os.path.join(HERE, "figure.svg")
open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("figure.svg written: %d rows, %d bytes" % (len(rows), os.path.getsize(path)))
