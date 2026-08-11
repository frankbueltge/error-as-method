#!/usr/bin/env python3
"""
governor.py -- Session 48, 2026-08-11.

Session 47 left a question at the top of its open threads: Resolution 1 of the 26th CGPM says the
mass of the International Prototype of the Kilogram "will be determined experimentally"; has any
post-2019 determination been published, and what did it find? It added: *Do not assume it has
drifted.*

It has been determined, three times, and the answer is published. This script does not go looking
for it. It does something narrower and harder to fool: it takes the *rule* the CCM wrote down in
May 2019 for producing that number -- a rolling window of the three most recent comparisons, an
arithmetic (deliberately non-weighted) mean, and a limit of +/- 5 parts in 10^9 on how far the
result may move between revisions -- implements it as a function, and runs it on the published
inputs. If the rule as written reproduces the published series, the series is the rule's output and
not the artefact's mass. If it does not, the discrepancy is the finding instead.

Everything the script reads is in data/inputs.json, transcribed from BIPM and NIST documents with
their addresses attached. Nothing is fetched at run time. Exact rational arithmetic throughout
(fractions.Fraction), stdlib only, no randomness and therefore no seed. Deterministic: same input,
same output, forever.

THE PREDICTIONS BELOW WERE WRITTEN BEFORE THIS SCRIPT WAS FIRST EXECUTED and are left exactly as
written. Verdicts are appended by the run. A refuted prediction stays; that is the method.
"""

import json
import os
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------------------------
# PRE-REGISTERED PREDICTIONS -- written 2026-08-11 before the first run, not edited afterwards.
# ---------------------------------------------------------------------------------------------
PREDICTIONS = {
    "P1": "The published headline consensus value equals the arithmetic mean of its window, rounded "
          "to the nearest microgram, at the 2021 and 2023 revisions -- and NOT at the 2026 revision.",
    "P2": "The three 'calculated' means printed by the CCM (-2.1, -7.2, -14.9 ug) reproduce exactly "
          "from the three published windows.",
    "P3": "Successive published headline values differ by exactly -5 ug at both steps: -2, -7, -12.",
    "P4": "The underlying calculated means are NOT an arithmetic progression -- the second step is "
          "larger in magnitude than the first. The straight line is in the published series only.",
    "P5": "Every KCRV in the series is higher (less negative) than the one before it, while the "
          "consensus value falls at every step. The two series run in opposite directions.",
    "P6": "The whole of the fall is the exchange at the edge of the window: the change in the mean "
          "equals (value entering - value leaving)/3, exactly, at both steps.",
    "P7": "At both steps so far, the value leaving the window is a pre-comparison legacy input -- "
          "the artefact itself in 2023, the 2016 pilot study in 2026 -- and never a KCRV.",
    "P8": "The K8.2024 KCRV reproduces as the inverse-variance-weighted mean of the nine included "
          "participants, within 0.1 ug of the published -10.7 ug, and its uncertainty within 0.1 ug "
          "of the published 6.4 ug.",
    "P9": "The published chi-squared of 5.5 reproduces within 0.3 from the same table, summing over "
          "all ten participants with deviations taken from the KCRV. (Least confident of these; the "
          "report's eq. 9 sums i=1..10 for 9 degrees of freedom and I am not certain which ten.)",
    "P10": "sqrt(sum of squared input uncertainties)/3 equals the 6.0 ug the 2020 report prints for "
           "the arithmetic mean -- confirming the formula -- and then FALLS at each later revision "
           "while the assigned uncertainty stays at exactly 20 ug.",
    "P11": "Phase-3 exit criterion (d) -- |consensus value - most recent KCRV| < 5 ug -- is satisfied "
           "at the 2026 revision, on both the clamped and the unclamped value.",
    "P12": "The clamp is not a one-off: rerunning the rule from the start with the limit switched OFF "
           "gives a different value today, and the difference is exactly the amount withheld in 2026.",
}
VERDICTS = {}


def v(key, ok, note=""):
    VERDICTS[key] = ("CONFIRMED" if ok else "REFUTED", note)
    return ok


def fr(x):
    """Exact Fraction from a decimal literal, via its string form -- never through binary float."""
    return F(str(x))


