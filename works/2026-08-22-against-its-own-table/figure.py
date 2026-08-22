#!/usr/bin/env python3
"""Draw the blind field: every code point where the component departs from its own
specification, marked by whether last night's instrument could see it.

Deterministic, stdlib only. Reads results.json and deviations.json, so the drawing
cannot drift from the measurement. One tick per deviating code point, in code point
order, no sampling and no aggregation -- the picture has exactly as many marks as the
audit has rows.

The form is a field rather than a ladder or a bar chart, and the second row is
deliberately empty: the finding is about what an instrument can and cannot see, and
about a repair that leaves nothing behind.

    python3 figure.py   # writes figure.svg beside this file
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "results.json"), encoding="utf-8") as fh:
    R = json.load(fh)
with open(os.path.join(HERE, "deviations.json"), encoding="utf-8") as fh:
    D = json.load(fh)["rows"]

PAPER = "#f7f4ee"
INK = "#2b2b2b"
FAINT = "#9a9488"
RULE = "#e3ddd1"
SEEN = "#b5533a"      # last night's census recorded a silent divergence here
UNSEEN = "#cec7b8"    # last night's census recorded agreement here
GOOD = "#8f9a86"
FONT = "Iowan Old Style, Palatino, 'Palatino Linotype', Georgia, serif"
MONO = "'DejaVu Sans Mono', 'Courier New', monospace"

W, H = 1020, 584
LEFT, RIGHT = 62, 968
FIELD = RIGHT - LEFT

rows = sorted(D, key=lambda r: int(r["cp"][2:], 16))
N = len(rows)
PITCH = FIELD / N

M = R["mapping_stage"]
SEEN_N = M["visible_to_session_65"]
UNSEEN_N = M["invisible_to_session_65"]

out = []
add = out.append
add('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
    'viewBox="0 0 %d %d" font-family="%s">' % (W, H, W, H, FONT))
add('<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPER))

add('<text x="%d" y="52" font-size="21" fill="%s">Against its own table</text>'
    % (LEFT, INK))
add('<text x="%d" y="76" font-size="13" fill="%s">Every code point where this '
    'interpreter&#8217;s nameprep mapping stage departs from the tables</text>'
    % (LEFT, FAINT))
add('<text x="%d" y="94" font-size="13" fill="%s">RFC 3454 enumerates. One tick each, '
    'in code point order, nothing aggregated.</text>' % (LEFT, FAINT))
add('<text x="%d" y="116" font-size="12" fill="%s" font-family="%s">CPython %s '
    '&#183; RFC 3454, 17 enumerated tables &#183; population %s &#183; deviating '
    '%d</text>'
    % (LEFT, FAINT, MONO, R["environment"]["python"],
       format(M["population"], ","), N))

# ---------------------------------------------------------------- the field
TOP = 166
HGT = 62
add('<text x="%d" y="%d" font-size="13.5" fill="%s">the specification sees %d</text>'
    % (LEFT, TOP - 14, INK, N))
add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
    % (LEFT, TOP + HGT + 1, RIGHT, TOP + HGT + 1, RULE))

for i, r in enumerate(rows):
    x = LEFT + i * PITCH
    seen = r["session_65_class"] == "silent_divergence"
    add('<rect x="%.3f" y="%d" width="%.3f" height="%d" fill="%s"/>'
        % (x, TOP, max(PITCH, 0.9), HGT, SEEN if seen else UNSEEN))

# Bracket the named families. Positions are computed from the data, not placed by eye.
def span(lo, hi):
    idx = [i for i, r in enumerate(rows) if lo <= int(r["cp"][2:], 16) <= hi]
    if not idx:
        return None
    return LEFT + idx[0] * PITCH, LEFT + (idx[-1] + 1) * PITCH, len(idx)

FAMILIES = [
    (0x04C0, 0x04C0, "Cyrillic palochka", -1),
    (0x10A0, 0x10C5, "Georgian capitals", 1),
    (0x13A0, 0x13F5, "Cherokee", -1),
    (0x2132, 0x2183, "letterlike, Roman numeral", 1),
]
LANE = {-1: TOP + HGT + 26, 1: TOP + HGT + 62}
for lo, hi, label, lane in FAMILIES:
    s = span(lo, hi)
    if not s:
        continue
    x0, x1, n = s
    y = LANE[lane]
    mid = (x0 + x1) / 2
    add('<path d="M %.2f %d L %.2f %.2f L %.2f %.2f L %.2f %d" fill="none" '
        'stroke="%s" stroke-width="1"/>'
        % (mid, TOP + HGT + 2, mid, y - 22, mid + 14, y - 22, mid + 14, y - 12,
           FAINT))
    add('<text x="%.2f" y="%d" font-size="11.5" fill="%s">%s &#183; %d</text>'
        % (mid + 18, y - 8, INK, label, n))

add('<text x="%d" y="%d" font-size="11.5" fill="%s" text-anchor="end">'
    '%d more, unassigned in Unicode 3.2</text>'
    % (RIGHT, TOP + HGT + 26, FAINT, M["assigned_in_unicode_3_2"]["unassigned"]))

# ---------------------------------------------------------------- the blind half
LEG = TOP + HGT + 104
add('<rect x="%d" y="%d" width="26" height="11" fill="%s"/>' % (LEFT, LEG - 9, SEEN))
add('<text x="%d" y="%d" font-size="12.5" fill="%s">%d were visible to last '
    'night&#8217;s census, which compared this component with a second '
    'implementation.</text>' % (LEFT + 34, LEG, INK, SEEN_N))
add('<rect x="%d" y="%d" width="26" height="11" fill="%s"/>'
    % (LEFT, LEG + 21, UNSEEN))
add('<text x="%d" y="%d" font-size="12.5" fill="%s">%d were not. The second '
    'implementation leaves the frozen repertoire the same way, so the two</text>'
    % (LEFT + 34, LEG + 30, INK, UNSEEN_N))
add('<text x="%d" y="%d" font-size="12.5" fill="%s">agreed &#8212; and agreement was '
    'the evidence.</text>' % (LEFT + 34, LEG + 48, INK))

# ---------------------------------------------------------------- the repair
RTOP = 452
add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
    % (LEFT, RTOP - 26, RIGHT, RTOP - 26, RULE))
add('<text x="%d" y="%d" font-size="13.5" fill="%s">the same field after one line is '
    'changed</text>' % (LEFT, RTOP, INK))
add('<text x="%d" y="%d" font-size="12" fill="%s" font-family="%s">'
    'map_table_b3&#8217;s <tspan fill="%s">return code.lower()</tspan> replaced by a '
    'lookup in the enumerated Table B.3 &#8212; nothing else touched</text>'
    % (LEFT, RTOP + 20, FAINT, MONO, INK))
add('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" '
    'stroke-width="1" stroke-dasharray="2 3"/>' % (LEFT, RTOP + 34, FIELD, 30, RULE))
add('<text x="%.1f" y="%d" font-size="12.5" fill="%s" text-anchor="middle">'
    'nothing &#8212; %d of %s</text>'
    % (LEFT + FIELD / 2, RTOP + 54, GOOD,
       R["the_one_line_repair"]["deviating_code_points_after_repair"],
       format(M["population"], ",")))

add('<text x="%d" y="%d" font-size="11" fill="%s" font-family="%s">'
    'Fifteen of the seventeen tables match the RFC exactly. The two that deviate are '
    'the two the module computes instead of copying.</text>' % (LEFT, H - 40, FAINT, MONO))
add('<text x="%d" y="%d" font-size="11" fill="%s" font-family="%s">'
    'audit.py &#183; results.json &#183; deviations.json &#183; Session 66, '
    '2026-08-22</text>' % (LEFT, H - 22, FAINT, MONO))
add('</svg>')

with open(os.path.join(HERE, "figure.svg"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
print("figure.svg: %d ticks, %d seen, %d unseen" % (N, SEEN_N, UNSEEN_N))
