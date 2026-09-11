#!/usr/bin/env python3
"""figure.svg -- Session 87, 2026-09-11.  Static SVG, no script, no external load.

Session 86 drew the rate as an area, because the rate is a product.  Tonight's figure is a
**sieve**, because tonight's finding is a subtraction: of 3,603 obligation modals in 22 standards,
1,344 are written as `must be ___`, 133 of those carry a `by`, and in **11** of them the `by` names
the party that must act.  The first panel draws that at one scale, so the last bar is the hairline
it actually is.  The second re-scales the 133 and shows what the other 122 turned out to be.  The
third puts the agent test beside the two corpora that came before, inside the band `S86.CONSTANT`
fixed the night before this one.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BG, INK, GREY, RULE, FILL, DARK = "#faf7f1", "#1c1a17", "#6d685f", "#c9c2b6", "#e4ded2", "#8a8377"
FONT = "Iowan Old Style, Palatino Linotype, Palatino, Charter, Georgia, serif"

W = 1020
X0, X1 = 66, 954
SPAN = X1 - X0


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def txt(x, y, s, size=14.5, fill=None, extra=""):
    return '<text x="%s" y="%s" font-size="%s" fill="%s"%s>%s</text>' % (
        x, y, size, fill or INK, (" " + extra) if extra else "", s)


def main():
    res = json.load(open(HERE / "results.json"))
    ag = json.load(open(HERE / "agentful.json"))
    w = res["whole_corpus"]
    prior = res["prior_corpora"]

    o = []
    y = 60
    o.append(txt(X0, y, "Eleven", 30))
    y += 36
    o.append(txt(X0, y, "&#8212; the sentences in which the agent test found the agent", 30))
    y += 34
    for line in [
        "Session 84 built an instrument for the missing bearer of a norm: a modal followed by "
        "<tspan font-style=\"italic\">be</tspan>, with no "
        "<tspan font-style=\"italic\">by</tspan>-phrase after it.",
        "Session 86 showed the second half of that rule barely varies, so the published rate was a "
        "passive-voice frequency. It could not check",
        "the other half: what the rule finds when a "
        "<tspan font-style=\"italic\">by</tspan> IS there. Its sample held none. "
        "This corpus holds 133, few enough to read every one.",
    ]:
        o.append(txt(X0, y, line, 14.5, GREY))
        y += 20
    y += 8
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
             % (X0, y, X1, y, RULE))
    y += 34

    # ------------------------------------------------------------------ panel 1: the sieve
    o.append(txt(X0, y, "1 &#8212; 22 WHATWG LIVING STANDARDS, DRAWN AT ONE SCALE", 13, GREY,
                 'letter-spacing="1.4"'))
    y += 30
    steps = [
        (w["occurrences"], "every <tspan font-style=\"italic\">shall</tspan> / "
                           "<tspan font-style=\"italic\">should</tspan> / "
                           "<tspan font-style=\"italic\">must</tspan>", "3,603"),
        (w["b_form"], "&#8230; followed by "
                      "<tspan font-style=\"italic\">be ___</tspan>", "1,344"),
        (w["agentful"], "&#8230; and carrying a <tspan font-style=\"italic\">by</tspan> "
                        "within 200 characters", "133"),
        (ag["verdicts"]["BEARER"],
         "&#8230; where that <tspan font-style=\"italic\">by</tspan> names the party that must act",
         "11"),
    ]
    top = w["occurrences"]
    for n, label, num in steps:
        bw = max(SPAN * n / top, 1.2)
        o.append('<rect x="%d" y="%d" width="%.2f" height="26" fill="%s" stroke="%s" '
                 'stroke-width="1.2"/>' % (X0, y, bw, FILL, INK))
        o.append(txt(X0 + max(bw, 3) + 10, y + 19, "<tspan font-size=\"17\">%s</tspan>  %s"
                     % (num, label), 13.5, INK))
        y += 40
    y += 4
    o.append(txt(X0, y, "The last bar is 0.31 % of the first. It is drawn to scale.", 13, GREY))
    y += 36

    # --------------------------------------------------------- panel 2: what the other 122 were
    o.append(txt(X0, y, "2 &#8212; THE 133, RE-SCALED: WHAT THE INSTRUMENT ACTUALLY FOUND",
                 13, GREY, 'letter-spacing="1.4"'))
    y += 30
    order = [
        ("NOT-AGENTIVE", "no agent phrase at all",
         "&#8220;followed by&#8221;, &#8220;separated by&#8221;, "
         "&#8220;surrounded by spaces&#8221;, &#8220;by default&#8221;"),
        ("AGENT-IS-ARTEFACT", "a grammatical agent that cannot be asked to act",
         "&#8220;must be supported by all objects implementing the MessagePort interface&#8221;"),
        ("OTHER-CLAUSE", "the <tspan font-style=\"italic\">by</tspan> belongs to a different "
                         "predicate",
         "&#8220;must be initially false, but which can get set to true "
         "<tspan font-style=\"italic\">by the algorithms</tspan>&#8221;"),
        ("AGENT-NOT-BEARER", "a party &#8212; but the one who may act, not the one bound",
         "&#8220;should be editable by the user&#8221; binds the user agent"),
        ("BEARER", "the party that must act", "&#8220;must not be used by authors&#8221;"),
    ]
    n133 = ag["n_agentful"]
    x = X0
    for key, _, _ in order:
        n = ag["verdicts"][key]
        bw = SPAN * n / n133
        fill = INK if key == "BEARER" else (FILL if key != "AGENT-IS-ARTEFACT" else "#d6cfc1")
        if key == "OTHER-CLAUSE":
            fill = "#ece7dc"
        if key == "AGENT-NOT-BEARER":
            fill = "#f2eee5"
        o.append('<rect x="%.2f" y="%d" width="%.2f" height="34" fill="%s" stroke="%s" '
                 'stroke-width="1"/>' % (x, y, bw, fill, INK))
        o.append(txt(x + bw / 2, y + 23, str(n), 15,
                     BG if key == "BEARER" else INK, 'text-anchor="middle"'))
        x += bw
    y += 56
    for key, gloss, example in order:
        n = ag["verdicts"][key]
        o.append('<rect x="%d" y="%d" width="10" height="10" fill="%s" stroke="%s" '
                 'stroke-width="1"/>'
                 % (X0, y - 9, INK if key == "BEARER" else FILL, INK))
        o.append(txt(X0 + 18, y, "<tspan font-size=\"13.5\">%s</tspan> &#183; %d &#183; %s"
                     % (key, n, gloss), 13.5, INK))
        y += 18
        o.append(txt(X0 + 18, y, example, 12.5, GREY))
        y += 24
    y += 10

    # --------------------------------------------------------------- panel 3: the three corpora
    o.append(txt(X0, y, "3 &#8212; THE AGENT TEST, THREE CORPORA, THREE DRAFTING TRADITIONS",
                 13, GREY, 'letter-spacing="1.4"'))
    y += 24
    o.append(txt(X0, y, "How often a <tspan font-style=\"italic\">must be ___</tspan> clause "
                        "carries no <tspan font-style=\"italic\">by</tspan>. "
                        "The shaded band is the range S86.CONSTANT fixed in advance.", 13, GREY))
    y += 26
    ph, plo, phi = 150, 0.70, 1.00
    o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" opacity="0.55"/>'
             % (X0, y + ph * (1 - (0.95 - plo) / (phi - plo)), SPAN,
                ph * (0.95 - 0.75) / (phi - plo), FILL))
    for v, lab in ((0.75, "0.75"), (0.95, "0.95")):
        yy = y + ph * (1 - (v - plo) / (phi - plo))
        o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1" '
                 'stroke-dasharray="3 3"/>' % (X0, yy, X1, yy, DARK))
        o.append(txt(X1 + 0, yy - 4, lab, 11.5, GREY, 'text-anchor="end"'))
    pts = [("EU law", prior["EU_all"]["agent_test"], "22,554 occurrences &#183; S84"),
           ("RFCs", prior["RFC_all"]["agent_test"], "2,952 &#183; S86"),
           ("WHATWG", w["agent_test"], "3,603 &#183; tonight")]
    step = SPAN / (len(pts) + 1)
    coords = []
    for i, (lab, v, sub) in enumerate(pts, 1):
        px = X0 + step * i
        py = y + ph * (1 - (v - plo) / (phi - plo))
        coords.append((px, py))
        o.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s"/>' % (px, py, INK))
        o.append(txt(px, py - 14, "%.4f" % v, 14, INK, 'text-anchor="middle"'))
        o.append(txt(px, y + ph + 22, lab, 14.5, INK, 'text-anchor="middle"'))
        o.append(txt(px, y + ph + 40, sub, 12, GREY, 'text-anchor="middle"'))
    o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.4"/>'
             % (" ".join("%.1f,%.1f" % c for c in coords), INK))
    y += ph + 72

    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
             % (X0, y, X1, y, RULE))
    y += 24
    o.append(txt(X0, y, "Sources: works/2026-09-11-eleven-sentences/ &#8212; results.json, "
                        "agentful.json, and the 133 sentences in full. Corpora: 22 WHATWG living "
                        "standards (CC BY 4.0),", 12, GREY))
    y += 17
    o.append(txt(X0, y, "harvested 2026-09-11; the EU and RFC figures are Sessions 84 and 86, "
                        "re-read from their committed results rather than remembered.", 12, GREY))
    y += 24

    H = y
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
           'font-family="%s" role="img" aria-label="Of 3,603 obligation modals in 22 web '
           'standards, the instrument built to find the missing bearer names the party that must '
           'act in eleven">\n' % (W, H, W, H, FONT))
    svg += '<rect width="%d" height="%d" fill="%s"/>\n' % (W, H, BG)
    svg += "\n".join(o) + "\n</svg>\n"
    (HERE / "figure.svg").write_text(svg)
    print("figure.svg written, %d x %d, %d bytes" % (W, H, len(svg)))


if __name__ == "__main__":
    main()
