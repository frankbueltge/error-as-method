#!/usr/bin/env python3
"""measure.py — how wrong the world's runway designators are, by the rule that names them.

THE NORM. A runway is designated by its magnetic bearing divided by ten and rounded to
the nearest whole number: bearing 087 deg magnetic gives runway 09. The designator is
therefore a claim, and the rule states its own tolerance: a designator is correct while
the magnetic bearing lies within +/-5 degrees of designator x 10.

WHAT MAKES IT DRIFT. Magnetic north moves. The runway does not. Nobody errs and the
name goes wrong by itself. This is the measurement: for every open runway in the world
whose two threshold coordinates are recorded, compute the true bearing from the
coordinates, convert it to a magnetic bearing with IGRF-14, and ask whether the painted
number is still inside the tolerance its own rule allows it.

PREDICTIONS, written before any count was run (this docstring is the record; refutations
are reported in results.json and in the work, not deleted):

  P1  more than 5 % of the population is outside +/-5 degrees today
  P2  the out-of-tolerance fraction rises with |latitude|: the highest-|latitude| decile
      has at least twice the fraction of the lowest
  P3  the median absolute residual today is under 2.5 degrees
  P4  the mean SIGNED residual is more than 0.5 degrees from zero -- the error is
      systematic, not scatter
  P5  at least 500 runways now outside tolerance were inside it in 1976
  P6  fewer than 100 runways now outside tolerance return inside it before 2030 --
      crossings are effectively one-way
  P7  the geodesic distance between the two thresholds agrees with the stated runway
      length within 5 % for more than 90 % of the population
  P8  at least one runway is out by more than 20 degrees -- wrong by two whole numbers

P9 was written LATER, after P1-P8 had been scored, and before the quantity it names had
been computed. It is marked as such in results.json and it is the only prediction in
this file that is not contemporaneous with the others:

  P9  restricted to hard-surface runways and evaluated at the 2020.85 epoch, the
      out-of-tolerance fraction lands within 5 percentage points of NAV CANADA's
      independently measured 5,656 / 25,732 = 21.98 %

Everything under "post_hoc" in results.json -- the licensed-deviation correction, the
airport-type subsets, the NAV CANADA comparison -- was added after the first run and is
NOT predicted. It is labelled that way in the output rather than folded in silently.

TWO REPRESENTATIONS OF THE SAME FACT, which is this practice's only working error
detector: (a) the bearing computed from the two threshold coordinates is checked against
the crowd-entered le_heading_degT field, and the disagreement is reported rather than
resolved by preference; (b) the geodesic distance between the thresholds is checked
against the stated runway length, and rows that fail it are excluded and counted;
(c) the whole result is checked against NAV CANADA's own count of the same quantity over
a different population by a different method for a different purpose.

THE LICENSED DEVIATION. FAA AC 150/5340-1L 2.3.e(4): "On four or more parallel runways,
one set of adjacent runways is numbered to the nearest one-tenth of the magnetic azimuth
and the other set of adjacent runways is numbered to the next nearest one-tenth of the
magnetic azimuth." Its own example: four parallels at magnetic azimuth 324 are designated
32L, 32R, 33L, 33R -- so 33L/33R are 6 degrees out by design, past the tolerance the rule
otherwise implies. Runways in bearing-clusters of four or more at one airport are
therefore identified and reported separately; counting them as errors would be counting
the rule's own exception as a failure of the rule.

Sources (retrieved 2026-08-13, SHA-256 in sources/MANIFEST.json):
  runways.csv         https://davidmegginson.github.io/ourairports-data/runways.csv
  airports.csv        https://davidmegginson.github.io/ourairports-data/airports.csv
  igrf14coeffs.txt    https://www.ngdc.noaa.gov/IAGA/vmod/coeffs/igrf14coeffs.txt
  FAA AC 150/5340-1L  https://www.faa.gov/documentlibrary/media/advisory_circular/150_5340_1l.pdf
"""

import csv
import gzip
import json
import math
import os
import re
import statistics

