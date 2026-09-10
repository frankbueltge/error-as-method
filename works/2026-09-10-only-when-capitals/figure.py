#!/usr/bin/env python3
"""figure.svg -- Session 86, 2026-09-10.  Static SVG, no script, no external load.

The figure IS the decomposition.  Session 84's measure is a product of two probabilities:

    bearer-deletion rate  =  P(modal is followed by "be ___")  x  P(no "by" | it is)

so it is an AREA.  Each cell is drawn as a rectangle in a unit square: width is the first factor,
height is the second, and the shaded area is the rate that both nights reported.  The dashed line
is the corpus-wide value of the second factor.  Every rectangle in a corpus reaches almost exactly
that line -- which is the whole finding: the heights do not move, so the areas are the widths.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BG, INK, GREY, RULE, FILL = "#faf7f1", "#1c1a17", "#6d685f", "#c9c2b6", "#e4ded2"
FONT = "Iowan Old Style, Palatino Linotype, Palatino, Charter, Georgia, serif"

W = 1020
S = 172          # side of a unit square
GAP = 66
X0 = 66


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def square(x, y, c, const, label, sub):
    """One cell: unit square, inscribed area rectangle, dashed constant line."""
    w = c["b_form_share"] * S
    h = c["no_by_given_b_form"] * S
    o = []
    o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" '
             'stroke-width="1"/>' % (x, y, S, S, RULE))
    o.append('<rect x="%d" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>'
             % (x, y + S - h, w, h, FILL))
    o.append('<rect x="%d" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="%s" '
             'stroke-width="1.4"/>' % (x, y + S - h, w, h, INK))
    o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1" '
             'stroke-dasharray="3 3"/>' % (x, y + S - const * S, x + S, y + S - const * S, INK))
    o.append('<text x="%d" y="%d" font-size="15" fill="%s">%s</text>'
             % (x, y - 26, INK, esc(label)))
    o.append('<text x="%d" y="%d" font-size="11" fill="%s">%s</text>'
             % (x, y - 10, GREY, esc(sub)))
    o.append('<text x="%d" y="%d" font-size="11.5" fill="%s">width %.1f%% · height %.1f%%</text>'
             % (x, y + S + 18, GREY, 100 * c["b_form_share"], 100 * c["no_by_given_b_form"]))
    o.append('<text x="%d" y="%d" font-size="15" fill="%s">area %.1f%%</text>'
             % (x, y + S + 38, INK, 100 * c["rate"]))
    return o


def main():
    d = json.load(open(HERE / "decomposition.json"))
    cells = {c["cell"]: c for c in d["rfc"] + d["eu"]}
    kr, ke = d["agent_test_constants"]["RFC"], d["agent_test_constants"]["EU"]

    rowA = [("RFC · must UPPER", "MUST", "normative, by the document's own key", kr),
            ("RFC · must LOWER", "must", "ordinary English, same documents", kr),
            ("RFC · should UPPER", "SHOULD", "normative", kr),
            ("RFC · should LOWER", "should", "ordinary English", kr)]
    rowB = [("EU · recitals", "recitals", "the half that does not bind", ke),
            ("EU · articles", "articles", "the half that does", ke),
            ("EU · should recitals", "should · recitals", "n = 6,889", ke),
            ("EU · shall articles", "shall · articles", "n = 15,474", ke)]

    o = []
    H = 1215
    o.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
             'font-family="%s" role="img" aria-label="The bearer-deletion rate drawn as an area: '
             'the agent test is a constant height and every difference two nights reported is a '
             'difference in width">' % (W, H, W, H, FONT))
    o.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG))

    o.append('<text x="66" y="60" font-size="27" fill="%s">The height never moves</text>' % INK)
    o.append('<text x="66" y="94" font-size="27" fill="%s">%s</text>'
             % (INK, esc("— so the area is the width")))
    o.append('<text x="66" y="128" font-size="14.5" fill="%s">Session 84 measured how often a '
             'norm’s bearer is deleted: the modal is followed by <tspan font-style="italic">'
             'be</tspan> and no <tspan font-style="italic">by</tspan>-phrase names</text>' % GREY)
    o.append('<text x="66" y="148" font-size="14.5" fill="%s">who must act. That rate is a product '
             'of two probabilities, so it is an area. Width: the modal is passive at all. '
             'Height: given</text>' % GREY)
    o.append('<text x="66" y="168" font-size="14.5" fill="%s">that it is, no agent is named. The '
             'dashed line is each corpus’s own average height.</text>' % GREY)
    o.append('<line x1="66" y1="196" x2="954" y2="196" stroke="%s" stroke-width="1"/>' % RULE)

    y = 288
    o.append('<text x="66" y="230" font-size="13" fill="%s" letter-spacing="1.4">1 &#8212; 63 RFCs, '
             '2,952 OCCURRENCES (SESSION 86). THE SAME WORD IS NORMATIVE IN CAPITALS AND NOT '
             'OTHERWISE</text>' % GREY)
    for i, (key, label, sub, const) in enumerate(rowA):
        o += square(X0 + i * (S + GAP), y, cells[key], const, label, sub)

    y2 = 640
    o.append('<text x="66" y="%d" font-size="13" fill="%s" letter-spacing="1.4">2 &#8212; 63 EU '
             'LEGAL ACTS, 22,554 OCCURRENCES (SESSION 84). THE SAME MEASURE, THE PUBLISHED '
             'RESULT</text>' % (y2 - 58, GREY))
    for i, (key, label, sub, const) in enumerate(rowB):
        o += square(X0 + i * (S + GAP), y2, cells[key], const, label, sub)

    y3 = 920
    o.append('<line x1="66" y1="%d" x2="954" y2="%d" stroke="%s" stroke-width="1"/>'
             % (y3, y3, RULE))
    o.append('<text x="66" y="%d" font-size="13" fill="%s" letter-spacing="1.4">3 &#8212; THROW THE '
             'AGENT TEST AWAY</text>' % (y3 + 30, GREY))
    o.append('<text x="66" y="%d" font-size="14.5" fill="%s">Replace every height with its '
             'corpus average — that is, stop looking for the agent at all — and the '
             'published rates come back:</text>' % (y3 + 60, INK))
    rows = [c for c in d["counterfactual"] if c["cell"] in
            ("EU · recitals", "EU · articles", "RFC · must UPPER", "RFC · should LOWER")]
    ty = y3 + 92
    for c in rows:
        o.append('<text x="86" y="%d" font-size="14" fill="%s">%s</text>'
                 % (ty, GREY, esc(c["cell"])))
        o.append('<text x="360" y="%d" font-size="14" fill="%s">reported %.2f%%</text>'
                 % (ty, INK, 100 * c["reported_rate"]))
        o.append('<text x="530" y="%d" font-size="14" fill="%s">rebuilt %.2f%%</text>'
                 % (ty, INK, 100 * c["rate_with_the_agent_test_replaced_by_its_corpus_average"]))
        o.append('<text x="700" y="%d" font-size="14" fill="%s">off by %.2f points</text>'
                 % (ty, GREY, c["difference_points"]))
        ty += 26
    o.append('<text x="66" y="%d" font-size="14.5" fill="%s">The instrument is named for the agent '
             'and does not depend on it. Across 25,506 occurrences, two drafting</text>'
             % (ty + 20, INK))
    o.append('<text x="66" y="%d" font-size="14.5" fill="%s">traditions and four registers, the '
             'chance that a passive norm names who must act is very nearly a constant.</text>'
             % (ty + 42, INK))
    o.append('<text x="66" y="%d" font-size="11.5" fill="%s">Sources: 63 RFCs carrying the RFC 8174 '
             'boilerplate, harvested 2026-09-10 (sources/MANIFEST.json); Session 84’s '
             'occurrences, works/2026-09-08-no-one-to-bear-it/.</text>' % (ty + 74, GREY))
    o.append('<text x="66" y="%d" font-size="11.5" fill="%s">Ulysses, Error as Method, Session 86. '
             'Panels 1 and 2 are pre-registered counts; panel 3 is post hoc and scores no '
             'prediction.</text>' % (ty + 92, GREY))
    o.append('</svg>')
    (HERE / "figure.svg").write_text("\n".join(o) + "\n")
    print("figure.svg written, %d bytes" % (HERE / "figure.svg").stat().st_size)


if __name__ == "__main__":
    main()
