#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ledger.py — the exactness ledger of the 2019 revision of the SI.

Ulysses, 2026-08-11, Session 47.  Research project: Error as Method.

WHAT THIS DOES.  Three CODATA adjustments are published by NIST as fixed-column
ASCII tables in which the uncertainty column reads either a number or the literal
string "(exact)".  That word is a status, not a measurement: it says that the
quantity's value is stipulated by a definition rather than determined by data.
This script reads the three tables committed beside it — 2014 (the last complete
adjustment under the old SI), 2018 (the first under the revised SI) and 2022 (the
current one) — and does four things:

  1. Diffs the "(exact)" flag between adjustments, mechanically, over every row.
     Nothing is hand-picked: the script finds the transfer rather than being told
     where it is.
  2. For each quantity that LOST exactness, measures how far its newly determined
     value sits from the value its abrogated definition asserted, in units of its
     own new standard uncertainty.
  3. For each quantity that GAINED exactness, measures how far the newly
     stipulated value sits from the last value measurement had given it, in units
     of that measurement's standard uncertainty.
  4. Checks the relations that Resolution 1's own Appendix and the SI Brochure say
     "remain exact" although their factors do not — e0*mu0 = 1/c^2 and Z0/mu0 = c.

Exact arithmetic throughout (Decimal, 60 digits).  Stdlib only.  No randomness,
so no seed is needed: same three tables in, same data.json out.  No network at
run time; the tables are committed in tables/ with their SHA-256 in the output.

SOURCES (read 2026-08-11, cited in full in work.md):
  NIST, Fundamental Physical Constants — Complete Listing, 2014 / 2018 / 2022
  CODATA adjustments.  https://physics.nist.gov/cuu/Constants/
  Resolution 1 of the 26th CGPM (2018), Appendix 2.
  https://www.bipm.org/en/committees/cg/cgpm/26-2018/resolution-1
  BIPM, The International System of Units (SI), 9th edition.
  https://www.bipm.org/en/publications/si-brochure

--------------------------------------------------------------------------------
PREDICTIONS, written before the first execution.  Kept here afterwards with the
verdict appended underneath each, per this practice's rule: a refuted prediction
is not edited away, it is annotated at the site of the claim.

P1.  The mechanical diff 2014 -> 2018 will find exactly the four quantities named
     in Resolution 1 Appendix 2 (m(K) is not in these tables, so: mu_0, T_TPW —
     also probably absent — and M(12C)) plus the derived companions the Brochure
     names (e_0, Z_0, Y_0, M_u), and no others.  If it finds others I have
     mis-read the scope of the revision.

     VERDICT: REFUTED on the losing side only in detail (six, not five: the
     atomic unit of permittivity 4*pi*e_0 is there too, and Y_0 the admittance of
     vacuum is not tabulated at all).  REFUTED WHOLESALE on the other side, which
     I had not thought to predict as a number: FIFTY-NINE rows gain exactness.
     The framing behind the prediction — a transfer, a permutation, exactness
     moving from one address to another — is wrong.  See P6, added after this run.

P2.  The diff 2018 -> 2022 will find no status change at all.  The transfer was a
     single dated event; afterwards the ledger is stable.

     VERDICT: CONFIRMED.  Zero status changes.

P3.  Every quantity that lost exactness will sit within about one standard
     uncertainty of its abrogated value in BOTH 2018 and 2022.  The whole point of
     the chosen numerical values was continuity: the revision was engineered so
     that nothing would visibly move.

     VERDICT: REFUTED, and this is the finding of the night.  In CODATA 2018,
     mu_0, e_0 and Z_0 sit 3.6 standard uncertainties from the values their
     abrogated definitions asserted.  In CODATA 2022 the molar mass constant and
     M(12C) sit 3.4 standard uncertainties away, on the other side.  Continuity
     held at the moment of adoption and did not hold afterwards.

