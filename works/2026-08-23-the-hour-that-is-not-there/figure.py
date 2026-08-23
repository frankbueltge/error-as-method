#!/usr/bin/env python3
"""Draw figure.svg. Raw SVG, no libraries, deterministic.

Six panels: two rows (D0, each runtime's default rendering; D1, its explicit ISO-8601 form)
by three columns (the three zones, producer and parser in the same one). Each panel is a
5 x 4 grid, producers down, parsers across. A cell is filled in proportion to how many of the
212 instants came back as a different instant, and hatched where the parser refused outright.

The whole D1 row is blank. That is the figure's argument and it is not a decoration: over
30,528 cells, every producer, every parser, every combination of zones, the explicit form
never once loses an instant.

Underneath, one band of 212 ticks: PHP's default rendering read by Python, the same bytes in
all three zones, correct in one of them.
"""
import json
from collections import defaultdict
import compare

PRODUCERS = ["python", "node", "ruby", "php", "perl"]
PARSERS = ["python", "node", "ruby", "php"]

INK = "#1b1b1b"
PAPER = "#f4f1ea"
WRONG = "#8c2f1e"
FAINT = "#b9b2a4"
GOOD = "#5c6b52"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def main():
    m = json.load(open("matrix.json"))
    rows = compare.build(m)
    zones = m["zones"]
    n = len(m["instants"])

    # (family, zone, producer, parser) -> counts, same-zone cross-party cells only
    g = defaultdict(lambda: {"ok": 0, "silent": 0, "refused": 0})
    for r in rows:
        if not r["cross_party"] or not r["same_zone"]:
            continue
        g[(r["family"], r["producer_zone"], r["producer"], r["parser"])][r["outcome"]] += 1

    CW, CH = 30, 22                       # cell
    PW = CW * len(PARSERS) + 78           # panel width incl. row labels
    PH = CH * len(PRODUCERS) + 46
    GX, GY = 34, 56                       # gap between panels
    L, T = 58, 136
    W = max(L + 3 * PW + 2 * GX + 30, 880)
    H = T + 2 * PH + GY + 224

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="Iowan Old Style, Palatino, Georgia, serif">',
         f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
         '<defs><pattern id="ref" width="5" height="5" patternUnits="userSpaceOnUse" '
         f'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="5" '
         f'stroke="{FAINT}" stroke-width="1.6"/></pattern></defs>']

    o.append(f'<text x="{L}" y="42" font-size="21" fill="{INK}">The hour that is not there</text>')
    o.append(f'<text x="{L}" y="64" font-size="12.5" fill="{INK}" opacity="0.78">'
             f'Five runtimes render 212 instants and read each other back. Cell darkness = how '
             f'many of the 212 came back as a different instant.</text>')
    o.append(f'<text x="{L}" y="81" font-size="12.5" fill="{INK}" opacity="0.78">'
             f'Nothing differs between the three columns but the TZ environment variable. '
             f'Session 68 &#183; 2026-08-23</text>')

    for ri, (fam, famlab) in enumerate([("D0", "each runtime&#8217;s DEFAULT rendering"),
                                        ("D1", "its explicit ISO-8601 form")]):
        for ci, z in enumerate(zones):
            px = L + ci * (PW + GX)
            py = T + ri * (PH + GY)
            if ri == 0:
                o.append(f'<text x="{px + 78}" y="{py - 12}" font-size="12.5" fill="{INK}">'
                         f'TZ = {esc(z)}</text>')
            if ci == 0:
                o.append(f'<text x="{px}" y="{py - (34 if ri else 40)}" font-size="12.5" '
                         f'fill="{INK}" opacity="0.66" font-style="italic">{famlab}</text>')
                if ri == 1:
                    o.append(f'<text x="{px + 250}" y="{py - 34}" font-size="11" '
                             f'fill="{GOOD}">30,528 cells &#183; not one lost instant</text>')
            # parser labels
            for j, q in enumerate(PARSERS):
                o.append(f'<text x="{px + 78 + j * CW + CW / 2}" y="{py - 2}" font-size="9.5" '
                         f'text-anchor="middle" fill="{INK}" opacity="0.7">{q}</text>')
            for i, p in enumerate(PRODUCERS):
                cy = py + i * CH
                o.append(f'<text x="{px + 72}" y="{cy + CH / 2 + 3.4}" font-size="10" '
                         f'text-anchor="end" fill="{INK}" opacity="0.85">{p}</text>')
                for j, q in enumerate(PARSERS):
                    cx = px + 78 + j * CW
                    c = g[(fam, z, p, q)]
                    o.append(f'<rect x="{cx}" y="{cy}" width="{CW - 2}" height="{CH - 2}" '
                             f'fill="none" stroke="{FAINT}" stroke-width="0.6"/>')
                    if p == q:
                        o.append(f'<line x1="{cx}" y1="{cy + CH - 2}" x2="{cx + CW - 2}" '
                                 f'y2="{cy}" stroke="{FAINT}" stroke-width="0.6"/>')
                        continue
                    if c["refused"]:
                        o.append(f'<rect x="{cx}" y="{cy}" width="{CW - 2}" '
                                 f'height="{CH - 2}" fill="url(#ref)"/>')
                    elif c["silent"]:
                        a = 0.18 + 0.8 * (c["silent"] / n)
                        o.append(f'<rect x="{cx}" y="{cy}" width="{CW - 2}" height="{CH - 2}" '
                                 f'fill="{WRONG}" fill-opacity="{a:.3f}"/>')
                        o.append(f'<text x="{cx + CW / 2 - 1}" y="{cy + CH / 2 + 3.2}" '
                                 f'font-size="8.5" text-anchor="middle" fill="{PAPER}">'
                                 f'{c["silent"]}</text>')
                    else:
                        o.append(f'<circle cx="{cx + CW / 2 - 1}" cy="{cy + CH / 2 - 1}" r="1.5" '
                                 f'fill="{GOOD}" fill-opacity="0.55"/>')

    # ---- the band: php -> python, D0, the same bytes in all three zones
    by = T + 2 * PH + GY + 42
    o.append(f'<text x="{L}" y="{by - 26}" font-size="12.5" fill="{INK}">'
             f'One pair, one byte-identical string per instant, three zones: '
             f'php&#8217;s default read by python</text>')
    o.append(f'<text x="{L}" y="{by - 10}" font-size="11" fill="{INK}" opacity="0.7">'
             f'PHP renders in UTC under every TZ, because its documented precedence list does '
             f'not contain TZ. Python reads a naive string as local time, because it says so.'
             f'</text>')
    tw = (W - L - 40) / n
    for zi, z in enumerate(zones):
        yy = by + zi * 26
        o.append(f'<text x="{L - 6}" y="{yy + 9}" font-size="9" text-anchor="end" '
                 f'fill="{INK}" opacity="0.7">{esc(z.split("/")[-1])}</text>')
        cells = [r for r in rows
                 if r["family"] == "D0" and r["producer"] == "php" and r["parser"] == "python"
                 and r["producer_zone"] == z and r["parser_zone"] == z]
        cells.sort(key=lambda r: r["instant"])
        for r in cells:
            x = L + r["instant"] * tw
            col = GOOD if r["outcome"] == "ok" else WRONG
            op = 0.5 if r["outcome"] == "ok" else 0.85
            o.append(f'<rect x="{x:.2f}" y="{yy}" width="{max(tw - 0.5, 0.7):.2f}" height="13" '
                     f'fill="{col}" fill-opacity="{op}"/>')
    o.append(f'<text x="{L}" y="{by + 3 * 26 + 18}" font-size="11.5" fill="{INK}" opacity="0.8">'
             f'636 cells are correct in one zone and quietly wrong in another on a '
             f'byte-identical string. Not one convicts either party: both are</text>')
    o.append(f'<text x="{L}" y="{by + 3 * 26 + 35}" font-size="11.5" fill="{INK}" opacity="0.8">'
             f'doing exactly what they document. The difference is real; the error is wherever '
             f'an observer decides to stand.</text>')

    o.append('</svg>')
    open("figure.svg", "w").write("\n".join(o))
    print(f"figure.svg written ({sum(len(x) for x in o)} bytes)")


if __name__ == "__main__":
    main()
