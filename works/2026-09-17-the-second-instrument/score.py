#!/usr/bin/env python3
"""score.py -- the six predictions of PREDICTIONS.md §4, adjudicated mechanically.

Nothing here reads a prediction from prose.  Each condition is the one written in §4, restated as a
comparison over results.json, and the verdict is whatever the comparison returns.  Writes
adjudication.json.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = json.load(open(HERE / "results.json"))
A = R["against_the_reader"]
P = R["over_the_population"]

DECLARED = ["R1_adjacent_subject", "R2_no_competing_nominal", "R3_active_governor"]

out = {
 "note": "The six predictions of PREDICTIONS.md §4, adjudicated against results.json.  R3b is the "
         "repair §3 permits and is NOT one of the declared three; where it changes a verdict that "
         "is reported beside the verdict and never in place of it.",
 "predictions": {},
}


def add(pid, text, condition, survives, numbers):
    out["predictions"][pid] = {"prediction": text, "falsified_if": condition,
                               "verdict": "survives" if survives else "FALSIFIED",
                               "numbers": numbers}


# P1 -----------------------------------------------------------------------
best = max(A["by_rule"][n]["agreements"] for n in DECLARED)
add("P1", "No rule reaches 0.80 agreement with the reader over the 40 rows.",
    "any declared rule agrees with 32 or more of the 40", best < 32,
    {"agreements_by_rule": {n: A["by_rule"][n]["agreements"] for n in DECLARED},
     "best": best, "threshold": 32,
     "majority_baseline_always_NO": A["reader_no"]})

# P2 -----------------------------------------------------------------------
r1 = A["by_rule"]["R1_adjacent_subject"]
if r1["fires"] < 5:
    add("P2", "R1's precision on the rows where it fires is below the reader's 0.425.",
        "R1 precision-on-YES >= 0.425 with 5 or more firings", None,
        {"fires": r1["fires"], "verdict_note": "unscoreable: fewer than 5 firings"})
    out["predictions"]["P2"]["verdict"] = "unscoreable"
else:
    add("P2", "R1's precision on the rows where it fires is below the reader's 0.425.",
        "R1 precision-on-YES >= 0.425 with 5 or more firings",
        r1["precision_on_yes"] < 0.425,
        {"fires": r1["fires"], "precision_on_yes": r1["precision_on_yes"],
         "reader_base_rate": A["reader_base_rate"],
         "margin": round(0.425 - r1["precision_on_yes"], 4)})

# P3 -----------------------------------------------------------------------
add("P3", "The rules disagree with each other more than any of them disagrees with the reader.",
    "largest rule-to-rule disagreement < largest rule-to-reader disagreement",
    A["max_rule_to_rule_disagreement"] > A["max_rule_to_reader_disagreement"],
    {"max_rule_to_rule": A["max_rule_to_rule_disagreement"],
     "max_rule_to_reader": A["max_rule_to_reader_disagreement"],
     "pairwise": A["pairwise_rule_disagreement"],
     "disagreements_by_rule": {n: A["by_rule"][n]["disagreements"] for n in DECLARED}})

# P4 -----------------------------------------------------------------------
bestrule = max(DECLARED, key=lambda n: A["by_rule"][n]["agreements"])
corrected = {l: P[l]["by_rule"][bestrule]["corrected_reach_pct"] for l in ("base", "narrow", "wide")}
span = round(max(corrected.values()) - min(corrected.values()), 2)
corrected_b = {l: P[l]["by_rule"]["R3b_active_governor_own_block"]["corrected_reach_pct"]
               for l in ("base", "narrow", "wide")}
span_b = round(max(corrected_b.values()) - min(corrected_b.values()), 2)
add("P4", "Precision correction does not collapse the interval.",
    "span between the three corrected figures is 20 points or less", span > 20,
    {"best_agreeing_declared_rule": bestrule,
     "uncorrected_span_session_90": 50.15,
     "corrected_reach_pct": corrected, "corrected_span_points": span,
     "with_the_repair_R3b": corrected_b, "corrected_span_points_R3b": span_b,
     "band": 20,
     "caution": "the BASE list has 5 rows in reach and its fire rate is 0 of 5; the span between "
                "the two powered lists alone is %s points (R3) and %s points (R3b)"
                % (round(abs(corrected["wide"] - corrected["narrow"]), 2),
                   round(abs(corrected_b["wide"] - corrected_b["narrow"]), 2))})

# P5 -----------------------------------------------------------------------
share = P["wide"]["R3_fire_share_by_carrier"]
five = {c: share[c] for c in ("person", "secretary of state", "court", "authority", "officer")}
lowest = min(five, key=lambda c: five[c])
add("P5", "`person` is the least active carrier of the five, under R3.",
    "person is not last of the five", lowest == "person",
    {"fire_share": five, "lowest": lowest,
     "with_the_repair_R3b": {c: P["wide"]["R3b_fire_share_by_carrier"][c] for c in five}})

# P6 -----------------------------------------------------------------------
fr = P["narrow"]["by_rule"][bestrule]["fire_rate"]
frb = P["narrow"]["by_rule"]["R3b_active_governor_own_block"]["fire_rate"]
add("P6", "No rule reproduces 0.425: the best rule's fire rate over the NARROW rows in reach "
          "falls outside 0.325-0.525.",
    "the fire rate lands inside 0.325-0.525", not (0.325 <= fr <= 0.525),
    {"best_agreeing_declared_rule": bestrule, "fire_rate_over_226_rows": fr,
     "band": [0.325, 0.525], "reader_sample_figure": 0.425,
     "with_the_repair_R3b": frb,
     "R3b_also_outside": not (0.325 <= frb <= 0.525),
     "note": "R3b lands 0.0108 below the band's floor"})

v = [p["verdict"] for p in out["predictions"].values()]
out["tally"] = {"survives": v.count("survives"), "FALSIFIED": v.count("FALSIFIED"),
                "unscoreable": v.count("unscoreable")}

(HERE / "adjudication.json").write_text(json.dumps(out, indent=1) + "\n")
for pid, p in out["predictions"].items():
    print("%-3s %-11s %s" % (pid, p["verdict"], p["prediction"][:88]))
print("\n  %s" % out["tally"])
