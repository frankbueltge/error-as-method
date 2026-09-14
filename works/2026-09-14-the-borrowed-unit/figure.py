#!/usr/bin/env python3
"""figure.py -- the night in one image: the same three corpora, two units, two different worlds.

Left panel: how far back a reader must look, counted in BLOCKS -- the unit S88.REACH fixed its test
in, and the unit one of the three traditions invented.  Right panel: the identical measurement
counted in WORDS.  The bracket on each panel is the spread at the window the predictions were scored
at: 54.74 points in blocks at window 0, 7.70 points in words at window 36.

Every number is read out of results.json.  Nothing is drawn that is not in that file.

Run after reach.py.  Writes figure.svg.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

W, H = 1020, 548
PAD_L, PAD_R, PAD_T, PAD_B = 62, 22, 108, 96
GAP = 58
PW = (W - PAD_L - PAD_R - GAP) / 2
PH = H - PAD_T - PAD_B

INK = "#22201c"
GRID = "#d8d2c6"
PAPER = "#f7f5f0"
COLOUR = {"whatwg": "#1d3557", "eu": "#a2391c", "rfc": "#2a6b5f"}
LABEL = {"whatwg": "22 WHATWG living standards", "eu": "63 EU acts, articles",
         "rfc": "63 RFCs, capitals"}
SERIF = "Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif"
MONO = "SFMono-Regular,Menlo,DejaVu Sans Mono,Consolas,monospace"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def panel(x0, res, unit, windows, scored_at, title, sub):
    """One panel. Positions are ranks: the windows are not evenly spaced and are not drawn as if."""
    out = []
    xs = list(windows) + ["doc"]
    n = len(xs)

    def px(i):
        return x0 + (PW * i / (n - 1))

    def py(pct):
        return PAD_T + PH - PH * pct / 100.0

    out.append('<text x="%.1f" y="%.1f" class="ttl">%s</text>' % (x0, PAD_T - 44, esc(title)))
    out.append('<text x="%.1f" y="%.1f" class="sub">%s</text>' % (x0, PAD_T - 25, esc(sub)))

    for v in (0, 25, 50, 75, 100):
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="grid"/>'
                   % (x0, py(v), x0 + PW, py(v)))
        out.append('<text x="%.1f" y="%.1f" class="ax ar">%d</text>' % (x0 - 8, py(v) + 4, v))

    si = list(windows).index(scored_at)
    out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="mark"/>'
               % (px(si), PAD_T - 8, px(si), PAD_T + PH))

    vals = {}
    for name in ("whatwg", "eu", "rfc"):
        c = res["corpora"][name]["row"][unit]
        pts = [(px(i), py(c["pct"][str(w)])) for i, w in enumerate(windows)]
        pts.append((px(n - 1), py(c["whole_document_pct"])))
        out.append('<polyline points="%s" class="ln" stroke="%s"/>'
                   % (" ".join("%.1f,%.1f" % p for p in pts), COLOUR[name]))
        for p in pts:
            out.append('<circle cx="%.1f" cy="%.1f" r="2.6" fill="%s"/>' % (p[0], p[1], COLOUR[name]))
        vals[name] = c["pct"][str(scored_at)]

    hi, lo = max(vals.values()), min(vals.values())
    bx = px(si) + 13
    out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="brk"/>'
               % (bx, py(hi), bx, py(lo)))
    for v in (hi, lo):
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="brk"/>'
                   % (bx - 4, py(v), bx + 4, py(v)))
    # a short bracket has no clear room beside its own arms -- the curves are right there --
    # so its label drops below it, into the empty quarter of the panel.
    span = py(lo) - py(hi)
    tx, ty = (bx + 14, (py(hi) + py(lo)) / 2 + 4) if span >= 34 else (bx - 4, py(lo) + 21)
    out.append('<text x="%.1f" y="%.1f" class="brt">%.1f points</text>' % (tx, ty, hi - lo))

    for i, w in enumerate(xs):
        lab = "doc" if w == "doc" else str(w)
        out.append('<text x="%.1f" y="%.1f" class="ax ac">%s</text>' % (px(i), PAD_T + PH + 18, lab))
    return out, px, py


def main():
    res = json.load(open(HERE / "results.json"))
    s = []
    s.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="100%%" '
             'role="img" aria-label="The same measurement in two units: a 54.7-point difference '
             'between three drafting traditions falls to 7.7 points when the unit changes from '
             'blocks to words.">' % (W, H))
    s.append("""<style>
 .bg{fill:%s}
 .grid{stroke:%s;stroke-width:1}
 .mark{stroke:#b9b2a3;stroke-width:1;stroke-dasharray:2 3}
 .ln{fill:none;stroke-width:2.1;stroke-linejoin:round}
 .brk{stroke:%s;stroke-width:1.2}
 .brt{font:600 12px %s;fill:%s}
 .ax{font:11px %s;fill:#6b655a}
 .ac{text-anchor:middle} .ar{text-anchor:end}
 .ttl{font:600 15px %s;fill:%s}
 .sub{font:12.5px %s;fill:#6b655a}
 .hd{font:600 17px %s;fill:%s}
 .hs{font:13px %s;fill:#55503f}
 .lg{font:12.5px %s;fill:%s}
 .ft{font:11px %s;fill:#6b655a}
</style>""" % (PAPER, GRID, INK, MONO, INK, MONO, SERIF, INK, SERIF, SERIF, INK, SERIF,
               SERIF, INK, MONO))
    s.append('<rect class="bg" x="0" y="0" width="%d" height="%d"/>' % (W, H))
    s.append('<text x="%d" y="26" class="hd">A party term in reach, counted two ways</text>' % PAD_L)
    s.append('<text x="%d" y="46" class="hs">the same obligations, the same terms, the same scan '
             '&#8212; only the unit of distance differs</text>' % PAD_L)

    a, _, _ = panel(PAD_L, res, "blocks", (0, 1, 2, 3, 5, 8, 13, 20, 35, 50, 100, 200), 0,
                    "in blocks", "the unit S88.REACH fixed — scored at window 0")
    s += a
    b, _, _ = panel(PAD_L + PW + GAP, res, "words",
                    (0, 5, 10, 25, 36, 50, 100, 200, 400, 800, 1600, 3200, 6400), 36,
                    "in words", "one WHATWG paragraph's worth — scored at 36")
    s += b

    y = H - 52
    x = PAD_L
    for name in ("whatwg", "eu", "rfc"):
        s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="ln" stroke="%s"/>'
                 % (x, y - 4, x + 22, y - 4, COLOUR[name]))
        s.append('<text x="%.1f" y="%.1f" class="lg">%s</text>' % (x + 29, y, esc(LABEL[name])))
        x += 31 + 7.0 * len(LABEL[name]) + 22
    s.append('<text x="%d" y="%d" class="ax">y: %% of binding agentless obligations with a party '
             'term within reach &#183; x: how far back the reader may look</text>' % (PAD_L, H - 28))
    s.append('<text x="%d" y="%d" class="ax">windows are ranks, not to scale &#183; a term in reach '
             'is a ceiling on a bearer actually named, never naming itself</text>' % (PAD_L, H - 12))
    s.append("</svg>")
    (HERE / "figure.svg").write_text("\n".join(s) + "\n")
    print("figure.svg written, %d bytes" % (HERE / "figure.svg").stat().st_size)


if __name__ == "__main__":
    main()
