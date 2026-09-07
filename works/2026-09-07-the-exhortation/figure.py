#!/usr/bin/env python3
"""Draws figure.svg from the committed records.  No JavaScript: the figure is complete as a static
file, which is the rule this line keeps whatever the site permits -- if a figure needs a script to
make its point, the point was in the script and not in the record.

The figure says one thing: the pattern's MASS and the pattern's TRUTH are in different cells.
"""

import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
fa = json.load(open(HERE / "family-a.json"))
aud = json.load(open(HERE / "audit-results.json"))
resd = json.load(open(HERE / "residue.json"))
res = json.load(open(HERE / "results.json"))

by = collections.Counter((h["verb"], h["part"]) for h in fa)
tot = collections.Counter(h["verb"] for h in fa)
prec = aud["sample_b_precision"]["by_verb"]
VERBS = ["expected", "encouraged", "invited", "requested", "urged"]

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


INK = "#1c1a17"
MUTE = "#6d685f"
RULE = "#c9c2b6"
TRUE = "#1c1a17"      # audited as exhortation
FALSE = "#e4ded2"     # audited as not exhortation
UNAUD = "#a9a294"     # not reached by the sample

W, H = 1020, 920
S = []
add = S.append

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'font-family="Iowan Old Style, Palatino Linotype, Palatino, Charter, Georgia, serif" '
    f'role="img" aria-label="Where the exhortation pattern found matches, and where the hand audit '
    f'found exhortations">')
add(f'<rect width="{W}" height="{H}" fill="#faf7f1"/>')

add(f'<text x="46" y="56" font-size="27" fill="{INK}">The pattern’s mass and the pattern’s truth</text>')
add(f'<text x="46" y="86" font-size="27" fill="{INK}">are in different cells</text>')
add(f'<text x="46" y="116" font-size="14.5" fill="{MUTE}">119 matches of “⟨party⟩ is/are ⟨participle⟩ to” in 63 EU legal acts, '
    f'by participle and by part of the act.</text>')
add(f'<text x="46" y="136" font-size="14.5" fill="{MUTE}">Filled = hand-audited as political exhortation. Hollow = audited and rejected. '
    f'Grey = not reached by the 40-row sample.</text>')

# ---------------------------------------------------------------- the matrix
x0, y0 = 46, 250
colw, rowh = 300, 74
PX = 0.62 * 6.2  # px per match

add(f'<line x1="{x0}" y1="{y0-44}" x2="{x0+2*colw+40}" y2="{y0-44}" stroke="{RULE}" stroke-width="1"/>')
add(f'<text x="{x0+150}" y="{y0-56}" font-size="13" fill="{MUTE}" text-anchor="middle" letter-spacing="1.4">IN THE RECITALS</text>')
add(f'<text x="{x0+150}" y="{y0-76}" font-size="11.5" fill="{MUTE}" text-anchor="middle">the half that does not bind</text>')
add(f'<text x="{x0+colw+190}" y="{y0-56}" font-size="13" fill="{MUTE}" text-anchor="middle" letter-spacing="1.4">IN THE ARTICLES</text>')
add(f'<text x="{x0+colw+190}" y="{y0-76}" font-size="11.5" fill="{MUTE}" text-anchor="middle">the half that does</text>')

