#!/usr/bin/env python3
"""Scores the seven predictions of PREDICTIONS.md §3 against the PRE-REGISTERED instrument, which
is the only instrument they were written about, and reports beside each one a non-scoring shadow:
what the same bar would have said on the `encouraged`-only re-cut the audit points to.

The shadow decides nothing.  It is here because Session 82 scored its predictions against all three
of its runs rather than only the surviving one, on the ground that a single scoring "would have been
true and would have hidden the thing worth knowing", and the same applies tonight in reverse: two of
the four wins below are wins on counts the audit condemns, and the shadow is where that is visible.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
res = json.load(open(HERE / "results.json"))
aud = json.load(open(HERE / "audit-results.json"))
resd = json.load(open(HERE / "residue.json"))

B = res["summary"]["stratum_B"]
acts_B = [a for a in resd["acts"] if a["stratum"] == "B"]
shadow_articles_acts = sum(1 for a in acts_B if a["articles"]["addressed_encouraged"] > 0)
shadow_recital_acts = sum(1 for a in acts_B if a["recitals"]["addressed_encouraged"] > 0)
shadow_recitals = sum(a["recitals"]["addressed_encouraged"] for a in acts_B)

ratio = B["family_b_recitals"] / B["family_a_recitals"]
prec = aud["sample_b_precision"]["precision"]
reasoned = aud["sample_a_10_5_2"]["verdicts"]["REASONED"]

P = [
    ("P1", "Family A in the recitals of fewer than 20 of 28 Stratum B acts",
     B["acts_with_family_a_recitals"], B["acts_with_family_a_recitals"] < 20,
     "%d acts on the `encouraged`-only re-cut -- the bar still holds" % shadow_recital_acts),
    ("P2", "under 100 Family A occurrences in Stratum B recitals",
     B["family_a_recitals"], B["family_a_recitals"] < 100,
     "%d on the re-cut -- the bar still holds" % shadow_recitals),
    ("P3", "Family B in the recitals of at least 24 of 28 acts",
     B["acts_with_family_b_recitals"], B["acts_with_family_b_recitals"] >= 24,
     "not affected: Family B was never touched by the audit"),
    ("P4", "Family B outnumbers Family A in recitals by at least 10 : 1",
     round(ratio, 2), ratio >= 10,
     "%.1f : 1 on the re-cut -- still short of 10, so this loss is not a loss to the junk: the "
     "Guide's own formula really is only about eight times as common as addressed exhortation, "
     "not ten" % (B["family_b_recitals"] / shadow_recitals)),
    ("P5", "Family A in the articles of at least 3 of 28 acts",
     B["acts_with_family_a_articles"], B["acts_with_family_a_articles"] >= 3,
     "%d act(s) on the re-cut -- THE BAR WOULD HAVE FAILED.  This win is a win on `expected`"
     % shadow_articles_acts),
    ("P6", "at least 30 of 40 directed recitals give reasons in the sense of 10.5.2",
     reasoned, reasoned >= 30,
     "not affected by the re-cut; affected instead by the generosity of REASONED and by the "
     "whole-recital unit, both declared in advance and both discussed in the work"),
    ("P7", "Family A's hand-audited precision is at least 0.85",
     prec, prec >= 0.85,
     "1.000 on the 14 `encouraged` rows in the same sample -- an observation about a sub-pattern, "
     "NOT an audited precision for a repaired instrument"),
]

rows = []
for pid, text, observed, won, shadow in P:
    rows.append({"id": pid, "prediction": text, "observed": observed,
                 "verdict": "WON" if won else "LOST", "shadow": shadow})

out = {
    "scored_against": "the pre-registered instrument of PREDICTIONS.md §2, unrepaired",
    "won": sum(1 for r in rows if r["verdict"] == "WON"),
    "lost": sum(1 for r in rows if r["verdict"] == "LOST"),
    "predictions": rows,
    "P8_unscorable": {
        "prediction": "the GDPR carries zero Family A occurrences in its 173 recitals",
        "observed": res["summary"]["gdpr_family_a_recitals"],
        "note": "wrong, and wrong on the surviving sub-pattern too: 5 pre-registered matches, of "
                "which the re-cut keeps 5 addressed `encouraged to` plus 1 agentless. The GDPR "
                "exhorts.",
    },
    "the_thing_worth_saying": (
        "Both predictions I named in advance as the ones I expected to lose -- P3 and P6 -- won. "
        "Both losses came from predictions I expected to win. My calibration about my own "
        "calibration was wrong, and P5 is the sharpest case: it won at 16 acts on a count that is "
        "almost entirely `expected` junk, and would have lost on the only reading of Family A the "
        "audit supports."
    ),
}
json.dump(out, open(HERE / "adjudication.json", "w"), indent=1)

print("%-4s %-6s %-8s %s" % ("id", "", "observed", "prediction"))
for r in rows:
    print("%-4s %-6s %-8s %s" % (r["id"], r["verdict"], r["observed"], r["prediction"]))
    print("       shadow: %s" % r["shadow"])
print("\nwon %d, lost %d" % (out["won"], out["lost"]))
print("P8 (unscorable): predicted 0, observed %s" % out["P8_unscorable"]["observed"])
