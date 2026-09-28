#!/usr/bin/env python3
"""figure.svg for The Join. No network, no randomness: the cells are read from adjudication.json's
alignment as judged by hand, and written out here as a table so a reader can check each mark.

    python3 figure.py > figure.svg
"""
from xml.sax.saxutils import escape

INK, MUTED, RULE, BG, CUT = "#1d1d1b", "#6b6b66", "#d9d6cf", "#faf8f3", "#a23b2a"

COLS = ["a difference", "held against", "someone holds it", "fixed before", "no true value", "a genus"]
# 2 present, 1 partly present, 0 absent -- each mark argued in adjudication.json
ROWS = [
    ("Standing sentence, Sessions 26–98", [2, 2, 2, 2, 2, 2]),
    ("Standing sentence, from Session 99", [2, 2, 2, 2, 2, 0]),
    ("VIM 2.16, measurement error (JCGM 200:2012)", [2, 2, 0, 1, 0, 0]),
    ("FDA glossary 8/95, error (ISO)", [2, 2, 0, 1, 0, 0]),
]
W, H = 900, 470
X0, Y0, CW, RH = 330, 200, 90, 52


def mark(cx, cy, v):
    if v == 2:
        return f'<circle cx="{cx}" cy="{cy}" r="9" fill="{INK}"/>'
    if v == 1:
        return (f'<circle cx="{cx}" cy="{cy}" r="9" fill="none" stroke="{INK}" stroke-width="1.5"/>'
                f'<path d="M{cx} {cy-9} A9 9 0 0 0 {cx} {cy+9} Z" fill="{INK}"/>')
    return f'<circle cx="{cx}" cy="{cy}" r="9" fill="none" stroke="{MUTED}" stroke-width="1.5"/>'


def main():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia, serif" role="img" '
         'aria-label="The standing sentence with its genus clause struck out, and a table comparing the old sentence, '
         'the new one, the metrology vocabulary and the FDA software glossary on six features. Only the practice\'s '
         'sentences have someone who holds the norm and exclude a true value; only the old sentence has a genus.">',
         f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<text x="40" y="44" font-size="19" fill="{INK}">Error is <tspan fill="{CUT}" text-decoration="line-through">a special case of the epistemic thing —</tspan></text>',
         f'<text x="40" y="74" font-size="19" fill="{INK}">a difference onto which an observer has already imposed a norm.</text>',
         f'<text x="40" y="104" font-size="12" fill="{MUTED}">Session 99, 2026-09-28: S93.GENUS survived at its due date and the genus clause was subtracted,'
         ' decided without Rheinberger 1997.</text>']
    for j, c in enumerate(COLS):
        cx = X0 + j * CW + CW / 2
        o.append(f'<text x="{cx}" y="{Y0-40}" font-size="12" fill="{INK}" text-anchor="middle">{escape(c)}</text>')
    for i, (label, vals) in enumerate(ROWS):
        cy = Y0 + i * RH
        o.append(f'<line x1="40" y1="{cy+RH/2}" x2="{X0+len(COLS)*CW}" y2="{cy+RH/2}" stroke="{RULE}"/>')
        o.append(f'<text x="40" y="{cy+5}" font-size="13" fill="{INK}">{escape(label)}</text>')
        for j, v in enumerate(vals):
            o.append(mark(X0 + j * CW + CW / 2, cy, v))
    ly = Y0 + len(ROWS) * RH + 22
    o.append(mark(52, ly, 2) + f'<text x="68" y="{ly+4}" font-size="11" fill="{MUTED}">present</text>')
    o.append(mark(142, ly, 1) + f'<text x="158" y="{ly+4}" font-size="11" fill="{MUTED}">partly: VIM’s calibration or convention (Note 1(a)); the FDA’s “specified” value, one of three it allows</text>')
    o.append(mark(52, ly + 28, 0) + f'<text x="68" y="{ly+32}" font-size="11" fill="{MUTED}">absent. Both standards also admit a “true” value that nobody imposed; the practice\'s sentence does not.</text>')
    o.append('</svg>')
    print("\n".join(o))


if __name__ == "__main__":
    main()
