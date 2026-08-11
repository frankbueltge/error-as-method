#!/usr/bin/env python3
"""
figure.py -- draws figure.svg from results.json and data/inputs.json. Stdlib only, no randomness,
deterministic. Run governor.py first.

One picture, one reading: three lines that ought to point the same way and do not. The measurements
climb, the published norm descends in a straight line at exactly its legislated maximum speed, and
the rule's own unclamped output falls away between them.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1000, 720
INK, MUTE, PAPER = "#16181d", "#8e887a", "#fbfaf7"
RULE, MEAS, CALC = "#1c1f26", "#8a5a2b", "#a8a08e"
BAND = "#ece7da"

# plot frame
L, R, T, B = 92, 848, 168, 560
X0, X1 = 2013.0, 2030.0
Y0, Y1 = 18.0, -26.0          # micrograms, top to bottom


def x(year):
    return L + (year - X0) / (X1 - X0) * (R - L)


def y(ug):
    return T + (Y0 - ug) / (Y0 - Y1) * (B - T)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


s = []
def add(t):
    s.append(t)


def text(px, py, txt, size=11, fill=INK, anchor="start", style="normal", weight="normal"):
    add(f'<text x="{px:.1f}" y="{py:.1f}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}" font-style="{style}" font-weight="{weight}">{esc(txt)}</text>')


def main():
    res = json.load(open(os.path.join(HERE, "results.json")))
    data = json.load(open(os.path.join(HERE, "data", "inputs.json")))
    revs = res["sections"]["revisions"]

    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="Iowan Old Style, Palatino, Georgia, serif">')
    add(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')

    # ---- heading -----------------------------------------------------------------------------
    text(48, 54, "The Governor", 27)
    text(48, 78, "The published mass of the International Prototype of the Kilogram descends in a "
                 "straight line at exactly", 13, MUTE)
    text(48, 95, "the maximum speed its own rule permits — while every measurement that goes into "
                 "it is rising.", 13, MUTE)
    text(48, 116, "Micrograms relative to 1 kg. Every point is transcribed from a BIPM document; "
                  "every line is computed by governor.py.", 11, MUTE, style="italic")

    # ---- uncertainty band around the published series ----------------------------------------
    pub = [(2021.08, float(revs[0]["published"])), (2023.16, float(revs[1]["published"])),
           (2026.16, float(revs[2]["published"]))]
    u = 20.0
    top = " ".join(f"{x(px):.1f},{y(min(pv + u, Y0)):.1f}" for px, pv in pub)
    bot = " ".join(f"{x(px):.1f},{y(max(pv - u, Y1)):.1f}" for px, pv in reversed(pub))
    add(f'<polygon points="{top} {bot}" fill="{BAND}" opacity="0.55"/>')
    text(R, T + 16, "the shaded band is ± 20 µg, the assigned uncertainty:", 10, MUTE, anchor="end")
    text(R, T + 29, "unchanged since 2021, and wider than everything that happens inside it",
         10, MUTE, anchor="end")

    # ---- axes --------------------------------------------------------------------------------
    add(f'<line x1="{L}" y1="{y(0)}" x2="{R}" y2="{y(0)}" stroke="{MUTE}" stroke-width="1" '
        f'stroke-dasharray="1 3"/>')
    text(L - 10, y(0) + 4, "1 kg", 10, MUTE, anchor="end")
    for ug in (10, -10, -20):
        add(f'<line x1="{L}" y1="{y(ug)}" x2="{R}" y2="{y(ug)}" stroke="{BAND}" stroke-width="1"/>')
        text(L - 10, y(ug) + 4, f"{ug:+d}", 10, MUTE, anchor="end")
    text(L - 10, T - 14, "µg", 10, MUTE, anchor="end")
    add(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{MUTE}" stroke-width="1"/>')
    for yr in (2014, 2016, 2019, 2021, 2024, 2026, 2029):
        add(f'<line x1="{x(yr):.1f}" y1="{B}" x2="{x(yr):.1f}" y2="{B+5}" stroke="{MUTE}"/>')
        text(x(yr), B + 20, str(yr), 10, MUTE, anchor="middle")

    # ---- the measurements: KCRVs and the two legacy inputs ------------------------------------
    meas = [(2014.0, 0.0, "IPK, 2014", True), (2016.0, 12.4, "Pilot study, 2016", True),
            (2019.0, -18.8, "K8.2019", False), (2021.0, -15.2, "K8.2021", False),
            (2024.0, -10.7, "K8.2024", False)]
    kc = [(px, pv) for px, pv, _, legacy in meas if not legacy]
    add(f'<polyline points="{" ".join(f"{x(px):.1f},{y(pv):.1f}" for px, pv in kc)}" '
        f'fill="none" stroke="{MEAS}" stroke-width="2.2"/>')
    for px, pv, lab, legacy in meas:
        if legacy:
            add(f'<circle cx="{x(px):.1f}" cy="{y(pv):.1f}" r="4.5" fill="{PAPER}" '
                f'stroke="{MUTE}" stroke-width="1.6" stroke-dasharray="2 2"/>')
            text(x(px), y(pv) - 12, lab, 10, MUTE, anchor="middle")
        else:
            add(f'<circle cx="{x(px):.1f}" cy="{y(pv):.1f}" r="4.5" fill="{MEAS}"/>')
            text(x(px), y(pv) + 20, lab, 10, MEAS, anchor="middle")
    text(x(2017.4), y(-16.6), "the measurements — rising", 11, MEAS, anchor="start", weight="bold")

    # ---- the calculated (unclamped) series ----------------------------------------------------
    calc = [(pub[i][0], float(revs[i]["calculated"])) for i in range(3)]
    add(f'<polyline points="{" ".join(f"{x(px):.1f},{y(pv):.1f}" for px, pv in calc)}" '
        f'fill="none" stroke="{CALC}" stroke-width="2" stroke-dasharray="5 4"/>')
    for px, pv in calc:
        add(f'<circle cx="{x(px):.1f}" cy="{y(pv):.1f}" r="3.2" fill="{CALC}"/>')
    text(x(calc[-1][0]) + 9, y(calc[-1][1]) + 4, "−14.9  what the rule computed", 11, "#6f6858")

    # ---- the published series ------------------------------------------------------------------
    add(f'<polyline points="{" ".join(f"{x(px):.1f},{y(pv):.1f}" for px, pv in pub)}" '
        f'fill="none" stroke="{RULE}" stroke-width="3"/>')
    for px, pv in pub:
        add(f'<circle cx="{x(px):.1f}" cy="{y(pv):.1f}" r="5" fill="{RULE}"/>')
        text(x(px), y(pv) - 14, f"{pv:+.0f}", 12, RULE, anchor="middle", weight="bold")
    text(x(pub[-1][0]) + 9, y(pub[-1][1]) + 4, "−12  what was published", 11, RULE, weight="bold")

    # step labels on the published line
    for i in range(2):
        mx = (x(pub[i][0]) + x(pub[i + 1][0])) / 2
        my = (y(pub[i][1]) + y(pub[i + 1][1])) / 2
        text(mx - 4, my - 8, "−5 µg", 10, RULE, anchor="middle", style="italic")

    # ---- the clamp gap --------------------------------------------------------------------------
    gx = x(2026.16)
    add(f'<line x1="{gx:.1f}" y1="{y(pub[-1][1]):.1f}" x2="{gx:.1f}" y2="{y(calc[-1][1]):.1f}" '
        f'stroke="{RULE}" stroke-width="1.4" stroke-dasharray="2 2"/>')
    add(f'<rect x="{gx-3:.1f}" y="{y(pub[-1][1]):.1f}" width="6" '
        f'height="{y(calc[-1][1])-y(pub[-1][1]):.1f}" fill="{RULE}" opacity="0.14"/>')
    text(gx - 10, (y(pub[-1][1]) + y(calc[-1][1])) / 2 + 4, "2.9 µg withheld", 10, RULE,
         anchor="end", style="italic")

    # ---- the projection --------------------------------------------------------------------------
    add(f'<line x1="{x(2026.16):.1f}" y1="{B-6:.1f}" x2="{x(2029.2):.1f}" y2="{B-6:.1f}" '
        f'stroke="{MUTE}" stroke-width="1" stroke-dasharray="3 3"/>')
    text(x(2026.6), y(-21.3), "next: the window holds only measurements. The value", 10, MUTE)
    text(x(2026.6), y(-23.0), "leaving is −18.8, the lowest ever. The line turns up.", 10, MUTE)

    # ---- the rule, quoted ------------------------------------------------------------------------
    ry = 600
    add(f'<line x1="48" y1="{ry-24}" x2="{W-48}" y2="{ry-24}" stroke="{BAND}" stroke-width="1"/>')
    text(48, ry, "“…changes in the Consensus Value between consecutive Key Comparisons will be "
                 "reviewed and, if necessary, limited to ± 5 parts in 10⁹.”", 12, INK, style="italic")
    text(48, ry + 18, "CCM detailed note on the dissemination process after the redefinition of the "
                      "kilogram, approved 17 May 2019 — three days before the definition it governs "
                      "took effect.", 10, MUTE)
    text(48, ry + 40, "“A Governor is a part of a machine by means of which the velocity of the "
                      "machine is kept nearly uniform, notwithstanding variations in the "
                      "driving-power or the resistance.”", 11, MUTE, style="italic")
    text(48, ry + 56, "J. C. Maxwell, “On Governors”, Proceedings of the Royal Society 16 (1868), "
                      "p. 270.", 10, MUTE)

    add("</svg>")
    open(os.path.join(HERE, "figure.svg"), "w").write("\n".join(s) + "\n")
    print(f"figure.svg written, {sum(len(t) for t in s)} bytes of markup")


if __name__ == "__main__":
    main()
