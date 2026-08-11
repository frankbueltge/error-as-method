#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
figure.py — draws figure.svg from data.json.  Ulysses, 2026-08-11, Session 47.

Nothing is drawn that is not in data.json; no coordinate is a typed-in result.
Stdlib only, deterministic.  Run ledger.py first.
"""

import json

D = json.load(open("data.json"))

W, H = 1000, 772
GROUND = "#fbfaf7"
INK = "#16181d"
FAINT = "#c9c4b6"
RULE = "#8e887a"
BAND = "#ece7da"
BEFORE = "#a8761a"   # the value measurement gave it before the revision
AFTER = "#14545c"    # the value measurement gives it after
STIP = "#111318"     # the value a definition stipulates: a line, not a point

SIG_MIN, SIG_MAX = -4.6, 4.6
PLOT_L, PLOT_R = 330, 952


def x(sig):
    return PLOT_L + (sig - SIG_MIN) / (SIG_MAX - SIG_MIN) * (PLOT_R - PLOT_L)


out = []
A = out.append
A('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
  'viewBox="0 0 %d %d" font-family="Iowan Old Style, Palatino, Georgia, serif">'
  % (W, H, W, H))
A('<rect width="%d" height="%d" fill="%s"/>' % (W, H, GROUND))


def text(xx, yy, s, size=13, fill=INK, anchor="start", style="", weight="normal"):
    A('<text x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="%s" '
      'font-style="%s" font-weight="%s">%s</text>'
      % (xx, yy, size, fill, anchor, style or "normal", weight,
         s.replace("&", "&amp;").replace("<", "&lt;")))


def axis(y0, y1, ylab, cap_dy=36):
    """The sigma axis: a shaded +/-1 band, ticks, and the heavy stipulation rule."""
    A('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>'
      % (x(-1), y0, x(1) - x(-1), y1 - y0, BAND))
    for s in range(-4, 5):
        A('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
          'stroke-width="0.7"/>' % (x(s), y0, x(s), y1, FAINT))
        text(x(s), y1 + 17, ("%+d" % s) if s else "0", 12,
             STIP if s == 0 else RULE, "middle")
    A('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
      'stroke-width="2.2"/>' % (x(0), y0, x(0), y1, STIP))
    text((PLOT_L + PLOT_R) / 2, y1 + cap_dy, ylab, 12, RULE, "middle", "italic")


# ---------------------------------------------------------------- title
text(48, 52, "The Forwarding Address", 27)
text(48, 76,
     "Where the 2019 revision of the SI put the exactness it took away, and how far "
     "the released quantities have drifted since.", 13, RULE)
text(48, 95,
     "Every number below is computed by ledger.py from the CODATA 2014, 2018 and "
     "2022 tables committed in tables/.", 11.5, RULE, style="italic")

# ---------------------------------------------------------------- panel A
PA0, PA1 = 148, 336
text(48, 132, "SIX QUANTITIES LOST EXACTNESS", 13.5, INK, weight="bold")
text(48, 148 - 2, "", 11)
axis(PA0, PA1, "distance from the value the abrogated definition asserted, "
                "in standard uncertainties")

LOSSES = [r for r in D["losses"] if "2018" in r]
LOSSES.sort(key=lambda r: r["2018"]["sigma"])
PRETTY = {
    "vacuum electric permittivity": "vacuum electric permittivity  ε₀",
    "atomic unit of permittivity": "atomic unit of permittivity  4πε₀",
    "molar mass constant": "molar mass constant  Mᵤ",
    "molar mass of carbon-12": "molar mass of carbon-12  M(¹²C)",
    "vacuum mag. permeability": "vacuum magnetic permeability  μ₀",
    "characteristic impedance of vacuum": "impedance of vacuum  Z₀",
}
row_h = (PA1 - PA0) / (len(LOSSES) + 0.6)
for i, r in enumerate(LOSSES):
    yy = PA0 + row_h * (i + 0.8)
    text(318, yy + 4, PRETTY.get(r["quantity"], r["quantity"]), 12.5, INK, "end")
    s18, s22 = r["2018"]["sigma"], r["2022"]["sigma"]
    A('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
      'stroke-width="1" stroke-dasharray="2 3"/>'
      % (x(s18), yy, x(s22), yy, RULE))
    A('<circle cx="%.1f" cy="%.1f" r="5.2" fill="%s" stroke="%s" '
      'stroke-width="1.6"/>' % (x(s18), yy, GROUND, AFTER))
    A('<circle cx="%.1f" cy="%.1f" r="5.2" fill="%s"/>' % (x(s22), yy, AFTER))
text(x(-4.4), PA0 - 12, "○  CODATA 2018        ●  CODATA 2022", 11.5, AFTER)

# ---------------------------------------------------------------- panel B
PB0, PB1 = 448, 596
gains = [r for r in D["gains"] if "sigma" in r]
text(48, 420, "FIFTY-NINE QUANTITIES GAINED IT", 13.5, INK, weight="bold")
axis(PB0, PB1, "distance of the stipulated value from the last measured one, "
                "in standard uncertainties", cap_dy=58)
text(318, PB0 + 34, "each mark is one row of the", 12.5, INK, "end")
text(318, PB0 + 50, "CODATA table that stopped", 12.5, INK, "end")
text(318, PB0 + 66, "being measured", 12.5, INK, "end")
text(318, PB0 + 88, "they fall in two bands, not", 11.5, RULE, "end", style="italic")
text(318, PB0 + 103, "fifty-nine: the h/e family and", 11.5, RULE, "end",
     style="italic")
text(318, PB0 + 118, "the k family, under many names", 11.5, RULE, "end",
     style="italic")

# deterministic vertical spread: order within each 0.1-wide bucket
seen = {}
for r in sorted(gains, key=lambda r: r["sigma"]):
    key = round(r["sigma"], 1)
    n = seen.get(key, 0)
    seen[key] = n + 1
    yy = PB0 + 16 + (n % 9) * 15.2
    A('<circle cx="%.1f" cy="%.1f" r="4.2" fill="%s" opacity="0.85"/>'
      % (x(r["sigma"]), yy, BEFORE))

LABELS = {"Planck constant": "h", "elementary charge": "e",
          "Boltzmann constant": "k", "Avogadro constant": "Nₐ"}
marks = sorted(((r["sigma"], LABELS[r["quantity"]]) for r in gains
                if r["quantity"] in LABELS), key=lambda t: t[0])
last_x, tier = -1e9, 0
for sig, lab in marks:
    xp = x(sig)
    tier = (tier + 1) % 2 if xp - last_x < 20 else 0
    last_x = xp
    dy = 12 + tier * 16
    A('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
      'stroke-width="1.1"/>' % (xp, PB1, xp, PB1 + dy, BEFORE))
    text(xp, PB1 + dy + 13, lab, 13, BEFORE, "middle", style="italic")

# ---------------------------------------------------------------- census strip
CY = 690
c = D["census"]
text(48, CY + 4, "AND THE COUNT DID NOT BALANCE", 12.5, INK, weight="bold")
text(48, CY + 24, "six released, fifty-nine stipulated", 11.5, RULE, style="italic")
unit = 5.6
BAR_L = 400
A('<rect x="%d" y="%.1f" width="%.1f" height="14" fill="%s" stroke="%s" '
  'stroke-width="0.6"/>' % (BAR_L, CY - 12, c["exact_2014"] * unit, RULE, RULE))
text(BAR_L - 12, CY, "CODATA 2014", 12, INK, "end")
text(BAR_L + c["exact_2014"] * unit + 9, CY,
     "%d rows exact" % c["exact_2014"], 12, INK)
xx = BAR_L
for n, fill in ((c["stayed_exact"], RULE), (c["gained"], BEFORE),
                (c["exact_and_new_in_2018"], BAND)):
    A('<rect x="%.1f" y="%.1f" width="%.1f" height="14" fill="%s" stroke="%s" '
      'stroke-width="0.6"/>' % (xx, CY + 14, n * unit, fill, RULE))
    xx += n * unit
text(BAR_L - 12, CY + 26, "CODATA 2018", 12, INK, "end")
text(xx + 9, CY + 26, "%d rows exact" % c["exact_2018"], 12, INK)

text(48, H - 20,
     "Ulysses · Session 47 · 2026-08-11 · sources: CGPM Resolution 1 "
     "(2018) App. 2; BIPM SI Brochure 9th ed.; NIST CODATA 2014 / 2018 / 2022",
     11, RULE)

A("</svg>")
open("figure.svg", "w", encoding="utf-8").write("\n".join(out))
print("wrote figure.svg  (%d losses, %d gains, census %s)"
      % (len(LOSSES), len(gains), c["exact_2014"]))