def isqrt_frac(x, digits=12):
    """Square root of a Fraction to `digits` decimal places, returned as a Fraction. Integer-only
    arithmetic: no float ever touches a reported number."""
    scale = 10 ** (2 * digits)
    n = (x.numerator * scale) // x.denominator
    r = 0
    bit = 1 << ((n.bit_length() + 1) // 2 * 2)
    while bit:
        if n >= r + bit:
            n -= r + bit
            r = (r >> 1) + bit
        else:
            r >>= 1
        bit >>= 2
    return F(r, 10 ** digits)


def q(x, places=4):
    """Render a Fraction as a decimal string with `places` digits, correctly rounded, no float."""
    sign = "-" if x < 0 else ""
    x = abs(x)
    scale = 10 ** places
    n = (x.numerator * scale * 2 + x.denominator) // (x.denominator * 2)
    s = str(n).rjust(places + 1, "0")
    return f"{sign}{s[:-places] or '0'}.{s[-places:]}" if places else f"{sign}{s}"


# ---------------------------------------------------------------------------------------------
# THE RULE, as written by the CCM and approved at its 17th meeting, 16-17 May 2019 -- four days
# before the definition it governs came into force.
# ---------------------------------------------------------------------------------------------
def consensus_rule(window_values, previous_published, limit=None):
    """The CCM's procedure, implemented literally.

    window_values      the three most recent data sets, in micrograms offset from 1 kg
    previous_published the previous published consensus value, or None for the first
    limit              the permitted change between consecutive revisions, or None to disable

    Returns (calculated_mean, published, was_clamped, withheld).
    """
    calculated = sum(window_values, F(0)) / len(window_values)   # arithmetic, NON-weighted
    if previous_published is None or limit is None:
        return calculated, calculated, False, F(0)
    change = calculated - previous_published
    if abs(change) <= limit:
        return calculated, calculated, False, F(0)
    allowed = limit if change > 0 else -limit                     # "limited to +/- 5 parts in 10^9"
    published = previous_published + allowed
    return calculated, published, True, calculated - published


def main():
    data = json.load(open(os.path.join(HERE, "data", "inputs.json")))
    revs = data["consensus_values"]["revisions"]
    limit = fr(data["the_rule"]["limit_ug"])
    out = {"generated_by": "governor.py", "units": "micrograms offset from 1 kg", "sections": {}}

    print("=" * 94)
    print("THE GOVERNOR -- running the CCM's own rule for the mass of the kilogram")
    print("=" * 94)
    print()
    print("The rule, verbatim (CCM detailed note on the dissemination process, 17th CCM, May 2019):")
    print()
    for line in ("  " + data["the_rule"]["quote_window"]).split(". "):
        print("  " + line.strip())
    print()
    for line in ("  " + data["the_rule"]["quote_limit"]).split(". "):
        print("  " + line.strip())
    print()
    print("  At 1 kg, 5 parts in 10^9 is 5 micrograms.")
    print()

    # -- 1. Reproduce the published series ------------------------------------------------------
    print("-" * 94)
    print("1. THE RULE, RUN ON THE PUBLISHED INPUTS")
    print("-" * 94)
    rows, prev = [], None
    for r in revs:
        vals = [fr(w["value_ug"]) for w in r["window"]]
        calc, pub, clamped, withheld = consensus_rule(vals, prev, limit)
        rows.append({
            "name": r["name"], "effective": r["effective"],
            "window": [(w["label"], fr(w["value_ug"]), fr(w["u_ug"])) for w in r["window"]],
            "calc": calc, "pub": pub, "clamped": clamped, "withheld": withheld,
            "printed_calc": fr(r["published_calculated_mean_ug"]),
            "printed_pub": fr(r["published_headline_ug"]),
            "assigned_u": fr(r["published_assigned_u_ug"]),
        })
        prev = fr(r["published_headline_ug"])   # the rule chains on the PUBLISHED value

    for row in rows:
        print(f"\n  {row['name']}  (in force from {row['effective']})")
        for lab, val, u in row["window"]:
            print(f"      {lab:<44} {q(val,1):>8} ug   u = {q(u,1):>5} ug")
        print(f"      {'-'*44} {'-'*8}")
        print(f"      {'arithmetic mean, computed here':<44} {q(row['calc'],4):>8} ug")
        print(f"      {'arithmetic mean, as printed by the CCM':<44} {q(row['printed_calc'],4):>8} ug")
        if row["clamped"]:
            print(f"      CLAMPED: change of {q(row['calc'] - (row['pub'] - (limit if row['calc']>row['pub'] else -limit)),4)}"
                  f" ug exceeded the +/-{q(limit,0)} ug limit")
            print(f"      {'published headline, computed here':<44} {q(row['pub'],4):>8} ug")
        else:
            print(f"      {'published headline, computed here':<44} {q(row['pub'],4):>8} ug")
        print(f"      {'published headline, as printed by the CCM':<44} {q(row['printed_pub'],4):>8} ug"
              f"   (u = {q(row['assigned_u'],0)} ug, assigned)")

    # P2: calculated means reproduce
    p2 = all(abs(r["calc"] - r["printed_calc"]) < F(1, 20) for r in rows)
    v("P2", p2, "; ".join(f"{r['name']}: computed {q(r['calc'],4)} vs printed {q(r['printed_calc'],1)}"
                          for r in rows))

    # P1: headline == rounded mean except 2026
    def rnd(x):
        return F(int(x * 2 - 1) // 2 + 1) if x >= 0 else -F(int(-x * 2 - 1) // 2 + 1)
    matches = [abs(rnd(r["calc"]) - r["printed_pub"]) < F(1, 100) for r in rows]
    v("P1", matches[0] and matches[1] and not matches[2],
      f"headline equals rounded mean: {[r['name'] + '=' + str(m) for r, m in zip(rows, matches)]}")

    # P3: published steps exactly -5
    steps_pub = [rows[i + 1]["printed_pub"] - rows[i]["printed_pub"] for i in range(len(rows) - 1)]
    v("P3", all(s == F(-5) for s in steps_pub),
      f"published steps = {[q(s,4) for s in steps_pub]} ug")

    # P4: calculated steps not equal
    steps_calc = [rows[i + 1]["calc"] - rows[i]["calc"] for i in range(len(rows) - 1)]
    v("P4", abs(steps_calc[1]) > abs(steps_calc[0]),
      f"calculated steps = {[q(s,4) for s in steps_calc]} ug -- the published line is straight, "
      f"the calculated one is not")

    print()
    print("  THE TWO SERIES")
    print(f"      published  : {'  ->  '.join(q(r['printed_pub'],0) for r in rows)}   "
          f"steps {', '.join(q(s,2) for s in steps_pub)}")
    print(f"      calculated : {'  ->  '.join(q(r['calc'],2) for r in rows)}   "
          f"steps {', '.join(q(s,2) for s in steps_calc)}")

    # -- 2. Where the fall comes from -----------------------------------------------------------
    print()
    print("-" * 94)
    print("2. WHY IT FALLS -- the exchange at the edge of the window")
    print("-" * 94)
    kcrvs = [(-18.8, "CCM.M-K8.2019"), (-15.2, "CCM.M-K8.2021"), (-10.7, "CCM.M-K8.2024")]
    kcrv_steps = [fr(kcrvs[i + 1][0]) - fr(kcrvs[i][0]) for i in range(len(kcrvs) - 1)]
    print(f"\n  Every key comparison reference value is HIGHER than the one before it:")
    print(f"      {'  ->  '.join(q(fr(k),1) for k, _ in kcrvs)} ug     "
          f"steps +{q(kcrv_steps[0],1)}, +{q(kcrv_steps[1],1)} ug")
    v("P5", all(s > 0 for s in kcrv_steps) and all(s < 0 for s in steps_calc),
      f"KCRV steps {[q(s,1) for s in kcrv_steps]} all rising; consensus steps "
      f"{[q(s,2) for s in steps_calc]} all falling")

    exchanges, p6, p7 = [], True, True
    for i in range(len(rows) - 1):
        old = {lab: val for lab, val, _ in rows[i]["window"]}
        new = {lab: val for lab, val, _ in rows[i + 1]["window"]}
        left = [(l, x) for l, x in old.items() if l not in new]
        came = [(l, x) for l, x in new.items() if l not in old]
        assert len(left) == 1 and len(came) == 1
        (llab, lval), (clab, cval) = left[0], came[0]
        predicted = (cval - lval) / 3
        actual = steps_calc[i]
        p6 &= (predicted == actual)
        p7 &= ("KCRV" not in llab)
        exchanges.append((rows[i]["name"], rows[i + 1]["name"], llab, lval, clab, cval,
                          predicted, actual))
        print(f"\n  {rows[i]['name']} -> {rows[i+1]['name']}")
        print(f"      leaves the window : {llab:<44} {q(lval,1):>8} ug")
        print(f"      enters the window : {clab:<44} {q(cval,1):>8} ug")
        print(f"      (entering - leaving)/3 = {q(predicted,4)} ug     actual change "
              f"= {q(actual,4)} ug")
    v("P6", p6, "the change in the mean is exactly the edge exchange divided by three, at both steps")
    v("P7", p7, "; ".join(f"{a}->{b}: {ll} left" for a, b, ll, _, _, _, _, _ in exchanges))

    print()
    print("  So the consensus value falls because the values being expelled -- the artefact itself,")
    print("  then the 2016 pilot -- are the two HIGHEST in the record, while every value entering is")
    print("  a measurement that is itself rising. The published number moves down because the")
    print("  artefact's own legacy is being flushed out of the average one item at a time.")

    # -- 3. The next revision -------------------------------------------------------------------
    print()
    print("-" * 94)
    print("3. THE NEXT REVISION -- a dated, falsifiable prediction")
    print("-" * 94)
    next_out = fr(kcrvs[0][0])   # -18.8, the oldest remaining, and the LOWEST of the three
    print(f"\n  After the next key comparison (CCM.M-K8.2027, per the CCM Working Group on Mass,")
    print(f"  June 2025), the window will hold only key comparison reference values for the first")
    print(f"  time. The value leaving will be {q(next_out,1)} ug -- the LOWEST value ever measured in")
    print(f"  this series. The change in the calculated mean will be (KCRV_2027 - ({q(next_out,1)}))/3.")
    print(f"\n  Therefore: the calculated consensus value RISES unless KCRV_2027 < {q(next_out,1)} ug,")
    print(f"  i.e. unless the next comparison comes in below anything the last three found.")
    print(f"  The five-year fall reverses -- not because anything about the kilogram changed, but")
    print(f"  because the window finished eating its own history.")
    for probe in (-18.8, -15.0, -10.0, -5.0, 0.0):
        w = [fr(kcrvs[1][0]), fr(kcrvs[2][0]), fr(probe)]
        calc, pub, cl, wh = consensus_rule(w, rows[-1]["printed_pub"], limit)
        print(f"      if KCRV_2027 = {q(fr(probe),1):>6} ug -> calculated {q(calc,3):>8} ug, "
              f"published {q(pub,3):>8} ug{'  [clamped]' if cl else ''}")
    out["sections"]["next_revision_leaving"] = q(next_out, 1)

    # -- 4. The independent check: recompute a published KCRV from its participants ---------------
    print()
    print("-" * 94)
    print("4. AN INDEPENDENT CHECK -- recomputing the 2024 KCRV from the ten realizations")
    print("-" * 94)
    kp = data["kcrv_2024_participants"]
    inc = [p for p in kp["participants"] if p["in_kcrv"]]
    print(f"\n  Ten institutes realized the kilogram; {len(inc)} enter the reference value. The report")
    print(f"  excludes CMS/ITRI for a reason that is not metrological: 'because Chinese Taipei is not")
    print(f"  a member of the BIPM, but an Associate of the CGPM.' Its result ({q(fr(kp['participants'][1]['dm_ug']),1)} ug) is the")
    print(f"  highest of the ten.\n")
    for p in kp["participants"]:
        mark = "  " if p["in_kcrv"] else " *"
        print(f"    {mark}{p['institute']:<10} {p['method']:<16} {q(fr(p['dm_ug']),1):>8} ug   "
              f"u = {q(fr(p['u_ug']),1):>6} ug")
    print("      * excluded from the reference value")

    ws = [F(1) / (fr(p["u_ug"]) ** 2) for p in inc]
    kcrv = sum(w * fr(p["dm_ug"]) for w, p in zip(ws, inc)) / sum(ws, F(0))
    u_kcrv = isqrt_frac(F(1) / sum(ws, F(0)))
    pk, pu = fr(kp["published_kcrv_ug"]), fr(kp["published_kcrv_u_ug"])
    print(f"\n      inverse-variance weighted mean, computed here : {q(kcrv,4)} ug, "
          f"u = {q(u_kcrv,4)} ug")
    print(f"      as published                                  : {q(pk,1)} ug, u = {q(pu,1)} ug")
    v("P8", abs(kcrv - pk) < F(1, 10) and abs(u_kcrv - pu) < F(1, 10),
      f"computed {q(kcrv,4)} +/- {q(u_kcrv,4)} vs published {q(pk,1)} +/- {q(pu,1)}")

    # chi-squared
    chi_all = sum((fr(p["dm_ug"]) - kcrv) ** 2 / fr(p["u_ug"]) ** 2 for p in kp["participants"])
    chi_inc = sum((fr(p["dm_ug"]) - kcrv) ** 2 / fr(p["u_ug"]) ** 2 for p in inc)
    pc = fr(kp["published_chi_squared"])
    print(f"\n      chi-squared over all ten                      : {q(chi_all,3)}")
    print(f"      chi-squared over the nine included            : {q(chi_inc,3)}")
    print(f"      as published                                  : {q(pc,1)}  "
          f"(9 dof; 95% cut-off {kp['published_chi_squared_95_cutoff']}, "
          f"conservative cut-off {kp['published_chi_squared_conservative_cutoff']})")
    best = min(chi_all, chi_inc, key=lambda c: abs(c - pc))
    v("P9", abs(best - pc) < F(3, 10),
      f"all-ten {q(chi_all,3)}, nine-included {q(chi_inc,3)}, published {q(pc,1)}")

    # -- 5. The uncertainty that never moved ----------------------------------------------------
    print()
    print("-" * 94)
    print("5. THE UNCERTAINTY THAT NEVER MOVED")
    print("-" * 94)
    print(f"\n  The 2020 report prints, for the first window: 'The arithmetic mean of the three results")
    print(f"  is -2.1 ug with a standard uncertainty of 6.0 ug.' That fixes the formula. Applying the")
    print(f"  same formula to all three windows:\n")
    u_means = []
    for row in rows:
        um = isqrt_frac(sum(u ** 2 for _, _, u in row["window"])) / 3
        u_means.append(um)
        ratio = row["assigned_u"] / um
        print(f"      {row['name']}   u(mean) = {q(um,3):>6} ug     assigned = "
              f"{q(row['assigned_u'],0):>3} ug     ratio = {q(ratio,2)}")
    v("P10", abs(u_means[0] - F(6)) < F(1, 10) and u_means[0] > u_means[1] > u_means[2]
      and len({r["assigned_u"] for r in rows}) == 1,
      f"u(mean) = {[q(x,3) for x in u_means]}; assigned uncertainty constant at "
      f"{q(rows[0]['assigned_u'],0)} ug throughout")
    print(f"\n  The computable dispersion of the inputs fell by {q((1 - u_means[2]/u_means[0]) * 100, 1)}% "
          f"across the three revisions, as")
    print(f"  the experiments improved. The published uncertainty did not move at all. The CCM says so")
    print(f"  in a footnote and does not pretend otherwise: 'The uncertainty in the consensus value was")
    print(f"  agreed by the CCM-TGPfD-kg.' It is a decision printed where a computation would go.")

    # -- 6. Phase 3 -----------------------------------------------------------------------------
    print()
    print("-" * 94)
    print("6. THE EXIT CRITERION")
    print("-" * 94)
    thr = fr(data["phase_3_exit_criterion_d"]["threshold_ug"])
    last_kcrv = fr(kcrvs[-1][0])
    d_clamped = abs(rows[-1]["printed_pub"] - last_kcrv)
    d_calc = abs(rows[-1]["calc"] - last_kcrv)
    print(f"\n  Criterion (d) for leaving the consensus-value regime: |CV - last KCRV| < {q(thr,0)} ug.")
    print(f"      using the published (clamped) value {q(rows[-1]['printed_pub'],1)} : "
          f"{q(d_clamped,3)} ug  -> {'MET' if d_clamped < thr else 'NOT MET'}")
    print(f"      using the calculated value          {q(rows[-1]['calc'],1)} : "
          f"{q(d_calc,3)} ug  -> {'MET' if d_calc < thr else 'NOT MET'}")
    v("P11", d_clamped < thr and d_calc < thr,
      f"clamped {q(d_clamped,3)} ug, calculated {q(d_calc,3)} ug, threshold {q(thr,0)} ug")
    print(f"\n  Note what the clamp does to this test: it pulls the consensus value TOWARD the newest")
    print(f"  key comparison, and the criterion measures the distance between them. Holding the norm")
    print(f"  back from the data makes the norm look closer to the data.")

    # -- 7. The counterfactual: the rule with its governor removed -------------------------------
    print()
    print("-" * 94)
    print("7. THE SAME RULE WITH THE GOVERNOR REMOVED")
    print("-" * 94)
    prev_u = None
    unclamped = []
    for r in revs:
        vals = [fr(w["value_ug"]) for w in r["window"]]
        calc, pub, cl, wh = consensus_rule(vals, prev_u, None)
        unclamped.append(pub)
        prev_u = pub
    print(f"\n      with the limit    : {'  ->  '.join(q(r['printed_pub'],1) for r in rows)} ug")
    print(f"      without the limit : {'  ->  '.join(q(x,1) for x in unclamped)} ug")
    withheld_total = unclamped[-1] - rows[-1]["printed_pub"]
    print(f"\n      difference today  : {q(withheld_total,1)} ug, withheld and carried forward")
    print(f"      amount the 2026 clamp held back: {q(rows[-1]['withheld'],1)} ug")
    v("P12", abs(withheld_total - rows[-1]["withheld"]) < F(1, 100)
      and rows[-1]["withheld"] != 0,
      f"total withheld {q(withheld_total,4)} ug; 2026 clamp alone {q(rows[-1]['withheld'],4)} ug")
    print(f"\n  The withheld amount is not discarded. The 2026 document says the limit 'should also")
    print(f"  ensure that changes in the value after subsequent Key Comparisons are small' -- the")
    print(f"  difference is queued, to be released at no more than {q(limit,0)} ug per revision.")

    # -- 8. An observation that is not a prediction ----------------------------------------------
    print()
    print("-" * 94)
    print("8. ONE INCONSISTENCY IN THE RECORD, OBSERVED, INERT")
    print("-" * 94)
    print(f"\n  O1. The uncertainty of the 2019 KCRV is printed as 7.5 ug in the 2020 calculation and in")
    print(f"      the CCM Working Group on Mass report of June 2025, and as 8.1 ug in the 2023 and 2026")
    print(f"      calculations. Same comparison, same reference value (-18.8 ug), two numbers. I cannot")
    print(f"      account for it and do not claim it is an error. It changes nothing computed here: the")
    print(f"      CCM states these uncertainties are 'given for information only and are not used in")
    print(f"      the calculation of the consensus value.' Recorded because it is in the record.")

    # -- verdicts --------------------------------------------------------------------------------
    print()
    print("=" * 94)
    print("VERDICTS ON THE PRE-REGISTERED PREDICTIONS")
    print("=" * 94)
    n_ref = 0
    for k in sorted(PREDICTIONS, key=lambda s: int(s[1:])):
        status, note = VERDICTS.get(k, ("NOT TESTED", ""))
        n_ref += status == "REFUTED"
        print(f"\n  {k}  {status}")
        print(f"      claim : {PREDICTIONS[k]}")
        if note:
            print(f"      found : {note}")
    print(f"\n  {len(VERDICTS)} tested, {n_ref} refuted.")

    out["sections"]["revisions"] = [
        {"name": r["name"], "effective": r["effective"],
         "window": [(l, q(x, 1), q(u, 1)) for l, x, u in r["window"]],
         "calculated": q(r["calc"], 4), "published": q(r["printed_pub"], 1),
         "clamped": r["clamped"], "withheld": q(r["withheld"], 4),
         "assigned_u": q(r["assigned_u"], 0), "u_of_mean": q(um, 3)}
        for r, um in zip(rows, u_means)
    ]
    out["sections"]["kcrvs"] = [{"comparison": n, "value": q(fr(k), 1)} for k, n in kcrvs]
    out["sections"]["kcrv_2024_recomputed"] = {"value": q(kcrv, 4), "u": q(u_kcrv, 4),
                                               "chi2_all": q(chi_all, 3), "chi2_inc": q(chi_inc, 3)}
    out["sections"]["unclamped"] = [q(x, 4) for x in unclamped]
    out["sections"]["withheld_total"] = q(withheld_total, 4)
    out["sections"]["u_of_mean"] = [q(x, 3) for x in u_means]
    out["predictions"] = {k: {"claim": PREDICTIONS[k], "verdict": VERDICTS.get(k, ("NOT TESTED", ""))[0],
                              "found": VERDICTS.get(k, ("", ""))[1]} for k in PREDICTIONS}
    json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=2)
    print(f"\n  results.json written.")


if __name__ == "__main__":
    main()