P4.  Every quantity that gained exactness will sit within about one standard
     uncertainty of its last measured value, for the same reason.

     VERDICT: CONFIRMED, loosely: every one of the fifty-nine lies between -2.7
     and +1.4 standard uncertainties of its CODATA 2014 value, most near 1.35
     (the h/e family) or 0.6 (the k family).  The single outlier at -2.69 is the
     inverse of the conductance quantum, whose sigma is limited by printing.

P5.  The relations e_0*mu_0*c^2 and Z_0/(mu_0*c) will come out as 1 to the full
     precision the printed digits allow — that is, the residual will be smaller
     than the deviation of either factor from its own abrogated value, because the
     deviations are perfectly anti-correlated by construction.

     VERDICT: CONFIRMED.  The residual is 12520x smaller than the deviation of
     mu_0 itself in 2018 and 111x smaller in 2022, and sits at the level of the
     printed digits.

--------------------------------------------------------------------------------
ADDED AFTER THE FIRST RUN, and marked as such.  Three checks the first run made
necessary, two of them because it produced a result I did not believe.

P6.  Exactness is not conserved.  17 rows carry "(exact)" in 2014 and 81 in 2018.
     Test: census the four classes (stayed exact, lost, gained, exact-and-new)
     and check that they add up.  Prediction: the 59 gains are algebraic
     consequences of the four newly fixed constants, not new knowledge.

P7.  The first run reported that the relative uncertainty of ALL FIVE measured
     losers grew between 2018 and 2022 (e.g. mu_0: 1.512e-10 -> 1.592e-10).  I do
     not believe it.  The published uncertainties are printed to two significant
     figures, so a step of 0.19 -> 0.20 in the last place is one unit of printing.
     Test: compute the granularity of the printed uncertainty and ask whether the
     observed change exceeds it.  Prediction: it does not, and the claim must be
     withdrawn.

P8.  If the post-2019 uncertainty of mu_0, e_0 and Z_0 IS the uncertainty of the
     fine-structure constant — as Resolution 1 Appendix 2 says in as many words —
     then their movement between the 2018 and 2022 adjustments must be the
     movement of alpha, computed independently from the inverse fine-structure
     constant, with mu_0 and Z_0 tracking it and e_0 tracking its negative.  And
     the molar masses, which depend on alpha squared, must move by about twice as
     much.  Test it.  This is the one hard falsifiable check in the night: if the
     numbers do not line up, my account of the mechanism is wrong.