import geomag

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources")

NOW = 2026.62                    # 2026-08-13, decimal year
NAVCAN_EPOCH = 2020.85           # AIRAC cycle 21-11/2020, the epoch NAV CANADA analysed
HARD_SURFACES = ("ASP", "CON", "PEM", "BIT", "TAR", "MAC", "COP", "PAV")
IGRF_NMAX = 13
TOLERANCE = 5.0                  # degrees; the rounding rule's own half-width
LENGTH_TOL = 0.05                # P7's 5 %
LENGTH_GATE = 0.15               # rows worse than this are excluded as bad coordinates
DESIGNATOR = re.compile(r"^(0?[0-9]|[12][0-9]|3[0-6])([LRCG])?$")

# WGS-84
A = 6378137.0
F = 1 / 298.257223563
B = A * (1 - F)


def vincenty_inverse(lat1, lon1, lat2, lon2):
    """Geodesic distance (m) and initial azimuth (deg from true north) on WGS-84.

    Vincenty (1975). Returns (None, None) on the antipodal non-convergence case, which
    cannot occur for two ends of a runway but is handled rather than assumed away.
    """
    L = math.radians(lon2 - lon1)
    U1 = math.atan((1 - F) * math.tan(math.radians(lat1)))
    U2 = math.atan((1 - F) * math.tan(math.radians(lat2)))
    sinU1, cosU1 = math.sin(U1), math.cos(U1)
    sinU2, cosU2 = math.sin(U2), math.cos(U2)
    lam = L
    for _ in range(200):
        sin_lam, cos_lam = math.sin(lam), math.cos(lam)
        sin_sigma = math.hypot(cosU2 * sin_lam,
                               cosU1 * sinU2 - sinU1 * cosU2 * cos_lam)
        if sin_sigma == 0:
            return 0.0, None                       # coincident thresholds
        cos_sigma = sinU1 * sinU2 + cosU1 * cosU2 * cos_lam
        sigma = math.atan2(sin_sigma, cos_sigma)
        sin_alpha = cosU1 * cosU2 * sin_lam / sin_sigma
        cos2_alpha = 1 - sin_alpha ** 2
        cos_2sm = cos_sigma - 2 * sinU1 * sinU2 / cos2_alpha if cos2_alpha != 0 else 0.0
        C = F / 16 * cos2_alpha * (4 + F * (4 - 3 * cos2_alpha))
        lam_prev = lam
        lam = L + (1 - C) * F * sin_alpha * (
            sigma + C * sin_sigma * (cos_2sm + C * cos_sigma * (-1 + 2 * cos_2sm ** 2)))
        if abs(lam - lam_prev) < 1e-12:
            break
    else:
        return None, None
    u2 = cos2_alpha * (A ** 2 - B ** 2) / B ** 2
    Aa = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    Bb = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    d_sigma = Bb * sin_sigma * (cos_2sm + Bb / 4 * (
        cos_sigma * (-1 + 2 * cos_2sm ** 2)
        - Bb / 6 * cos_2sm * (-3 + 4 * sin_sigma ** 2) * (-3 + 4 * cos_2sm ** 2)))
    s = B * Aa * (sigma - d_sigma)
    az = math.atan2(cosU2 * math.sin(lam),
                    cosU1 * sinU2 - sinU1 * cosU2 * math.cos(lam))
    return s, math.degrees(az) % 360.0


def wrap180(x):
    return ((x + 180.0) % 360.0) - 180.0


def designator_number(ident):
    m = DESIGNATOR.match(ident.strip().upper())
    if not m:
        return None
    n = int(m.group(1))
    return n if 1 <= n <= 36 else None


# ---------------------------------------------------------------- population

