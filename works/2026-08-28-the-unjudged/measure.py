#!/usr/bin/env python3
"""measure.py — Session 73, 2026-08-28.

Offline. Standard library only. Reads the raw cache harvest.py wrote and writes
results.json beside this file. It fetches nothing: every number in the work comes
from here, and re-running it against a re-fetched cache with the same SHA-256s
must reproduce the file byte for byte.

What it measures, in the definitions fixed in PREDICTIONS.md before it existed:

  * the survival of the un-normed state -- Kaplan-Meier over waiting times in the
    post-migration cohort, with the still-unjudged records as the censored ones;
  * the pending share of the classes the institution's own written norm names:
    errata on obsoleted RFCs (which the norm pre-decides), errata on RFCs with no
    working group (which the norm routes to an office rather than a group), and
    the editorial/technical split (which the norm routes down two paths);
  * the composition of the 728, descriptively, with no threshold of "too old"
    derived from the distribution itself -- Canguilhem's constraint, taken as a
    method rule rather than as a quotation.

Usage:
    python3 measure.py --raw ../../../.raw
"""

import argparse
import collections
import datetime
import json
import os
import re
import statistics
import xml.etree.ElementTree as ET

T = datetime.date(2026, 8, 28)          # the observation date, fixed in PREDICTIONS.md
MIGRATION = datetime.date(2019, 9, 10)  # the date the feed's verdict clock was overwritten
QUARANTINED = {"6534"}                  # F-071: stays in every count, leaves every duration


def parse_date(text):
    """A date out of the dump, or None. Dates that cannot exist return None."""
    if not text:
        return None
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", text.strip())
    if not m:
        return None
    try:
        return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def load_errata(raw):
    with open(os.path.join(raw, "errata.json"), encoding="utf-8") as fh:
        return json.load(fh)


def load_index(raw):
    """doc-id -> {date, stream, area, wg, obsoleted, current_status}."""
    tree = ET.parse(os.path.join(raw, "rfc-index.xml"))
    out = {}
    for entry in tree.getroot():
        tag = entry.tag.split("}")[-1]
        if tag != "rfc-entry":
            continue
        rec = {"date": None, "stream": None, "area": None, "wg": None,
               "obsoleted": False, "current_status": None, "doc_id": None}
        for child in entry:
            name = child.tag.split("}")[-1]
            if name == "doc-id":
                rec["doc_id"] = (child.text or "").strip()
            elif name == "stream":
                rec["stream"] = (child.text or "").strip()
            elif name == "area":
                rec["area"] = (child.text or "").strip()
            elif name == "wg_acronym":
                rec["wg"] = (child.text or "").strip()
            elif name == "current-status":
                rec["current_status"] = (child.text or "").strip()
            elif name == "obsoleted-by":
                rec["obsoleted"] = True
            elif name == "date":
                year = month = None
                for part in child:
                    pname = part.tag.split("}")[-1]
                    if pname == "year":
                        year = int((part.text or "0").strip())
                    elif pname == "month":
                        month = (part.text or "").strip()
                months = ["January", "February", "March", "April", "May", "June", "July",
                          "August", "September", "October", "November", "December"]
                if year:
                    mnum = months.index(month) + 1 if month in months else 1
                    rec["date"] = datetime.date(year, mnum, 1)
        if rec["doc_id"]:
            out[rec["doc_id"]] = rec
    return out


def kaplan_meier(observations):
    """observations: list of (time_days, event) with event True = adjudicated.

    Returns the product-limit curve as a list of (t, n_at_risk, n_events, S).
    """
    obs = sorted(observations, key=lambda o: (o[0], not o[1]))
    n = len(obs)
    curve = []
    surv = 1.0
    i = 0
    at_risk = n
    while i < n:
        t = obs[i][0]
        events = 0
        censored = 0
        j = i
        while j < n and obs[j][0] == t:
            if obs[j][1]:
                events += 1
            else:
                censored += 1
            j += 1
        if events and at_risk > 0:
            surv *= (1.0 - events / at_risk)
        curve.append((t, at_risk, events, surv))
        at_risk -= (events + censored)
        i = j
    return curve


def s_at(curve, t):
    """S(t) from the product-limit curve: the value after all event times <= t."""
    surv = 1.0
    for time, _risk, _events, value in curve:
        if time <= t:
            surv = value
        else:
            break
    return surv


