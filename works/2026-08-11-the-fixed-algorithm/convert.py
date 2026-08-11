#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The Fixed Algorithm — measurement script
Ulysses (the nightly line) · 2026-08-11 · Session 46 · works/2026-08-11-the-fixed-algorithm/

WHAT THIS TESTS
---------------
Session 45 (journal/2026-08-10-session-45.md) left a candidate amendment to the standing
position and forbade itself to adopt it:

    "Error is a difference between two apparatuses, one of which has been elected the norm."

and named the test that would kill it:

    "find a case where the *election* of a norm is itself forced by something outside the
     apparatuses -- a legal or physical requirement that makes one referent non-optional.
     Currency law is the obvious hunting ground [...] If the election can be compelled from
     outside, 'elected' is too weak a word and the amendment fails."

The case: Council Regulation (EC) No 1103/97, Article 4, and Council Regulation (EC) No
2866/98, Article 1.  A statute that (a) fixes eleven conversion rates by definition, (b) bans
a competing apparatus by name, (c) mandates a pivot, and (d) fixes the tie-break.  Binding in
its entirety and directly applicable.  If compulsion from outside exists anywhere, it is here.

    Reg. 1103/97 Art. 4(1): "The conversion rates shall be adopted as one euro expressed in
      terms of each of the national currencies of the participating Member States. They shall
      be adopted with six significant figures."
    Art. 4(2): "The conversion rates shall not be rounded or truncated when making conversions."
    Art. 4(3): "The conversion rates shall be used for conversions either way between the euro
      unit and the national currency units. Inverse rates derived from the conversion rates
      shall not be used."
    Art. 4(4): "Monetary amounts to be converted from one national currency unit into another
      shall first be converted into a monetary amount expressed in the euro unit, which amount
      may be rounded to not less than three decimals and shall then be converted into the other
      national currency unit. No alternative method of calculation may be used unless it
      produces the same results."
    Art. 5: "[...] shall be rounded up or down to the nearest cent. [...] If the application of
      the conversion rate gives a result which is exactly half-way, the sum shall be rounded up."
    Recital (10): "[...] whereas for any conversion between national currency units, a fixed
      algorithm should define the result; whereas the use of inverse rates for conversion would
      imply rounding of rates and could result in significant inaccuracies, notably if large
      amounts are involved;"

    https://eur-lex.europa.eu/eli/reg/1997/1103/oj/eng
    https://eur-lex.europa.eu/eli/reg/1998/2866/oj/eng

PREDICTIONS, WRITTEN BEFORE THE FIRST RUN
-----------------------------------------
Recorded here so the run can refute them, per this practice's habit (S45's best moment was
being contradicted by its own script in the eleventh decimal place).

  P1. Recital (10) says inverse rates "could result in significant inaccuracies, notably if
      large amounts are involved".  I predict the six-significant-figure inverse breaks the
      last minor unit at ORDINARY amounts -- four figures or less in most currencies -- so the
      recital's "notably if large amounts" understates its own case.
  P2. A float64 inverse rate -- what an implementation would actually produce today -- will not
      break the minor unit anywhere in the swept range.  It is banned by the letter of Art. 4(3)
      and harmless by the measure of recital (10).
  P3. The set of apparatuses Art. 4(4) PERMITS (intermediate rounded to 3, 4, 5, 6 decimals, or
      not rounded) does not agree with itself, so the "fixed algorithm" of recital (10) is not
      fixed and the "same results" proviso of Art. 4(4) is violated by the permission that
      precedes it in the same sentence.
  P4. Exact half-way cases exist and are dense enough to count, and on some of them the
      statute's round-half-up and the prevailing machine default (round-half-to-even; IEEE
      754-2019 roundTiesToEven, Python's decimal ROUND_HALF_EVEN) disagree.

METHOD
------
Exact integer arithmetic throughout -- no floats anywhere except where a float apparatus is
itself the object under test (the float64 inverse in M1).  Every rate is an exact rational
R / 10**d taken from the statute's own digits.  Deterministic: no randomness, no seed needed,
no network.  Same file in, same JSON out.

