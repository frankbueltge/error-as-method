#!/usr/bin/env python3
"""figure.svg -- Session 88, 2026-09-12.  Static SVG, no script, no external load.

Session 87 drew a sieve, because its finding was a subtraction.  Tonight's finding is not a
quantity but a **function**, so tonight's figure is a curve: the share of this corpus's agentless
obligations whose reader has met a party term, plotted against how far back the reader is allowed
to look.  The two hand-read points sit on it, below it, where they belong -- a party term in the
window is a ceiling on naming, never naming itself.  The dashed rule is the threshold this night
pre-registered, drawn where it actually stands: to the right of the window the same night fixed.

The x-axis is drawn at even spacing over an uneven scale (0, 1, 2, 3, 5, 8, 13, 20, 35, 50, 100,
200).  That is a distortion and it is labelled as one under the axis, because the alternative --
a linear axis -- would put ten of the twelve readings in the first centimetre.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BG, INK, GREY, RULE, FILL, DARK = "#faf7f1", "#1c1a17", "#6d685f", "#c9c2b6", "#e4ded2", "#8a8377"
FONT = "Iowan Old Style, Palatino Linotype, Palatino, Charter, Georgia, serif"

W = 1020
X0, X1 = 78, 946
STEPS = [0, 1, 2, 3, 5, 8, 13, 20, 35, 50, 100, 200]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def txt(x, y, s, size=14.5, fill=None, extra=""):
    return '<text x="%s" y="%s" font-size="%s" fill="%s"%s>%s</text>' % (
        x, y, size, fill or INK, (" " + extra) if extra else "", s)


def main():
    res = json.load(open(HERE / "results.json"))
    pop = json.load(open(HERE / "population-curve.json"))

    n_pop = pop["population"]
    pop_curve = [pop["curve"][str(w)] / n_pop for w in STEPS]
    samp = res["mechanical_ceiling"]["windows"]
    samp_curve = [samp[str(w)]["windows_containing_a_party_term"] / 60.0 for w in STEPS]

    named2 = len(res["named_stage2"])          # 11
    named1 = len(res["named_stage1"])          # 2
    present5 = samp["5"]["windows_containing_a_party_term"]   # 18

    o = []
    y = 58
    o.append(txt(X0, y, "Adjacent Text", 31))
    y += 36
    o.append(txt(X0, y, "&#8212; how far a reader goes before a norm has somebody to bear it", 31))
    y += 36
    for line in [
        "Requirements engineering reports that passive voice in requirements is mostly "
        "unproblematic because <tspan font-style=\"italic\">adjacent text often compensates</tspan>",
        "for the omitted agent (Krisch &amp; Houdek 2015, as reported by Frattini et al. 2024 &#8212; "
        "the paper itself is behind a paywall and unread here).",
        "This is that claim asked how far <tspan font-style=\"italic\">adjacent</tspan> reaches, over "
        "1,190 agentless obligations in 22 WHATWG living standards.",
    ]:
        o.append(txt(X0, y, line, 14.5, GREY))
        y += 20
    y += 8
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>' % (X0, y, X1, y, RULE))

    # ------------------------------------------------------------------ panel 1: the curve
    y += 34
    o.append(txt(X0, y, "1 &#8212; A PARTY TERM IS IN REACH  (share of obligations, by how many "
                        "blocks back the reader may look)", 13, GREY, 'letter-spacing="1.3"'))
    top, bot = y + 26, y + 316
    span = X1 - X0
    dx = span / (len(STEPS) - 1.0)

    def px(i):
        return X0 + i * dx

    def py(v):
        return bot - v * (bot - top)

    for frac, lab in ((0, "0"), (0.25, "25%"), (0.5, "50%"), (0.75, "75%"), (1.0, "100%")):
        o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="%s"/>'
                 % (X0, py(frac), X1, py(frac), RULE, "1" if frac in (0, 1.0) else "0.6"))
        o.append(txt(X0 - 10, py(frac) + 4, lab, 12, GREY, 'text-anchor="end"'))

    # the threshold this night pre-registered, drawn where it stands
    o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1.4" '
             'stroke-dasharray="7 5"/>' % (X0, py(0.5), X1, py(0.5), INK))

    # the window this night fixed
    i5 = STEPS.index(5)
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.1" '
             'stroke-dasharray="3 4"/>' % (px(i5), top - 8, px(i5), bot, DARK))

    o.append('<polyline fill="none" stroke="%s" stroke-width="2.2" points="%s"/>'
             % (INK, " ".join("%.1f,%.1f" % (px(i), py(v)) for i, v in enumerate(pop_curve))))
    o.append('<polyline fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="4 4" '
             'points="%s"/>' % (DARK, " ".join("%.1f,%.1f" % (px(i), py(v))
                                               for i, v in enumerate(samp_curve))))
    for i, v in enumerate(pop_curve):
        o.append('<circle cx="%.1f" cy="%.1f" r="3.2" fill="%s"/>' % (px(i), py(v), INK))

    # the two hand readings
    o.append('<rect x="%.1f" y="%.1f" width="9" height="9" fill="%s"/>'
             % (px(i5) - 4.5, py(named2 / 60.0) - 4.5, INK))
    o.append(txt(px(i5) + 12, py(named2 / 60.0) + 4,
                 "%d of 60 read by hand and judged to NAME this bearer" % named2, 13))
    o.append('<rect x="%.1f" y="%.1f" width="9" height="9" fill="%s"/>'
             % (X0 - 4.5, py(named1 / 60.0) - 4.5, INK))
    o.append(txt(X0 + 12, py(named1 / 60.0) - 10,
                 "%d of 60 named by the sentence alone" % named1, 13))

    for i, w in enumerate(STEPS):
        o.append(txt(px(i), bot + 20, str(w), 12.5, GREY, 'text-anchor="middle"'))
    o.append(txt(X0, bot + 42, "blocks of prose the reader is allowed to look back over "
                               "(uneven scale, drawn evenly)", 12.5, GREY))
    o.append(txt(X1, bot + 42, "solid: all 1,190 &#183; dashed: the 60 sampled", 12.5, GREY,
                 'text-anchor="end"'))
    o.append(txt(px(i5) + 6, top + 4, "the window fixed before any of this was computed", 12.5, DARK))
    o.append(txt(X1, py(0.5) - 8, "the threshold this night pre-registered for the same window",
                 12.5, INK, 'text-anchor="end"'))

    # ------------------------------------------------------- panel 2: presence is not naming
    y = bot + 76
    o.append(txt(X0, y, "2 &#8212; AND A PARTY TERM IN REACH IS NOT A BEARER NAMED  "
                        "(the 60, at the fixed window)", 13, GREY, 'letter-spacing="1.3"'))
    y += 26
    bars = [(60, "every sampled obligation", FILL),
            (present5, "a party term stands somewhere in the window", FILL),
            (named2, "it names the party that must act here", INK)]
    for v, lab, fill in bars:
        wpx = span * v / 60.0
        o.append('<rect x="%d" y="%d" width="%.2f" height="26" fill="%s" stroke="%s" '
                 'stroke-width="1.2"/>' % (X0, y, wpx, fill, INK))
        o.append(txt(X0 + wpx + 12, y + 18, "<tspan font-size=\"17\">%d</tspan>  %s" % (v, lab), 13.5))
        y += 34

    y += 16
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>' % (X0, y, X1, y, RULE))
    y += 26
    for line in [
        "Of the %s agentless obligations in this corpus, <tspan font-size=\"17\">%d</tspan> have no "
        "party term anywhere earlier in their own document. The other %s do &#8212; at a median"
        % ("{:,}".format(n_pop), pop["none_anywhere"], "{:,}".format(pop["whole_document"])),
        "of %s blocks and a mean of %s. So whether these norms have a bearer is not a fact about the "
        "sentences. It is a fact about where the reader is made to stop."
        % (pop["median_distance_where_present"], pop["mean_distance_where_present"]),
    ]:
        o.append(txt(X0, y, line, 14.5))
        y += 21

    y += 14
    o.append(txt(X0, y, "Ulysses &#183; Error as Method &#183; Session 88, 2026-09-12 &#183; "
                        "corpus and code in the work&#8217;s directory", 12.5, GREY))

    H = y + 26
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
           'font-family="%s" role="img" aria-label="The share of 1,190 agentless obligations in 22 '
           'web standards whose reader has met a term for a party, plotted against how far back the '
           'reader may look: 13.6 per cent in the paragraph itself, 40.9 per cent within five '
           'blocks, 99.6 per cent somewhere earlier in the document">\n'
           '<rect width="%d" height="%d" fill="%s"/>\n%s\n</svg>\n'
           % (W, H, W, H, FONT, W, H, BG, "\n".join(o)))
    (HERE / "figure.svg").write_text(svg)
    print("figure.svg  %d x %d" % (W, H))


if __name__ == "__main__":
    main()
