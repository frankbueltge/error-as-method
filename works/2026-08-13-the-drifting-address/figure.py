#!/usr/bin/env python3
"""
Generates figure.svg from results.json and residuals.csv. Deterministic: no
randomness, no seed, no network. Run `measure.py` first.

Three panels, and the argument runs left to right.

  1. THE SPILL. Every runway's signed residual -- the degrees by which its magnetic
     bearing exceeds the number painted on it. A population whose designators were
     all correct would fill the +/-5 degree box and nothing outside it, because the
     rule rounds to the nearest ten. The grey box is that population. The bars are
     this one. Everything outside the box is a name that has gone wrong on its own.

  2. THE INVERSION. The same fraction, by how much traffic depends on the address.
     The claim under test says a norm is incorrigible where something holds a
     reference to it. The bars run the other way.

  3. THE OUTSIDE CHECK. This measurement at three epochs against NAV CANADA's two
     independently measured points, from a different population, tool and purpose.
"""

import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json"), encoding="utf-8"))

PAPER = "#f6f3ea"
INK = "#16150f"
MUTE = "#6f6a5c"
RULE = "#c9c2b0"
IN = "#2f4858"          # inside the tolerance the rule allows itself
OUT = "#a8442a"         # outside it
GHOST = "#e2ddcd"       # the population a maintained world would have
CHECK = "#7d8c7a"       # the outside measurement

W, H = 960, 880
S = []


def t(x, y, s, size=13, fill=INK, anchor="start", family=None, weight=None):
    f = f' font-family="{family}"' if family else ""
    wt = f' font-weight="{weight}"' if weight else ""
    S.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
             f'text-anchor="{anchor}"{f}{wt}>{s}</text>')


def rect(x, y, w, h, fill, stroke=None, sw=1, op=None):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    o = f' opacity="{op}"' if op else ""
    S.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w,0):.1f}" '
             f'height="{max(h,0):.1f}" fill="{fill}"{st}{o}/>')


def line(x1, y1, x2, y2, stroke=RULE, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    S.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
             f'stroke="{stroke}" stroke-width="{sw}"{d}/>')


MONO = "ui-monospace, SFMono-Regular, Menlo, monospace"

S.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" font-family="Iowan Old Style, '
         f'Palatino Linotype, Palatino, Georgia, serif">')
rect(0, 0, W, H, PAPER)

today = R["today"]
t(40, 52, "A name that goes wrong by itself", 27)
t(40, 76, "Every runway is designated by its magnetic bearing, rounded to the "
          "nearest ten degrees. Magnetic north moves; the runway does not.", 14, MUTE)
t(40, 95, f'{today["n"]:,} runways, computed from their threshold coordinates and '
          f'IGRF-14 at 2026.6. {today["out_of_tolerance"]:,} of them '
          f'({today["fraction_out"]*100:.1f} %) no longer round to the number they carry.',
  14, MUTE)

# ------------------------------------------------------------------ panel 1
resids = []
with open(os.path.join(HERE, "residuals.csv")) as fh:
    for row in csv.DictReader(fh):
        resids.append(float(row["residual_2026_deg"]))

LO, HI, BW = -20.0, 20.0, 0.5
nb = int((HI - LO) / BW)
bins = [0] * nb
for r in resids:
    if LO <= r < HI:
        bins[int((r - LO) / BW)] += 1
tails = (sum(1 for r in resids if r < LO), sum(1 for r in resids if r >= HI))

PX, PY, PW, PH = 60, 160, 840, 250
# a maintained population is uniform on +/-5, so its bins stand higher than the real
# ones; both are scaled by whichever is taller so neither leaves the panel
ghost_per_bin = len(resids) * (BW / 10.0)
peak = max(max(bins), ghost_per_bin)


def bx(v):
    return PX + (v - LO) / (HI - LO) * PW


ghost_h = ghost_per_bin / peak * PH
rect(bx(-5), PY + PH - ghost_h, bx(5) - bx(-5), ghost_h, GHOST)
t(bx(5) + 8, PY + PH - ghost_h + 13, "the population a fully maintained", 12, MUTE)
t(bx(5) + 8, PY + PH - ghost_h + 28, "world would have: every designator", 12, MUTE)
t(bx(5) + 8, PY + PH - ghost_h + 43, "inside the rounding it was named by", 12, MUTE)

for i, c in enumerate(bins):
    v = LO + i * BW
    h = c / peak * PH
    inside = abs(v + BW / 2) <= 5.0
    rect(bx(v), PY + PH - h, PW / nb - 0.6, h, IN if inside else OUT)

line(PX, PY + PH, PX + PW, PY + PH, RULE, 1)
for v in range(-20, 21, 5):
    line(bx(v), PY + PH, bx(v), PY + PH + 5, RULE)
    t(bx(v), PY + PH + 20, f"{v:+d}°" if v else "0°", 11.5, MUTE, "middle")
line(bx(-5), PY - 6, bx(-5), PY + PH, INK, 1, "3 3")
line(bx(5), PY - 6, bx(5), PY + PH, INK, 1, "3 3")
t(bx(0), PY - 14, "the tolerance the rounding rule allows itself", 12, INK, "middle")
t(PX, PY + PH + 44, f'{tails[0]:,} runways lie left of this axis and {tails[1]:,} right '
                    f'of it; the worst is {today["max_abs_residual_deg"]:.0f}° out. '
                    f'Median |residual| {today["median_abs_residual_deg"]}° against '
                    f'the 2.5° a maintained population would show.', 12.5, MUTE)
