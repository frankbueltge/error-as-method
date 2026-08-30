#!/usr/bin/env python3
"""measure.py — Session 75, 2026-08-30.

Offline, stdlib only. Reads `harvest.json` and nothing else; makes no network call; writes
`results.json`. Every number in `work.md` comes from here, so that a stranger with the harvest can
re-derive the whole argument without touching the far end again.

The five conditions were fixed in `PREDICTIONS.md` before this file existed. This file scores them
and does not restate them.
"""

import json
import os
import statistics
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
MIN_N = 1000  # fixed in PREDICTIONS.md, before the branch sizes were known


def pct(a, b):
    return None if not b else round(100.0 * a / b, 4)


def gap(values):
    """Max minus min, in points, over the branches that clear MIN_N. The comparative quantity."""
    if len(values) < 2:
        return None
    return round(max(values) - min(values), 4)


def trimmed_gap(values):
    """The same quantity with the single highest and single lowest branch dropped.

    Post-hoc and marked as such everywhere it is reported. A max-minus-min over fourteen branches
    of wildly unequal size can be carried by one small branch; this says whether it is.
    """
    if len(values) < 4:
        return None
    v = sorted(values)[1:-1]
    return round(max(v) - min(v), 4)


def jaccard(a, b):
    u = a | b
    return 0.0 if not u else len(a & b) / len(u)


