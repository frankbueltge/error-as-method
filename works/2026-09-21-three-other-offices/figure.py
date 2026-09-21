#!/usr/bin/env python3
"""figure.py -- figure.svg, complete without a line of script.

Left panel: the four traditions on the axis S91.RULEBOUND's own account named -- how often a
tradition puts its declared party terms in subject position -- against what the rule returns.  The
band that would falsify the row is drawn as a stripe, because the row is a stripe.

Right panel: the same decision taken twelve times, once per corpus and declared vocabulary, so that
the two cells inside the stripe can be counted by eye.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R3B = "R3b_active_governor_own_block"
LOW, HIGH, UKV = 21.42, 41.42, 31.42

INK = "#1b1b1b"
MUTED = "#6f6f6f"
BAND = "#d8d2c4"
HIT = "#a33"

W, H = 1180, 620
L, T = 92, 74
PW, PH = 470, 430          # left panel plot box
RX = 700                   # right panel origin x


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    res = json.load(open(HERE / "results.json"))
    ins = json.load(open(HERE / "inspection.json"))
    adj = json.load(open(HERE / "adjudication.json"))

    pts = []
    for r in ins["rows"]:
        pts.append({"name": r["corpus"].replace(" (calibration)", ""),
                    "calib": "calibration" in r["corpus"],
                    "x": r["subjecthood_rate_pct"], "y": r["R3b_fire_pct_narrow"]})

    xlo, xhi = 10.0, 32.0
    ylo, yhi = 20.0, 72.0
    px = lambda v: L + PW * (v - xlo) / (xhi - xlo)
    py = lambda v: T + PH - PH * (v - ylo) / (yhi - ylo)

    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
         'font-family="Georgia, \'Times New Roman\', serif" fill="%s">' % (W, H, W, H, INK)]
    o.append('<rect width="%d" height="%d" fill="#faf8f4"/>' % (W, H))
    o.append('<text x="%d" y="34" font-size="20">A rule written for one drafting office, '
             'asked of four</text>' % L)
    o.append('<text x="%d" y="56" font-size="13" fill="%s">R3b -- does the party term standing '
             'nearest the obligation act in its own block? -- over every row in reach at word '
             'window 36, declared narrow vocabulary. Session 94, 2026-09-21.</text>' % (L, MUTED))

    # ---------------------------------------------------------------- left panel
    o.append('<rect x="%.1f" y="%.1f" width="%d" height="%.1f" fill="%s" fill-opacity="0.55"/>'
             % (L, py(HIGH), PW, py(LOW) - py(HIGH), BAND))
    o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1" '
             'stroke-dasharray="5 4"/>' % (L, py(UKV), L + PW, py(UKV), HIT))
    o.append('<text x="%d" y="%.1f" font-size="11" fill="%s" text-anchor="end">31.42 %% -- UK '
             'statute, the value the row fixed</text>' % (L + PW - 4, py(UKV) - 6, HIT))
    o.append('<text x="%d" y="%.1f" font-size="11" fill="%s" text-anchor="end">the band that '
             'falsifies S91.RULEBOUND</text>' % (L + PW - 4, py(LOW) - 7, MUTED))

    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (L, T + PH, L + PW, T + PH, INK))
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (L, T, L, T + PH, INK))
    for v in (20, 30, 40, 50, 60, 70):
        o.append('<text x="%d" y="%.1f" font-size="11" text-anchor="end" fill="%s">%d</text>'
                 % (L - 8, py(v) + 4, MUTED, v))
        o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="0.5"/>'
                 % (L - 4, py(v), L, py(v), MUTED))
    for v in (10, 15, 20, 25, 30):
        o.append('<text x="%.1f" y="%d" font-size="11" text-anchor="middle" fill="%s">%d</text>'
                 % (px(v), T + PH + 20, MUTED, v))
    o.append('<text x="%.1f" y="%d" font-size="12" text-anchor="middle">subjecthood of the declared '
             'party terms, %% </text>' % (L + PW / 2, T + PH + 46))
    o.append('<text transform="translate(%d,%.1f) rotate(-90)" font-size="12" '
             'text-anchor="middle">R3b fire rate, %%</text>' % (L - 46, T + PH / 2))

    order = sorted(pts, key=lambda p: p["x"])
    o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="0.8" '
             'stroke-dasharray="3 5"/>' % (" ".join("%.1f,%.1f" % (px(p["x"]), py(p["y"]))
                                                    for p in order), MUTED))
    for p in pts:
        x, y = px(p["x"]), py(p["y"])
        hit = LOW <= p["y"] <= HIGH
        if p["calib"]:
            o.append('<circle cx="%.1f" cy="%.1f" r="6.5" fill="none" stroke="%s" '
                     'stroke-width="1.6"/>' % (x, y, INK))
        else:
            o.append('<circle cx="%.1f" cy="%.1f" r="6.5" fill="%s"/>'
                     % (x, y, HIT if hit else INK))
        dy = 24 if p["name"] == "UK Acts" else -14
        o.append('<text x="%.1f" y="%.1f" font-size="12.5" text-anchor="middle">%s</text>'
                 % (x, y + dy, esc(p["name"])))
        o.append('<text x="%.1f" y="%.1f" font-size="11" text-anchor="middle" fill="%s">%.2f</text>'
                 % (x, y + dy + (15 if dy > 0 else -13), MUTED, p["y"]))
    o.append('<text x="%d" y="%d" font-size="11.5" fill="%s">The ordering is the finding: of three '
             'candidate explanations measured, only subjecthood</text>' % (L, T + PH + 72, MUTED))
    o.append('<text x="%d" y="%d" font-size="11.5" fill="%s">orders the four traditions as the rule '
             'does. Block length and term density do not. Four points.</text>'
             % (L, T + PH + 90, MUTED))

    # ---------------------------------------------------------------- right panel
    cells = []
    for name in res["corpora"]:
        row = [res["corpora"][name]["lists"][l]["by_rule"][R3B]["fire_pct"]
               for l in ("base", "narrow", "wide")]
        cells.append((name, row))
    uk = res["calibration_UK_statute"]["lists"]
    cells.append(("UK Acts (calibration)",
                  [uk[l]["by_rule"][R3B]["fire_pct"] for l in ("base", "narrow", "wide")]))

    o.append('<text x="%d" y="%d" font-size="14">The same decision, twelve times</text>' % (RX, T - 12))
    o.append('<text x="%d" y="%d" font-size="11.5" fill="%s">R3b %%, by corpus and by the '
             'vocabulary its checker declared</text>' % (RX, T + 6, MUTED))
    cw, ch = 118, 60
    for j, l in enumerate(("base", "narrow", "wide")):
        o.append('<text x="%.1f" y="%d" font-size="12" text-anchor="middle" fill="%s">%s</text>'
                 % (RX + 128 + j * cw + cw / 2, T + 34, MUTED, l))
    for i, (name, row) in enumerate(cells):
        yy = T + 46 + i * ch
        o.append('<text x="%d" y="%.1f" font-size="12.5">%s</text>'
                 % (RX, yy + ch / 2 + 4, esc(name.replace(" (calibration)", ""))))
        for j, v in enumerate(row):
            xx = RX + 128 + j * cw
            hit = LOW <= v <= HIGH
            o.append('<rect x="%.1f" y="%.1f" width="%d" height="%d" fill="%s" '
                     'fill-opacity="%s" stroke="%s" stroke-width="%s"/>'
                     % (xx, yy, cw - 8, ch - 10, BAND if hit else "#ffffff",
                        "0.9" if hit else "1", HIT if hit else MUTED, "1.6" if hit else "0.6"))
            o.append('<text x="%.1f" y="%.1f" font-size="15" text-anchor="middle" fill="%s">'
                     '%.2f</text>' % (xx + (cw - 8) / 2, yy + ch / 2 + 2,
                                      HIT if hit else INK, v))
    tested = [v for name, row in cells if "calibration" not in name for v in row]
    n_hit = sum(1 for v in tested if LOW <= v <= HIGH)
    o.append('<text x="%d" y="%d" font-size="11.5" fill="%s">%d of the %d cells put to the test '
             'fall in the band, both of them RFCs; UK\u2019s own two are in it by</text>'
             % (RX, T + 46 + 4 * ch + 26, MUTED, n_hit, len(tested)))
    o.append('<text x="%d" y="%d" font-size="11.5" fill="%s">construction, since the band was drawn '
             'around its narrow value. One cell decides the row, because the</text>'
             % (RX, T + 46 + 4 * ch + 44, MUTED))
    o.append('<text x="%d" y="%d" font-size="11.5" fill="%s">check names one declared vocabulary '
             'and the checker is the one who declares it.</text>'
             % (RX, T + 46 + 4 * ch + 62, MUTED))
    o.append('<text x="%d" y="%d" font-size="13" fill="%s">S91.RULEBOUND: %s</text>'
             % (RX, T + 46 + 4 * ch + 96, HIT, adj["S91.RULEBOUND"]["verdict"]))

    o.append('<text x="%d" y="%d" font-size="10.5" fill="%s">Sources: this repository. '
             'works/2026-09-21-three-other-offices/{results,inspection,adjudication}.json; rules '
             'imported unchanged from works/2026-09-17-the-second-instrument/validate.py.</text>'
             % (L, H - 16, MUTED))
    o.append('</svg>')
    (HERE / "figure.svg").write_text("\n".join(o) + "\n")
    print("wrote figure.svg (%d bytes)" % (HERE / "figure.svg").stat().st_size)


if __name__ == "__main__":
    main()