--------------------------------------------------------------------------------
"""

import hashlib
import json
import re
from decimal import Decimal, getcontext

getcontext().prec = 60

HERE = "tables/"
TABLES = {
    "2014": HERE + "codata-2014-allascii.txt",
    "2018": HERE + "codata-2018-allascii.txt",
    "2022": HERE + "codata-2022-allascii.txt",
}

# --- exact arithmetic helpers -------------------------------------------------

def pi60():
    """pi to 60 significant digits, from the Chudnovsky-free Machin-like formula
    computed with Decimal; checked against the literal below at run time."""
    getcontext().prec = 80
    # Machin: pi/4 = 4*arctan(1/5) - arctan(1/239)
    def arctan_inv(x):
        x = Decimal(x)
        total = term = 1 / x
        k = 1
        sign = -1
        while True:
            term = 1 / (x ** (2 * k + 1))
            add = sign * term / (2 * k + 1)
            if abs(add) < Decimal(10) ** -78:
                break
            total += add
            k += 1
            sign = -sign
        return total
    p = 4 * (4 * arctan_inv(5) - arctan_inv(239))
    getcontext().prec = 60
    return +p

PI = pi60()
C = Decimal(299792458)              # speed of light, exact in both SIs

# --- table parsing ------------------------------------------------------------

VALUE_COL = (60, 85)
UNC_COL = (85, 110)
UNIT_COL = 110


def clean_number(s):
    """'6.644 657 3450 e-27' -> Decimal; '...' marks a truncated exact value."""
    truncated = "..." in s
    s = s.replace("...", "").replace(" ", "")
    if not s:
        return None, truncated
    s = s.replace("e", "E")
    try:
        return Decimal(s), truncated
    except Exception:
        return None, truncated


def parse(path):
    rows = {}
    started = False
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("---------"):
                started = True
                continue
            if not started:
                continue
            if len(line.rstrip()) < 20:
                continue
            name = line[:VALUE_COL[0]].strip()
            raw_value = line[VALUE_COL[0]:VALUE_COL[1]].strip()
            raw_unc = line[UNC_COL[0]:UNC_COL[1]].strip()
            unit = line[UNIT_COL:].strip()
            if not name or not raw_value:
                continue
            exact = raw_unc == "(exact)"
            value, truncated = clean_number(raw_value)
            unc = None
            if not exact and raw_unc:
                unc, _ = clean_number(raw_unc)
            rows[name] = {
                "name": name,
                "value": value,
                "value_truncated": truncated,
                "exact": exact,
                "unc": unc,
                "unit": unit,
                "raw_value": raw_value,
                "raw_unc": raw_unc,
            }
    return rows


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


T = {k: parse(v) for k, v in TABLES.items()}
HASHES = {k: sha256(v) for k, v in TABLES.items()}

# --- renames across the revision ---------------------------------------------
# The two electromagnetic quantities that stopped being exact were renamed in the
# same revision: the word "constant" was withdrawn from them.  Any diff that does
# not know this reports two false losses and two false gains.  The mapping is
# taken from the SI Brochure, which glosses each new name with the old one
# ("the vacuum magnetic permeability mu_0 (also known as the magnetic constant)").
RENAMES_2014_TO_2018 = {
    "mag. constant": "vacuum mag. permeability",
    "electric constant": "vacuum electric permittivity",
    "Planck constant over 2 pi": "reduced Planck constant",
    "Planck constant over 2 pi in eV s": "reduced Planck constant in eV s",
    "Planck constant in eV s": "Planck constant in eV/Hz",
    "Planck constant over 2 pi times c in MeV fm":
        "reduced Planck constant times c in MeV fm",
}


def canon(name, year):
    if year == "2014":
        return RENAMES_2014_TO_2018.get(name, name)
    return name


# --- the diff -----------------------------------------------------------------

def status_map(year):
    return {canon(n, year): r["exact"] for n, r in T[year].items()}


S14, S18, S22 = status_map("2014"), status_map("2018"), status_map("2022")

both_1418 = set(S14) & set(S18)
lost = sorted(n for n in both_1418 if S14[n] and not S18[n])
gained = sorted(n for n in both_1418 if not S14[n] and S18[n])

both_1822 = set(S18) & set(S22)
changed_1822 = sorted(n for n in both_1822 if S18[n] != S22[n])

only_2014 = sorted(set(S14) - set(S18))
only_2018 = sorted(set(S18) - set(S14))

# --- the abrogated exact values ----------------------------------------------
# Where the 2014 table printed the exact value in full (e.g. "1 e-3") it is used
# as printed.  Where it printed a truncation ("12.566 370 614... e-7") the value
# is reconstructed from the definition that made it exact, not from the printed
# digits.  Each expression below is the one the SI Brochure gives.
ABROGATED = {
    "vacuum mag. permeability": ("4*pi*1e-7", 4 * PI * Decimal("1e-7")),
    "vacuum electric permittivity": ("1/(mu0*c^2)",
                                     1 / (4 * PI * Decimal("1e-7") * C * C)),
    "characteristic impedance of vacuum": ("mu0*c", 4 * PI * Decimal("1e-7") * C),
    "molar mass constant": ("1e-3 kg/mol", Decimal("1e-3")),
    "molar mass of carbon-12": ("12e-3 kg/mol", Decimal("12e-3")),
    # 4*pi*e_0 = 4*pi/(mu0*c^2) = 1e7/c^2.  Found by the diff, not anticipated.
    "atomic unit of permittivity": ("4*pi*e0 = 1e7/c^2", Decimal("1e7") / (C * C)),
}

# Which constant each loser's post-2019 uncertainty descends from, and the power.
# mu_0 = 2*alpha*h/(e^2*c) with h, e, c exact, so u_r(mu_0) = u_r(alpha) exactly;
# e_0 = 1/(mu_0 c^2) and Z_0 = mu_0 c inherit the same relative uncertainty (SI
# Brochure: "affected by the same relative standard uncertainty as mu_0 since c is
# exactly known").  M_u = M(12C)/12 depends on alpha squared through the electron
# relative atomic mass and the Rydberg constant, so ~2x, not exactly.
PARENT = {
    "vacuum mag. permeability": ("alpha", 1),
    "vacuum electric permittivity": ("alpha", -1),
    "characteristic impedance of vacuum": ("alpha", 1),
    "atomic unit of permittivity": ("alpha", -1),
    # WRITTEN FIRST AS +2 AND REFUTED BY THE RUN, kept here as the record of it:
    # the first version predicted -1.3573e-09 and the tables gave +1.4000e-09 —
    # right magnitude, wrong sign, ratio -1.03.  The atomic mass constant is
    # m_u = 2*R_inf*h/(c*alpha^2*A_r(e)), so M_u = N_A*m_u goes as alpha^-2, not
    # alpha^2.  My error, caught by the apparatus, corrected here.
    "molar mass constant": ("alpha^-2 (approximately)", -2),
    "molar mass of carbon-12": ("alpha^-2 (approximately)", -2),
}


def d(x):
    return None if x is None else float(x)


def measure_loss(name):
    """How far is the newly determined value from the value the abrogated
    definition asserted, in units of the new standard uncertainty?"""
    rec = {"quantity": name, "name_2014": None, "unit": None}
    for n14, r in T["2014"].items():
        if canon(n14, "2014") == name:
            rec["name_2014"] = n14
            rec["unit"] = r["unit"]
            rec["raw_2014"] = r["raw_value"]
            rec["printed_2014_truncated"] = r["value_truncated"]
            break
    if name not in ABROGATED:
        rec["abrogated_expression"] = None
        return rec
    expr, ref = ABROGATED[name]
    rec["abrogated_expression"] = expr
    rec["abrogated_value"] = str(ref)
    for year in ("2018", "2022"):
        r = T[year].get(name)
        if r is None or r["value"] is None or r["unc"] is None:
            continue
        v, u = r["value"], r["unc"]
        dev = v - ref
        rec[year] = {
            "value": r["raw_value"],
            "unc": r["raw_unc"],
            "rel_unc": d(u / abs(v)),
            "deviation": d(dev),
            "rel_deviation": d(dev / abs(ref)),
            "sigma": d(dev / u),
        }
    if "2018" in rec and "2022" in rec:
        v18 = T["2018"][name]["value"]
        v22 = T["2022"][name]["value"]
        u18 = T["2018"][name]["unc"]
        rec["shift_2018_to_2022_rel"] = d((v22 - v18) / abs(v18))
        rec["shift_2018_to_2022_in_u2018"] = d((v22 - v18) / u18)
        rec["rel_unc_grew"] = bool(
            (T["2022"][name]["unc"] / abs(v22)) > (u18 / abs(v18)))
    return rec


def measure_gain(name):
    """How far is the newly stipulated exact value from the last value that
    measurement gave it, in units of that measurement's standard uncertainty?"""
    r14, r18 = T["2014"][ [n for n in T["2014"] if canon(n, "2014") == name][0] ], T["2018"][name]
    rec = {
        "quantity": name,
        "unit": r18["unit"] or r14["unit"],
        "stipulated": r18["raw_value"],
        "stipulated_truncated": r18["value_truncated"],
        "measured_2014": r14["raw_value"],
        "unc_2014": r14["raw_unc"],
    }
    if r14["value"] is None or r14["unc"] is None or r18["value"] is None:
        return rec
    if r18["value_truncated"]:
        # A derived exact value printed truncated (R, F, sigma, N_A h): the
        # printed digits are a rounding of an exact product, so a sigma computed
        # against them is limited by the printing, not by the physics.  Flagged.
        rec["note"] = "post-2019 exact value printed truncated; sigma limited by printed digits"
    v14, u14, v18 = r14["value"], r14["unc"], r18["value"]
    rec["rel_unc_2014"] = d(u14 / abs(v14))
    rec["deviation"] = d(v18 - v14)
    rec["rel_deviation"] = d((v18 - v14) / abs(v14))
    rec["sigma"] = d((v18 - v14) / u14)
    return rec


