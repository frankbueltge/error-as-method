#!/usr/bin/env python3
"""inspect.py -- exploratory, written and run AFTER the predictions were closed and scored.

Nothing here is a prediction and nothing here scores one.  Its job is to ask what the forty rows
are made of, once the pre-registered quantities are on the record: which words the rule was
actually reading, whether the two corpora's differences survive the smallness of n=40, and how the
known forwards-looking defect in block window 0 behaves in a corpus that is not UK statute.

Writes inspection.json.  Everything it produces is marked exploratory in the work.
"""

import json
import re
from collections import Counter
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = json.load(open(HERE / "results.json"))
ROWS = R["rows"]
WORD = re.compile(r"\S+")


def fisher_two_sided(a, b, c, d):
    """Fisher's exact test on the 2x2 [[a,b],[c,d]], two-sided by the point-probability method.

    Written here rather than imported because this environment has no scientific stack.

    ITS SELF-CHECK WAS WRONG BEFORE THE FUNCTION WAS.  This docstring first said the check below
    used "a textbook 2x2 whose two-sided p is 0.0476 (Fisher's tea-tasting table, 3/1/1/3)".  The
    0.0476 was typed from memory and is not that table's value.  With margins 4,4 / 4,4 the
    hypergeometric point probabilities are 1/70, 16/70, 36/70, 16/70, 1/70 for a = 0..4, so the
    two-sided p by the point-probability method is 34/70 = 17/35 = 0.4857 for the 3/1/1/3 table and
    2/70 = 1/35 = 0.0286 for 4/0/0/4.  Both are derived in the self-check below from math.comb
    rather than remembered, which is the repair: a check written from memory can only test the
    memory.  Had the assertion been enforced, it would have failed a correct implementation.
    """
    n = a + b + c + d
    r1, r2, c1 = a + b, c + d, a + c

    def p(x):
        return comb(r1, x) * comb(r2, c1 - x) / comb(n, c1)

    obs = p(a)
    lo = max(0, c1 - r2)
    hi = min(r1, c1)
    return round(sum(p(x) for x in range(lo, hi + 1) if p(x) <= obs * (1 + 1e-9)), 4)


def context(row, span=6):
    """The carrier in its own words, with a few words either side -- so a reader can see what the
    rule was looking at without opening the corpus."""
    sheet = {r["n"]: r for r in json.load(open(HERE / "sheet.json"))["rows"]}
    text = sheet[row["n"]]["block_text"]
    m = re.search(r"\b" + re.escape(row["carrier"]) + r"\b", text, re.IGNORECASE)
    if not m:
        return None
    before = WORD.findall(text[:m.start()])[-span:]
    after = WORD.findall(text[m.end():])[:span]
    return " ".join(before + ["[[" + m.group(0) + "]]"] + after)


