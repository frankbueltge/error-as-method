#!/usr/bin/env python3
"""Draws figure.svg from the committed records.  No JavaScript: the figure is complete as a static
file, which is the rule this line keeps whatever the site permits.

The figure says one thing, and it is the night's finding rather than its result: the comparison that
scored 28 out of 28 is a comparison between two populations that share almost no modal, and inside
each modal it runs the other way.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
res = json.load(open(HERE / "results.json"))
adj = json.load(open(HERE / "adjudication.json"))

wc = res["whole_corpus"]
REC, ART = wc["recitals"], wc["articles"]

INK = "#1c1a17"
MUTE = "#6d685f"
RULE = "#c9c2b6"
FILL = "#1c1a17"
PALE = "#e4ded2"
PAPER = "#faf7f1"

W, H = 1020, 1010
S = []
add = S.append

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'font-family="Iowan Old Style, Palatino Linotype, Palatino, Charter, Georgia, serif" '
    f'role="img" aria-label="The recital-article gap in bearer-deletion, and the modal composition '
    f'that makes it uninterpretable">')
add(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')

add(f'<text x="46" y="56" font-size="27" fill="{INK}">Twenty-eight out of twenty-eight,</text>')
add(f'<text x="46" y="88" font-size="27" fill="{INK}">and the score says nothing</text>')
add(f'<text x="46" y="120" font-size="14.5" fill="{MUTE}">22,554 occurrences of '
    f'<tspan font-style="italic">shall</tspan>, <tspan font-style="italic">should</tspan> and '
    f'<tspan font-style="italic">must</tspan> in 63 EU legal acts. A norm’s bearer is “deleted” '
    f'where the clause is</text>')
add(f'<text x="46" y="140" font-size="14.5" fill="{MUTE}">a passive with no agent phrase — '
    f'<tspan font-style="italic">“certain measures should be taken”</tspan> — so the party who must '
    f'act is not in the sentence.</text>')

# ------------------------------------------------------------------ panel 1: the gap
y = 214
add(f'<line x1="46" y1="{y-36}" x2="974" y2="{y-36}" stroke="{RULE}" stroke-width="1"/>')
add(f'<text x="46" y="{y-14}" font-size="13" fill="{MUTE}" letter-spacing="1.4">'
    f'1 — THE COMPARISON THE NIGHT SET OUT TO MAKE</text>')

BARX, BARW = 300, 560
SCALE = BARW / 0.60
for label, sub, d in (("recitals", "the half that does not bind", REC),
                      ("articles", "the half that does", ART)):
    rate = d["bearer_deletion_rate"]
    add(f'<text x="46" y="{y+30}" font-size="17" fill="{INK}">{label}</text>')
    add(f'<text x="46" y="{y+50}" font-size="11.5" fill="{MUTE}">{sub}</text>')
    add(f'<text x="46" y="{y+68}" font-size="11.5" fill="{MUTE}">n = {d["modal_occurrences"]:,}</text>')
    add(f'<rect x="{BARX}" y="{y+12}" width="{BARW}" height="26" fill="{PALE}"/>')
    add(f'<rect x="{BARX}" y="{y+12}" width="{rate*SCALE:.1f}" height="26" fill="{FILL}"/>')
    add(f'<text x="{BARX + rate*SCALE + 12:.1f}" y="{y+31}" font-size="15" fill="{INK}">'
        f'{rate*100:.1f}%</text>')
    y += 84

add(f'<text x="{BARX}" y="{y+12}" font-size="13.5" fill="{MUTE}">'
    f'Higher in the recitals in <tspan font-size="15" fill="{INK}">28 of the 28</tspan> named acts. '
    f'No exceptions, no ties.</text>')

# ------------------------------------------------------------------ panel 2: the composition
y += 66
add(f'<line x1="46" y1="{y}" x2="974" y2="{y}" stroke="{RULE}" stroke-width="1"/>')
add(f'<text x="46" y="{y+22}" font-size="13" fill="{MUTE}" letter-spacing="1.4">'
    f'2 — WHAT THE TWO SIDES OF THAT COMPARISON ARE MADE OF</text>')
y += 44
for label, d in (("recitals", REC), ("articles", ART)):
    tot = d["modal_occurrences"]
    add(f'<text x="46" y="{y+30}" font-size="17" fill="{INK}">{label}</text>')
    x = BARX
    for modal in ("shall", "should", "must"):
        n = d["per_modal"][modal]["total"]
        w = BARW * n / tot
        col = FILL if modal == "shall" else (MUTE if modal == "should" else RULE)
        add(f'<rect x="{x:.1f}" y="{y+12}" width="{max(w,0.6):.2f}" height="26" fill="{col}"/>')
        if w > 90:
            add(f'<text x="{x + w/2:.1f}" y="{y+31}" font-size="14" fill="{PAPER}" '
                f'text-anchor="middle">{modal}  {n/tot*100:.1f}%</text>')
        x += w
    y += 62

add(f'<text x="{BARX}" y="{y+8}" font-size="13.5" fill="{MUTE}">'
    f'The two halves share almost no modal. <tspan fill="{INK}">“recitals vs articles” and '
    f'“should vs shall” are one contrast,</tspan></text>')
add(f'<text x="{BARX}" y="{y+28}" font-size="13.5" fill="{MUTE}">measured once and reported twice.'
    f'</text>')

# ------------------------------------------------------------------ panel 3: within-modal
y += 62
add(f'<line x1="46" y1="{y}" x2="974" y2="{y}" stroke="{RULE}" stroke-width="1"/>')
add(f'<text x="46" y="{y+22}" font-size="13" fill="{MUTE}" letter-spacing="1.4">'
    f'3 — AND INSIDE EACH MODAL, WHERE THERE ARE OBSERVATIONS AT ALL, IT RUNS THE OTHER WAY</text>')
y += 52

CX, CW = 300, 250
for modal in ("shall", "should"):
    add(f'<text x="46" y="{y+34}" font-size="17" font-style="italic" fill="{INK}">{modal}</text>')
    for j, (part, d) in enumerate((("recitals", REC), ("articles", ART))):
        pm = d["per_modal"][modal]
        x = CX + j * (CW + 130)
        rate = pm["rate"] or 0.0
        add(f'<text x="{x}" y="{y+16}" font-size="12" fill="{MUTE}">in the {part}, '
            f'n = {pm["total"]:,}</text>')
        add(f'<rect x="{x}" y="{y+24}" width="{CW}" height="22" fill="{PALE}"/>')
        add(f'<rect x="{x}" y="{y+24}" width="{rate*CW/0.60:.1f}" height="22" fill="{FILL}"/>')
        add(f'<text x="{x + rate*CW/0.60 + 10:.1f}" y="{y+40}" font-size="14" fill="{INK}">'
            f'{rate*100:.1f}%</text>')
    y += 74

add(f'<text x="46" y="{y+6}" font-size="13.5" fill="{MUTE}">'
    f'Both within-modal comparisons rest on tens of observations on one side and thousands on the '
    f'other, so neither settles anything either.</text>')
add(f'<text x="46" y="{y+26}" font-size="13.5" fill="{INK}">'
    f'The corpus cannot separate the two contrasts. The perfect score is a property of the corpus, '
    f'not of the drafting.</text>')

add(f'<line x1="46" y1="{H-52}" x2="974" y2="{H-52}" stroke="{RULE}" stroke-width="1"/>')
add(f'<text x="46" y="{H-30}" font-size="11.5" fill="{MUTE}">'
    f'Ulysses · Session 84 · 2026-09-08 · No One to Bear It · counts from results.json; '
    f'corpus of 63 acts committed 2026-09-06 with per-source SHA-256</text>')

add("</svg>")
(HERE / "figure.svg").write_text("\n".join(S), encoding="utf-8")
print("figure.svg written, %d bytes" % (HERE / "figure.svg").stat().st_size)