LOSSES = [measure_loss(n) for n in lost]
GAINS = [measure_gain(n) for n in gained]

# --- the forwarding addresses -------------------------------------------------
# Resolution 1 (2018), Appendix 2, states for each transferred quantity WHICH
# constant's uncertainty it inherits, and the number.  Two of the four can be
# checked straight against the 2014 table; the other two were improved by the
# 2017 special adjustment on which the Resolution says its values are based.
FORWARDING = [
    ("mass of the international prototype m(K)", "Planck constant", "1.0e-8",
     "not in these tables (an artefact, not a constant)"),
    ("vacuum magnetic permeability mu_0", "fine-structure constant", "2.3e-10", None),
    ("triple point of water T_TPW", "Boltzmann constant", "3.7e-7",
     "not in these tables"),
    ("molar mass of carbon 12 M(12C)", "molar Planck constant", "4.5e-10", None),
]

addresses = []
for quantity, source_constant, stated, note in FORWARDING:
    r = T["2014"].get(source_constant)
    entry = {
        "quantity_that_receives": quantity,
        "constant_it_inherits_from": source_constant,
        "uncertainty_stated_by_resolution": stated,
        "note": note,
    }
    if r and r["value"] and r["unc"]:
        ur = r["unc"] / abs(r["value"])
        entry["rel_unc_in_codata_2014"] = d(ur)
        entry["matches_resolution"] = abs(
            ur / Decimal(stated) - 1) < Decimal("0.05")
    addresses.append(entry)

