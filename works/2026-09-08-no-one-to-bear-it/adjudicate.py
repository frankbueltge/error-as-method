#!/usr/bin/env python3
"""Scoring the six predictions of PREDICTIONS.md §3 against the measurement, plus P7.

Session 83's principle, applied again and in both directions: where a single scoring "would have
been true and would have hidden the thing worth knowing", the shadow reading is carried beside the
verdict.  Tonight the shadow is attached to a WIN -- P2's -- and it is the night's result.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    r = json.load(open(HERE / "results.json"))
    a = json.load(open(HERE / "audit-results.json"))
    slots = json.load(open(HERE / "slot-tokens.json"))

    B_rec = r["stratum_B"]["recitals"]
    wc = r["whole_corpus"]
    p2 = r["p2_per_act_stratum_B"]["n_recitals_higher"]
    prec_a = a["4a_agentless_precision"]["precision"]
    absent = a["4b_bearer_recall"]["bearer_absent"]
    prec_c = a["4c_encouraged_census"]["precision"]

    rows = [
        {
            "id": "P1",
            "claim": "Stratum B recitals bearer-deletion rate >= 0.20",
            "observed": B_rec["bearer_deletion_rate"],
            "verdict": "WON" if B_rec["bearer_deletion_rate"] >= 0.20 else "LOST",
            "shadow": "the rate is a RAW rate over a B-FORM class the 4a audit finds 72.5 %% pure. "
                      "On the audited estimate the recital figure is about 0.347 and the bar still "
                      "clears; on the same estimate corrected upward for the gapped misses (residue "
                      "§2, 529 more agentless recital forms the rule cannot see) it is higher again. "
                      "The bar clears on every reading, which is a fact about the bar.",
        },
        {
            "id": "P2",
            "claim": "recitals delete the bearer more often than articles in >= 20 of 28 Stratum B acts",
            "observed": "%d of 28" % p2,
            "verdict": "WON" if p2 >= 20 else "LOST",
            "shadow": "WON AT 28 OF 28 AND THE WIN CARRIES NO INFORMATION.  The recitals of this "
                      "corpus are 99.24 %% `should` and the articles 99.12 %% `shall`.  The two sides "
                      "of the comparison share almost no modal, so `recitals vs articles` and "
                      "`should vs shall` are one contrast measured once.  Where the within-modal "
                      "comparison has observations at all it runs the OTHER way: `shall` deletes the "
                      "bearer in 24.53 %% of its 15,474 article occurrences against 18.18 %% of its 11 "
                      "recital ones, and `should` in 53.52 %% of its 71 article occurrences against "
                      "37.51 %% of its 6,889 recital ones.  Both within-modal comparisons rest on tens "
                      "of observations on one side and thousands on the other, so neither refutes "
                      "anything either.  The honest statement is that this corpus cannot separate "
                      "the two contrasts, and the confound was named in PREDICTIONS.md §2c before "
                      "the numbers existed.",
        },
        {
            "id": "P3",
            "claim": "AGENTFUL under 15 %% of B-FORM in recitals and in articles alike",
            "observed": {"recitals": wc["recitals"]["agentful_share_of_b_form"],
                         "articles": wc["articles"]["agentful_share_of_b_form"]},
            "verdict": "WON" if (wc["recitals"]["agentful_share_of_b_form"] < 0.15
                                 and wc["articles"]["agentful_share_of_b_form"] < 0.15) else "LOST",
            "shadow": "lost on both parts and by a similar margin, and the rule counts EVERY `by` -- "
                      "`by 31 December`, `by way of derogation`, `by means of` -- so the true agent "
                      "share is lower than 19 %% and the direction of the loss is not in doubt, only "
                      "its size.  A rule declared in advance as an over-count lost a prediction that "
                      "the over-count made easier to lose.",
        },
        {
            "id": "P4",
            "claim": "hand-audited precision of AGENTLESS >= 0.80",
            "observed": prec_a,
            "verdict": "WON" if prec_a >= 0.80 else "LOST",
            "shadow": "29 of 40.  8 rows are copulas (`proportionate`, `responsible`, `valid`, "
                      "`subject to`, `without prejudice to`) and 3 are passives whose agent is in "
                      "the sentence where the right-hand window cannot look.  Split by part, on 13 "
                      "and 27 rows: recitals 0.923, articles 0.630.",
        },
        {
            "id": "P5",
            "claim": "at most 8 of 30 NON-B occurrences have no bearer in the sentence either",
            "observed": "%d of 30" % absent,
            "verdict": "WON" if absent <= 8 else "LOST",
            "shadow": "11.  A procedure is told to enable, a Plan is told to lay down a level of "
                      "safety performance, a relation is told to involve employees.  The passive is "
                      "not where most of the bearer-deletion is; it is only where this rule can see "
                      "it.  Two of the 30 were agentless passives the B-FORM rule missed on an "
                      "intervening adverbial, which is a second failure inside the same 30 rows.",
        },
        {
            "id": "P6",
            "claim": "complete census of Session 83's 40 `encouraged` matches, precision >= 0.90",
            "observed": prec_c,
            "verdict": "WON" if prec_c >= 0.90 else "LOST",
            "shadow": "39 of 40, and the single failure is the row with no party in it at all -- "
                      "`the use of administrative records should be encouraged`.  Session 83's "
                      "repaired instrument is confirmed on its whole population and the one thing it "
                      "cannot classify is tonight's object.",
        },
        {
            "id": "P7",
            "claim": "(unscorable) the most frequent recital slot token will be `taken`",
            "observed": list(slots["recitals"].items())[:5],
            "verdict": "WRONG",
            "shadow": "`able` at 267, `allowed` 114, `delegated` 113, `considered` 105, `possible` "
                      "95; `taken` is tenth at 61.  The most frequent token in the slot is a copula, "
                      "and the second most frequent adjective in the top five is another.  P7 was "
                      "written to stop me claiming afterwards that I had expected whatever appeared, "
                      "and it did that job: I would have said the class was full of `taken`, and its "
                      "largest single member is the word that is not in the class at all.",
        },
    ]

    won = [x["id"] for x in rows if x["verdict"] == "WON"]
    lost = [x["id"] for x in rows if x["verdict"] == "LOST"]

    out = {
        "session": 84, "date": "2026-09-08",
        "scorable": 6, "won": won, "lost": lost,
        "expected_to_lose_in_advance": ["P2", "P4"],
        "note": "P4 lost, and its losing sentence is owed and written in the journal under its own "
                "heading.  P2 won at the maximum and the win is the night's finding rather than its "
                "result.  Nothing here was rewritten after a number was seen; the repairs are in "
                "residue.py, labelled post-hoc, and score nothing.",
        "predictions": rows,
    }
    json.dump(out, open(HERE / "adjudication.json", "w"), indent=1, ensure_ascii=False)

    for x in rows:
        print("%-3s %-6s %s" % (x["id"], x["verdict"], x["observed"]))
    print("\nwon: %s   lost: %s" % (", ".join(won), ", ".join(lost)))


if __name__ == "__main__":
    main()
