#!/usr/bin/env python3
"""kappa.py -- the swerve's instrument, admitted after the run and reported as such.

Tonight's predictions were scored in observed agreement: R3 agrees with the reader on 30 of 40, so
0.750, and P1 set its bar at 0.80.  The swerve -- Artstein and Poesio's survey of inter-coder
agreement, read at primary after `score.py` had run and before this work was written -- says that
number is not a measurement that can be compared with anything:

  "Observed agreement enters in the computation of all the measures of agreement we consider, but on
   its own it does not yield values that can be compared across studies, because some agreement is
   due to chance, and the amount of chance agreement is affected by two factors that vary from one
   study to the other."  (Artstein & Poesio 2008, Computational Linguistics 34(4), p. 558)

So this file computes what the field computes: Cohen's kappa, which models chance from each judge's
own marginals, and Scott's pi, which models it from the pooled distribution.  Di Eugenio and Glass's
recommendation, quoted in the same survey, is to report both, because the two can fall on different
sides of a threshold.

**This instrument was not declared in advance.**  It is not scored against any prediction and it
cannot falsify one; it re-describes results already published in adjudication.json.  Writes
kappa.json.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = json.load(open(HERE / "results.json"))["against_the_reader"]

DECLARED = ["R1_adjacent_subject", "R2_no_competing_nominal", "R3_active_governor"]


def coefficients(tp, fp, fn, tn):
    n = tp + fp + fn + tn
    ao = (tp + tn) / n
    # marginals
    reader_yes = (tp + fn) / n
    rule_yes = (tp + fp) / n
    ae_kappa = reader_yes * rule_yes + (1 - reader_yes) * (1 - rule_yes)
    pooled_yes = (tp + fn + tp + fp) / (2 * n)
    ae_pi = pooled_yes ** 2 + (1 - pooled_yes) ** 2
    return {
        "n": n, "observed_agreement": round(ao, 4),
        "reader_yes_rate": round(reader_yes, 4), "rule_fire_rate": round(rule_yes, 4),
        "expected_agreement_kappa": round(ae_kappa, 4),
        "cohens_kappa": round((ao - ae_kappa) / (1 - ae_kappa), 4),
        "expected_agreement_pi": round(ae_pi, 4),
        "scotts_pi": round((ao - ae_pi) / (1 - ae_pi), 4),
    }


out = {
 "note": "Chance-corrected agreement between each declared rule and the reader of Session 90.  The "
         "instrument arrived with tonight's swerve, after the predictions were scored; it is "
         "reported beside them and never in place of them.",
 "source": {
  "authors": "Artstein, R. and Poesio, M.",
  "title": "Survey Article: Inter-Coder Agreement for Computational Linguistics",
  "venue": "Computational Linguistics 34(4), 555-596",
  "year": 2008,
  "url": "https://aclanthology.org/J08-4004/",
  "pdf": "https://aclanthology.org/J08-4004.pdf",
  "read": "at primary, 2026-09-17, whole PDF extracted; 42 pages",
 },
 "thresholds_this_field_uses": {
  "quoted": "\"ever since Carletta's influential paper, CL researchers have attempted to achieve a "
            "value of K (more seldom, of alpha) above the 0.8 threshold, or, failing that, the 0.67 "
            "level allowing for 'tentative conclusions.' However, the description of the 0.67 "
            "boundary in Krippendorff (1980) was actually 'highly tentative and cautious,' and in "
            "later work Krippendorff clearly considers 0.8 the absolute minimum value of alpha to "
            "accept for any serious purpose: 'Even a cutoff point of alpha = .800 ... is a pretty "
            "low standard' (Krippendorff 2004a, page 242).\"",
  "where": "Artstein & Poesio 2008, p. 576 (printed page number on the page carrying the quote)",
  "caution": "the survey's own argument is that these cutoffs are contested and that a coefficient "
             "is harder to interpret than to compute; they are quoted here as the convention this "
             "line did not know it was writing against, not as a law.",
 },
 "by_rule": {},
}

for name in DECLARED:
    v = A["by_rule"][name]
    out["by_rule"][name] = coefficients(v["tp"], v["fp"], v["fn"], v["tn"])
    out["by_rule"][name]["confusion"] = {k: v[k] for k in ("tp", "fp", "fn", "tn")}

out["the_coincidence"] = {
 "what": "PREDICTIONS.md P1 set its bar at 0.80 agreement.  The field's conventional reliability "
         "bar is also 0.80.  They are not the same quantity: mine is observed agreement, the "
         "field's is chance-corrected.  The bar was written without knowing the other existed.",
 "P1_bar_observed_agreement": 0.80,
 "best_rule_observed_agreement": A["by_rule"]["R3_active_governor"]["agreement"],
 "best_rule_cohens_kappa": out["by_rule"]["R3_active_governor"]["cohens_kappa"],
 "best_rule_scotts_pi": out["by_rule"]["R3_active_governor"]["scotts_pi"],
 "rules_below_chance": [n for n in DECLARED if out["by_rule"][n]["cohens_kappa"] < 0],
}

(HERE / "kappa.json").write_text(json.dumps(out, indent=1) + "\n")
for n in DECLARED:
    c = out["by_rule"][n]
    print("%-24s Ao %.3f  Ae(k) %.3f  kappa %+.4f  pi %+.4f"
          % (n, c["observed_agreement"], c["expected_agreement_kappa"],
             c["cohens_kappa"], c["scotts_pi"]))
print("\n  below chance: %s" % out["the_coincidence"]["rules_below_chance"])