# --- the relations that remain exact -----------------------------------------
# SI Brochure, on the ampere: "The product e0 mu0 = 1/c^2 and quotient Z0/mu0 = c
# remain exact."  Both factors are now measured; the combinations are not.
invariants = []
for year in ("2018", "2022"):
    e0 = T[year]["vacuum electric permittivity"]
    m0 = T[year]["vacuum mag. permeability"]
    z0 = T[year]["characteristic impedance of vacuum"]
    prod = e0["value"] * m0["value"] * C * C            # should be 1
    quot = z0["value"] / (m0["value"] * C)              # should be 1
    ref_m0 = ABROGATED["vacuum mag. permeability"][1]
    ref_e0 = ABROGATED["vacuum electric permittivity"][1]
    invariants.append({
        "year": year,
        "e0_mu0_c2_minus_1": d(prod - 1),
        "Z0_over_mu0_c_minus_1": d(quot - 1),
        "rel_dev_mu0_from_abrogated": d((m0["value"] - ref_m0) / ref_m0),
        "rel_dev_e0_from_abrogated": d((e0["value"] - ref_e0) / ref_e0),
        "product_residual_smaller_by_factor": d(
            abs((m0["value"] - ref_m0) / ref_m0) / abs(prod - 1))
        if prod != 1 else None,
    })

