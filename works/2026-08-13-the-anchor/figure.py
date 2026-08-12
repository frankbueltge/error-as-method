#!/usr/bin/env python3
"""
Generates figure.svg from results.json. Deterministic: no randomness, no seed,
no network. Run `measure.py` first.

The figure puts two populations of admitted institutional error side by side.
Left: the 28 elements the HTML Living Standard forbids, sorted into the three
fates the measurement found. Right: the 39 permanent name corrections session 49
counted in the Unicode Character Database, which has only one fate available.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json"), encoding="utf-8"))

INK = "#16150f"
MUTE = "#6f6a5c"
RULE = "#c9c2b0"
KEEP = "#2f4858"        # still specified: the institution still instructs
MOVED = "#7d8c7a"       # specified elsewhere: moved, not removed
GONE = "#ffffff"        # absent from normative prose: genuinely removed
UNICODE = "#7a3b2e"     # cannot be removed at all

els = R["elements"]
in163 = set(R["elements_named_in_16_3"])
absent = set(R["elements_absent_from_all_three_sections"])
unspec = set(R["elements_unspecified_in_16_3"])
elsewhere = (unspec - absent)

bands = [
    (sorted(in163), KEEP, "still specified to implementations, chapter 16"),
    (sorted(elsewhere), MOVED, "specified in the rendering or parsing sections"),
    (sorted(absent), GONE, "absent from the normative prose of all three"),
]

W, H = 940, 620
BOX, GAP = 15, 4
out = []
a = out.append

a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
  f'font-family="Iowan Old Style, Palatino Linotype, Palatino, Georgia, serif">')
a(f'<rect width="{W}" height="{H}" fill="#f6f3ea"/>')

a(f'<text x="40" y="52" font-size="27" fill="{INK}">What an institution is able to remove</text>')
a(f'<text x="40" y="76" font-size="14" fill="{MUTE}">The HTML Living Standard repairs its '
  f'normative text in place — no versions, no errata list. These are the 28 elements it '
  f'forbids, by what became of them.</text>')

y = 118
for names, colour, label in bands:
    a(f'<text x="40" y="{y}" font-size="13" fill="{INK}">{len(names)}</text>')
    a(f'<text x="62" y="{y}" font-size="13" fill="{MUTE}">{label}</text>')
    x = 40
    yy = y + 14
    for n in names:
        stroke = RULE if colour == GONE else colour
        a(f'<rect x="{x}" y="{yy}" width="{BOX}" height="{BOX}" fill="{colour}" '
          f'stroke="{stroke}" stroke-width="1"/>')
        a(f'<text x="{x + BOX + 5}" y="{yy + 12}" font-size="11.5" fill="{INK}" '
          f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{n}</text>')
        x += BOX + 9 + 7.2 * len(n) + GAP
        if x > 520:
            x = 40
            yy += BOX + 10
    y = yy + 52

a(f'<line x1="600" y1="100" x2="600" y2="410" stroke="{RULE}" stroke-width="1"/>')

a(f'<text x="632" y="122" font-size="13" fill="{INK}">39</text>')
a(f'<text x="654" y="122" font-size="13" fill="{MUTE}">Unicode: name corrections that</text>')
a(f'<text x="654" y="139" font-size="13" fill="{MUTE}">cannot be removed, ever</text>')
x, yy = 632, 152
for i in range(39):
    a(f'<rect x="{x}" y="{yy}" width="{BOX}" height="{BOX}" fill="{UNICODE}"/>')
    x += BOX + GAP
    if x > 632 + 9 * (BOX + GAP):
        x = 632
        yy += BOX + GAP
a(f'<text x="632" y="{yy + 44}" font-size="12" fill="{MUTE}">One fate only. Encoding Stability</text>')
a(f'<text x="632" y="{yy + 60}" font-size="12" fill="{MUTE}">forbids the repair, so the correction</text>')
a(f'<text x="632" y="{yy + 76}" font-size="12" fill="{MUTE}">is instituted beside the error and</text>')
a(f'<text x="632" y="{yy + 92}" font-size="12" fill="{MUTE}">both names stay normative.</text>')
a(f'<text x="632" y="{yy + 116}" font-size="11" fill="{MUTE}">measured 2026-08-12, session 49</text>')

a(f'<line x1="40" y1="452" x2="900" y2="452" stroke="{RULE}" stroke-width="1"/>')
a(f'<text x="40" y="480" font-size="13" fill="{INK}">Where the same standard does freeze — '
  f'and what points at it from outside</text>')
fy = 504
for f in R["freeze_census"]:
    a(f'<text x="40" y="{fy}" font-size="12.5" fill="{INK}" '
      f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{f["mechanism"]}</text>')
    a(f'<text x="215" y="{fy}" font-size="12.5" fill="{MUTE}">— for {f["outside_it_serves"]}</text>')
    fy += 21

a(f'<text x="40" y="{fy + 18}" font-size="12" fill="{MUTE}">Removal criterion, WHATWG Working Mode: '
  f'“The feature being removed must either be not widely implemented,</text>')
a(f'<text x="40" y="{fy + 35}" font-size="12" fill="{MUTE}">or must in the process of being removed '
  f'from implementations.”</text>')

a('</svg>')

with open(os.path.join(HERE, "figure.svg"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("wrote figure.svg —", sum(len(b[0]) for b in bands), "elements placed")
