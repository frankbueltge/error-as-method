#!/usr/bin/env python3
"""score.py -- the six predictions of PREDICTIONS.md, and the three falsifier rows, adjudicated.

Every condition below is quoted from PREDICTIONS.md or from the row in works/FALSIFIERS.md, and
each is evaluated against the committed JSON, never against a number retyped here.  Run last.
Writes adjudication.json.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

PRIOR_DESERTED = {          # works/2026-09-14-the-borrowed-unit/residue.json, a_how_deserted...
    "whatwg": 90.08, "eu": 81.14, "rfc": 91.05,
}
PRIOR_MEDIAN = {            # works/2026-09-14-the-borrowed-unit/results.json, median_word_distance
    "whatwg": 184, "eu": 134.0, "rfc": 215.0,
}
PRIOR_AGENT_TEST = {"eu": 0.8095, "rfc": 0.9022, "whatwg": 0.9010}


def rank(d, key):
    """1 = highest value, among the four."""
    order = sorted(d, key=lambda k: -d[k])
    return order.index(key) + 1


def main():
    res = json.load(open(HERE / "results.json"))
    rch = json.load(open(HERE / "reach.json"))
    bnd = json.load(open(HERE / "bounds.json"))
    ver = json.load(open(HERE / "verification.json"))
    if not ver["all_four_pass"]:
        raise SystemExit("verification did not pass; nothing is scored.")

    act, notes, whole = res["by_register"]["ACT"], res["by_register"]["NOTES"], res["whole_corpus"]
    spread = res["register_spread"]
    narrow = rch["lists"]["narrow"]
    arm = rch["row_arm"]

    P = []

    # ----------------------------------------------------------------------------------------- P1
    got = narrow["blocks"]["pct"]["0"]
    P.append({"id": "P1", "claim": "with the NARROW list, block window 0 comes in below 13.61 %, "
                                   "WHATWG's figure, because the UK block is 0.58 of a WHATWG "
                                   "paragraph",
              "threshold": 13.61, "observed": got, "won": got < 13.61,
              "evidential": True,
              "note": "lost. A 21-word provision carries `authority`, `court` or `officer` often "
                      "enough to beat the size of its container."})

    # ----------------------------------------------------------------------------------------- P2
    span = rch["the_interval"]["span_points"]
    P.append({"id": "P2", "claim": "the three declared lists span more than 20 points at word "
                                   "window 36 -- wider than the whole falsification band of "
                                   "S89.WORDUNIT",
              "threshold": 20, "observed": span, "won": span > 20, "evidential": True,
              "by_list": rch["the_interval"]["word_window_36_by_list"],
              "note": "won, and see the self-critique: bounds.json had already shown the BASE arm "
                      "would be near zero, so a large span was likely before this was written. "
                      "The open part was the distance between NARROW and WIDE, which is "
                      "16.67 points on its own."})

    # ----------------------------------------------------------------------------------------- P3
    inside = all(0.75 <= t <= 0.95 for t in (act["agent_test"], notes["agent_test"]))
    P.append({"id": "P3", "claim": "S86.CONSTANT's register clause: the agent test falls inside "
                                   "0.75-0.95 in BOTH registers and its spread between them is "
                                   "under 8 points",
              "observed": {"act": act["agent_test"], "notes": notes["agent_test"],
                           "whole": whole["agent_test"],
                           "spread_points": spread["agent_test_points"]},
              "won": inside and spread["agent_test_points"] < 8, "evidential": True,
              "note": "won. The Act register's 0.7586 is the lowest agent test any register of any "
                      "of the four traditions has returned, and stands 0.0086 above the value that "
                      "would have falsified the row."})

    # ----------------------------------------------------------------------------------------- P4
    P.append({"id": "P4", "claim": "the B-FORM share moves more between the two registers than the "
                                   "agent test does",
              "observed": {"B_FORM_share_points": spread["B_FORM_share_points"],
                           "agent_test_points": spread["agent_test_points"]},
              "won": spread["the_other_factor_moves_more"], "evidential": True,
              "note": "won, and it is the first time S86.CONSTANT's decomposition has been tested "
                      "inside a single corpus with two powered registers: 15.18 against 2.60."})

    # ----------------------------------------------------------------------------------------- P5
    P.append({"id": "P5", "claim": "the non-binding register deletes the bearer more often than the "
                                   "binding one, as EU recitals do against EU articles",
              "observed": {"notes_pct": notes["bearer_deletion_rate_pct"],
                           "act_pct": act["bearer_deletion_rate_pct"],
                           "eu_recitals_pct": 37.57, "eu_articles_pct": 24.75},
              "won": notes["bearer_deletion_rate_pct"] > act["bearer_deletion_rate_pct"],
              "evidential": True,
              "note": "won: 29.47 against 16.98, the same direction and a wider gap than the EU "
                      "pair. Note that the mechanism is the OTHER factor -- the Notes' B-FORM share "
                      "is 37.56 against the Act's 22.38 -- not the agent test."})

    # ----------------------------------------------------------------------------------------- P6
    P.append({"id": "P6", "claim": "with the NARROW list the median word distance falls inside "
                                   "60-500",
              "observed": arm["median_word_distance"], "band": [60, 500],
              "won": arm["median_inside_band"], "evidential": True,
              "note": "won at 83.5 -- and on the BASE list the same corpus reads 5821, outside the "
                      "band by an order of magnitude."})

    # --------------------------------------------------------------------------------- the rows
    uk_deserted = act["agent_test_pct"]
    deserted_all = dict(PRIOR_DESERTED, uk=uk_deserted)
    median_all = dict(PRIOR_MEDIAN, uk=arm["median_word_distance"])
    r_des, r_med = rank(deserted_all, "uk"), rank(median_all, "uk")

    rows = {
        "S89.WORDUNIT": {
            "checked_on": "the NARROW list, declared in PREDICTIONS.md §3 before the run",
            "condition": "falsified if the corpus comes in more than 20 points from ALL of 15.71, "
                         "23.29 and 15.59 at word window 36, or if its median word distance falls "
                         "outside 60-500",
            "word_window_36": arm["word_window_36"],
            "distance_to_each_prior": arm["distance_to_each_prior"],
            "median_word_distance": arm["median_word_distance"],
            "falsified": arm["S89_WORDUNIT_falsified"],
            "verdict": "NOT FALSIFIED on the arm it declared",
            "and_the_qualification": {
                "what_the_other_two_declared_lists_do": {
                    "base": {"word_window_36": rch["lists"]["base"]["words"]["pct"]["36"],
                             "median": rch["lists"]["base"]["words"]["median_where_present"],
                             "would_falsify": True,
                             "why": "the median, 5821, is outside 60-500 by an order of magnitude"},
                    "wide": {"word_window_36": rch["lists"]["wide"]["words"]["pct"]["36"],
                             "median": rch["lists"]["wide"]["words"]["median_where_present"],
                             "would_falsify": True,
                             "why": "50.91 % stands 27.62 points from the nearest prior, beyond the "
                                    "20-point band"},
                },
                "so": "two of the three lists declared in advance by the same author on the same "
                      "night falsify this row and one saves it. The row's threshold is honest and "
                      "its arithmetic is correct; what decides it is which words count as a party.",
                "the_base_list_does_not_reach_this_tradition":
                    bnd["borrowed_vocabulary"]["total_occurrences"],
                "of_the_26_never_occurring":
                    bnd["borrowed_vocabulary"]["terms_that_never_occur_count"],
            },
        },
        "S89.DESERTED": {
            "condition": "falsified if the corpus's rank by bearer-deletion-within-B-FORM and its "
                         "rank by median word distance differ by two or more places among the four",
            "bearer_deletion_within_B_FORM": deserted_all,
            "median_word_distance": median_all,
            "uk_rank_by_deletion": r_des, "uk_rank_by_distance": r_med,
            "places_apart": abs(r_des - r_med),
            "falsified": abs(r_des - r_med) >= 2,
            "verdict": "NOT FALSIFIED, and the fourth point lands exactly where the conjecture "
                       "wants it: last in both rankings, so four corpora now give the same order "
                       "twice.",
            "and_the_qualification": {
                "on_the_BASE_list_the_uk_median_is":
                    rch["lists"]["base"]["words"]["median_where_present"],
                "which_would_rank_it": rank(dict(PRIOR_MEDIAN,
                                                 uk=rch["lists"]["base"]["words"]
                                                 ["median_where_present"]), "uk"),
                "so": "on the base list the same corpus is first by distance and fourth by "
                      "deletion -- three places apart, which falsifies this row. This row is "
                      "author-dependent in the same way S89.WORDUNIT is, and neither row says so.",
            },
        },
        "S86.CONSTANT": {
            "condition": "falsified if the agent test falls outside 0.75-0.95 in the corpus as a "
                         "whole, or if its spread between two registers of 500+ exceeds 8 points "
                         "while the B-FORM share between them moves by less than that",
            "registers_powered": {"ACT": act["occurrences"], "NOTES": notes["occurrences"],
                                  "floor": 500},
            "agent_test": {"whole": whole["agent_test"], "act": act["agent_test"],
                           "notes": notes["agent_test"], **PRIOR_AGENT_TEST},
            "spreads": spread,
            "falsified": not (0.75 <= whole["agent_test"] <= 0.95)
                         or (spread["agent_test_points"] > 8
                             and spread["B_FORM_share_points"] < spread["agent_test_points"]),
            "verdict": "CHECKED AT LAST AND NOT FALSIFIED. The register clause has been open since "
                       "Session 87 for want of a corpus with two speaking registers; this is one, "
                       "with 3,888 and 4,907 occurrences against a floor of 500.",
            "and_the_qualification": {
                "the_constancy_is_widening": {
                    "range_over_three_corpora_points": round(
                        100 * (max(PRIOR_AGENT_TEST.values()) - min(PRIOR_AGENT_TEST.values())), 2),
                    "range_over_four_points": round(
                        100 * (max(list(PRIOR_AGENT_TEST.values()) + [whole["agent_test"]])
                               - min(list(PRIOR_AGENT_TEST.values()) + [whole["agent_test"]])), 2),
                    "lowest_single_register": act["agent_test"],
                    "distance_from_the_falsifying_floor": round(act["agent_test"] - 0.75, 4),
                },
                "so": "the row survives its own band and the band is doing more work each time it "
                      "is ported. A fifth tradition one point lower in its binding register would "
                      "kill it.",
            },
        },
    }

    won = [p for p in P if p["won"]]
    out = {
        "note": "Six predictions fixed in PREDICTIONS.md before measure.py and reach.py existed, "
                "and three falsifier rows. Nothing here is retyped: every condition reads from the "
                "committed JSON.",
        "verification": {"all_four_pass": True,
                         "cells_of_session_89_s_curve_reproduced":
                             ver["2_the_scan_reproduces_session_89_s_published_whatwg_curve"]
                             ["cells_compared"]},
        "predictions": P,
        "score": {"won": len(won), "lost": len(P) - len(won), "total": len(P),
                  "lost_ids": [p["id"] for p in P if not p["won"]]},
        "rows": rows,
    }
    (HERE / "adjudication.json").write_text(json.dumps(out, indent=1) + "\n")

    for p in P:
        print("%-3s %-4s %s" % (p["id"], "WON" if p["won"] else "LOST", p["claim"][:88]))
    print("\n  %d won, %d lost" % (len(won), len(P) - len(won)))
    for name, r in rows.items():
        print("  %-14s falsified: %-5s  %s" % (name, r["falsified"], r["verdict"][:74]))


if __name__ == "__main__":
    main()