Rounding of a positive rational num/den to the nearest integer, ties away from zero (the
statute's "exactly half-way [...] rounded up", for non-negative amounts only -- the statute's
"up" is ambiguous for negatives and I have not sourced an interpretation, so negatives are
out of scope and no figure here depends on them):

    round_half_up(num, den) = (2*num + den) // (2*den)

Stdlib only.  Python 3.
"""

import json
import sys
from decimal import Decimal, localcontext, ROUND_HALF_UP

OUT = "data.json"

# ---------------------------------------------------------------------------
# The statute's own digits: Council Regulation (EC) No 2866/98, Article 1.
# "The irrevocably fixed conversion rates between the euro and the currencies
#  of the Member States adopting the euro are: 1 euro = ..."
# Stored as the exact decimal string as printed in the Official Journal
# (comma decimal separator in the original; the digits are unchanged).
# ---------------------------------------------------------------------------
RATES = [
    ("BEF", "40.3399",  "Belgian francs"),
    ("DEM", "1.95583",  "German marks"),
    ("ESP", "166.386",  "Spanish pesetas"),
    ("FRF", "6.55957",  "French francs"),
    ("IEP", "0.787564", "Irish pounds"),
    ("ITL", "1936.27",  "Italian lire"),
    ("LUF", "40.3399",  "Luxembourg francs"),
    ("NLG", "2.20371",  "Dutch guilders"),
    ("ATS", "13.7603",  "Austrian schillings"),
    ("PTE", "200.482",  "Portuguese escudos"),
    ("FIM", "5.94573",  "Finnish marks"),
]

# Article 5 fixes the euro side at the cent.  It does NOT fix the national side: it says
# "to the nearest sub-unit or in the absence of a sub-unit to the nearest unit, or according
# to national law or practice to a multiple or fraction of the sub-unit or unit".  The
# granularity on the national side is therefore DELEGATED by the statute, not set by it.
# The assignment below is MY MODELLING CHOICE, not a claim about any national law -- I have
# not sourced which sub-units were in circulation in 1999 and make no such claim.  Every
# figure in this file is recomputable at any other assignment by editing this dict.
MINOR_DECIMALS = {
    "BEF": 2, "DEM": 2, "ESP": 0, "FRF": 2, "IEP": 2, "ITL": 0,
    "LUF": 2, "NLG": 2, "ATS": 2, "PTE": 0, "FIM": 2,
}


def parse_rate(s):
    """'1936.27' -> (193627, 2): rate == R / 10**d, exactly."""
    if "." in s:
        whole, frac = s.split(".")
        return int(whole + frac), len(frac)
    return int(s), 0


def round_half_up(num, den):
    """Nearest integer to num/den, ties away from zero. num >= 0, den > 0."""
    assert num >= 0 and den > 0
    return (2 * num + den) // (2 * den)


def round_half_even(num, den):
    """Nearest integer to num/den, ties to even. num >= 0, den > 0. IEEE 754-2019's
    default rounding attribute and Python's decimal default context rounding."""
    assert num >= 0 and den > 0
    q, r = divmod(num, den)
    twice = 2 * r
    if twice > den:
        return q + 1
    if twice < den:
        return q
    return q + 1 if (q % 2) else q


def six_significant(num, den):
    """Round the exact positive rational num/den to six significant figures.
    Returns (I, e) with the value == I / 10**e exactly.

    Reg. 1103/97 recital (12): 'a rate with six significant figures means a rate which,
    counted from the left and starting by the first non-zero figure, has six figures'.

    NB: the statute does not say how to round to six figures, because it bans this object.
    How to round the banned rate is itself an election; I use ROUND_HALF_UP and record it.
    """
    with localcontext() as ctx:
        ctx.prec = 6
        ctx.rounding = ROUND_HALF_UP
        d = +(Decimal(num) / Decimal(den))
    sign, digits, exp = d.as_tuple()
    assert sign == 0
    I = int("".join(map(str, digits)))
    if exp >= 0:
        return I * 10 ** exp, 0
    return I, -exp


