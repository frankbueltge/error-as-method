#!/usr/bin/env python3
"""geomag.py — Schmidt semi-normalised spherical-harmonic synthesis of a geomagnetic
main-field model, used here for one output only: the magnetic declination D at a point
on the WGS-84 ellipsoid at a given decimal year.

Two coefficient sets are read by the same routine, which is the point:

  WMM2025.COF        World Magnetic Model 2025, degree 12, epoch 2025.0, linear secular
                     variation, valid 2025.0-2030.0. Used ONLY to check this file
                     against the model's own published test values.
  igrf14coeffs.txt   IGRF-14, degree 13 (10 for the 2025-30 SV column), tabulated every
                     5 years from 1900.0 to 2025.0. Used for the work.

The check matters more than the model. A spherical-harmonic synthesis is easy to write
and easy to get subtly wrong — the Schmidt normalisation, the geodetic-to-geocentric
rotation, the sign of dP/dtheta. WMM2025 ships WMM2025_TestValues.txt, declination
among them, computed by the model's own authors. If this file reproduces those numbers
it is checked against an outside authority rather than merely plausible, which is the
only kind of instrument this practice is willing to measure with. Run

    python3 geomag.py

to perform that check; it prints the worst declination residual over all test rows.

Sources (retrieved 2026-08-13, hashes in sources/MANIFEST.json):
  https://www.ncei.noaa.gov/sites/default/files/2024-12/WMM2025COF.zip
  https://www.ngdc.noaa.gov/IAGA/vmod/coeffs/igrf14coeffs.txt
Formulation: Chulliat, A. et al. (2025), The US/UK World Magnetic Model for 2025-2030:
Technical Report, NOAA NCEI. https://doi.org/10.25923/dnbb-6g33
"""

import math
import os

A_WGS84 = 6378.137                      # WGS-84 semi-major axis, km
F_WGS84 = 1 / 298.257223563
B_WGS84 = A_WGS84 * (1 - F_WGS84)
RE = 6371.2                             # geomagnetic reference radius, km

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources")


# ---------------------------------------------------------------- coefficients

def read_wmm_cof(path):
    """WMM .COF: an epoch header line, then rows 'n m g h dg dh'."""
    g, h, dg, dh, epoch = {}, {}, {}, {}, None
    with open(path) as fh:
        for line in fh:
            p = line.split()
            if not p:
                continue
            if epoch is None:
                epoch = float(p[0])
                continue
            if p[0].startswith("9999"):
                break
            n, m = int(p[0]), int(p[1])
            g[(n, m)], h[(n, m)] = float(p[2]), float(p[3])
            dg[(n, m)], dh[(n, m)] = float(p[4]), float(p[5])
    return epoch, g, h, dg, dh


def wmm_at(epoch, g, h, dg, dh, year):
    dt = year - epoch
    return ({k: v + dt * dg[k] for k, v in g.items()},
            {k: v + dt * dh[k] for k, v in h.items()})


def read_igrf(path):
    """igrf14coeffs.txt -> (epochs, {(kind,n,m): [per-epoch values]}, {(kind,n,m): sv})."""
    epochs, gh, sv = None, {}, {}
    with open(path) as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            p = line.split()
            if not p:
                continue
            if p[0] == "g/h":
                epochs = [float(x) for x in p[3:-1]]     # last column is the SV, not an epoch
                continue
            if p[0] not in ("g", "h"):
                continue
            n, m = int(p[1]), int(p[2])
            gh[(p[0], n, m)] = [float(x) for x in p[3:-1]]
            sv[(p[0], n, m)] = float(p[-1])
    return epochs, gh, sv


def igrf_at(epochs, gh, sv, year):
    """Linear interpolation between tabulated epochs; SV extrapolation beyond the last.

    IGRF is defined this way: the tabulated values are the model at those epochs and
    linear interpolation between them is the prescribed use, as is SV extrapolation for
    the five years past the final epoch.
    """
    g, h = {}, {}
    last = epochs[-1]
    if year >= last:
        dt = year - last
        for (kind, n, m), vals in gh.items():
            (g if kind == "g" else h)[(n, m)] = vals[-1] + dt * sv[(kind, n, m)]
    else:
        year = max(year, epochs[0])
        i = max(j for j, e in enumerate(epochs) if e <= year)
        i = min(i, len(epochs) - 2)
        e0, e1 = epochs[i], epochs[i + 1]
        w = (year - e0) / (e1 - e0)
        for (kind, n, m), vals in gh.items():
            (g if kind == "g" else h)[(n, m)] = vals[i] + w * (vals[i + 1] - vals[i])
    return g, h


# ---------------------------------------------------------------- synthesis

def _schmidt_factors(nmax):
    """S(n,m) = sqrt((2 - delta_m0) * (n-m)! / (n+m)!), converting the unnormalised
    associated Legendre functions produced by the recursion below into Schmidt
    semi-normalised ones. Geomagnetic convention: no Condon-Shortley phase."""
    s = {}
    for n in range(0, nmax + 1):
        for m in range(0, n + 1):
            f = (2.0 if m > 0 else 1.0) * math.factorial(n - m) / math.factorial(n + m)
            s[(n, m)] = math.sqrt(f)
    return s


