#!/usr/bin/env python3
"""score.py -- the seven predictions of PREDICTIONS.md, scored mechanically against results.json.

Every verdict string below is generated from the committed numbers.  None is typed.

One correction is carried here rather than in PREDICTIONS.md, which its own header forbids editing
once verdicts.json exists: section 5's calibration table gives R2's Cohen's kappa as -0.1611 and
R3's as +0.4964.  Session 91 published -0.1609 and +0.4962, and tonight's pre-registration extended
its journal's three-place rounding by a digit that had not been read.  P4's bar is therefore the
committed +0.4962, and the field `p4_would_the_wrong_bar_have_changed_the_verdict` says whether the
difference could have mattered.

Writes adjudication.json.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = json.load(open(HERE / "results.json"))
V = json.load(open(HERE / "verdicts.json"))

UK_KAPPA_PUBLISHED = 0.4962          # works/2026-09-17-the-second-instrument/kappa.json
UK_KAPPA_AS_MISTYPED_IN_PREDICTIONS = 0.4964
UK_R3 = R["calibration"]["by_rule"]["R3_active_governor"]
RFC_R3 = R["against_the_reader"]["M1"]["R3_active_governor"]
READ = R["reading"]


def main():
    named = READ["bearer_named"]
    m1 = READ["m1_yes"]
    preds = [
        {"id": "P1",
         "claim": "The reader names a bearer (not NONE) in at least 30 of the 40 rows.",
         "observed": "%d of 40" % named,
         "won": named >= 30},
        {"id": "P2",
         "claim": "Under M1 the nearest party term is the bearer in more than 17 of 40 -- above "
                  "UK statute's 17/40 = 0.425.",
         "observed": "%d of 40 (%.4f)" % (m1, m1 / 40),
         "won": m1 > 17},
        {"id": "P3",
         "claim": "R3's agreement with the reader comes in below 0.75, its UK figure.",
         "observed": "%.4f against %.4f" % (RFC_R3["agreement"], UK_R3["agreement"]),
         "won": RFC_R3["agreement"] < UK_R3["agreement"]},
        {"id": "P4",
         "claim": "R3's Cohen's kappa is positive and below the UK figure.",
         "observed": "%+.4f against %+.4f" % (RFC_R3["cohens_kappa"], UK_KAPPA_PUBLISHED),
         "won": 0 < RFC_R3["cohens_kappa"] < UK_KAPPA_PUBLISHED},
        {"id": "P5",
         "claim": "R3 fires on fewer than 19 of the 40, mirroring 28.15 %% against 31.42 %% over "
                  "the populations.",
         "observed": "%d of 40 against %d of 40" % (RFC_R3["fires"], UK_R3["fires"]),
         "won": RFC_R3["fires"] < UK_R3["fires"]},
        {"id": "P6",
         "claim": "M1 and M2 disagree on at most 5 of the 40 rows.",
         "observed": "%d rows %s" % (READ["m1_m2_disagreements"],
                                     READ["m1_m2_disagreeing_rows"] or "(none)"),
         "won": READ["m1_m2_disagreements"] <= 5},
        {"id": "P7",
         "claim": "R1 and R2 each agree with the reader on no more rows than the always-NO "
                  "baseline.",
         "observed": "R1 %d, R2 %d, baseline %d"
                     % (R["against_the_reader"]["M1"]["R1_adjacent_subject"]["agreements"],
                        R["against_the_reader"]["M1"]["R2_no_competing_nominal"]["agreements"],
                        R["against_the_reader"]["baseline_M1"]["always_no_agreements"]),
         "won": (R["against_the_reader"]["M1"]["R1_adjacent_subject"]["agreements"]
                 <= R["against_the_reader"]["baseline_M1"]["always_no_agreements"]
                 and R["against_the_reader"]["M2"] is not None
                 and R["against_the_reader"]["M1"]["R2_no_competing_nominal"]["agreements"]
                 <= R["against_the_reader"]["baseline_M1"]["always_no_agreements"])},
    ]
    for p in preds:
        p["verdict"] = "WON" if p["won"] else "LOST"

    won = sum(1 for p in preds if p["won"])
    wrong_bar = (0 < RFC_R3["cohens_kappa"] < UK_KAPPA_AS_MISTYPED_IN_PREDICTIONS) != preds[3]["won"]

    out = {
        "note": "Seven predictions, declared in PREDICTIONS.md before the sheet was read, scored "
                "from results.json. Verdict strings are generated, not typed.",
        "predictions": preds,
        "won": won, "lost": len(preds) - won,
        "the_headline": {
            "which": "P2 and P3, declared as pulling against each other",
            "P2": preds[1]["verdict"], "P3": preds[2]["verdict"],
            "reading": "P2 lost and P3 won: the RFC series puts a true bearer in reach LESS often "
                       "than UK statute does (14 of 40 against 17 of 40), and the rule reads the "
                       "rows it fires on LESS well (precision %s against %s). The rate matched; "
                       "the decisions did not."
                       % (RFC_R3["precision_on_yes"], UK_R3["precision_on_yes"])},
        "p4_would_the_wrong_bar_have_changed_the_verdict": bool(wrong_bar),
        "p4_bars": {"committed": UK_KAPPA_PUBLISHED,
                    "as_mistyped_in_the_pre_registration": UK_KAPPA_AS_MISTYPED_IN_PREDICTIONS,
                    "observed": RFC_R3["cohens_kappa"]},
        "reading_notes_recorded_by_the_reader": len(V["reading_notes"]),
    }
    (HERE / "adjudication.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    for p in preds:
        print("%-3s %-6s %s" % (p["id"], p["verdict"], p["observed"]))
    print("\n%d won, %d lost" % (won, len(preds) - won))
    print("P4: the mistyped bar would have changed the verdict: %s" % wrong_bar)
    print("wrote adjudication.json")


if __name__ == "__main__":
    main()