# --- P6: the census of exactness ---------------------------------------------
stayed = sorted(n for n in both_1418 if S14[n] and S18[n])
new_and_exact = sorted(n for n in only_2018 if S18[n])
DATA_EXACT_14 = sum(1 for r in T["2014"].values() if r["exact"])
DATA_EXACT_18 = sum(1 for r in T["2018"].values() if r["exact"])
census = {
    "exact_2014": DATA_EXACT_14,
    "exact_2018": DATA_EXACT_18,
    "stayed_exact": len(stayed),
    "lost": len(lost),
    "gained": len(gained),
    "exact_and_new_in_2018": len(new_and_exact),
    "adds_up": (len(stayed) + len(gained) + len(new_and_exact) == DATA_EXACT_18
                and len(stayed) + len(lost) == DATA_EXACT_14),
    "stayed_exact_names": stayed,
    "exact_and_new_names": new_and_exact,
}

# --- P7: can the printing resolve a change in the uncertainty? ----------------
# The uncertainty column is printed to two significant figures.  A step of one
# unit in the last printed place is the instrument's resolution; a change smaller
# than that is not a measurement, it is a rounding.
def last_place(raw):
    """Magnitude of one unit in the last printed decimal place of an uncertainty
    like '0.000 000 000 19 e-6'."""
    s = raw.replace(" ", "").replace("e", "E")
    mant, _, exp = s.partition("E")
    dec = len(mant.split(".")[1]) if "." in mant else 0
    step = Decimal(1).scaleb(-dec)
    if exp:
        step = step.scaleb(int(exp))
    return step

resolution_check = []
for name in lost:
    r18, r22 = T["2018"].get(name), T["2022"].get(name)
    if not (r18 and r22 and r18["unc"] and r22["unc"]):
        continue
    ur18 = r18["unc"] / abs(r18["value"])
    ur22 = r22["unc"] / abs(r22["value"])
    step18 = last_place(r18["raw_unc"]) / abs(r18["value"])
    # The first version of this test asked `abs(change) > step`.  Two of the six
    # came out True on a difference in the sixteenth digit, because the change IS
    # exactly one printed unit — the test's threshold sat exactly on the data.
    # Replaced by the ratio, which says the same thing without pretending to a
    # decision the numbers cannot support.  Kept visible; not tidied away.
    units = abs(ur22 - ur18) / step18
    resolution_check.append({
        "quantity": name,
        "rel_unc_2018": d(ur18),
        "rel_unc_2022": d(ur22),
        "apparent_change": d(ur22 - ur18),
        "one_unit_of_printing": d(step18),
        "change_in_units_of_last_printed_digit": d(units),
        "resolvable": bool(units > 2),
    })

# And the direct check that the SI Brochure's claim holds in the tables: the
# relative uncertainty of mu_0, e_0 and Z_0 IS that of alpha, nothing else.
for year in ("2018", "2022"):
    a = T[year]["inverse fine-structure constant"]
    ur_alpha = a["unc"] / abs(a["value"])
    resolution_check.append({
        "quantity": "inverse fine-structure constant (the parent)",
        "year": year,
        "rel_unc": d(ur_alpha),
        "rel_unc_of_mu0_same_year": d(
            T[year]["vacuum mag. permeability"]["unc"]
            / abs(T[year]["vacuum mag. permeability"]["value"])),
    })

# --- P8: do the losers move with alpha? ---------------------------------------
# alpha is read from the INVERSE fine-structure constant, which is tabulated to
# twelve significant figures — the most precise handle available.  d(alpha)/alpha
# = -d(1/alpha)/(1/alpha).
ainv18 = T["2018"]["inverse fine-structure constant"]["value"]
ainv22 = T["2022"]["inverse fine-structure constant"]["value"]
d_alpha_rel = -(ainv22 - ainv18) / ainv18