def main():
    uk = R["calibration"]["by_rule"]["R3_active_governor"]
    rfc = R["against_the_reader"]["M1"]["R3_active_governor"]

    # 1 -- what the rule was reading
    carriers = Counter(r["carrier"].lower() for r in ROWS)
    none_rows = [r for r in ROWS if not r["bearer_named"]]
    application_rows = [{"n": r["n"], "rfc": r["rfc"], "bearer": r["bearer"],
                         "r3": r["rules"]["R3_active_governor"], "m1": r["m1"],
                         "context": context(r)}
                        for r in ROWS if r["carrier"].lower() == "application"]

    # 2 -- does the difference survive n=40?
    tests = {
        "precision_of_R3_UK_vs_RFC": {
            "table": {"UK_right": uk["tp"], "UK_wrong": uk["fp"],
                      "RFC_right": rfc["tp"], "RFC_wrong": rfc["fp"]},
            "p_two_sided": fisher_two_sided(uk["tp"], uk["fp"], rfc["tp"], rfc["fp"])},
        "reader_base_rate_UK_vs_RFC": {
            "table": {"UK_yes": R["calibration"]["reader_yes"],
                      "UK_no": 40 - R["calibration"]["reader_yes"],
                      "RFC_yes": R["reading"]["m1_yes"], "RFC_no": 40 - R["reading"]["m1_yes"]},
            "p_two_sided": fisher_two_sided(
                R["calibration"]["reader_yes"], 40 - R["calibration"]["reader_yes"],
                R["reading"]["m1_yes"], 40 - R["reading"]["m1_yes"])},
        "agreement_of_R3_UK_vs_RFC": {
            "table": {"UK_agree": uk["agreements"], "UK_disagree": uk["disagreements"],
                      "RFC_agree": rfc["agreements"], "RFC_disagree": rfc["disagreements"]},
            "p_two_sided": fisher_two_sided(uk["agreements"], uk["disagreements"],
                                            rfc["agreements"], rfc["disagreements"])},
    }

    # The self-check, derived rather than remembered: both values are computed from the
    # hypergeometric distribution with math.comb and compared with the function's own answer.
    def _point(a, r1, r2, c1):
        return comb(r1, a) * comb(r2, c1 - a) / comb(r1 + r2, c1)

    derived_3113 = sum(_point(a, 4, 4, 4) for a in (0, 1, 3, 4))
    derived_4004 = sum(_point(a, 4, 4, 4) for a in (0, 4))
    tests["self_check"] = {
        "note": "derived from math.comb in this file, not quoted from a textbook",
        "table_3_1_1_3": {"derived": round(derived_3113, 4),
                          "function": fisher_two_sided(3, 1, 1, 3)},
        "table_4_0_0_4": {"derived": round(derived_4004, 4),
                          "function": fisher_two_sided(4, 0, 0, 4)},
    }
    assert tests["self_check"]["table_3_1_1_3"]["derived"] == \
        tests["self_check"]["table_3_1_1_3"]["function"]
    assert tests["self_check"]["table_4_0_0_4"]["derived"] == \
        tests["self_check"]["table_4_0_0_4"]["function"]

    # 2b -- what a hand reading of forty COULD have separated.  Holding the two fire counts at
    # what they were (19 in UK, 18 in the RFCs), how far apart must the two precisions be before
    # Fisher's exact test would call the difference significant at 0.05?
    detect = []
    for rfc_tp in range(0, rfc["fires"] + 1):
        p = fisher_two_sided(uk["tp"], uk["fp"], rfc_tp, rfc["fires"] - rfc_tp)
        detect.append({"rfc_right": rfc_tp,
                       "rfc_precision": round(rfc_tp / rfc["fires"], 4),
                       "p_two_sided": p, "significant_at_0.05": p < 0.05})
    sig = [d for d in detect if d["significant_at_0.05"]]
    tests["what_forty_rows_could_have_separated"] = {
        "note": "EXPLORATORY. UK is held at its published 13 right of 19 fires; the RFC arm is "
                "swept over every possible count of right answers on its 18 fires.",
        "uk_precision": uk["precision_on_yes"],
        "rfc_precision_observed": rfc["precision_on_yes"],
        "p_observed": fisher_two_sided(uk["tp"], uk["fp"], rfc["tp"], rfc["fp"]),
        "highest_rfc_precision_that_would_have_been_significant": max(
            (d["rfc_precision"] for d in sig if d["rfc_precision"] < uk["precision_on_yes"]),
            default=None),
        "gap_in_points_needed": None,
        "sweep": detect,
    }
    w = tests["what_forty_rows_could_have_separated"]
    if w["highest_rfc_precision_that_would_have_been_significant"] is not None:
        w["gap_in_points_needed"] = round(
            100 * (uk["precision_on_yes"] - w["highest_rfc_precision_that_would_have_been_significant"]), 2)

    # 2c -- the price of the question.  Holding both arms at tonight's proportions -- UK 19 fires
    # in 40 at precision 0.6842, the RFC series 18 in 40 -- how many hand-read rows would it take
    # before a gap the size of tonight's became visible at all?
    uk_p = uk["tp"] / uk["fires"]
    price = []
    for n in range(40, 1001, 20):
        ukf = round(n * uk["fires"] / 40)
        rfcf = round(n * rfc["fires"] / 40)
        uktp = round(ukf * uk_p)
        best = None
        for tp in range(rfcf + 1):
            if tp / rfcf >= uktp / ukf:
                break
            if fisher_two_sided(uktp, ukf - uktp, tp, rfcf - tp) < 0.05:
                best = tp / rfcf
        price.append({"rows_read": n, "uk_fires": ukf, "rfc_fires": rfcf,
                      "smallest_visible_gap_points": None if best is None
                      else round(100 * (uktp / ukf - best), 2)})
    observed_gap = 100 * (uk["precision_on_yes"] - rfc["precision_on_yes"])
    enough = next((r["rows_read"] for r in price
                   if r["smallest_visible_gap_points"] is not None
                   and r["smallest_visible_gap_points"] <= observed_gap), None)
    tests["the_price_of_the_question"] = {
        "note": "EXPLORATORY. Both arms held at tonight's proportions and scaled; the reader's "
                "verdicts are assumed to come out the same way, which is exactly what is not "
                "known. It is an order of magnitude, not a promise.",
        "observed_gap_points": round(observed_gap, 2),
        "rows_needed_to_see_a_gap_that_size": enough,
        "curve": price,
    }

    # 3 -- the forwards-looking window, in a corpus that is not UK statute
    by_direction = {}
    for d in ("before", "after"):
        sel = [r for r in ROWS if r["direction"] == d]
        if not sel:
            continue
        by_direction[d] = {
            "rows": len(sel),
            "reader_says_this_is_the_bearer": sum(1 for r in sel if r["m1"]),
            "precision_of_the_nearest_term": round(
                sum(1 for r in sel if r["m1"]) / len(sel), 4),
            "R3_fires": sum(1 for r in sel if r["rules"]["R3_active_governor"]),
            "R3_right_when_it_fires": sum(1 for r in sel
                                          if r["rules"]["R3_active_governor"] and r["m1"]),
        }

    out = {
        "note": "EXPLORATORY. Written after PREDICTIONS.md was scored; nothing here is a "
                "prediction, and no quantity here may be read as one.",
        "what_the_rule_was_reading": {
            "carriers": dict(carriers.most_common()),
            "distinct_carriers": len(carriers),
            "most_frequent": carriers.most_common(1)[0],
            "share_of_rows_carried_by_the_single_most_frequent_term": round(
                carriers.most_common(1)[0][1] / len(ROWS), 4),
            "rows_the_reader_called_NONE": len(none_rows),
            "their_carriers": dict(Counter(r["carrier"].lower() for r in none_rows).most_common()),
            "every_row_whose_carrier_is_application": application_rows,
        },
        "does_it_survive_n_40": tests,
        "the_forwards_looking_window": {
            "note": "Block window 0 looks forwards as well as back -- a defect Session 89 named, "
                    "Session 90 kept unrepaired so its replication would hold, and this night "
                    "inherits unchanged. In UK statute the nearest term stood AFTER the modal in "
                    "10 of 40 rows.",
            "UK_after_rows_published_by_session_91": 10,
            "RFC": by_direction,
        },
        "frame_effect": {
            "note": "Both samples are block-window-0 rows, where a carrier is in the obligation's "
                    "own block by construction. The population fire rates are not these.",
            "R3_over_the_sample_RFC": round(rfc["fires"] / 40, 4),
            "R3_over_the_sample_UK": round(uk["fires"] / 40, 4),
            "R3b_over_the_population_RFC_session_94": 0.2815,
            "R3b_over_the_population_UK_session_91": 0.3142,
        },
    }
    (HERE / "inspection.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")

    print("distinct carriers in 40 rows : %d; most frequent %r x %d"
          % (len(carriers), *carriers.most_common(1)[0]))
    print("rows the reader called NONE  : %d, their carriers %s"
          % (len(none_rows), out["what_the_rule_was_reading"]["their_carriers"]))
    for k, v in tests.items():
        if isinstance(v, dict) and "p_two_sided" in v and "table" in v:
            print("%-28s p = %s   %s" % (k, v["p_two_sided"], v["table"]))
    sc = tests["self_check"]
    print("self check, derived not quoted: 3/1/1/3 -> %s, 4/0/0/4 -> %s"
          % (sc["table_3_1_1_3"]["function"], sc["table_4_0_0_4"]["function"]))
    w = tests["what_forty_rows_could_have_separated"]
    print("forty rows could only have separated a precision gap of %s points or more "
          "(observed gap %.2f, p = %s)"
          % (w["gap_in_points_needed"],
             100 * (w["uk_precision"] - w["rfc_precision_observed"]), w["p_observed"]))
    pq = tests["the_price_of_the_question"]
    print("to see a gap of %.2f points at all, this line would have to hand-read about %s rows"
          % (pq["observed_gap_points"], pq["rows_needed_to_see_a_gap_that_size"]))
    for d, v in by_direction.items():
        print("carrier %-7s : %2d rows, precision %.4f, R3 fires %d of which right %d"
              % (d, v["rows"], v["precision_of_the_nearest_term"], v["R3_fires"],
                 v["R3_right_when_it_fires"]))
    print("wrote inspection.json")


if __name__ == "__main__":
    main()
