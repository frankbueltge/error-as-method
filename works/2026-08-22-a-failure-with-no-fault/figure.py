#!/usr/bin/env python3
"""Draw the boundary ladder: one event carried up six boundaries, renamed at each.

Deterministic, stdlib only. Reads results.json for the computed values and
adjudication.json for the per-boundary verdicts, so the drawing cannot drift from
the measurement.

The form is a ladder rather than a bar chart on purpose: the finding is about
position, not magnitude. The one bar in the picture is the inset strip, which is
the only place a magnitude is the point -- how narrow the no-fault band is.

    python3 figure.py   # writes figure.svg beside this file
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "results.json"), encoding="utf-8") as fh:
    R = json.load(fh)
with open(os.path.join(HERE, "adjudication.json"), encoding="utf-8") as fh:
    A = json.load(fh)

BOUND = A["worked_example"]["boundaries"]
FAULT = A["the_fault_question"]

INK = "#2b2b2b"
ERR = "#b5533a"      # content failure: a value is there and it is wrong
NON = "#5b6b78"      # halt: the value is not there
NONE_ = "#8f9a86"    # no failure at this boundary
SPLIT = "#8a6a3c"    # sign not fixed by the event
FAINT = "#9a9488"
RULE = "#e3ddd1"
PAPER = "#f7f4ee"
FONT = "Iowan Old Style, Palatino, 'Palatino Linotype', Georgia, serif"
MONO = "'DejaVu Sans Mono', 'Courier New', monospace"

COLOUR = {"none": NONE_, "W": ERR, "N": NON, "split": SPLIT}

# The label each boundary gets, and the sign key used for colour. Taken from the
# signed adjudication rather than re-decided here.
def signkey(row):
    if not row["difference"]:
        return "none"
    s = row["sign"]
    if s == "W":
        return "W"
    if s == "N":
        return "N"
    return "split"


SHORT = {
    0: ("the character", "U+00DF is assigned; NFC leaves it alone"),
    1: ("the component, against its own RFC", "nameprep(faß) = fass — exactly as RFC 3491 requires"),
    2: ("the component, against its caller's assumption", "a well-formed name that is not the name given"),
    3: ("the URL standard the browsers implement", "fass.de here, xn--fa-hia.de there"),
    4: ("the round trip", "decode(encode(faß.de)) ≠ faß.de"),
    5: ("resolution", "the sign is settled by a DNS zone"),
}
VERDICT = {
    0: "no failure",
    1: "no failure — correct service",
    2: "content failure, unsignaled",
    3: "content failure, unsignaled",
    4: "the expected value is absent",
    5: "content failure or halt — not fixed here",
}

W, H = 1020, 700
LEFT = 56
LADDER = 470          # x of the ladder spine
top = 132
rowh = 66

out = []
out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" font-family="{FONT}">')
out.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')

out.append(f'<text x="{LEFT}" y="52" font-size="21" fill="{INK}">A failure with no fault</text>')
out.append(f'<text x="{LEFT}" y="76" font-size="13" fill="{FAINT}">'
           f'One string, faß.de, carried up six boundaries. The bytes never change. '
           f'What the taxonomy calls them changes four times.</text>')
out.append(f'<text x="{LEFT}" y="96" font-size="12" fill="{FAINT}" font-family="{MONO}">'
           f'CPython {R["environment"]["python"]} · IdnaMappingTable {R["mapping_table"]["version"]} '
           f'· vocabulary: Avizienis et al. 2004, §2.2, §3.3.1, §3.5</text>')

# the spine
out.append(f'<line x1="{LADDER}" y1="{top - 18}" x2="{LADDER}" y2="{top + rowh * 5 + 18}" '
           f'stroke="{RULE}" stroke-width="2"/>')

for row in BOUND:
    i = row["b"]
    y = top + rowh * i
    k = signkey(row)
    c = COLOUR[k]

    # boundary name, left of the spine
    name, detail = SHORT[i]
    out.append(f'<text x="{LADDER - 26}" y="{y - 2}" font-size="14" fill="{INK}" '
               f'text-anchor="end">{name}</text>')
    out.append(f'<text x="{LADDER - 26}" y="{y + 16}" font-size="11.5" fill="{FAINT}" '
               f'text-anchor="end" font-family="{MONO}">{detail}</text>')

    # the marker on the spine: a ring when there is no difference, a filled disc when there is
    if k == "none":
        out.append(f'<circle cx="{LADDER}" cy="{y}" r="8" fill="{PAPER}" stroke="{c}" stroke-width="2.5"/>')
    elif k == "split":
        # half and half: the sign is not fixed by the event
        out.append(f'<path d="M {LADDER} {y - 9} A 9 9 0 0 1 {LADDER} {y + 9} Z" fill="{ERR}"/>')
        out.append(f'<path d="M {LADDER} {y - 9} A 9 9 0 0 0 {LADDER} {y + 9} Z" fill="{NON}"/>')
        out.append(f'<line x1="{LADDER}" y1="{y - 9}" x2="{LADDER}" y2="{y + 9}" '
                   f'stroke="{PAPER}" stroke-width="1.4"/>')
    else:
        out.append(f'<circle cx="{LADDER}" cy="{y}" r="8" fill="{c}"/>')

    # verdict, right of the spine
    out.append(f'<text x="{LADDER + 26}" y="{y + 4}" font-size="13.5" fill="{INK}">{VERDICT[i]}</text>')

# the two brackets that carry the argument
b1y, b3y, b4y = top + rowh * 1, top + rowh * 3, top + rowh * 4
bx = LADDER + 330
out.append(f'<path d="M {bx} {b1y} L {bx + 10} {b1y} L {bx + 10} {b3y} L {bx} {b3y}" '
           f'fill="none" stroke="{FAINT}" stroke-width="1"/>')
out.append(f'<text x="{bx + 16}" y="{(b1y + b3y) / 2 - 4}" font-size="11.5" fill="{FAINT}">'
           f'the same call,</text>')
out.append(f'<text x="{bx + 16}" y="{(b1y + b3y) / 2 + 10}" font-size="11.5" fill="{FAINT}">'
           f'conformant and failing</text>')
out.append(f'<path d="M {bx} {b3y} L {bx + 10} {b3y} L {bx + 10} {b4y} L {bx} {b4y}" '
           f'fill="none" stroke="{ERR}" stroke-width="1"/>')
out.append(f'<text x="{bx + 16}" y="{(b3y + b4y) / 2 + 4}" font-size="11.5" fill="{ERR}">'
           f'the sign flips here</text>')

# ---- inset: the census, and how narrow the no-fault band is
iy = top + rowh * 5 + 62
total = R["classes"]["silent_divergence"]
loc = FAULT["locatable_fault"]["count"]
defe = FAULT["defensible_not_a_fault"]["count"]
nof = FAULT["no_fault_locatable"]["count"]
assert loc + defe + nof == total, (loc, defe, nof, total)

out.append(f'<text x="{LEFT}" y="{iy}" font-size="13.5" fill="{INK}">'
           f'All {total:,} silent divergences between the two norms, over every Unicode code point '
           f'— both sides return a name, and the names differ</text>')

bw, bx0, bh = W - 2 * LEFT, LEFT, 24
by = iy + 14
xx = bx0
for count, colour, label in ((defe, "#c9c2b4", "input outside the frozen repertoire"),
                             (loc, ERR, "a locatable fault: one line, 85 Cherokee letters"),
                             (nof, NON, f"no fault on either side: {nof}")):
    wpx = bw * count / total
    out.append(f'<rect x="{xx:.2f}" y="{by}" width="{wpx:.2f}" height="{bh}" fill="{colour}"/>')
    xx += wpx
out.append(f'<rect x="{bx0}" y="{by}" width="{bw}" height="{bh}" fill="none" stroke="{RULE}"/>')

# leader line to the sliver, which is far too narrow to label in place
sliver_x = bx0 + bw * (defe + loc) / total + bw * nof / total / 2
out.append(f'<line x1="{sliver_x:.2f}" y1="{by + bh}" x2="{sliver_x:.2f}" y2="{by + bh + 14}" '
           f'stroke="{NON}" stroke-width="1"/>')
out.append(f'<text x="{sliver_x - 4:.2f}" y="{by + bh + 27}" font-size="11.5" fill="{NON}" '
           f'text-anchor="end">{nof} with no fault on either side '
           f'— 4 by design, 5 frozen-vs-current, 10 editorial</text>')

leg = by + bh + 50
out.append(f'<text x="{LEFT}" y="{leg}" font-size="11.5" fill="{FAINT}" font-family="{MONO}">'
           f'{defe:,} · unassigned in Unicode 3.2, passed through '
           f'│ {loc} · stringprep.map_table_b3, code.lower() '
           f'│ {nof} · no fault</text>')
out.append(f'<text x="{LEFT}" y="{leg + 18}" font-size="11.5" fill="{FAINT}">'
           f'Session 65 · 2026-08-22 · census.py over {R["population"]["code_points_examined"]:,} '
           f'code points · mapping stage only</text>')

out.append("</svg>")

path = os.path.join(HERE, "figure.svg")
with open(path, "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
print("wrote", path)