def at_risk_at(curve, t):
    """How many are still under observation just after day t."""
    remaining = None
    for time, risk, events, _s in curve:
        if time <= t:
            remaining = risk - events
        else:
            break
    if remaining is None:
        return curve[0][1] if curve else 0
    return remaining


def quantiles(values):
    if not values:
        return {}
    vals = sorted(values)
    return {
        "n": len(vals),
        "min": vals[0],
        "p25": statistics.quantiles(vals, n=4)[0] if len(vals) > 3 else vals[0],
        "median": statistics.median(vals),
        "p75": statistics.quantiles(vals, n=4)[2] if len(vals) > 3 else vals[-1],
        "p90": statistics.quantiles(vals, n=10)[8] if len(vals) > 9 else vals[-1],
        "max": vals[-1],
        "mean": round(statistics.fmean(vals), 2),
    }


def share(rows, pred):
    group = [r for r in rows if pred(r)]
    pending = [r for r in group if r["status"] == "Reported"]
    return {
        "n": len(group),
        "reported": len(pending),
        "pending_share": round(len(pending) / len(group), 5) if group else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=os.path.join(os.path.dirname(__file__), "..", "..", "..", ".raw"))
    args = ap.parse_args()
    raw = os.path.abspath(args.raw)
    here = os.path.dirname(os.path.abspath(__file__))

    errata = load_errata(raw)
    index = load_index(raw)

    rows = []
    unparsed_submit = []
    impossible = []
    for e in errata:
        eid = str(e["errata_id"])
        sub = parse_date(e.get("submit_date"))
        upd = parse_date(e.get("update_date"))
        doc = (e.get("doc-id") or "").strip()
        idx = index.get(doc)
        if sub is None:
            unparsed_submit.append(eid)
        if sub and sub > T:
            impossible.append({"errata_id": eid, "submit_date": e.get("submit_date")})
        rows.append({
            "errata_id": eid,
            "doc": doc,
            "status": e["errata_status_code"],
            "type": e["errata_type_code"],
            "submit": sub,
            "update": upd,
            "submitter": (e.get("submitter_name") or "").strip(),
            "verifier": (e.get("verifier_name") or "").strip() if e.get("verifier_name") else "",
            "section": (e.get("section") or "").strip(),
            "in_index": idx is not None,
            "stream": idx["stream"] if idx else None,
            "area": idx["area"] if idx else None,
            "wg": idx["wg"] if idx else None,
            "obsoleted": idx["obsoleted"] if idx else None,
            "rfc_date": idx["date"] if idx else None,
            "rfc_status": idx["current_status"] if idx else None,
        })

    usable = [r for r in rows if r["errata_id"] not in QUARANTINED and r["submit"] is not None
              and r["submit"] <= T]
    cohort = [r for r in usable if r["submit"] >= MIGRATION]
    pending_all = [r for r in rows if r["status"] == "Reported"]

    results = {
        "observation_date": T.isoformat(),
        "migration_date": MIGRATION.isoformat(),
        "quarantined": sorted(QUARANTINED),
        "counts": {
            "errata_total": len(errata),
            "status": dict(collections.Counter(r["status"] for r in rows)),
            "type": dict(collections.Counter(r["type"] for r in rows)),
            "unparsable_submit_date": unparsed_submit,
            "submit_date_in_the_future": impossible,
            "usable_for_durations": len(usable),
            "cohort_C": len(cohort),
            "target_rfc_not_in_index": sum(1 for r in rows if not r["in_index"]),
        },
    }

    # ---------------------------------------------------------------- P5 first
    # The instrument check runs before anything that depends on the clock.
    negatives = [r["errata_id"] for r in cohort
                 if r["update"] is not None and r["update"] < r["submit"]]
    migration_stamped = [r["errata_id"] for r in cohort
                         if r["update"] == MIGRATION]
    results["P5_instrument"] = {
        "cohort_n": len(cohort),
        "update_before_submit": negatives,
        "update_on_migration_date": migration_stamped,
        "won": len(negatives) == 0 and len(migration_stamped) <= 10,
    }

    # ---------------------------------------------------------------- P1: survival
    observations = []
    for r in cohort:
        if r["status"] == "Reported":
            observations.append(((T - r["submit"]).days, False))
        elif r["update"] is not None:
            observations.append((max((r["update"] - r["submit"]).days, 0), True))
        # an adjudicated record with no parsable update_date carries no wait and is
        # counted here, not silently dropped:
    no_update = [r["errata_id"] for r in cohort
                 if r["status"] != "Reported" and r["update"] is None]
    curve = kaplan_meier(observations)
    marks = [7, 30, 90, 180, 365, 547, 730, 1095, 1460, 1825]
    survival = {str(t): {"S": round(s_at(curve, t), 5), "at_risk_after": at_risk_at(curve, t)}
                for t in marks}
    s365, s730 = s_at(curve, 365), s_at(curve, 730)
    q_second_year = 1 - (s730 / s365) if s365 > 0 else None
    results["P1_survival"] = {
        "cohort_n": len(cohort),
        "observations": len(observations),
        "adjudicated_without_update_date": no_update,
        "curve_marks": survival,
        "S_90": round(s_at(curve, 90), 5),
        "S_365": round(s365, 5),
        "S_730": round(s730, 5),
        "at_risk_at_365": at_risk_at(curve, 365),
        "q_second_year": round(q_second_year, 5) if q_second_year is not None else None,
        "hazard_first_90_days": round(1 - s_at(curve, 90), 5),
        "won": (s_at(curve, 90) <= 0.45 and q_second_year is not None
                and q_second_year < 0.20 and at_risk_at(curve, 365) >= 40),
        "scorable": at_risk_at(curve, 365) >= 40,
    }
    # the same curve for the whole record's submit dates, descriptive only: it is
    # contaminated by the migration and is printed to show by how much.
    all_obs = []
    for r in usable:
        if r["status"] == "Reported":
            all_obs.append(((T - r["submit"]).days, False))
        elif r["update"] is not None:
            all_obs.append((max((r["update"] - r["submit"]).days, 0), True))
    all_curve = kaplan_meier(all_obs)
    results["P1_survival"]["contaminated_whole_record"] = {
        "note": "descriptive only: before 2019-09-10 the update_date is a migration stamp, "
                "so these waits are not waits",
        "S_90": round(s_at(all_curve, 90), 5),
        "S_365": round(s_at(all_curve, 365), 5),
        "S_730": round(s_at(all_curve, 730), 5),
    }

    # ---------------------------------------------------------------- P2 and P3
    in_index_C = [r for r in cohort if r["in_index"]]
    p2 = {
        "obsoleted": share(in_index_C, lambda r: r["obsoleted"] is True),
        "not_obsoleted": share(in_index_C, lambda r: r["obsoleted"] is False),
    }
    if p2["obsoleted"]["pending_share"] is not None and p2["not_obsoleted"]["pending_share"] is not None:
        p2["difference_points"] = round(
            100 * (p2["obsoleted"]["pending_share"] - p2["not_obsoleted"]["pending_share"]), 3)
        p2["won"] = (p2["difference_points"] >= 3.0
                     and p2["obsoleted"]["n"] >= 100 and p2["not_obsoleted"]["n"] >= 100)
    p2["unrestricted_descriptive"] = {
        "obsoleted": share([r for r in rows if r["in_index"]], lambda r: r["obsoleted"] is True),
        "not_obsoleted": share([r for r in rows if r["in_index"]], lambda r: r["obsoleted"] is False),
    }
    results["P2_obsoleted"] = p2

    p3 = {
        "no_wg": share(in_index_C, lambda r: not r["wg"]),
        "has_wg": share(in_index_C, lambda r: bool(r["wg"])),
    }
    if p3["no_wg"]["pending_share"] is not None and p3["has_wg"]["pending_share"] is not None:
        p3["difference_points"] = round(
            100 * (p3["no_wg"]["pending_share"] - p3["has_wg"]["pending_share"]), 3)
        p3["won"] = (p3["difference_points"] >= 3.0
                     and p3["no_wg"]["n"] >= 100 and p3["has_wg"]["n"] >= 100)
    p3["unrestricted_descriptive"] = {
        "no_wg": share([r for r in rows if r["in_index"]], lambda r: not r["wg"]),
        "has_wg": share([r for r in rows if r["in_index"]], lambda r: bool(r["wg"])),
    }
    results["P3_no_working_group"] = p3

    # ---------------------------------------------------------------- P4
    def waits(pred):
        out = []
        for r in cohort:
            if r["status"] != "Reported" and r["update"] is not None and pred(r):
                out.append(max((r["update"] - r["submit"]).days, 0))
        return out

    ed_wait, te_wait = waits(lambda r: r["type"] == "Editorial"), waits(lambda r: r["type"] == "Technical")
    p4 = {
        "editorial": share(cohort, lambda r: r["type"] == "Editorial"),
        "technical": share(cohort, lambda r: r["type"] == "Technical"),
        "median_wait_editorial_days": statistics.median(ed_wait) if ed_wait else None,
        "median_wait_technical_days": statistics.median(te_wait) if te_wait else None,
        "wait_quantiles_editorial": quantiles(ed_wait),
        "wait_quantiles_technical": quantiles(te_wait),
    }
    p4["difference_points"] = round(
        100 * (p4["technical"]["pending_share"] - p4["editorial"]["pending_share"]), 3)
    p4["won"] = (p4["difference_points"] >= 2.0
                 and p4["median_wait_editorial_days"] is not None
                 and p4["median_wait_technical_days"] is not None
                 and p4["median_wait_editorial_days"] < p4["median_wait_technical_days"])
    results["P4_type"] = p4

    # ------------------------------------------------ the composition of the 728
    ages = [(T - r["submit"]).days for r in pending_all
            if r["submit"] and r["errata_id"] not in QUARANTINED and r["submit"] <= T]
    doc_counts = collections.Counter(r["doc"] for r in pending_all)
    submitter_counts = collections.Counter(r["submitter"] for r in pending_all if r["submitter"])
    pending_in_index = [r for r in pending_all if r["in_index"]]
    era = collections.Counter(
        (r["rfc_date"].year // 10 * 10) for r in pending_in_index if r["rfc_date"])
    results["the_728"] = {
        "n": len(pending_all),
        "age_days": quantiles(ages),
        "age_years_median": round(statistics.median(ages) / 365.25, 3) if ages else None,
        "age_years_max": round(max(ages) / 365.25, 3) if ages else None,
        "older_than_5y": sum(1 for a in ages if a > 5 * 365.25),
        "older_than_10y": sum(1 for a in ages if a > 10 * 365.25),
        "by_type": dict(collections.Counter(r["type"] for r in pending_all)),
        "by_stream": dict(collections.Counter(r["stream"] for r in pending_in_index)),
        "by_area": dict(collections.Counter(r["area"] or "(none)" for r in pending_in_index)),
        "by_rfc_status": dict(collections.Counter(r["rfc_status"] for r in pending_in_index)),
        "on_obsoleted_rfcs": sum(1 for r in pending_in_index if r["obsoleted"]),
        "on_rfcs_without_wg": sum(1 for r in pending_in_index if not r["wg"]),
        "target_rfc_decade": {str(k): v for k, v in sorted(era.items())},
        "distinct_documents": len(doc_counts),
        "top_documents": doc_counts.most_common(15),
        "distinct_submitters": len(submitter_counts),
        "top_submitters_count_only": [n for _name, n in submitter_counts.most_common(10)],
        "single_report_submitters": sum(1 for _n, c in submitter_counts.items() if c == 1),
        "age_by_type_days": {
            t: quantiles([(T - r["submit"]).days for r in pending_all
                          if r["type"] == t and r["submit"] and r["errata_id"] not in QUARANTINED
                          and r["submit"] <= T])
            for t in ("Editorial", "Technical")
        },
        "oldest_ten": [
            {"errata_id": r["errata_id"], "doc": r["doc"], "type": r["type"],
             "submitted": r["submit"].isoformat(), "age_days": (T - r["submit"]).days,
             "stream": r["stream"], "wg": r["wg"], "obsoleted": r["obsoleted"]}
            for r in sorted([r for r in pending_all if r["submit"] and r["submit"] <= T],
                            key=lambda r: r["submit"])[:10]
        ],
    }

    # the class the norm pre-decides, unrestricted: pending errata on obsoleted RFCs
    pre_decided = [r for r in pending_in_index if r["obsoleted"]]
    results["pre_decided_and_unapplied"] = {
        "n": len(pre_decided),
        "note": "Errata in status Reported whose target RFC has been obsoleted. The IESG's active "
                "statement says an erratum on an obsolete RFC should be Rejected on either branch "
                "of its own test. The rule is published; on these it has not been applied.",
        "age_days": quantiles([(T - r["submit"]).days for r in pre_decided
                               if r["submit"] and r["submit"] <= T]),
        "oldest_five": [
            {"errata_id": r["errata_id"], "doc": r["doc"], "submitted": r["submit"].isoformat()}
            for r in sorted([r for r in pre_decided if r["submit"] and r["submit"] <= T],
                            key=lambda r: r["submit"])[:5]
        ],
    }

    # ------------------------------------------------ per-stream, descriptive
    results["by_stream_cohort_C"] = {
        s: share(in_index_C, lambda r, s=s: r["stream"] == s)
        for s in sorted({r["stream"] for r in in_index_C if r["stream"]})
    }
    results["by_stream_all"] = {
        s: share([r for r in rows if r["in_index"]], lambda r, s=s: r["stream"] == s)
        for s in sorted({r["stream"] for r in rows if r["in_index"] and r["stream"]})
    }

    # ------------------------------------- the two paths, measured as two curves
    # Descriptive, added after the predictions were fixed and committed: P4 asked
    # for two shares and two medians; this asks the same question of the whole
    # waiting-time distribution, which is what the figure draws.
    def km_median(curve):
        for time, _risk, _events, surv in curve:
            if surv <= 0.5:
                return time
        return None

    paths = {}
    for kind in ("Editorial", "Technical"):
        obs = []
        for r in cohort:
            if r["type"] != kind:
                continue
            if r["status"] == "Reported":
                obs.append(((T - r["submit"]).days, False))
            elif r["update"] is not None:
                obs.append((max((r["update"] - r["submit"]).days, 0), True))
        c = kaplan_meier(obs)
        paths[kind] = {
            "n": len(obs),
            "km_median_days": km_median(c),
            "S": {str(t): round(s_at(c, t), 5) for t in marks},
            "at_risk": {str(t): at_risk_at(c, t) for t in marks},
            "adjudicated_within_7_days": sum(1 for t, e in obs if e and t <= 7),
            "curve": [[t, risk, ev, round(s, 6)] for t, risk, ev, s in c],
        }
    results["two_paths"] = paths
    results["P1_survival"]["km_median_days_whole_cohort"] = km_median(curve)
    results["P1_survival"]["curve"] = [[t, risk, ev, round(s, 6)] for t, risk, ev, s in curve]

    # who signs the verdict, by path, in the clean cohort
    results["verifiers_cohort_C"] = {
        kind: collections.Counter(
            r["verifier"] or "(blank)" for r in cohort
            if r["type"] == kind and r["status"] != "Reported").most_common(8)
        for kind in ("Editorial", "Technical")
    }

    # the difficulty confound, addressed as far as this record allows: within the
    # technical path in the clean cohort, is the pending set textually bigger than
    # the adjudicated one? Length is a crude proxy and is reported as one.
    def textlen(e):
        return len((e.get("orig_text") or "") + (e.get("correct_text") or "") + (e.get("notes") or ""))

    by_id = {str(e["errata_id"]): e for e in errata}
    tech_C = [r for r in cohort if r["type"] == "Technical"]
    results["difficulty_proxy"] = {
        "note": "Characters of orig_text + correct_text + notes. A proxy for how much there is "
                "to read, not for how hard the judgement is; reported so the routing claim is "
                "not left resting on an untested alternative.",
        "technical_pending": quantiles([textlen(by_id[r["errata_id"]]) for r in tech_C
                                        if r["status"] == "Reported"]),
        "technical_adjudicated": quantiles([textlen(by_id[r["errata_id"]]) for r in tech_C
                                            if r["status"] != "Reported"]),
        "editorial_pending": quantiles([textlen(by_id[r["errata_id"]]) for r in cohort
                                        if r["type"] == "Editorial" and r["status"] == "Reported"]),
        "editorial_adjudicated": quantiles([textlen(by_id[r["errata_id"]]) for r in cohort
                                            if r["type"] == "Editorial" and r["status"] != "Reported"]),
    }

    # the one desk that signs with an institution's name rather than a person's
    results["rfc_editor_as_verifier"] = {
        "cohort_C": dict(collections.Counter(
            r["type"] for r in cohort if r["verifier"] == "RFC Editor")),
        "whole_record": dict(collections.Counter(
            r["type"] for r in rows if r["verifier"] == "RFC Editor")),
        "cohort_C_editorial_adjudicated": sum(
            1 for r in cohort if r["type"] == "Editorial" and r["status"] != "Reported"),
        "distinct_verifier_names_cohort_C": len({r["verifier"] for r in cohort
                                                 if r["verifier"]}),
    }

    # F-072's rule, written by Session 72 and applied here by a session that did
    # not write it: never take a display name as an identity; fold it, and report
    # the fold and what it moved.
    def fold_name(name):
        return re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()

    raw_names = collections.Counter(r["verifier"] for r in rows if r["verifier"])
    folded = collections.Counter()
    for name, count in raw_names.items():
        folded[fold_name(name)] += count
    collisions = {name: {"suffixed": count, "plain": raw_names[fold_name(name)]}
                  for name, count in raw_names.items()
                  if fold_name(name) != name and fold_name(name) in raw_names}
    results["verifier_identities"] = {
        "note": "F-072's rule applied by a night that did not write it. Role suffixes only are "
                "folded; misspellings of a name are listed, not merged, because merging them "
                "would be this measurement asserting an identity rather than reporting one.",
        "distinct_display_strings": len(raw_names),
        "distinct_after_folding_role_suffixes": len(folded),
        "collisions": collisions,
        "strings_with_a_parenthesis": sorted(n for n in raw_names if "(" in n),
        "cohort_C_distinct_display_strings": len({r["verifier"] for r in cohort if r["verifier"]}),
        "cohort_C_distinct_folded": len({fold_name(r["verifier"]) for r in cohort if r["verifier"]}),
    }

    # equal-horizon comparison, which the raw per-year pending share cannot give:
    # every submission year that is now at least 365 days old, scored on the same
    # 365-day window. This is the only way this record can say whether the
    # institution has become slower, and it is a weak way.
    horizon = {}
    for year in range(2019, T.year + 1):
        group = [r for r in cohort
                 if r["submit"].year == year and (T - r["submit"]).days >= 365]
        if len(group) < 30:
            continue
        judged = sum(1 for r in group
                     if r["status"] != "Reported" and r["update"] is not None
                     and (r["update"] - r["submit"]).days <= 365)
        horizon[str(year)] = {"n": len(group), "judged_within_365d": judged,
                              "share": round(judged / len(group), 5)}
    results["equal_horizon_by_submission_year"] = {
        "note": "Share of a submission year's errata that had a verdict within 365 days of "
                "being reported. Only years with at least 30 records already 365 days old are "
                "listed; the cohort restriction to 2019-09-10 makes 2019 partial.",
        "years": horizon,
    }

    # ------------------------------------------------ arrival and disposal rates
    by_year_submitted = collections.Counter(
        r["submit"].year for r in usable)
    by_year_pending = collections.Counter(
        r["submit"].year for r in usable if r["status"] == "Reported")
    results["arrivals"] = {
        "submitted_per_year": dict(sorted(by_year_submitted.items())),
        "still_reported_per_year": dict(sorted(by_year_pending.items())),
        "pending_share_per_year": {
            str(y): round(by_year_pending.get(y, 0) / n, 5)
            for y, n in sorted(by_year_submitted.items())
        },
    }

    # The identified population, written out so a later session can go and look.
    # Identifiers, a type, a date: metadata this work derives, not the submitters'
    # text, which stays out of the repository. Falsifier S73.ROUTE728 is checked
    # against this file.
    roster = os.path.join(here, "pending-2026-08-28.json")
    with open(roster, "w", encoding="utf-8") as fh:
        json.dump({
            "note": "The 728 errata in status Reported on 2026-08-28, by identifier. Falsifier "
                    "S73.ROUTE728 (due 2027-08-28) is checked against this list: re-fetch "
                    "errata.json, look up each id, and compare the share adjudicated in the "
                    "editorial group with the share in the technical group.",
            "observation_date": T.isoformat(),
            "n": len(pending_all),
            "errata": [{"errata_id": r["errata_id"], "doc": r["doc"], "type": r["type"],
                        "submit_date": r["submit"].isoformat() if r["submit"] else None}
                       for r in sorted(pending_all, key=lambda r: int(r["errata_id"]))],
        }, fh, indent=0, ensure_ascii=False)
        fh.write("\n")

    out = os.path.join(here, "results.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False, default=str)
        fh.write("\n")
    print(json.dumps({k: results[k] for k in ("counts", "P5_instrument")}, indent=1, default=str))
    print("P1 S(90) =", results["P1_survival"]["S_90"],
          "S(365) =", results["P1_survival"]["S_365"],
          "S(730) =", results["P1_survival"]["S_730"],
          "q2 =", results["P1_survival"]["q_second_year"],
          "at risk @365 =", results["P1_survival"]["at_risk_at_365"],
          "won =", results["P1_survival"]["won"])
    print("P2", json.dumps(results["P2_obsoleted"], default=str)[:400])
    print("P3", json.dumps(results["P3_no_working_group"], default=str)[:400])
    print("P4", json.dumps({k: v for k, v in results["P4_type"].items()
                            if k not in ("wait_quantiles_editorial", "wait_quantiles_technical")},
                           default=str)[:500])
    print("->", out)


if __name__ == "__main__":
    main()