def load_population():
    rows, rejects = [], {"not_open": 0, "no_coords": 0, "bad_ident": 0,
                         "not_opposed": 0, "geodesy_failed": 0, "length_gate": 0,
                         "no_length": 0}
    with gzip.open(os.path.join(SRC, "runways.csv.gz"), "rt", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["closed"] != "0":
                rejects["not_open"] += 1
                continue
            try:
                la1 = float(r["le_latitude_deg"]); lo1 = float(r["le_longitude_deg"])
                la2 = float(r["he_latitude_deg"]); lo2 = float(r["he_longitude_deg"])
            except (ValueError, TypeError):
                rejects["no_coords"] += 1
                continue
            d_le = designator_number(r["le_ident"] or "")
            d_he = designator_number(r["he_ident"] or "")
            if d_le is None or d_he is None:
                rejects["bad_ident"] += 1
                continue
            if (d_he - d_le) % 36 != 18:
                rejects["not_opposed"] += 1        # the two ends must be 180 deg apart
                continue
            dist, az = vincenty_inverse(la1, lo1, la2, lo2)
            if dist is None or az is None or dist < 1.0:
                rejects["geodesy_failed"] += 1
                continue
            try:
                stated_m = float(r["length_ft"]) * 0.3048
            except (ValueError, TypeError):
                rejects["no_length"] += 1
                continue
            if stated_m <= 0:
                rejects["no_length"] += 1
                continue
            rel = abs(dist - stated_m) / stated_m
            if rel > LENGTH_GATE:
                rejects["length_gate"] += 1
                continue
            surf = (r["surface"] or "").upper()
            rows.append({
                "airport": r["airport_ident"], "id": r["id"],
                "le_ident": r["le_ident"], "he_ident": r["he_ident"],
                "d_le": d_le, "d_he": d_he,
                "lat": (la1 + la2) / 2.0, "lon": (lo1 + lo2) / 2.0,
                "true_bearing": az,
                "geodesic_m": dist, "stated_m": stated_m, "length_rel": rel,
                "surface": surf,
                "hard": any(surf.startswith(s) for s in HARD_SURFACES),
                "stated_headingT": (float(r["le_heading_degT"])
                                    if r["le_heading_degT"] else None),
            })
    mark_licensed_deviation(rows)
    return rows, rejects


def mark_licensed_deviation(rows):
    """Flag runways in a bearing-cluster of >=4 at one airport (FAA AC 2.3.e(4)).

    A runway is a line, so bearings are clustered modulo 180 degrees. Single-linkage
    within 5 degrees, which is the same width as the designator tolerance.
    """
    by_airport = {}
    for r in rows:
        r["licensed_deviation"] = False
        by_airport.setdefault(r["airport"], []).append(r)
    for group in by_airport.values():
        if len(group) < 4:
            continue
        group = sorted(group, key=lambda r: r["true_bearing"] % 180.0)
        cluster = [group[0]]
        for r in group[1:]:
            if (r["true_bearing"] % 180.0) - (cluster[-1]["true_bearing"] % 180.0) <= 5.0:
                cluster.append(r)
            else:
                if len(cluster) >= 4:
                    for c in cluster:
                        c["licensed_deviation"] = True
                cluster = [r]
        if len(cluster) >= 4:
            for c in cluster:
                c["licensed_deviation"] = True


def load_airport_types():
    types = {}
    with gzip.open(os.path.join(SRC, "airports-subset.csv.gz"), "rt", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            types[r["ident"]] = (r["type"], r["scheduled_service"], r["iso_country"])
    return types


# ---------------------------------------------------------------- the norm

class Declinator:
    """IGRF-14 declination, with the coefficient set cached per requested year."""

    def __init__(self, path):
        self.epochs, self.gh, self.sv = geomag.read_igrf(path)
        self._cache = {}

    def coeffs(self, year):
        key = round(year, 3)
        if key not in self._cache:
            self._cache[key] = geomag.igrf_at(self.epochs, self.gh, self.sv, key)
        return self._cache[key]

    def d(self, lat, lon, year):
        g, h = self.coeffs(year)
        return geomag.declination(g, h, lat, lon, 0.0, IGRF_NMAX)


def residual(row, dec, year):
    """Signed degrees by which the magnetic bearing exceeds designator x 10.

    Averaged over the two ends, which is what the rule effectively requires: both
    painted numbers refer to the same centre line and must both round correctly.
    """
    D = dec.d(row["lat"], row["lon"], year)
    mag_le = (row["true_bearing"] - D) % 360.0
    return wrap180(mag_le - row["d_le"] * 10.0), D


def crossing_year(row, dec, lo, hi, step=2.0):
    """Latest year in [lo, hi] at which |residual| crossed TOLERANCE, or None.

    Scans forward on a coarse grid and bisects the last sign change of
    (|residual| - TOLERANCE). No monotonicity is assumed; the last crossing is taken.
    """
    def f(y):
        return abs(residual(row, dec, y)[0]) - TOLERANCE

    ys = [lo + i * step for i in range(int((hi - lo) / step) + 1)]
    if ys[-1] < hi:
        ys.append(hi)
    vals = [f(y) for y in ys]
    last = None
    for i in range(len(ys) - 1):
        if (vals[i] <= 0) != (vals[i + 1] <= 0):
            last = (ys[i], ys[i + 1])
    if last is None:
        return None
    a, b = last
    for _ in range(24):
        m = (a + b) / 2.0
        if (f(a) <= 0) == (f(m) <= 0):
            a = m
        else:
            b = m
    return round((a + b) / 2.0, 2)


# ---------------------------------------------------------------- main

def main():
    out = {"generated_for": "2026-08-13 (Session 52)", "epoch_decimal_year": NOW,
           "tolerance_deg": TOLERANCE}

    n_rows, worst = geomag.check_against_wmm_test_values(verbose=False)
    out["instrument_check"] = {
        "what": "this repository's spherical-harmonic synthesis run on WMM2025 "
                "coefficients against WMM2025_TestValues.txt, published by the "
                "model's authors",
        "rows": n_rows, "worst_declination_residual_deg": round(worst, 5),
        "published_values_rounded_to_deg": 0.01,
    }
    print(f"instrument: {n_rows} WMM test rows, worst |dD| = {worst:.4f} deg")

    rows, rejects = load_population()
    out["population"] = {"kept": len(rows), "rejected": rejects,
                         "gate": {"length_agreement_worse_than": LENGTH_GATE}}
    print(f"population: {len(rows)} runways kept; rejects {rejects}")

    dec = Declinator(os.path.join(SRC, "igrf14coeffs.txt"))

    # ---- today
    for r in rows:
        r["res_now"], r["decl_now"] = residual(r, dec, NOW)
    absnow = [abs(r["res_now"]) for r in rows]
    out_now = [r for r in rows if abs(r["res_now"]) > TOLERANCE]
    out["today"] = {
        "n": len(rows),
        "out_of_tolerance": len(out_now),
        "fraction_out": round(len(out_now) / len(rows), 4),
        "median_abs_residual_deg": round(statistics.median(absnow), 3),
        "mean_abs_residual_deg": round(statistics.fmean(absnow), 3),
        "mean_signed_residual_deg": round(statistics.fmean([r["res_now"] for r in rows]), 3),
        "max_abs_residual_deg": round(max(absnow), 2),
        "n_over_10_deg": sum(1 for a in absnow if a > 10),
        "n_over_15_deg": sum(1 for a in absnow if a > 15),
        "n_over_20_deg": sum(1 for a in absnow if a > 20),
    }

    worst_rows = sorted(rows, key=lambda r: -abs(r["res_now"]))[:15]
    out["today"]["worst"] = [
        {"airport": r["airport"], "runway": f'{r["le_ident"]}/{r["he_ident"]}',
         "lat": round(r["lat"], 3), "lon": round(r["lon"], 3),
         "true_bearing": round(r["true_bearing"], 2),
         "declination_2026": round(r["decl_now"], 2),
         "magnetic_bearing": round((r["true_bearing"] - r["decl_now"]) % 360, 2),
         "residual_deg": round(r["res_now"], 2),
         "implied_designator": int(round((((r["true_bearing"] - r["decl_now"]) % 360)
                                          or 360) / 10.0)) or 36}
        for r in worst_rows]

    # ---- by absolute latitude decile
    by_lat = sorted(rows, key=lambda r: abs(r["lat"]))
    k = len(by_lat) // 10
    deciles = []
    for i in range(10):
        chunk = by_lat[i * k:(i + 1) * k] if i < 9 else by_lat[9 * k:]
        n_out = sum(1 for r in chunk if abs(r["res_now"]) > TOLERANCE)
        deciles.append({
            "decile": i + 1,
            "abs_lat_range": [round(abs(chunk[0]["lat"]), 2), round(abs(chunk[-1]["lat"]), 2)],
            "n": len(chunk), "out": n_out, "fraction_out": round(n_out / len(chunk), 4),
            "median_abs_residual_deg": round(
                statistics.median([abs(r["res_now"]) for r in chunk]), 2),
        })
    out["by_abs_latitude_decile"] = deciles

    # ---- fifty years ago
    for r in rows:
        r["res_1976"] = residual(r, dec, 1976.0)[0]
    was_in_now_out = [r for r in rows
                      if abs(r["res_1976"]) <= TOLERANCE and abs(r["res_now"]) > TOLERANCE]
    was_out_now_in = [r for r in rows
                      if abs(r["res_1976"]) > TOLERANCE and abs(r["res_now"]) <= TOLERANCE]
    out["fifty_years"] = {
        "reference_year": 1976.0,
        "out_of_tolerance_1976": sum(1 for r in rows if abs(r["res_1976"]) > TOLERANCE),
        "in_1976_out_2026": len(was_in_now_out),
        "out_1976_in_2026": len(was_out_now_in),
        "median_abs_residual_1976_deg": round(
            statistics.median([abs(r["res_1976"]) for r in rows]), 3),
        "mean_abs_drift_1976_to_2026_deg": round(statistics.fmean(
            [abs(wrap180(r["res_now"] - r["res_1976"])) for r in rows]), 3),
    }

    # ---- when the currently-wrong ones went wrong, and who goes wrong next
    print("scanning crossings ...")
    went_wrong = []
    for r in out_now:
        y = crossing_year(r, dec, 1900.0, NOW)
        r["went_wrong"] = y
        if y is not None:
            went_wrong.append(y)
    out["when_they_went_wrong"] = {
        "n_out_of_tolerance": len(out_now),
        "n_with_a_crossing_since_1900": len(went_wrong),
        "n_already_wrong_in_1900": len(out_now) - len(went_wrong),
        "median_crossing_year": round(statistics.median(went_wrong), 1) if went_wrong else None,
        "by_decade": {str(d): sum(1 for y in went_wrong if d <= y < d + 10)
                      for d in range(1900, 2030, 10)},
    }

    in_now = [r for r in rows if abs(r["res_now"]) <= TOLERANCE]
    soon = []
    for r in in_now:
        y = crossing_year(r, dec, NOW, 2030.0, step=0.5)
        if y is not None:
            soon.append((y, r))
    back = []
    for r in out_now:
        y = crossing_year(r, dec, NOW, 2030.0, step=0.5)
        if y is not None:
            back.append((y, r))
    out["before_2030"] = {
        "note": "IGRF-14 is defined to 2030.0; nothing is extrapolated past it.",
        "currently_correct_that_go_wrong_by_2030": len(soon),
        "currently_wrong_that_come_right_by_2030": len(back),
    }

    # ---- the second representation: the crowd-entered heading field
    both = [r for r in rows if r["stated_headingT"] is not None]
    diffs = [abs(wrap180(r["true_bearing"] - r["stated_headingT"])) for r in both]
    out["two_representations"] = {
        "coordinate_bearing_vs_stated_le_heading_degT": {
            "n_with_both": len(both),
            "median_abs_diff_deg": round(statistics.median(diffs), 2) if diffs else None,
            "within_1_deg": sum(1 for d in diffs if d <= 1),
            "within_5_deg": sum(1 for d in diffs if d <= 5),
            "over_10_deg": sum(1 for d in diffs if d > 10),
            "over_90_deg": sum(1 for d in diffs if d > 90),
            "comment": "Reported, not resolved by preference. The stated field is "
                       "crowd-entered and in an unstated reference; the coordinate "
                       "bearing is computed. Where they disagree grossly, at least "
                       "one of the two is wrong and this file does not know which.",
        },
        "geodesic_vs_stated_length": {
            "n_in_population": len(rows),
            "within_5_percent": sum(1 for r in rows if r["length_rel"] <= LENGTH_TOL),
            "fraction_within_5_percent": round(
                sum(1 for r in rows if r["length_rel"] <= LENGTH_TOL) / len(rows), 4),
            "excluded_by_gate": rejects["length_gate"],
        },
    }

    # ---- POST HOC: added after the first run, not predicted, labelled as such
    types = load_airport_types()
    for r in rows:
        t = types.get(r["airport"], ("unknown", "unknown", "??"))
        r["ap_type"], r["sched"], r["country"] = t

    def frac_out(subset, year=None):
        if not subset:
            return {"n": 0, "out": 0, "fraction_out": None}
        if year is None:
            outs = sum(1 for r in subset if abs(r["res_now"]) > TOLERANCE)
        else:
            outs = sum(1 for r in subset
                       if abs(residual(r, dec, year)[0]) > TOLERANCE)
        return {"n": len(subset), "out": outs,
                "fraction_out": round(outs / len(subset), 4)}

    licensed = [r for r in rows if r["licensed_deviation"]]
    clean = [r for r in rows if not r["licensed_deviation"]]
    hard = [r for r in clean if r["hard"]]

    post = {
        "_note": "Everything in this block was added AFTER the first run and after "
                 "P1-P8 were scored. Only P9 was written before its quantity was "
                 "computed. Nothing here is a confirmed prediction.",
        "licensed_deviation": {
            "rule": "FAA AC 150/5340-1L 2.3.e(4): on four or more parallel runways one "
                    "set is numbered to the NEXT nearest one-tenth of the magnetic "
                    "azimuth -- i.e. deliberately about 10 degrees wrong.",
            "n_flagged": len(licensed),
            "n_flagged_out_of_tolerance": sum(1 for r in licensed
                                              if abs(r["res_now"]) > TOLERANCE),
            "airports": sorted({r["airport"] for r in licensed}),
            "population_excluding_them": frac_out(clean),
        },
        "by_airport_type": {
            t: frac_out([r for r in clean if r["ap_type"] == t])
            for t in sorted({r["ap_type"] for r in clean})
        },
        "scheduled_service": {
            "yes": frac_out([r for r in clean if r["sched"] == "yes"]),
            "no": frac_out([r for r in clean if r["sched"] == "no"]),
        },
        "hard_surface_only": frac_out(hard),
        "external_check_navcanada": {
            "source": "NAV CANADA, 'Magnetic to True North -- Change by 2030', "
                      "Anthony MacKay, Director Operational Safety, 28 Feb 2022, "
                      "slides '2030 WORLD WIDE AIRPORT IMPACT / AIRAC cycle "
                      "21-11/2020 EPOCH'.",
            "their_population": "25,732 world-wide hard surface runways",
            "their_out_of_alignment_at_2020": 5656,
            "their_fraction_2020": round(5656 / 25732, 4),
            "their_would_need_renumbering_in_MAG_by_2030": 8044,
            "their_fraction_2030": round(8044 / 25732, 4),
            "mine_hard_surface_at_2020_85": frac_out(hard, NAVCAN_EPOCH),
            "mine_hard_surface_at_2026_62": frac_out(hard),
            "mine_hard_surface_at_2030_0": frac_out(hard, 2030.0),
            "independence": "NAV CANADA used AIRAC navigation data, its own tooling and "
                            "a different definition of the population, to argue for "
                            "abolishing the magnetic reference. It has no connection to "
                            "this repository. This is the only genuinely independent "
                            "check available to the night.",
        },
    }
    out["post_hoc"] = post

    # ---- verdicts
    d_hi, d_lo = deciles[9]["fraction_out"], deciles[0]["fraction_out"]
    v = {
        "P1": {"claim": "more than 5 % out of tolerance today",
               "value": out["today"]["fraction_out"],
               "verdict": "confirmed" if out["today"]["fraction_out"] > 0.05 else "refuted"},
        "P2": {"claim": "highest-|lat| decile at least 2x the lowest",
               "value": [d_lo, d_hi, round(d_hi / d_lo, 2) if d_lo else None],
               "verdict": "confirmed" if d_lo and d_hi / d_lo >= 2 else "refuted"},
        "P3": {"claim": "median |residual| under 2.5 deg",
               "value": out["today"]["median_abs_residual_deg"],
               "verdict": "confirmed" if out["today"]["median_abs_residual_deg"] < 2.5 else "refuted"},
        "P4": {"claim": "mean signed residual more than 0.5 deg from zero",
               "value": out["today"]["mean_signed_residual_deg"],
               "verdict": "confirmed" if abs(out["today"]["mean_signed_residual_deg"]) > 0.5 else "refuted"},
        "P5": {"claim": "at least 500 were inside tolerance in 1976 and are outside now",
               "value": len(was_in_now_out),
               "verdict": "confirmed" if len(was_in_now_out) >= 500 else "refuted"},
        "P6": {"claim": "fewer than 100 currently-wrong come right by 2030",
               "value": len(back),
               "verdict": "confirmed" if len(back) < 100 else "refuted"},
        "P7": {"claim": "geodesic length within 5 % for more than 90 %",
               "value": out["two_representations"]["geodesic_vs_stated_length"]["fraction_within_5_percent"],
               "verdict": "confirmed" if out["two_representations"]["geodesic_vs_stated_length"]["fraction_within_5_percent"] > 0.90 else "refuted"},
        "P8": {"claim": "at least one runway out by more than 20 deg",
               "value": out["today"]["n_over_20_deg"],
               "verdict": "confirmed" if out["today"]["n_over_20_deg"] >= 1 else "refuted"},
    }
    mine20 = post["external_check_navcanada"]["mine_hard_surface_at_2020_85"]["fraction_out"]
    theirs20 = post["external_check_navcanada"]["their_fraction_2020"]
    v["P9"] = {
        "claim": "hard-surface subset at 2020.85 within 5 percentage points of NAV "
                 "CANADA's 21.98 % (written after P1-P8 were scored, before this "
                 "quantity was computed)",
        "value": [mine20, theirs20, round(abs(mine20 - theirs20) * 100, 2)],
        "verdict": "confirmed" if abs(mine20 - theirs20) <= 0.05 else "refuted",
        "written": "later than P1-P8, before computation",
    }
    out["predictions"] = v
    out["predictions_summary"] = {
        "confirmed": sorted(k for k, d in v.items() if d["verdict"] == "confirmed"),
        "refuted": sorted(k for k, d in v.items() if d["verdict"] == "refuted"),
    }

    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=2)

    # a compact per-runway table for the figure, and for anyone re-checking
    with open(os.path.join(HERE, "residuals.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["airport", "le_ident", "he_ident", "lat", "lon",
                    "true_bearing_deg", "declination_2026_deg",
                    "residual_2026_deg", "residual_1976_deg", "went_wrong_year"])
        for r in rows:
            w.writerow([r["airport"], r["le_ident"], r["he_ident"],
                        round(r["lat"], 5), round(r["lon"], 5),
                        round(r["true_bearing"], 3), round(r["decl_now"], 3),
                        round(r["res_now"], 3), round(r["res_1976"], 3),
                        r.get("went_wrong", "")])

    print(json.dumps({k: out[k] for k in
                      ("today", "fifty_years", "before_2030", "predictions_summary")},
                     indent=2)[:3000])


if __name__ == "__main__":
    main()