t(PX, PY + PH + 62, f'The whole distribution leans: mean signed residual '
                    f'{today["mean_signed_residual_deg"]:+.2f}°. The field drifts one way '
                    f'and takes every name with it.', 12.5, MUTE)

# ------------------------------------------------------------------ panel 2
ph = R["post_hoc"]
QY = 500
t(40, QY, "The claim under test says a norm is incorrigible where something holds "
          "a reference to it. It is the other way round.", 15, INK)
t(40, QY + 20, "Fraction of runways whose painted number no longer rounds correctly, "
               "by how much depends on the address.", 12.5, MUTE)

groups = [
    ("large airports", ph["by_airport_type"]["large_airport"]),
    ("medium airports", ph["by_airport_type"]["medium_airport"]),
    ("small airports", ph["by_airport_type"]["small_airport"]),
    (None, None),
    ("with scheduled service", ph["scheduled_service"]["yes"]),
    ("without", ph["scheduled_service"]["no"]),
]
BY, BH, GAP = QY + 44, 26, 9
BX, BMAX = 250, 480
for i, (lab, d) in enumerate(groups):
    y = BY + i * (BH + GAP)
    if lab is None:
        continue
    f = d["fraction_out"]
    t(BX - 12, y + 18, lab, 13, INK, "end")
    rect(BX, y, BMAX, BH, GHOST)
    rect(BX, y, BMAX * f / 0.40, BH, OUT)
    t(BX + BMAX * f / 0.40 + 8, y + 18, f"{f*100:.1f} %", 13, INK, family=MONO)
    t(BX + BMAX + 84, y + 18, f'{d["out"]:,} of {d["n"]:,}', 12, MUTE, family=MONO)
line(BX, BY - 6, BX, BY + 6 * (BH + GAP) - GAP, RULE)

# ------------------------------------------------------------------ panel 3
CY = 736
nc = ph["external_check_navcanada"]
t(40, CY, "Checked against an outside party that measured the same thing for a "
          "different reason", 15, INK)
t(40, CY + 19, "NAV CANADA counted it over 25,732 hard-surface runways from AIRAC "
               "navigation data, to argue for abolishing the magnetic reference "
               "altogether.", 12.5, MUTE)

CX, CW2, CH2 = 250, 480, 62
CB, CT = 0.15, 0.35


def cy_(f):
    return CY + 44 + CH2 - (f - CB) / (CT - CB) * CH2


mine = [(2020.85, nc["mine_hard_surface_at_2020_85"]["fraction_out"]),
        (2026.62, nc["mine_hard_surface_at_2026_62"]["fraction_out"]),
        (2030.0, nc["mine_hard_surface_at_2030_0"]["fraction_out"])]
theirs = [(2020.85, nc["their_fraction_2020"]), (2030.0, nc["their_fraction_2030"])]


def cx_(y):
    return CX + (y - 2019.0) / 12.0 * CW2


line(CX, CY + 44 + CH2, CX + CW2, CY + 44 + CH2, RULE)
for yr in (2020, 2022, 2024, 2026, 2028, 2030):
    t(cx_(yr), CY + 44 + CH2 + 18, str(yr), 11.5, MUTE, "middle")
for a, b in zip(mine, mine[1:]):
    line(cx_(a[0]), cy_(a[1]), cx_(b[0]), cy_(b[1]), IN, 2)
for a, b in zip(theirs, theirs[1:]):
    line(cx_(a[0]), cy_(a[1]), cx_(b[0]), cy_(b[1]), CHECK, 2, "5 4")
for yr, f in mine:
    S.append(f'<circle cx="{cx_(yr):.1f}" cy="{cy_(f):.1f}" r="4.5" fill="{IN}"/>')
    t(cx_(yr), cy_(f) - 12, f"{f*100:.1f}", 12, IN, "middle", family=MONO)
for yr, f in theirs:
    S.append(f'<circle cx="{cx_(yr):.1f}" cy="{cy_(f):.1f}" r="4.5" fill="{PAPER}" '
             f'stroke="{CHECK}" stroke-width="2"/>')
    t(cx_(yr), cy_(f) + 21, f"{f*100:.1f}", 12, CHECK, "middle", family=MONO)
t(CX + CW2 + 14, cy_(mine[-1][1]) + 4, "this measurement", 12, IN)
t(CX + CW2 + 14, cy_(theirs[-1][1]) + 20, "NAV CANADA, 2022", 12, CHECK)

t(40, H - 26, "Ulysses (the nightly line), Session 52 · 2026-08-13 · "
              "runway geometry from OurAirports, declination from IGRF-14, the "
              "synthesis checked against WMM2025's own published test values "
              "(worst 0.005° over 100 rows)", 11.5, MUTE)

S.append("</svg>")
open(os.path.join(HERE, "figure.svg"), "w").write("\n".join(S))
print(f"figure.svg written: {len(''.join(S))} bytes, {len(resids)} runways plotted, "
      f"tails {tails}")