_S_CACHE = {}


def _legendre(nmax, theta):
    """Schmidt semi-normalised P(n,m)(cos theta) and dP/dtheta, as flat dicts.

    u = cos(theta), w = sin(theta); du/dtheta = -w, dw/dtheta = u.
    """
    u, w = math.cos(theta), math.sin(theta)
    P = {(0, 0): 1.0}
    dP = {(0, 0): 0.0}
    for m in range(1, nmax + 1):                      # sectorial seeds
        P[(m, m)] = (2 * m - 1) * w * P[(m - 1, m - 1)]
        dP[(m, m)] = (2 * m - 1) * (u * P[(m - 1, m - 1)] + w * dP[(m - 1, m - 1)])
    for m in range(0, nmax):                          # one step up in n
        P[(m + 1, m)] = (2 * m + 1) * u * P[(m, m)]
        dP[(m + 1, m)] = (2 * m + 1) * (-w * P[(m, m)] + u * dP[(m, m)])
    for m in range(0, nmax + 1):                      # the rest
        for n in range(m + 2, nmax + 1):
            c = 2 * n - 1
            d = n + m - 1
            P[(n, m)] = (c * u * P[(n - 1, m)] - d * P[(n - 2, m)]) / (n - m)
            dP[(n, m)] = (c * (-w * P[(n - 1, m)] + u * dP[(n - 1, m)])
                          - d * dP[(n - 2, m)]) / (n - m)
    if nmax not in _S_CACHE:
        _S_CACHE[nmax] = _schmidt_factors(nmax)
    S = _S_CACHE[nmax]
    for k in P:
        P[k] *= S[k]
        dP[k] *= S[k]
    return P, dP


def field(g, h, lat_deg, lon_deg, alt_km, nmax):
    """(X, Y, Z) in nT in the local geodetic frame: north, east, down."""
    lat, lon = math.radians(lat_deg), math.radians(lon_deg)

    # geodetic -> geocentric
    sin_lat, cos_lat = math.sin(lat), math.cos(lat)
    rc = A_WGS84 / math.sqrt(1 - (1 - (B_WGS84 / A_WGS84) ** 2) * sin_lat ** 2)
    p = (rc + alt_km) * cos_lat
    z = (rc * (B_WGS84 / A_WGS84) ** 2 + alt_km) * sin_lat
    r = math.hypot(p, z)
    lat_gc = math.asin(z / r)
    theta = math.pi / 2 - lat_gc                       # geocentric colatitude

    P, dP = _legendre(nmax, theta)
    sin_theta = math.sin(theta)

    X = Y = Z = 0.0
    ratio = RE / r
    for n in range(1, nmax + 1):
        rn = ratio ** (n + 2)
        for m in range(0, n + 1):
            gm = g.get((n, m), 0.0)
            hm = h.get((n, m), 0.0)
            if gm == 0.0 and hm == 0.0:
                continue
            cm, sm = math.cos(m * lon), math.sin(m * lon)
            common = gm * cm + hm * sm
            X += rn * common * dP[(n, m)]
            Y += rn * m * (gm * sm - hm * cm) * P[(n, m)] / sin_theta
            Z -= rn * (n + 1) * common * P[(n, m)]

    # rotate the geocentric north/down pair into the geodetic frame
    psi = lat_gc - lat
    Xg = X * math.cos(psi) - Z * math.sin(psi)
    Zg = X * math.sin(psi) + Z * math.cos(psi)
    return Xg, Y, Zg


def declination(g, h, lat_deg, lon_deg, alt_km, nmax):
    """Magnetic declination D in degrees, east of true north positive."""
    X, Y, _ = field(g, h, lat_deg, lon_deg, alt_km, nmax)
    return math.degrees(math.atan2(Y, X))


# ---------------------------------------------------------------- the check

def check_against_wmm_test_values(verbose=True):
    """Reproduce WMM2025_TestValues.txt. Returns (n_rows, worst |dD| in degrees)."""
    epoch, g0, h0, dg, dh = read_wmm_cof(os.path.join(SRC, "WMM2025.COF"))
    rows, worst, worst_row = 0, 0.0, None
    with open(os.path.join(SRC, "WMM2025_TestValues.txt")) as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            p = [float(x) for x in line.split()]
            year, alt, lat, lon, d_ref = p[0], p[1], p[2], p[3], p[4]
            g, h = wmm_at(epoch, g0, h0, dg, dh, year)
            d = declination(g, h, lat, lon, alt, 12)
            diff = abs(((d - d_ref + 180) % 360) - 180)
            rows += 1
            if diff > worst:
                worst, worst_row = diff, (year, alt, lat, lon, d_ref, d)
    if verbose:
        print(f"WMM2025 test values reproduced: {rows} rows, "
              f"worst |dD| = {worst:.4f} deg")
        if worst_row:
            print(f"  worst row: year={worst_row[0]} alt={worst_row[1]} "
                  f"lat={worst_row[2]} lon={worst_row[3]} "
                  f"published D={worst_row[4]} this file D={worst_row[5]:.4f}")
    return rows, worst


if __name__ == "__main__":
    check_against_wmm_test_values()
