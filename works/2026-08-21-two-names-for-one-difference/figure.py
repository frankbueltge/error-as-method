#!/usr/bin/env python3
"""Draw the object-side split by track, straight from results.json. Deterministic, stdlib only.

One row per track, concrete works only (W + N; the meta works are named in the caption, not
drawn). Each row is a bar split wrong-result | non-arrival. Track C is the whole point: it is
the only bar with no wrong-result in it.

    python3 figure.py   # writes figure.svg beside this file
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "results.json"), encoding="utf-8") as fh:
    R = json.load(fh)

TRACKS = [
    ("C", "C · model collapse, the prohibited exit"),
    ("B", "B · glitch, error as medium"),
    ("A", "A · what error is"),
    ("I", "I · institutional norms"),
    ("S", "S · self-audit"),
]
by = R["by_track_concrete_only"]

# palette: two restrained inks on paper, error warm, non-arrival cool-grey.
INK = "#2b2b2b"
ERR = "#b5533a"      # wrong-result: present, warm
NON = "#5b6b78"      # non-arrival: absent, cool
FAINT = "#9a9488"
PAPER = "#f7f4ee"
FONT = "Iowan Old Style, Palatino, 'Palatino Linotype', Georgia, serif"
MONO = "'DejaVu Sans Mono', 'Courier New', monospace"

W, H = 760, 470
x0, top = 300, 96
unit = 34          # px per work
rowh, gap = 34, 16

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" font-family="{FONT}">')
svg.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
svg.append(f'<text x="40" y="44" font-size="21" fill="{INK}">Two names for one difference</text>')
svg.append(f'<text x="40" y="68" font-size="13" fill="{FAINT}">'
           f'the 27 works with a concrete object, by track and by the sign of the difference '
           f'— wrong-result vs non-arrival</text>')

# axis ticks
for k in range(0, 11, 2):
    xx = x0 + k * unit
    svg.append(f'<line x1="{xx}" y1="{top-8}" x2="{xx}" y2="{top + len(TRACKS)*(rowh+gap) - gap + 4}" '
               f'stroke="#e3ddd1" stroke-width="1"/>')
    svg.append(f'<text x="{xx}" y="{top-14}" font-size="10" fill="{FAINT}" '
               f'text-anchor="middle" font-family="{MONO}">{k}</text>')

y = top
for key, label in TRACKS:
    w = by.get(key, {}).get("W", 0)
    n = by.get(key, {}).get("N", 0)
    svg.append(f'<text x="{x0-14}" y="{y+rowh//2+4}" font-size="12.5" fill="{INK}" '
               f'text-anchor="end">{label}</text>')
    xx = x0
    if w:
        wpx = w * unit
        svg.append(f'<rect x="{xx}" y="{y}" width="{wpx}" height="{rowh}" fill="{ERR}"/>')
        svg.append(f'<text x="{xx+wpx/2}" y="{y+rowh//2+5}" font-size="13" fill="{PAPER}" '
                   f'text-anchor="middle" font-family="{MONO}">{w}</text>')
        xx += wpx
    if n:
        npx = n * unit
        svg.append(f'<rect x="{xx}" y="{y}" width="{npx}" height="{rowh}" fill="{NON}"/>')
        svg.append(f'<text x="{xx+npx/2}" y="{y+rowh//2+5}" font-size="13" fill="{PAPER}" '
                   f'text-anchor="middle" font-family="{MONO}">{n}</text>')
    if key == "C":
        cx = x0 + (w + n) * unit
        svg.append(f'<text x="{cx+12}" y="{y+rowh//2+4}" font-size="11.5" fill="{NON}" '
                   f'font-style="italic">no wrong-result in it</text>')
    y += rowh + gap

# legend
ly = y + 10
svg.append(f'<rect x="{x0}" y="{ly}" width="16" height="16" fill="{ERR}"/>')
svg.append(f'<text x="{x0+22}" y="{ly+13}" font-size="12" fill="{INK}">wrong-result '
           f'(error: a present, wrong value) — {R["by_class"]["W"]}</text>')
svg.append(f'<rect x="{x0}" y="{ly+24}" width="16" height="16" fill="{NON}"/>')
svg.append(f'<text x="{x0+22}" y="{ly+37}" font-size="12" fill="{INK}">non-arrival '
           f'(failure: an expected value, absent) — {R["by_class"]["N"]}</text>')

cap1 = ("22 further works are meta — the object is a norm, a self-audit, or the epistemic "
        "thing itself, so they are not drawn.")
cap2 = ("The sign is observer-relative: 7 rows are boundary cases (Ariane 501 is a wrong "
        "value that became a halt); flip all 7 and Track C stays 1 : 9.")
svg.append(f'<text x="40" y="{H-30}" font-size="10.5" fill="{FAINT}">{cap1}</text>')
svg.append(f'<text x="40" y="{H-16}" font-size="10.5" fill="{FAINT}">{cap2}</text>')
svg.append('</svg>')

out = os.path.join(HERE, "figure.svg")
with open(out, "w", encoding="utf-8") as fh:
    fh.write("\n".join(svg) + "\n")
print("wrote", out)