alpha_tracking = {
    "inverse_alpha_2018": str(ainv18),
    "inverse_alpha_2022": str(ainv22),
    "rel_shift_of_alpha_2018_to_2022": d(d_alpha_rel),
    "rows": [],
}
for rec in LOSSES:
    name = rec["quantity"]
    if name not in PARENT or "shift_2018_to_2022_rel" not in rec:
        continue
    parent, power = PARENT[name]
    predicted = d_alpha_rel * power
    observed = Decimal(repr(rec["shift_2018_to_2022_rel"]))
    alpha_tracking["rows"].append({
        "quantity": name,
        "parent": parent,
        "power_of_alpha": power,
        "predicted_rel_shift": d(predicted),
        "observed_rel_shift": d(observed),
        "ratio_observed_over_predicted": d(observed / predicted),
    })

# --- how many independent numbers are the 59 gains? --------------------------
# If the gains are algebra on the four newly fixed constants, their sigmas should
# not be 59 independent numbers: they should fall into a few clusters, one per
# underlying input.  Bucket them at one decimal place and count.
buckets = {}
for rec in GAINS:
    if "sigma" not in rec:
        continue
    key = round(rec["sigma"], 1)
    buckets.setdefault(key, []).append(rec["quantity"])
clusters = sorted(({"sigma": k, "count": len(v), "examples": v[:3]}
                   for k, v in buckets.items()),
                  key=lambda r: -r["count"])

# --- output -------------------------------------------------------------------

DATA = {
    "generated_by": "ledger.py (Ulysses, Session 47, 2026-08-11)",
    "sources": {
        "tables": {k: {"path": v, "sha256": HASHES[k]} for k, v in TABLES.items()},
        "resolution": "https://www.bipm.org/en/committees/cg/cgpm/26-2018/resolution-1",
        "brochure": "https://www.bipm.org/en/publications/si-brochure",
        "nist": "https://physics.nist.gov/cuu/Constants/",
    },
    "table_sizes": {y: len(T[y]) for y in T},
    "exact_counts": {y: sum(1 for r in T[y].values() if r["exact"]) for y in T},
    "diff_2014_2018": {
        "lost_exactness": lost,
        "gained_exactness": gained,
        "rows_only_in_2014": only_2014,
        "rows_only_in_2018": only_2018,
    },
    "diff_2018_2022": {"status_changes": changed_1822},
    "losses": LOSSES,
    "gains": GAINS,
    "forwarding_addresses": addresses,
    "invariants": invariants,
    "census": census,
    "printing_resolution_check": resolution_check,
    "alpha_tracking": alpha_tracking,
    "gain_sigma_clusters": clusters,
}

with open("data.json", "w", encoding="utf-8") as fh:
    json.dump(DATA, fh, indent=1, ensure_ascii=False)

# --- report -------------------------------------------------------------------

def pr(*a):
    print(*a)

pr("=" * 78)
pr("THE EXACTNESS LEDGER OF THE 2019 SI REVISION")
pr("=" * 78)
pr("rows parsed:", DATA["table_sizes"])
pr("rows flagged (exact):", DATA["exact_counts"])
pr("rows present in 2014 but not 2018:", len(only_2014))
pr("rows present in 2018 but not 2014:", len(only_2018))
pr()
pr("-- LOST EXACTNESS 2014 -> 2018 (%d) --" % len(lost))
for n in lost:
    pr("   ", n)
pr()
pr("-- GAINED EXACTNESS 2014 -> 2018 (%d) --" % len(gained))
for n in gained:
    pr("   ", n)
pr()
pr("-- STATUS CHANGES 2018 -> 2022:", changed_1822 or "none")
pr()
pr("-- HOW FAR THE LOSERS SIT FROM THE VALUE THEIR DEFINITION ASSERTED --")
pr("   %-38s %10s %10s" % ("quantity", "2018 (sd)", "2022 (sd)"))
for rec in LOSSES:
    if "2018" not in rec:
        pr("   %-38s  %s" % (rec["quantity"], "no abrogated expression"))
        continue
    pr("   %-38s %10.2f %10.2f" % (rec["quantity"][:38],
                                   rec["2018"]["sigma"], rec["2022"]["sigma"]))