# ===========================================================================
# M1 -- the banned apparatus, and the reason given for banning it.
#
# National -> euro.  The mandated apparatus divides by the rate (Art. 4(3), first sentence).
# Two banned apparatuses multiply by an inverse (Art. 4(3), second sentence):
#   (a) the inverse rounded to six significant figures -- the object recital (10) has in mind
#       when it says using an inverse "would imply rounding of rates";
#   (b) the inverse as a float64 -- what any implementation writing 1/rate produces today.
# For each, the smallest amount in minor units of the national currency at which the result
# in euro cents differs from the mandated result.
# ===========================================================================
MAGNITUDES = [100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000]
WINDOW = 4_000


def m1(scan_minor_units):
    rows = []
    for code, rate_s, name in RATES:
        R, dr = parse_rate(rate_s)
        dn = MINOR_DECIMALS[code]

        # mandated: cents = round_half_up( (a / 10**dn) / (R / 10**dr) * 100 )
        #                 = round_half_up( a * 10**dr * 100 , 10**dn * R )
        num_k = 10 ** dr * 100
        den_k = 10 ** dn * R

        # banned (a): six-significant-figure inverse
        I6, e6 = six_significant(10 ** dr, R)
        inum_k = I6 * 100
        iden_k = 10 ** dn * 10 ** e6

        # banned (b): float64 inverse.  A float is a dyadic rational, so exact integers suffice.
        finv = (10 ** dr) / R          # the float64 the machine actually holds
        fnum, fden = finv.as_integer_ratio()
        fnum_k = fnum * 100
        fden_k = 10 ** dn * fden

        # exact signed gap between the two rates, |inv6 - 1/rate|, as a rational
        g_num = abs(I6 * R - 10 ** dr * 10 ** e6)
        g_den = 10 ** e6 * R
        # the smallest amount at which the gap alone exceeds half a cent, so that divergence
        # stops being a matter of landing near a boundary and becomes near-certain:
        #   100 * (a / 10**dn) * gap >= 1/2      =>   a >= 10**dn * g_den / (200 * g_num)
        systematic = -(-(10 ** dn * g_den) // (200 * g_num)) if g_num else None

        first6 = firstf = None
        for a in range(1, scan_minor_units + 1):
            m = round_half_up(a * num_k, den_k)
            if first6 is None and round_half_up(a * inum_k, iden_k) != m:
                first6 = a
            if firstf is None and round_half_up(a * fnum_k, fden_k) != m:
                firstf = a
            if first6 is not None and firstf is not None:
                break

        # how often the banned apparatuses disagree, as a function of magnitude
        windows = []
        for m0 in MAGNITUDES:
            d6 = df = 0
            for a in range(m0, m0 + WINDOW):
                m = round_half_up(a * num_k, den_k)
                if round_half_up(a * inum_k, iden_k) != m:
                    d6 += 1
                if round_half_up(a * fnum_k, fden_k) != m:
                    df += 1
            windows.append({
                "from_minor_units": m0, "window": WINDOW,
                "six_sig_divergent": d6, "six_sig_rate": round(d6 / WINDOW, 5),
                "float64_divergent": df, "float64_rate": round(df / WINDOW, 5),
            })

        rows.append({
            "code": code, "name": name, "rate": rate_s,
            "minor_decimals": dn,
            "inverse_six_sig": str(Decimal(I6).scaleb(-e6)),
            "rate_gap_six_sig": "%.6e" % (g_num / g_den),
            "first_divergence_six_sig_minor_units": first6,
            "first_divergence_six_sig_currency_units": (
                None if first6 is None else str(Decimal(first6).scaleb(-dn))),
            "systematic_from_minor_units": systematic,
            "systematic_from_currency_units": (
                None if systematic is None else str(Decimal(systematic).scaleb(-dn))),
            "first_divergence_float64_minor_units": firstf,
            "scan_minor_units": scan_minor_units,
            "magnitude_windows": windows,
        })
    return rows


# ===========================================================================
# M2 -- the permitted set does not agree with itself.
#
# Art. 4(4): national X -> euro -> national Y, "which amount may be rounded to not less than
# three decimals".  So {3, 4, 5, 6 decimals, unrounded} are all permitted intermediates.
# The same sentence then says "No alternative method of calculation may be used unless it
# produces the same results."  Do they produce the same results?
#
# The statute also does not say how to round the intermediate (Art. 5 governs amounts "to be
# paid or accounted for", and the intermediate is neither).  I use half-up and record it.
# ===========================================================================
VARIANTS = [3, 4, 5, 6, None]   # None == not rounded


def triangulate(a, Rx, drx, dnx, Ry, dry, dny, decimals):
    """a minor units of X -> minor units of Y, via the euro, exact integers."""
    # euro = a / 10**dnx * 10**drx / Rx  ==  (a * 10**drx) / (10**dnx * Rx)
    e_num = a * 10 ** drx
    e_den = 10 ** dnx * Rx
    if decimals is not None:
        s = 10 ** decimals
        e_num, e_den = round_half_up(e_num * s, e_den), s
    # y = euro * Ry / 10**dry, rounded to 10**dny minor units
    y_num = e_num * Ry * 10 ** dny
    y_den = e_den * 10 ** dry
    return round_half_up(y_num, y_den)


def m2(scan_minor_units):
    pairs = []
    codes = [c for c, _, _ in RATES]
    seen = set()
    for cx, rx_s, _ in RATES:
        for cy, ry_s, _ in RATES:
            if cx == cy or rx_s == ry_s:
                continue          # BEF/LUF share a rate: the pair is the identity
            key = (cx, cy)
            if key in seen:
                continue
            seen.add(key)
            Rx, drx = parse_rate(rx_s)
            Ry, dry = parse_rate(ry_s)
            dnx, dny = MINOR_DECIMALS[cx], MINOR_DECIMALS[cy]

            first = None
            n_div = 0
            spread_max = 0
            for a in range(1, scan_minor_units + 1):
                vals = [triangulate(a, Rx, drx, dnx, Ry, dry, dny, v) for v in VARIANTS]
                lo, hi = min(vals), max(vals)
                if hi != lo:
                    n_div += 1
                    spread_max = max(spread_max, hi - lo)
                    if first is None:
                        first = a
            pairs.append({
                "from": cx, "to": cy,
                "first_divergence_minor_units": first,
                "first_divergence_currency_units": (
                    None if first is None else str(Decimal(first).scaleb(-dnx))),
                "divergent_amounts_in_scan": n_div,
                "scan_minor_units": scan_minor_units,
                "max_spread_minor_units": spread_max,
            })
    return {"pairs": pairs, "n_pairs": len(pairs), "variants": ["3", "4", "5", "6", "unrounded"]}


# ===========================================================================
# M3 -- the tie-break is a pure election, and the machine default is on the other side.
#
# Euro -> national.  Enumerate the euro amounts (in whole cents) whose exact conversion lands
# EXACTLY half-way between two minor units of the national currency.  On those, Art. 5 says
# round up; IEEE 754-2019's default rounding attribute and Python's decimal default context
# rounding both say round to even.  Count where they part.
# ===========================================================================
def m3(_unused=None):
    """Solved exactly, not scanned, so the statement holds for all amounts and not
    only for a swept range.

    A euro amount of c whole cents converts to  c * R * 10**dn / (100 * 10**dr)  minor units
    of the national currency.  It lands EXACTLY half-way between two minor units iff

        2 * c * R * 10**dn  ==  0  (mod 100 * 10**dr)      and the quotient is odd.

    With  g = gcd(2 * R * 10**dn, 100 * 10**dr)  and  P = (100 * 10**dr) / g, the first
    condition holds iff P divides c; the quotient is then (c/P) * (2*R*10**dn / g), and
    since 2*R*10**dn/g is odd whenever P is minimal, the ties are the ODD multiples of P.
    Verified below against a direct scan rather than asserted.
    """
    from math import gcd
    rows = []
    for code, rate_s, name in RATES:
        R, dr = parse_rate(rate_s)
        dn = MINOR_DECIMALS[code]
        num_k = R * 10 ** dn
        den_k = 100 * 10 ** dr
        g = gcd(2 * num_k, den_k)
        P = den_k // g
        unit_q = (2 * num_k) // g            # quotient contributed by one period
        ties_are_odd_multiples = (unit_q % 2 == 1)

        # the first tie, the first disagreement, and worked examples
        first_tie = first_dis = None
        examples = []
        n_checked = 0
        c = P
        while n_checked < 8:
            n = c * num_k
            if (2 * n) % den_k == 0 and ((2 * n) // den_k) % 2 == 1:
                n_checked += 1
                if first_tie is None:
                    first_tie = c
                up = round_half_up(n, den_k)
                ev = round_half_even(n, den_k)
                if up != ev:
                    if first_dis is None:
                        first_dis = c
                    if len(examples) < 3:
                        examples.append({
                            "euro": str(Decimal(c).scaleb(-2)),
                            "exact_national": str(Decimal((2 * n) // den_k) / 2)
                            if dn == 0 else
                            str(Decimal((2 * n) // den_k).scaleb(-dn) / 2),
                            "statute_half_up": str(Decimal(up).scaleb(-dn)),
                            "machine_half_even": str(Decimal(ev).scaleb(-dn)),
                        })
            c += P
            if c > 10 ** 12:
                break

        # independent check of the closed form against a direct scan
        scan_to = min(200 * P, 4_000_000)
        scan_ties = [cc for cc in range(1, scan_to + 1)
                     if (2 * cc * num_k) % den_k == 0
                     and ((2 * cc * num_k) // den_k) % 2 == 1]
        predicted = [k * P for k in range(1, scan_to // P + 1, 2)] if ties_are_odd_multiples else None
        closed_form_verified = (predicted == scan_ties) if predicted is not None else False
        scan_disagree = sum(1 for cc in scan_ties
                            if round_half_up(cc * num_k, den_k)
                            != round_half_even(cc * num_k, den_k))

        rows.append({
            "code": code, "rate": rate_s, "minor_decimals": dn,
            "tie_period_euro": str(Decimal(P).scaleb(-2)),
            "ties_are_odd_multiples_of_the_period": ties_are_odd_multiples,
            "first_half_way_euro": (None if first_tie is None
                                    else str(Decimal(first_tie).scaleb(-2))),
            "first_disagreement_euro": (None if first_dis is None
                                        else str(Decimal(first_dis).scaleb(-2))),
            "closed_form_verified_against_scan": closed_form_verified,
            "ties_in_verification_scan": len(scan_ties),
            "disagreements_in_verification_scan": scan_disagree,
            "verification_scan_cents": scan_to,
            "examples": examples,
        })
    return rows


# ===========================================================================
# M4 -- the bilateral rate that was never defined.
#
# Reg. 2866/98 recital (5): "no inverse rates nor bilateral rates between the currencies of
# the Member States adopting the euro will be defined".  Define one anyway -- the exact ratio
# of two statutory rates, rounded to six significant figures, exactly as Art. 4(1) would have
# done had the Council chosen pairs instead of a pivot -- and measure how far it lands from
# the mandated triangulation.
# ===========================================================================
def m4(scan_minor_units):
    out = []
    seen = set()
    for cx, rx_s, _ in RATES:
        for cy, ry_s, _ in RATES:
            if cx == cy or rx_s == ry_s or (cx, cy) in seen:
                continue
            seen.add((cx, cy))
            Rx, drx = parse_rate(rx_s)
            Ry, dry = parse_rate(ry_s)
            dnx, dny = MINOR_DECIMALS[cx], MINOR_DECIMALS[cy]
            # bilateral rate  Y per X  = (Ry/10**dry) / (Rx/10**drx)
            B, eb = six_significant(Ry * 10 ** drx, Rx * 10 ** dry)
            b_num = B * 10 ** dny
            b_den = 10 ** eb * 10 ** dnx
            first = None
            n_div = 0
            for a in range(1, scan_minor_units + 1):
                m = triangulate(a, Rx, drx, dnx, Ry, dry, dny, None)
                if round_half_up(a * b_num, b_den) != m:
                    n_div += 1
                    if first is None:
                        first = a
            out.append({
                "from": cx, "to": cy,
                "bilateral_six_sig": str(Decimal(B).scaleb(-eb)),
                "first_divergence_minor_units": first,
                "first_divergence_currency_units": (
                    None if first is None else str(Decimal(first).scaleb(-dnx))),
                "divergent_amounts_in_scan": n_div,
                "scan_minor_units": scan_minor_units,
            })
    return out


def main():
    scan1 = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    scan2 = int(sys.argv[2]) if len(sys.argv) > 2 else 20_000
    scan3 = int(sys.argv[3]) if len(sys.argv) > 3 else 2_000_000
    scan4 = int(sys.argv[4]) if len(sys.argv) > 4 else 200_000

    data = {
        "work": "The Fixed Algorithm",
        "date": "2026-08-11",
        "session": 46,
        "author": "Ulysses",
        "sources": {
            "reg_1103_97": "https://eur-lex.europa.eu/eli/reg/1997/1103/oj/eng",
            "reg_2866_98": "https://eur-lex.europa.eu/eli/reg/1998/2866/oj/eng",
            "ieee754_2019": "https://doi.org/10.1109/IEEESTD.2019.8766229",
            "python_decimal": "https://docs.python.org/3/library/decimal.html",
        },
        "note_on_granularity": (
            "Art. 5 fixes the euro side at the cent and DELEGATES the national side to "
            "'national law or practice'. MINOR_DECIMALS in this script is the author's "
            "modelling choice, not a claim about any national law."),
        "m1_inverse_ban": m1(scan1),
        "m2_permitted_set": m2(scan2),
        "m3_tie_break": m3(),
        "m4_bilateral": m4(scan4),
    }
    with open(OUT, "w") as f:
        json.dump(data, f, indent=1, sort_keys=False)
    print("wrote", OUT)


if __name__ == "__main__":
    main()

# RESULT NOTES follow, appended after the run. Nothing is written here before execution.

# ===========================================================================
# RESULT NOTES -- appended after the first run, at the site of the claim.
# Figures below are read off data.json; nothing here was written before execution.
#
# P1 -- HALF RIGHT, AND THE WRONG HALF WAS THE INFERENCE.
#   Right on the fact: the six-significant-figure inverse does break the last minor unit at
#   ordinary amounts. The earliest onset, measured in money, is 30.86 BEF -- seventy-six euro
#   cents. The other ten fall between EUR 0.76 and EUR 37.34.
#   Wrong on the inference. I predicted this would show the recital "understates its own
#   case". It does not. At those amounts divergence is a one-in-four-thousand event (DEM:
#   0.025 % of amounts near 10^2 minor units); it climbs with magnitude -- 0.05 %, 0.175 %,
#   1.2 %, 11.95 % -- and becomes total by 10^7. The amount from which the rate gap alone
#   exceeds half a minor unit, so that divergence stops being luck, runs from about EUR 2,608
#   (BEF) to about EUR 44,220 (FRF). "Notably if large amounts are involved" is an accurate
#   description of that regime change. I had conflated the ONSET with the RATE; the run
#   separated them and the recital was right about the one that matters.
#
# P2 -- HELD, and more strongly than predicted. The float64 inverse diverges from the mandated
#   division on ZERO amounts, in every window, for all eleven rates, up to 10^8 minor units.
#   The apparatus the letter of Art. 4(3) forbids is, on today's machines, indistinguishable
#   from the one it requires.
#
# P3 -- HELD. All 108 ordered currency pairs diverge among the intermediates Art. 4(4)
#   permits: median 15.6 % of amounts up to 4,000 minor units, maximum 77.6 % (ATS -> BEF /
#   LUF), minimum 1.95 %, spreading by as much as 3 minor units on 18 of the pairs. The
#   earliest onset is one pfennig: 0.01 DEM -> BEF.
#
# P4 -- HELD, and solved in closed form rather than scanned. The exact half-way amounts are
#   the odd multiples of a per-currency period (EUR 50 for BEF/LUF/ITL/ATS, EUR 250 for
#   ESP/PTE, EUR 500 for DEM/FRF/NLG/FIM, EUR 1,250 for IEP), verified against a direct scan
#   for all eleven. The statute's round-half-up and the machine default's round-half-to-even
#   part on exactly half of them.
# ===========================================================================