def main():
    H = json.load(open(os.path.join(HERE, "harvest.json")))
    R = {
        "night": "2026-08-30",
        "session": 75,
        "window": H["window"],
        "source_meta": H.get("meta", {}),
        "population_total": H["total"],
        "branch_floor_n": MIN_N,
    }

    by = H["by_product"]
    branches = list(by.keys())
    sizes = {p: by[p]["total_from_aggs_query"] for p in branches}
    scored = sorted([p for p in branches if sizes[p] >= MIN_N], key=lambda p: -sizes[p])
    R["branches_all"] = {p: sizes[p] for p in sorted(branches, key=lambda p: -sizes[p])}
    R["branches_scored"] = scored
    R["branches_below_floor"] = {p: sizes[p] for p in branches if sizes[p] < MIN_N}

    # PREDICTIONS.md said "the eleven values of product", read off a neighbouring window. This
    # window has a different number, because the institution renamed a product inside it. The
    # operative restriction fixed in advance was n >= 1000, and that is what is applied.
    R["branch_count_predicted"] = 11
    R["branch_count_found"] = len(branches)

    # ---------------------------------------------------------------- per-branch shares
    rows = {}
    for p in branches:
        rec = by[p]
        n = rec["total_from_aggs_query"]
        resp = dict(rec["company_response"])
        tim = dict(rec["timely"])
        narr = {str(k): v for k, v in dict(rec["has_narrative"]).items()}
        via = dict(rec["submitted_via"])
        responded = sum(resp.values())
        rows[p] = {
            "n": n,
            "company_response": resp,
            "unnormed_n": n - responded,
            "unnormed_pct": pct(n - responded, n),
            "monetary_pct": pct(resp.get("Closed with monetary relief", 0), n),
            "nonmonetary_pct": pct(resp.get("Closed with non-monetary relief", 0), n),
            "explanation_pct": pct(resp.get("Closed with explanation", 0), n),
            "untimely_response_pct": pct(resp.get("Untimely response", 0), n),
            "timely_no_pct": pct(tim.get("No", 0), n),
            "has_narrative_pct": pct(narr.get("1", narr.get("True", 0)), n),
            "submitted_web_pct": pct(via.get("Web", 0), n),
            "submitted_referral_n": via.get("Referral", 0),
        }
    R["by_branch"] = rows

    # ---------------------------------------------------------------- P1
    tot_resp = sum(v for p in branches for v in dict(by[p]["company_response"]).values())
    unnormed_pop = H["total"] - tot_resp
    p1_vals = [rows[p]["unnormed_pct"] for p in scored]
    R["P1"] = {
        "claim": "the routing gap in WHETHER a norm arrives does not port to a compelled applier",
        "comparative_quantity_points": gap(p1_vals),
        "comparative_threshold_points": 5.0,
        "comparative_won": gap(p1_vals) is not None and gap(p1_vals) < 5.0,
        "comparative_blind": True,
        "comparative_trimmed_points": trimmed_gap(p1_vals),
        "trimmed_is_post_hoc": True,
        "absolute_quantity_pct": pct(unnormed_pop, H["total"]),
        "absolute_threshold_pct": 1.0,
        "absolute_won": pct(unnormed_pop, H["total"]) < 1.0,
        "absolute_blind": False,
        "absolute_note": "carried expectation, not a blind prediction; declared in PREDICTIONS.md",
        "unnormed_n_population": unnormed_pop,
        "per_branch_pct": {p: rows[p]["unnormed_pct"] for p in scored},
    }

    # ---------------------------------------------------------------- P2
    p2_vals = [rows[p]["monetary_pct"] for p in scored]
    R["P2"] = {
        "claim": "the gap relocates into WHICH norm arrives",
        "quantity_points": gap(p2_vals),
        "threshold_points": 10.0,
        "won": gap(p2_vals) is not None and gap(p2_vals) >= 10.0,
        "trimmed_points_post_hoc": trimmed_gap(p2_vals),
        "per_branch_pct": {p: rows[p]["monetary_pct"] for p in scored},
        "highest": max(scored, key=lambda p: rows[p]["monetary_pct"]) if scored else None,
        "lowest": min(scored, key=lambda p: rows[p]["monetary_pct"]) if scored else None,
        "ratio_highest_to_lowest": (
            round(max(p2_vals) / min(p2_vals), 1) if p2_vals and min(p2_vals) else None),
        "ratio_is_descriptive": "the quantity fixed in advance is the gap in points; this ratio is "
                                "reported because a gap in points understates a difference whose "
                                "lower end is near zero.",
    }

    # ---------------------------------------------------------------- P3
    p3_vals = [rows[p]["timely_no_pct"] for p in scored]
    R["P3"] = {
        "claim": "the deadline is not kept evenly across the branches",
        "quantity_points": gap(p3_vals),
        "threshold_points": 3.0,
        "won": gap(p3_vals) is not None and gap(p3_vals) >= 3.0,
        "trimmed_points_post_hoc": trimmed_gap(p3_vals),
        "per_branch_pct": {p: rows[p]["timely_no_pct"] for p in scored},
        "highest": max(scored, key=lambda p: rows[p]["timely_no_pct"]) if scored else None,
        "lowest": min(scored, key=lambda p: rows[p]["timely_no_pct"]) if scored else None,
        "ratio_highest_to_lowest": (
            round(max(p3_vals) / min(p3_vals), 1) if p3_vals and min(p3_vals) else None),
    }

    # ---------------------------------------------------------------- P4
    U = H["issue_vocabulary_union"]
    inc = H["incidence"]
    totals_pre = {i: sum((inc[p].get(i) or 0) for p in by) for i in U}
    sets = {p: {i for i in U if (inc[p].get(i) or 0) > 0} for p in scored}
    pairs = []
    for a in range(len(scored)):
        for b in range(a + 1, len(scored)):
            pa, pb = scored[a], scored[b]
            pairs.append({"a": pa, "b": pb, "jaccard": round(jaccard(sets[pa], sets[pb]), 4),
                          "shared": len(sets[pa] & sets[pb])})
    occ = {i: sum(1 for p in scored if i in sets[p]) for i in U}
    present = [i for i in U if occ[i] > 0]
    exactly_one = [i for i in present if occ[i] == 1]
    mean_j = round(statistics.mean(p["jaccard"] for p in pairs), 4) if pairs else None
    b_pct = pct(len(exactly_one), len(present))
    R["P4"] = {
        "claim": "the classification decides what the difference may be called",
        "vocabulary_union_size": len(U),
        "vocabulary_present_in_window": len(present),
        "mean_pairwise_jaccard": mean_j,
        "mean_pairwise_jaccard_threshold": 0.15,
        "share_in_exactly_one_branch_pct": b_pct,
        "share_threshold_pct": 60.0,
        "won": (mean_j is not None and mean_j < 0.15 and b_pct is not None and b_pct >= 60.0),
        "won_half_jaccard": mean_j is not None and mean_j < 0.15,
        "won_half_share": b_pct is not None and b_pct >= 60.0,
        "disjoint_pairs": [p for p in pairs if p["shared"] == 0],
        "vocabulary_size_per_branch": {p: len(sets[p]) for p in scored},
        "issue_occurrence_histogram": {str(k): sum(1 for i in present if occ[i] == k)
                                       for k in sorted(set(occ[i] for i in present))},
        "pairs": sorted(pairs, key=lambda d: -d["jaccard"])[:20],
        "disjoint_pair_count": sum(1 for p in pairs if p["shared"] == 0),
        "pair_count": len(pairs),
        "disjoint_pair_pct": pct(sum(1 for p in pairs if p["shared"] == 0), len(pairs)),
        "shared_core": sorted(
            [{"issue": i, "branches": occ[i], "total": totals_pre.get(i, 0)}
             for i in present if occ[i] >= 7],
            key=lambda d: (-d["branches"], -d["total"])),
        "sensitivity_excluding_rename_pairs_post_hoc": None,  # filled below
        "boundary": "U is the union of issue strings surfaced by six facet slices per branch, not "
                    "the institution's full taxonomy; issues too rare to reach any facet are "
                    "outside it and unmeasured.",
    }

    # Post-hoc, and marked as such: the two highest-overlap pairs in the table are one product
    # compared with itself under its old name (F-086). This says what the mean overlap is with
    # every such pair removed. The scored value above is unchanged.
    RENAMES = [
        ("Credit reporting or other personal consumer reports",
         "Credit reporting, credit repair services, or other personal consumer reports"),
        ("Credit card", "Credit card or prepaid card"),
        ("Prepaid card", "Credit card or prepaid card"),
        ("Payday loan, title loan, personal loan, or advance loan",
         "Payday loan, title loan, or personal loan"),
    ]
    ren_set = {frozenset(r) for r in RENAMES}
    kept = [q for q in pairs if frozenset((q["a"], q["b"])) not in ren_set]
    R["P4"]["sensitivity_excluding_rename_pairs_post_hoc"] = {
        "pairs_excluded": len(pairs) - len(kept),
        "which": [sorted(r) for r in RENAMES],
        "mean_pairwise_jaccard": round(statistics.mean(q["jaccard"] for q in kept), 4) if kept else None,
        "scored_value_unchanged": R["P4"]["mean_pairwise_jaccard"],
        "note": "post-hoc; the prediction is scored on the branches as the record gives them, "
                "which is what PREDICTIONS.md fixed.",
    }

    # what the plate needs: the incidence rows in the branch order it draws, and one fixed
    # column order — by the first branch (largest first) in which a string occurs, then by how
    # often it occurs. Deterministic; no choice is made after the numbers are seen.
    all_branches = list(R["branches_all"].keys())
    sets_all = {p: {i for i in U if (inc[p].get(i) or 0) > 0} for p in all_branches}
    totals = {i: sum((inc[p].get(i) or 0) for p in all_branches) for i in U}

    def first_branch(i):
        for k, p in enumerate(all_branches):
            if i in sets_all[p]:
                return k
        return len(all_branches)

    R["issue_order_for_figure"] = sorted(
        [i for i in U if totals[i] > 0], key=lambda i: (first_branch(i), -totals[i], i))
    R["incidence_for_figure"] = {p: {i: (inc[p].get(i) or 0) for i in sets_all[p]}
                                 for p in all_branches}
    R["issue_totals"] = {i: totals[i] for i in R["issue_order_for_figure"]}

    # ---------------------------------------------------------------- P5a
    disagreements = []
    for p in branches:
        a = by[p]["total_from_aggs_query"]
        c = by[p]["total_from_count_query"]
        f = dict(H["facets_unfiltered"]["product"]).get(p)
        if not (a == c == f):
            disagreements.append({"branch": p, "aggs_query": a, "count_query": c, "facet": f})
    R["P5a"] = {
        "claim": "three routes to one branch total agree",
        "comparisons": len(branches) * 2,
        "branches": len(branches),
        "disagreements": disagreements,
        "won": not disagreements,
    }

    # ---------------------------------------------------------------- P5b + the id sample
    S = H["sample"]
    recs = S["records"]
    misses = S["misses"]
    in_window = [r for r in recs if H["window"]["date_received_min"] <= (r["date_received"] or "")[:10]
                 <= H["window"]["date_received_max"]]
    prod_counts = {}
    for r in in_window:
        prod_counts[r["product"]] = prod_counts.get(r["product"], 0) + 1
    two_largest = scored[:2]
    checks = []
    for p in two_largest:
        pop = pct(sizes[p], H["total"])
        smp = pct(prod_counts.get(p, 0), len(in_window))
        checks.append({"branch": p, "population_pct": pop, "sample_pct": smp,
                       "delta_points": round(abs(pop - smp), 4) if (pop is not None and smp is not None) else None})
    R["P5b"] = {
        "claim": "a seeded sample fetched through the per-complaint endpoint reproduces the "
                 "population's product shares",
        "seed": S["seed"], "draws": S["n"],
        "returned_a_record": len(recs),
        "returned_nothing": len(misses),
        "in_window": len(in_window),
        "checks": checks,
        "threshold_points": 3.0,
        "won": all(c["delta_points"] is not None and c["delta_points"] <= 3.0 for c in checks),
    }

    # measurements carried by the same sample, not predictions
    R["id_density"] = {
        "id_range": [S["lo"], S["hi"]],
        "draws": S["n"],
        "published_and_returned_pct": pct(len(recs), S["n"]),
        "returned_nothing_pct": pct(len(misses), S["n"]),
        "returned_but_out_of_window_pct": pct(len(recs) - len(in_window), S["n"]),
        "reading": "an id in this range that returns no record is one the database does not "
                   "publish. The institution's own sentence names one reason (complaints referred "
                   "to other regulators are never published); non-contiguous id assignment and "
                   "complaints withdrawn or still unpublished are others. This measurement does "
                   "not distinguish them and no cause is asserted.",
    }

    lags, lag_by_branch = [], {}
    for r in in_window:
        try:
            d0 = datetime.datetime.fromisoformat(r["date_received"].replace("Z", "+00:00"))
            d1 = datetime.datetime.fromisoformat(r["date_sent_to_company"].replace("Z", "+00:00"))
        except (AttributeError, ValueError):
            continue
        days = (d1 - d0).total_seconds() / 86400.0
        lags.append(days)
        lag_by_branch.setdefault(r["product"], []).append(days)
    R["routing_lag_days"] = {
        "n": len(lags),
        "median": round(statistics.median(lags), 4) if lags else None,
        "mean": round(statistics.mean(lags), 4) if lags else None,
        "same_day_pct": pct(sum(1 for x in lags if x < 1.0), len(lags)),
        "over_15_days_pct": pct(sum(1 for x in lags if x > 15.0), len(lags)),
        "max": round(max(lags), 4) if lags else None,
        "by_branch_median": {p: round(statistics.median(v), 4)
                             for p, v in sorted(lag_by_branch.items(), key=lambda kv: -len(kv[1]))
                             if len(v) >= 20},
        "histogram": [[d, sum(1 for x in lags if d <= x < d + 1)] for d in range(0, 30)]
                     + [[30, sum(1 for x in lags if x >= 30)]],
        "what": "date_sent_to_company minus date_received: the interval before anyone is asked.",
    }

    flagged = [r for r in in_window if r["has_narrative"]]
    served = [r for r in flagged if r["narrative_chars"] > 0]
    R["narratives"] = {
        "measured_on": "2026-08-30, sixteen days after the institution said it would cease "
                       "discretionary publication of complaint narratives",
        "sampled_in_window": len(in_window),
        "flagged_has_narrative": len(flagged),
        "flagged_and_text_returned": len(served),
        "served_pct_of_flagged": pct(len(served), len(flagged)),
        "population_flagged_pct": pct(
            sum(dict((str(k), v) for k, v in dict(by[p]["has_narrative"]).items()).get("1", 0)
                for p in branches), H["total"]),
        "note": "no narrative text is committed anywhere in this work; only the count and the "
                "character length were carried out of harvest.py.",
    }

    # ------------------------------------------------- sensitivity: the renamed branch, merged
    ren = [p for p in branches if p.lower().startswith("credit reporting")]
    if len(ren) > 1:
        n = sum(sizes[p] for p in ren)
        resp = {}
        for p in ren:
            for k, v in dict(by[p]["company_response"]).items():
                resp[k] = resp.get(k, 0) + v
        tim_no = sum(dict(by[p]["timely"]).get("No", 0) for p in ren)
        merged = {
            "merged_branches": ren, "n": n,
            "unnormed_pct": pct(n - sum(resp.values()), n),
            "monetary_pct": pct(resp.get("Closed with monetary relief", 0), n),
            "timely_no_pct": pct(tim_no, n),
        }
        others = [p for p in scored if p not in ren]
        for key, pred in (("unnormed_pct", "P1"), ("monetary_pct", "P2"), ("timely_no_pct", "P3")):
            vals = [rows[p][key] for p in others] + [merged[key]]
            merged[f"{pred}_gap_if_merged"] = gap(vals)
        R["sensitivity_renamed_branch_merged"] = merged
        R["sensitivity_note"] = (
            "The institution renamed products inside the window, so some products appear twice. "
            "Scoring uses the branches as the record gives them, fixed in advance; this block "
            "reports what the three gaps would be with the one rename that is a clean 1:1 "
            "substitution merged — 'Credit reporting, credit repair services, or other personal "
            "consumer reports' into 'Credit reporting or other personal consumer reports'. The "
            "other two renamings are NOT merged and are left as the record has them, because "
            "neither is 1:1: 'Credit card or prepaid card' corresponds to two later branches, and "
            "'Payday loan, title loan, or personal loan' to a later branch that also absorbs "
            "advance loans. Merging a one-to-many rename would invent a mapping the record does "
            "not contain.")

    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(R, fh, indent=1)

    # The population a dated falsifier needs: the complaint ids that, on this night, were flagged
    # as carrying a narrative AND still returned narrative text through the API, sixteen days after
    # the institution said it would cease publishing narratives. Ids and lengths only; the text
    # itself is not committed and never left harvest.py.
    with open(os.path.join(HERE, "narratives-2026-08-30.json"), "w") as fh:
        json.dump({
            "night": "2026-08-30", "session": 75,
            "falsifier": "S75.NARRATIVE",
            "measured_utc_date": "2026-08-30",
            "what": "Complaint ids from the seeded sample (seed 20260830) that were in the window, "
                    "carried has_narrative = true, and for which the search API returned non-empty "
                    "complaint_what_happened on this night. Re-fetch each in a year: if the text is "
                    "gone, the 2026-08-14 announcement reached this endpoint late; if it is still "
                    "there, 'publication' never meant this endpoint.",
            "announcement": "https://www.consumerfinance.gov/about-us/newsroom/"
                            "the-cfpb-to-cease-discretionary-publication-of-complaint-narratives-"
                            "and-visualizations/",
            "field_reference_at_the_time": "https://cfpb.github.io/api/ccdb/fields.html — lists "
                                           "fifteen fields 'currently included in the database' "
                                           "and no narrative field among them.",
            "count": len(served),
            "ids": [{"complaint_id": r["complaint_id"], "date_received": r["date_received"][:10],
                     "product": r["product"], "narrative_chars": r["narrative_chars"]}
                    for r in served],
        }, fh, indent=1)

    # ------------------------------------------------------------------- the scoreboard
    def mark(b):
        return "WON " if b else "LOST"
    print(f"population {R['population_total']:,} in {R['branch_count_found']} branches "
          f"({len(scored)} at or above n={MIN_N}); PREDICTIONS.md said {R['branch_count_predicted']}")
    print(f"P1 comparative {mark(R['P1']['comparative_won'])}  gap {R['P1']['comparative_quantity_points']} pts (< 5.0)")
    print(f"P1 absolute    {mark(R['P1']['absolute_won'])}  {R['P1']['absolute_quantity_pct']} % (< 1.0) [carried]")
    print(f"P2             {mark(R['P2']['won'])}  gap {R['P2']['quantity_points']} pts (>= 10.0)")
    print(f"P3             {mark(R['P3']['won'])}  gap {R['P3']['quantity_points']} pts (>= 3.0)")
    print(f"P4             {mark(R['P4']['won'])}  jaccard {R['P4']['mean_pairwise_jaccard']} (< 0.15), "
          f"private {R['P4']['share_in_exactly_one_branch_pct']} % (>= 60)")
    print(f"P5a            {mark(R['P5a']['won'])}  {len(R['P5a']['disagreements'])} disagreements")
    print(f"P5b            {mark(R['P5b']['won'])}  {R['P5b']['checks']}")
    print(f"id density: {R['id_density']['published_and_returned_pct']} % of drawn ids return a record")
    print(f"routing lag: median {R['routing_lag_days']['median']} d, "
          f"{R['routing_lag_days']['same_day_pct']} % same day, n={R['routing_lag_days']['n']}")
    print(f"narratives: {R['narratives']['flagged_and_text_returned']}/"
          f"{R['narratives']['flagged_has_narrative']} flagged records still return text")


if __name__ == "__main__":
    main()