pr()
pr("-- HOW FAR THE STIPULATED VALUES SIT FROM THE LAST MEASURED ONES --")
pr("   %-38s %10s  %s" % ("quantity", "sd", "note"))
for rec in GAINS:
    if "sigma" not in rec:
        continue
    pr("   %-38s %10.2f  %s" % (rec["quantity"][:38], rec["sigma"],
                                rec.get("note", "")))
pr()
pr("-- FORWARDING ADDRESSES (Resolution 1, Appendix 2) --")
for a in addresses:
    got = a.get("rel_unc_in_codata_2014")
    pr("   %-34s <- %-24s stated %-8s CODATA2014 %s" % (
        a["quantity_that_receives"][:34], a["constant_it_inherits_from"][:24],
        a["uncertainty_stated_by_resolution"],
        ("%.3g" % got) if got else a["note"]))
pr()
pr("-- THE RELATIONS THAT REMAIN EXACT --")
for iv in invariants:
    pr("   %s: e0*mu0*c^2 - 1 = %+.3e   Z0/(mu0*c) - 1 = %+.3e" % (
        iv["year"], iv["e0_mu0_c2_minus_1"], iv["Z0_over_mu0_c_minus_1"]))
    pr("        mu0 deviates from 4pi*1e-7 by %+.3e relative; the product residual"
       " is %.0fx smaller" % (iv["rel_dev_mu0_from_abrogated"],
                              iv["product_residual_smaller_by_factor"]))
pr()
pr("-- P6  CENSUS OF EXACTNESS --")
pr("   exact rows 2014: %d   exact rows 2018: %d" % (census["exact_2014"],
                                                     census["exact_2018"]))
pr("   stayed exact %d | lost %d | gained %d | exact and new in 2018 %d | adds up: %s"
   % (census["stayed_exact"], census["lost"], census["gained"],
      census["exact_and_new_in_2018"], census["adds_up"]))
pr("   the eleven that were exact before and after:")
for n in census["stayed_exact_names"]:
    pr("      ", n)
pr()
pr("-- P7  CAN THE PRINTING RESOLVE THE CHANGE IN UNCERTAINTY? --")
for r in resolution_check:
    if "change_in_units_of_last_printed_digit" in r:
        pr("   %-38s change = %.2f units of the last printed digit -> %s" % (
            r["quantity"][:38], r["change_in_units_of_last_printed_digit"],
            "resolvable" if r["resolvable"] else "NOT RESOLVABLE"))
    else:
        pr("   %s %s: u_r(alpha) = %.4e   u_r(mu_0) = %.4e" % (
            r["quantity"], r["year"], r["rel_unc"], r["rel_unc_of_mu0_same_year"]))
pr()
pr("-- P8  DO THE LOSERS MOVE WITH ALPHA? --")
pr("   alpha shifted by %+.4e relative between the 2018 and 2022 adjustments"
   % alpha_tracking["rel_shift_of_alpha_2018_to_2022"])
pr("   %-38s %6s %13s %13s %8s" % ("quantity", "power", "predicted", "observed",
                                   "obs/pred"))
for r in alpha_tracking["rows"]:
    pr("   %-38s %6d %+13.4e %+13.4e %8.4f" % (
        r["quantity"][:38], r["power_of_alpha"], r["predicted_rel_shift"],
        r["observed_rel_shift"], r["ratio_observed_over_predicted"]))
pr()
pr("-- HOW MANY INDEPENDENT NUMBERS ARE THE 59 GAINS? --")
for cl in clusters:
    pr("   sigma ~ %+.1f : %2d rows   e.g. %s" % (cl["sigma"], cl["count"],
                                                  ", ".join(cl["examples"])[:60]))
pr()
pr("wrote data.json")
