"""figure.py -- one vocabulary, drawn twice.

The argument is that a published vocabulary of norms and the set of norms its publisher
can impose are different sets, and that nothing on the published face shows the
difference. So the figure draws the same 268 cells, in the same 268 positions, twice:

  ABOVE   as the manual publishes them -- Appendix A gives every code one row, and the
          262 rows are typographically identical. A reader cannot tell 0A000, which the
          system raises at 740 sites, from HV00R, which it raises nowhere.

  BELOW   the same cells, with the sites drawn. Ink is imposition.

and then, at the foot, the 43 classes at true width, so the concentration is a shape and
not a ratio.

Deterministic: same input, same file. No randomness, so no seed.

Usage:  python3 figure.py <results.json> <string-routes.json> <out.svg>
"""

import json
import math
import sys

W = 1000
PAD = 34
CELL = 26          # cell pitch in the grids
GAP = 3

INK = "#141210"
PAPER = "#f4f1ea"
RULE = "#b9b2a4"
FAINT = "#ded8cb"
HOT = "#8c2f18"     # siteless
WARM = "#c08a2e"    # imposed by a form the first rule did not model


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def main(results_path, strings_path, out):
    res = json.load(open(results_path, encoding="utf-8"))
    st = json.load(open(strings_path, encoding="utf-8"))
    rescued = {r["sqlstate"] for r in st["P1_correction"]["rescued"]}

    rows = sorted(res["rows"], key=lambda r: (r["klass"], r["sqlstate"]))
    n = len(rows)
    cols = (W - 2 * PAD) // CELL
    grid_rows = math.ceil(n / cols)

    named_not_raised = {r["macro"] for r in rows
                        if r["sites_b"] > 0 and r["sites_a"] == 0}

    def state(r):
        if r["sqlstate"] in rescued:
            return "string"
        if r["macro"] in named_not_raised:
            return "other-form"
        if r["sites_a"] > 0:
            return "raised"
        return "siteless"

    states = [state(r) for r in rows]
    n_siteless = sum(1 for s in states if s == "siteless")
    max_sites = max(r["sites_a"] for r in rows)

    grid_h = grid_rows * CELL
    y_a = 150
    y_b = y_a + grid_h + 96
    y_c = y_b + grid_h + 104
    class_h = 78
    H = y_c + class_h + 116

    o = []
    a = o.append
    a('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
      'viewBox="0 0 %d %d" font-family="ui-monospace, DejaVu Sans Mono, Menlo, '
      'Consolas, monospace">' % (W, H, W, H))
    a('<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPER))

    a('<text x="%d" y="42" font-size="20" fill="%s" letter-spacing="0.04em">'
      'ONE VOCABULARY, DRAWN TWICE</text>' % (PAD, INK))
    a('<text x="%d" y="64" font-size="12.5" fill="%s">PostgreSQL 18.6 &#183; '
      '%d SQLSTATE codes in %d classes &#183; src/backend/utils/errcodes.txt'
      '</text>' % (PAD, INK, n, res["n_classes"]))
    a('<text x="%d" y="82" font-size="12.5" fill="%s">the same %d cells in the same %d '
      'positions in both grids, ordered by class then code</text>'
      % (PAD, INK, n, n))

    def grid(y0, mode, label, sub):
        a('<text x="%d" y="%d" font-size="13" fill="%s" letter-spacing="0.10em">%s</text>'
          % (PAD, y0 - 30, INK, esc(label)))
        a('<text x="%d" y="%d" font-size="11.5" fill="%s">%s</text>'
          % (PAD, y0 - 13, INK, esc(sub)))
        for i, r in enumerate(rows):
            cx = PAD + (i % cols) * CELL
            cy = y0 + (i // cols) * CELL
            s = CELL - GAP
            if mode == "published":
                # every code is one identical row in Appendix A -- unless it has no
                # condition name at all, in which case it is not in Appendix A
                if r["condition"]:
                    a('<rect x="%d" y="%d" width="%d" height="%d" fill="none" '
                      'stroke="%s" stroke-width="1"/>' % (cx, cy, s, s, RULE))
                else:
                    a('<rect x="%d" y="%d" width="%d" height="%d" fill="none" '
                      'stroke="%s" stroke-width="1" stroke-dasharray="2 2"/>'
                      % (cx, cy, s, s, FAINT))
            else:
                stt = states[i]
                if stt == "siteless":
                    a('<rect x="%d" y="%d" width="%d" height="%d" fill="none" '
                      'stroke="%s" stroke-width="1.6"/>' % (cx, cy, s, s, HOT))
                    a('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" '
                      'stroke-width="1.6"/>' % (cx, cy + s, cx + s, cy, HOT))
                elif stt in ("other-form", "string"):
                    a('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" '
                      'fill-opacity="0.30" stroke="%s" stroke-width="1.4"/>'
                      % (cx, cy, s, s, WARM, WARM))
                else:
                    # ink proportional to log(sites), so 740 and 1 are both legible
                    f = math.log1p(r["sites_a"]) / math.log1p(max_sites)
                    a('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" '
                      'fill-opacity="%.3f" stroke="%s" stroke-width="0.8"/>'
                      % (cx, cy, s, s, INK, 0.10 + 0.85 * f, INK))

    grid(y_a, "published",
         "AS PUBLISHED",
         "Appendix A of the manual gives each code one row: SQLSTATE, condition name. "
         "262 identical rows. (6 codes carry no condition name and are not in it -- "
         "dashed.)")

    grid(y_b, "sites",
         "AS IMPOSABLE",
         "ink = log of the number of errcode( ) sites, 1 to %d \u00b7 amber = imposed by a "
         "form the first rule did not model \u00b7 struck = no site anywhere, %d of %d"
         % (max_sites, n_siteless, n))

    # --- classes at true width ---
    a('<text x="%d" y="%d" font-size="13" fill="%s" letter-spacing="0.10em">'
      'THE 43 CLASSES AT TRUE WIDTH</text>' % (PAD, y_c - 30, INK))
    a('<text x="%d" y="%d" font-size="11.5" fill="%s">each class as wide as it is large; '
      'the struck part is the codes with no site</text>' % (PAD, y_c - 13, INK))

    klasses = []
    for r in rows:
        if not klasses or klasses[-1][0] != r["klass"]:
            klasses.append([r["klass"], 0, 0])
        klasses[-1][1] += 1
        if state(r) == "siteless":
            klasses[-1][2] += 1

    total = sum(k[1] for k in klasses)
    x = PAD
    avail = W - 2 * PAD
    for k, tot, dead in klasses:
        w = avail * tot / total
        a('<rect x="%.2f" y="%d" width="%.2f" height="%d" fill="none" stroke="%s" '
          'stroke-width="1"/>' % (x, y_c, w, class_h, RULE))
        if dead:
            hh = class_h * dead / tot
            a('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s" '
              'fill-opacity="0.14" stroke="%s" stroke-width="1.2"/>'
              % (x, y_c + class_h - hh, w, hh, HOT, HOT))
        if w > 15:
            a('<text x="%.2f" y="%d" font-size="9.5" fill="%s" text-anchor="middle">'
              '%s</text>' % (x + w / 2, y_c + class_h + 14, INK, k))
        if w > 26 and dead:
            a('<text x="%.2f" y="%d" font-size="9.5" fill="%s" text-anchor="middle">'
              '%d</text>' % (x + w / 2, y_c + class_h + 26, HOT, dead))
        x += w

    a('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
      % (PAD, H - 80, W - PAD, H - 80, RULE))
    a('<text x="%d" y="%d" font-size="11.5" fill="%s">'
      '73 of 268 codes have no imposition site anywhere in the tree that publishes them. '
      'All 73 stand in Appendix A of the manual.</text>' % (PAD, H - 60, INK))
    a('<text x="%d" y="%d" font-size="11.5" fill="%s">'
      '21 are Class HV, the SQL/MED foreign-data-wrapper class, whose own generic code '
      'HV000 is one of them. Three classes are wholly siteless: 03, 0B, 0F.</text>'
      % (PAD, H - 43, INK))
    a('<text x="%d" y="%d" font-size="11" fill="%s">Session 77 \u00b7 2026-09-01 \u00b7 '
      'Error as Method \u00b7 postgresql-18.6.tar.bz2, sha256 555610c2\u2026 \u00b7 '
      'deterministic, no seed</text>' % (PAD, H - 22, INK))
    a('</svg>')

    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(o))
    print("%s -- %d cells, %d siteless, max sites %d, %d classes"
          % (out, n, n_siteless, max_sites, len(klasses)))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