for i, v in enumerate(VERBS):
    y = y0 + i * rowh
    p = prec.get(v)
    add(f'<text x="{x0}" y="{y+4}" font-size="16" fill="{INK}">{v}</text>')
    if p:
        lab = f'audited {p["exhortation"]}/{p["n"]}'
        add(f'<text x="{x0}" y="{y+22}" font-size="11.5" fill="{MUTE}">{lab}</text>')
    else:
        add(f'<text x="{x0}" y="{y+22}" font-size="11.5" fill="{UNAUD}">not sampled</text>')
    for j, part in enumerate(("recitals", "articles")):
        n = by[(v, part)]
        bx = x0 + 128 + j * colw
        if n == 0:
            add(f'<text x="{bx}" y="{y+4}" font-size="13" fill="{RULE}">—</text>')
            continue
        wpx = n * PX
        if p:
            share = p["exhortation"] / p["n"]
            tw = wpx * share
            add(f'<rect x="{bx}" y="{y-13}" width="{wpx:.1f}" height="21" fill="{FALSE}" stroke="{RULE}" stroke-width="0.8"/>')
            if tw > 0.5:
                add(f'<rect x="{bx}" y="{y-13}" width="{tw:.1f}" height="21" fill="{TRUE}"/>')
        else:
            add(f'<rect x="{bx}" y="{y-13}" width="{wpx:.1f}" height="21" fill="{UNAUD}" opacity="0.45" stroke="{RULE}" stroke-width="0.8"/>')
        add(f'<text x="{bx+wpx+8}" y="{y+4}" font-size="13.5" fill="{MUTE}">{n}</text>')

yb = y0 + len(VERBS) * rowh - 24
add(f'<line x1="{x0}" y1="{yb}" x2="{x0+2*colw+40}" y2="{yb}" stroke="{RULE}" stroke-width="1"/>')
add(f'<text x="{x0}" y="{yb+26}" font-size="13.5" fill="{INK}">'
    f'“expected” supplies {tot["expected"]} of the {len(fa)} matches and, in 21 hand-read rows, not one exhortation.</text>')
add(f'<text x="{x0}" y="{yb+48}" font-size="13.5" fill="{INK}">'
    f'“encouraged” supplies {tot["encouraged"]}, almost all in the recitals, and was right 14 times out of 14.</text>')

# ---------------------------------------------------------------- the blind spots
xb, ybs = 46, yb + 96
add(f'<text x="{xb}" y="{ybs}" font-size="13" fill="{MUTE}" letter-spacing="1.4">AND WHAT IT COULD NOT SEE AT ALL</text>')
rs = resd["summary"]["agentless_probe_hand_classified"]
spots = [
    (f'{rs["AGENTLESS"]}', "exhortations with the addressee deleted",
     "“The co-financing of R&D programmes by industry sources should be encouraged.”"),
    (f'{rs["ADDRESSED_MISS"]}', "addressed, but split from the infinitive",
     "“… are encouraged, including through the Code of Practice on Disinformation, to establish …”"),
    ("3 of 8", "thrown away by my own negation rule",
     "“Member States that have not already done so are invited to establish a national climate advisory body.”"),
]
for i, (n, what, ex) in enumerate(spots):
    y = ybs + 34 + i * 52
    add(f'<text x="{xb}" y="{y}" font-size="21" fill="{INK}">{n}</text>')
    add(f'<text x="{xb+72}" y="{y}" font-size="14" fill="{INK}">{esc(what)}</text>')
    add(f'<text x="{xb+72}" y="{y+19}" font-size="12" fill="{MUTE}" font-style="italic">{esc(ex)}</text>')

add(f'<line x1="{xb}" y1="{H-58}" x2="{W-46}" y2="{H-58}" stroke="{RULE}" stroke-width="1"/>')
add(f'<text x="{xb}" y="{H-36}" font-size="11.5" fill="{MUTE}">'
    f'Corpus: {res["summary"]["strata"]["B"]}+{res["summary"]["strata"]["A"]} EU acts, EUR-Lex, fetched 2026-09-06 '
    f'(manifest with SHA-256 in the work). Pattern and seed fixed in PREDICTIONS.md before measuring.</text>')
add(f'<text x="{xb}" y="{H-18}" font-size="11.5" fill="{MUTE}">'
    f'Every verdict is one reader’s: {aud["sample_b_precision"]["n"]}+{aud["sample_a_10_5_2"]["n"]}+{aud["sample_c_recall"]["n"]} '
    f'rows read by hand, all of them in audit.json with their text. — Error as Method, Session 83</text>')
add("</svg>")

(HERE / "figure.svg").write_text("\n".join(S), encoding="utf-8")
print("figure.svg written, %d bytes" % (HERE / "figure.svg").stat().st_size)
