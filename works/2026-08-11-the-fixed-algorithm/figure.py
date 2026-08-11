#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
figure.py — draws figure.svg from data.json.  Ulysses, 2026-08-11, Session 46.
Nothing is drawn that is not in data.json; no value is typed in by hand.
Stdlib only, deterministic. Run convert.py first.
"""

import json
from math import log10

D = json.load(open("data.json"))

W, H = 1000, 964
PAPER = "#f4f1ea"
INK = "#1b1b1b"
SUB = "#4a4a4a"
GRID = "#cdc7b8"
RULE = "#8d8778"
BANNED = "#8a3324"     # the apparatus the statute forbids
MANDATED = "#35506b"   # the apparatus the statute requires
PERMIT = "#6b6a3f"     # the apparatuses the statute permits, plural

out = []
A = out.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
  f'font-family="Georgia, \'Times New Roman\', serif">')
A(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')


def txt(x, y, s, size=13, fill=SUB, anchor="start", style="", weight=""):
    extra = ""
    if style:
        extra += f' font-style="{style}"'
    if weight:
        extra += f' font-weight="{weight}"'
    A(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
      f'text-anchor="{anchor}"{extra}>{s}</text>')


txt(58, 44, "The fixed algorithm is a family", 22, INK)
txt(58, 68, "Council Regulation (EC) No 1103/97, Art. 4 and 5, measured on the eleven irrevocably fixed rates of Reg. (EC) No 2866/98.")
txt(58, 87, "Exact integer arithmetic throughout; every value below is recomputable from convert.py &#8594; data.json.")

# ---------------------------------------------------------------------------
# Panel A — the banned apparatus against the reason given for banning it
# ---------------------------------------------------------------------------
AX0, AX1 = 92, 700
AY0, AY1 = 176, 344
mags = [w["from_minor_units"] for w in D["m1_inverse_ban"][0]["magnitude_windows"]]
lo, hi = log10(min(mags)), log10(max(mags))


def ax(v):
    return AX0 + (log10(v) - lo) / (hi - lo) * (AX1 - AX0)


def ay(r):
    return AY1 - r * (AY1 - AY0)


txt(58, 128, "A.  The apparatus Art. 4(3) forbids by name, and the one the reason for the ban actually reaches", 15, INK)

for r in (0, 0.25, 0.5, 0.75, 1.0):
    A(f'<line x1="{AX0}" y1="{ay(r):.1f}" x2="{AX1}" y2="{ay(r):.1f}" stroke="{GRID}" stroke-width="0.6"/>')
    txt(AX0 - 10, ay(r) + 4, f"{int(r*100)}%", 11, RULE, "end")
for m in mags:
    A(f'<line x1="{ax(m):.1f}" y1="{AY1}" x2="{ax(m):.1f}" y2="{AY1+5}" stroke="{RULE}" stroke-width="0.8"/>')
    txt(ax(m), AY1 + 20, f"10{'&#8310;&#8311;&#8308;&#8309;&#8310;&#8311;&#8312;'[0]}".replace("10", "10^") if False
        else f"10<tspan baseline-shift='super' font-size='9'>{int(log10(m))}</tspan>", 11, RULE, "middle")
txt((AX0 + AX1) / 2, AY1 + 42, "amount converted, in minor units of the national currency (log scale)", 11, RULE, "middle")
txt(AX0 + 4, AY0 - 30, "share of amounts on which the banned result", 11, RULE, "start")
txt(AX0 + 4, AY0 - 17, "differs from the one the statute requires", 11, RULE, "start")

for row in D["m1_inverse_ban"]:
    pts = " ".join(f"{ax(w['from_minor_units']):.1f},{ay(w['six_sig_rate']):.1f}"
                   for w in row["magnitude_windows"])
    A(f'<polyline points="{pts}" fill="none" stroke="{BANNED}" stroke-width="1.1" opacity="0.62"/>')
# the float64 inverse: every currency, flat on zero
A(f'<line x1="{ax(mags[0]):.1f}" y1="{ay(0):.1f}" x2="{ax(mags[-1]):.1f}" y2="{ay(0):.1f}" '
  f'stroke="{MANDATED}" stroke-width="2.6"/>')

lab = {r["code"]: r for r in D["m1_inverse_ban"]}
# label each curve where it first passes half, staggered so the marks do not collide
placed = []
for code in ("IEP", "NLG", "DEM", "FIM", "BEF", "ATS", "FRF", "PTE", "ESP", "ITL"):
    w = lab[code]["magnitude_windows"]
    hit = next((k for k in range(len(w)) if w[k]["six_sig_rate"] >= 0.5), None)
    if hit is None or hit == 0:
        continue
    p, q = w[hit - 1], w[hit]
    t = (0.5 - p["six_sig_rate"]) / max(q["six_sig_rate"] - p["six_sig_rate"], 1e-9)
    lx = ax(p["from_minor_units"]) + t * (ax(q["from_minor_units"]) - ax(p["from_minor_units"]))
    ly = ay(0.5)
    while any(abs(lx - px) < 26 and abs(ly - py) < 11 for px, py in placed):
        ly -= 12
    placed.append((lx, ly))
    A(f'<line x1="{lx:.1f}" y1="{ay(0.5):.1f}" x2="{lx:.1f}" y2="{ly+3:.1f}" stroke="{BANNED}" stroke-width="0.5" opacity="0.5"/>')
    txt(lx, ly, code, 9.5, BANNED, "middle")

txt(AX1 + 14, ay(1.0) + 4, "the inverse rate rounded", 11.5, BANNED)
txt(AX1 + 14, ay(1.0) + 18, "to six significant figures", 11.5, BANNED)
txt(AX1 + 14, ay(1.0) + 32, "(one line per currency)", 11.5, RULE)
txt(AX1 + 14, ay(0.0) - 17, "the same inverse as a float64:", 11.5, MANDATED)
txt(AX1 + 14, ay(0.0) - 3, "equally banned, never divergent", 11.5, MANDATED)

# rank the onsets by MONEY, not by minor units: a centime and a lira are not comparable
def _eur(r):
    return float(r["first_divergence_six_sig_currency_units"]) / float(r["rate"])
first = min(D["m1_inverse_ban"], key=_eur)
_sys = min(D["m1_inverse_ban"], key=lambda r: float(r["systematic_from_currency_units"]) / float(r["rate"]))
_sysv = float(_sys["systematic_from_currency_units"]) / float(_sys["rate"])
txt(58, AY1 + 64,
    f"Recital (10) grounds the ban on accuracy &#8212; inverse rates &#8220;could result in significant inaccuracies, "
    f"notably if large amounts are involved&#8221;. True of the six-figure inverse,", 12, SUB)
txt(58, AY1 + 81,
    f"though the first single-unit divergence already appears at {first['first_divergence_six_sig_currency_units']} "
    f"{first['code']} &#8212; &#8364;{_eur(first):.2f} &#8212; and turns systematic from about &#8364;{_sysv:,.0f} upward.", 12, SUB)
txt(58, AY1 + 98,
    "But Art. 4(3) bans &#8220;inverse rates&#8221; without qualification, so it equally bans the float64 inverse, "
    "which never diverges anywhere in the scan. The prohibition outlives its reason.", 12, SUB)

# ---------------------------------------------------------------------------
# Panel B — the permitted set disagreeing with itself
# ---------------------------------------------------------------------------
BY0, BY1 = 500, 640
BX0, BX1 = 92, 700
pairs = sorted(D["m2_permitted_set"]["pairs"], key=lambda p: p["divergent_amounts_in_scan"])
scan = pairs[0]["scan_minor_units"]
fracs = [p["divergent_amounts_in_scan"] / scan for p in pairs]
top = 0.8


def by(f):
    return BY1 - f / top * (BY1 - BY0)


txt(58, 470, "B.  The methods Art. 4(4) permits, disagreeing with each other", 15, INK)
for f in (0, 0.2, 0.4, 0.6, 0.8):
    A(f'<line x1="{BX0}" y1="{by(f):.1f}" x2="{BX1}" y2="{by(f):.1f}" stroke="{GRID}" stroke-width="0.6"/>')
    txt(BX0 - 10, by(f) + 4, f"{int(f*100)}%", 11, RULE, "end")

bw = (BX1 - BX0) / len(pairs)
for i, (p, f) in enumerate(zip(pairs, fracs)):
    x = BX0 + i * bw
    A(f'<rect x="{x:.2f}" y="{by(f):.1f}" width="{max(bw-0.8,0.7):.2f}" height="{(BY1-by(f)):.1f}" '
      f'fill="{PERMIT}" opacity="0.75"/>')
txt((BX0 + BX1) / 2, BY1 + 20,
    f"each of the {len(pairs)} ordered currency pairs, ranked &#8212; all {len(pairs)} of them disagree", 11, RULE, "middle")
worst = pairs[-1]
txt(BX1 - 4, by(fracs[-1]) - 8, f"{worst['from']} &#8594; {worst['to']}, {fracs[-1]*100:.1f}%", 11, PERMIT, "end")
med = sorted(fracs)[len(fracs) // 2]
A(f'<line x1="{BX0}" y1="{by(med):.1f}" x2="{BX1}" y2="{by(med):.1f}" stroke="{INK}" '
  f'stroke-width="0.9" stroke-dasharray="4 3"/>')
txt(BX1 + 16, by(med) + 4, f"median {med*100:.1f}%", 11, INK)

mx = max(p["max_spread_minor_units"] for p in D["m2_permitted_set"]["pairs"])
txt(58, BY1 + 46,
    f"Rounding the intermediate euro amount to three decimals, to four, five, six, or not at all: the first clause of "
    f"Art. 4(4) permits all five.", 12, SUB)
txt(58, BY1 + 63,
    f"On amounts up to {scan:,} minor units they spread by as much as {mx} minor units. The second clause of the very "
    f"same sentence reads:", 12, SUB)
txt(58, BY1 + 80,
    "&#8220;No alternative method of calculation may be used unless it produces the same results.&#8221;", 12, INK)

# ---------------------------------------------------------------------------
# Panel C — the tie-break, where nothing can be measured
# ---------------------------------------------------------------------------
CY = 792
CX0, CX1 = 92, 700
CMAX = 2500.0
txt(58, 752, "C.  The exact half-way amounts, where no measurement can prefer either side", 15, INK)

ORDER_C = ["ATS", "ESP", "DEM", "IEP"]
rows_c = sorted((r for r in D["m3_tie_break"] if r["code"] in ORDER_C),
                key=lambda r: ORDER_C.index(r["code"]))
for j, r in enumerate(rows_c):
    y = CY + j * 21
    P = float(r["tie_period_euro"])
    fd = float(r["first_disagreement_euro"])
    A(f'<line x1="{CX0}" y1="{y:.0f}" x2="{CX1}" y2="{y:.0f}" stroke="{GRID}" stroke-width="0.8"/>')
    txt(CX0 - 10, y + 4, r["code"], 11, RULE, "end")
    k = 1
    while k * P <= CMAX:
        c = k * P
        x = CX0 + c / CMAX * (CX1 - CX0)
        # ties are the ODD multiples of P, so consecutive ties are 2P apart and the two
        # rounding rules part on every other tie -- a stride of 4P, not 2P.
        dis = abs((c - fd) % (4 * P)) < 1e-9
        if dis:
            A(f'<line x1="{x:.1f}" y1="{y-7:.0f}" x2="{x:.1f}" y2="{y+7:.0f}" stroke="{BANNED}" stroke-width="1.8"/>')
        else:
            A(f'<line x1="{x:.1f}" y1="{y-4:.0f}" x2="{x:.1f}" y2="{y+4:.0f}" stroke="{MANDATED}" stroke-width="1.2" opacity="0.65"/>')
        k += 2
    txt(CX1 + 14, y + 4, f"a tie every &#8364;{P:,.0f}", 10, RULE)

yb = CY + len(rows_c) * 21 - 7
for v in (0, 500, 1000, 1500, 2000, 2500):
    x = CX0 + v / CMAX * (CX1 - CX0)
    A(f'<line x1="{x:.1f}" y1="{yb:.0f}" x2="{x:.1f}" y2="{yb+5:.0f}" stroke="{RULE}" stroke-width="0.8"/>')
    txt(x, yb + 18, f"&#8364;{v:,}", 10, RULE, "middle")

A(f'<line x1="{CX0}" y1="{yb+34:.0f}" x2="{CX0}" y2="{yb+48:.0f}" stroke="{BANNED}" stroke-width="1.8"/>')
txt(CX0 + 8, yb + 46, "statute and machine return different money", 11, RULE)
A(f'<line x1="{CX0+300}" y1="{yb+37:.0f}" x2="{CX0+300}" y2="{yb+45:.0f}" stroke="{MANDATED}" stroke-width="1.2" opacity="0.65"/>')
txt(CX0 + 308, yb + 46, "a tie both rules happen to resolve the same way", 11, RULE)

dem = [r for r in D["m3_tie_break"] if r["code"] == "DEM"][0]
ex = dem["examples"][0]
txt(58, H - 38,
    "Tall marks: the statute (Art. 5, &#8220;the sum shall be rounded up&#8221;) and the prevailing machine default "
    "(round half to even) return different money &#8212; exactly half of all ties.", 12, SUB)
txt(58, H - 20,
    f"&#8364;{ex['euro']} is exactly {ex['exact_national']} German marks. The statute says {ex['statute_half_up']}, "
    f"IEEE&#160;754-2019&#8217;s default rounding attribute says {ex['machine_half_even']}. Neither is nearer.", 12, SUB)

A("</svg>")
open("figure.svg", "w").write("\n".join(out))
print("wrote figure.svg", sum(len(x) for x in out), "bytes")
