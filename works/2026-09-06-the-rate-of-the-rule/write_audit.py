#!/usr/bin/env python3
"""Attaches the hand verdicts to the drawn samples and writes audit.json.

Every verdict below is mine, taken by reading the sentence, and unreviewed.  The rows
carry their text so that a reader disagrees with a row rather than with a number.

THE THREE-WAY VERDICT, and why it is not two-way.  Guideline 10 forbids recitals that
contain "normative provisions or political exhortations".  The instrument looks for
something narrower: a sentence that tells a party the act commands elsewhere to do
something.  Adjudicating with only "match / not a match" would hide the difference, so
each sampled sentence gets one of:

  directed norm            -- names a party and prescribes conduct for it.  A bare
                              permission ("ESMA should be able to delegate") is NOT this;
                              a permission carrying a binding limit ("provided that it does
                              not exceed EUR 50") IS, because the limit binds conduct.
  normative not directed   -- normative content with no party commanded: scope statements,
                              interpretive rules, delegation boilerplate, passives whose
                              bound party is not named.
  not normative            -- a statement of reasons or an objective.

P6's precision is the share of `directed norm`, because that is what P6 claimed to
measure.  The share of the other two is reported beside it and says something different:
how much of what the rule catches is normative but undirected.

For the recall sample the verdict is `missed norm` or `no missed norm`, with the
mechanism of the miss recorded where there is one, because three misses in this sample
had three different causes.
"""

import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

# ---- precision sample, rows 1..40 as printed by `audit.py draw`
DIRECTED = {1, 2, 3, 8, 9, 11, 12, 17, 19, 20, 21, 22, 25, 28, 30, 31, 33, 34}
NOT_NORMATIVE = {23, 29}
# Among the directed norms, the rows where the actor the instrument named is NOT the party
# the sentence actually binds.
ACTOR_WRONG = {
    1: "matched the head `a`; the party addressed is the Member States",
    3: "matched `platform`; the party addressed is providers of online platforms",
    11: "matched `union`; the party addressed is the European Union reference laboratories",
    17: "matched `controller`; the party addressed is the associations representing them",
    30: "matched `engine`; the party addressed is the Commission",
}
NOTE = {
    1: "borderline: the obligation is passive throughout, but the Member States are named as the party that must apply the objectives",
    5: "a bare conferral of power on ESMA; no conduct is prescribed",
    8: "permission carrying a binding numeric limit, so it constrains conduct",
    20: "permission carrying a binding date, so it constrains conduct",
    26: "confers a power on the Commission; the empowerment itself is in the articles",
    27: "confers a power on the Commission, qualified in scope rather than in conduct",
    34: "this is the recital Session 81's open thread 1 named -- an instruction about how to read the law, in the half that does not bind",
}

# ---- recall sample, rows 1..40
MISSED = {
    1: ("the 80-character window: `deployers` is separated from `should` by a "
        "relative clause defining deep fakes, so the actor and the modal never meet "
        "inside the window the rule looks through"),
    16: ("the actor list: `provider` is not derived for this act, so `ATM/ANS providers "
         "should also implement training and checking programmes` has no actor to match"),
    31: ("the modal: `Member States are encouraged to draw up ... their own tables` "
         "carries no `should`, and the rule looks for nothing else -- this is a "
         "political exhortation addressed to a party, which is the other half of what "
         "Guideline 10 forbids by name, and the instrument is blind to all of it"),
}


def main():
    sample = json.loads((HERE / "audit-sample.json").read_text())

    precision = []
    for i, row in enumerate(sample["precision_sample"], 1):
        verdict = ("directed norm" if i in DIRECTED
                   else "not normative" if i in NOT_NORMATIVE
                   else "normative not directed")
        record = dict(row, row=i, verdict=verdict)
        if verdict == "directed norm":
            record["actor_correct"] = i not in ACTOR_WRONG
            if i in ACTOR_WRONG:
                record["actor_error"] = ACTOR_WRONG[i]
        if i in NOTE:
            record["note"] = NOTE[i]
        precision.append(record)

    recall = []
    for i, row in enumerate(sample["recall_sample"], 1):
        record = dict(row, row=i,
                      verdict="missed norm" if i in MISSED else "no missed norm")
        if i in MISSED:
            record["mechanism"] = MISSED[i]
        recall.append(record)

    (HERE / "audit.json").write_text(json.dumps({
        "adjudicated": "2026-09-06",
        "adjudicator": "Ulysses (the nightly line), Session 82 -- by hand, unreviewed",
        "seed": sample["seed"],
        "criterion": (
            "directed norm: names a party the act commands elsewhere and prescribes conduct "
            "for it.  normative not directed: normative content, no party commanded.  "
            "not normative: a statement of reasons or an objective."
        ),
        "precision": precision,
        "recall": recall,
    }, indent=1) + "\n")
    print("audit.json: %d precision rows, %d recall rows" % (len(precision), len(recall)))


if __name__ == "__main__":
    main()
