#!/usr/bin/env python3
"""The hand adjudication -- Session 84, 2026-09-08.

Every verdict below is mine alone, one adjudicator over 110 rows, under the three schemes written
in PREDICTIONS.md §4 before any sample was drawn.  Rows are keyed by the index in
audit-sample.json, so a reader can put each verdict beside its full sentence and disagree with it.

TWO THINGS FIXED WHILE ADJUDICATING, BOTH RECORDED RATHER THAN SMOOTHED OVER
---------------------------------------------------------------------------
1.  Scheme 4a's third verdict, PASSIVE BUT BEARER PRESENT, asks whether the agent is recoverable
    from the sentence.  Rows 3, 23, 25, 32 and 34 forced a tie-break the scheme did not carry, and
    it is stated here and applied uniformly to all forty rows, including re-checking the ones
    already read:

        The bearer is the party who would have to act to satisfy THIS occurrence's norm, and no
        other.  A party named in the sentence as bearing some OTHER norm does not make this one's
        bearer present.

    Under it, row 15 ("common rules should be established to govern the actions that the competent
    authorities and operators should take") is AGENTLESS: the authorities and operators bear the
    embedded norm, nobody in the sentence bears the establishing.  And row 34 is BEARER PRESENT,
    because "Permission BY THE COMPETENT AUTHORITIES ... shall be granted" names the granter -- to
    the left of the modal, where the rule's right-hand window cannot see it.

2.  Scheme 4b asks whether the subject of the modal "is a party that could act".  Rows 0, 23 and 27
    have a bare anaphoric subject -- `it`, `They`, `which` -- which denotes a party without naming
    one.  Counted as BEARER PRESENT, by the scheme's words, and counted separately as well, because
    under 4a's tie-break they would have gone the other way.  The count is reported; the verdict is
    not quietly moved to whichever side helps.
"""

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

# --------------------------------------------------------------------------- 4a, 40 rows
# AL = AGENTLESS PASSIVE · COP = NOT PASSIVE, copular · BP = PASSIVE BUT BEARER PRESENT · OTH = other
A4 = {
    0:  ("COP", "'proportionate' is a predicative adjective, not a participle"),
    1:  ("AL",  "who discloses is not in the sentence"),
    2:  ("AL",  "who gives is not in the sentence; 'the parties' agree a language, they do not give"),
    3:  ("BP",  "\"Institutions' internal assessments ... shall be based\" -- the genitive names the "
                "party who must base them"),
    4:  ("AL",  "who regards information as proprietary is not in the sentence"),
    5:  ("AL",  "who grants or withholds the assistance is not in the sentence"),
    6:  ("COP", "'suited to' is a predicative adjective; nothing is done to the system"),
    7:  ("AL",  "the slot token is the ADVERB 'properly'; the construction is still an agentless "
                "passive ('shall be properly justified and communicated') and is classified right "
                "for a reason the rule does not know about"),
    8:  ("AL",  "who adopts the implementing acts is not in the sentence"),
    9:  ("AL",  "who considers is not in the sentence"),
    10: ("AL",  "who considers is not in the sentence"),
    11: ("AL",  "who issues the approval is not in the sentence"),
    12: ("AL",  "who calculates is not in the sentence"),
    13: ("COP", "'responsible' is a predicative adjective"),
    14: ("AL",  "who strengthens the bargaining power is not in the sentence; the producers are "
                "beneficiaries, not actors"),
    15: ("AL",  "who establishes the common rules is not in the sentence; the authorities and "
                "operators named bear the EMBEDDED norm -- tie-break 1"),
    16: ("AL",  "who develops the common specifications is not in the sentence"),
    17: ("AL",  "who is to require Member States is not in the sentence -- the addressee of the "
                "resulting duty is named and the imposer of it is deleted"),
    18: ("COP", "'subject to' is a predicative phrase"),
    19: ("AL",  "who establishes the crisis-management measures is not in the sentence"),
    20: ("AL",  "who defines the notion is not in the sentence"),
    21: ("AL",  "who integrates the rules is not in the sentence"),
    22: ("COP", "the slot token is the PREPOSITION 'without'; 'shall be without prejudice to' is "
                "copular"),
    23: ("AL",  "the occurrence is 'shall be performed'; who performs is not in the sentence.  The "
                "'in cooperation with' phrase attaches to the earlier conjunct 'shall be organised' "
                "-- tie-break 1"),
    24: ("COP", "'responsible' is a predicative adjective"),
    25: ("AL",  "who keeps the register is not in the sentence; 'under the control of official "
                "authority' names a controller, not the keeper -- tie-break 1"),
    26: ("AL",  "who is to require the Commission is not in the sentence -- same class as row 17"),
    27: ("COP", "'effective, proportionate and dissuasive' are predicative adjectives"),
    28: ("AL",  "who allows or disallows the providers is not in the sentence -- same class as 17"),
    29: ("AL",  "who adopts and updates is not in the sentence"),
    30: ("AL",  "who suspends the time period is not in the sentence"),
    31: ("AL",  "who reduces the administrative burdens is not in the sentence"),
    32: ("BP",  "the sentence opens 'where contracting authorities choose to include ...'; the "
                "awarder of the contract is the contracting authority, named"),
    33: ("AL",  "who adopts the implementing acts is not in the sentence"),
    34: ("BP",  "'Permission BY THE COMPETENT AUTHORITIES ... shall be granted' -- the agent is "
                "named to the LEFT of the modal, where the rule's right-hand window cannot look"),
    35: ("AL",  "who includes the privilege in the scope is not in the sentence"),
    36: ("COP", "'valid' is a predicative adjective"),
    37: ("AL",  "who gives consideration is not in the sentence -- the textbook form"),
    38: ("AL",  "who permits the institutions is not in the sentence -- same class as 17"),
    39: ("AL",  "who uses the conversion factor is not in the sentence"),
}

# --------------------------------------------------------------------------- 4b, 30 rows
# BP = bearer present · BA = bearer absent · UND = undecidable (counted as BA, per §4b)
B4 = {
    0:  ("BP",  "subject 'it' -- anaphoric to an institution", True),
    1:  ("BA",  "subject 'Relevant work-related contractual relationships' -- a relation, not a "
                "party", False),
    2:  ("BA",  "subject 'the maturity of the credit derivative contract'", False),
    3:  ("BP",  "Member States", False),
    4:  ("BP",  "Institutions", False),
    5:  ("BA",  "subject 'The insurance and the institutions' insurance framework'", False),
    6:  ("BP",  "the Economic and Financial Committee", False),
    7:  ("BA",  "subject 'The same principles'", False),
    8:  ("BP",  "the competent authorities", False),
    9:  ("BA",  "subject 'The registration procedure' -- a procedure is told to enable", False),
    10: ("BP",  "Member States", False),
    11: ("BP",  "institutions", False),
    12: ("BP",  "Member States", False),
    13: ("BP",  "The Commission", False),
    14: ("BA",  "subject 'the European Plan for Aviation Safety' -- a document is told to lay down "
                "a level of safety performance", False),
    15: ("BA",  "subject 'liquidity outflows to be reported'", False),
    16: ("BP",  "the controller", False),
    17: ("BP",  "National reference laboratories", False),
    18: ("BP",  "Member States", False),
    19: ("BA",  "subject 'Cooperation between such actors and those involved in the ESS'.  AND: "
                "this row is 'should THEREFORE be reinforced' -- a genuine agentless passive the "
                "B-FORM rule missed because one adverb stands between the modal and 'be'", False),
    20: ("BP",  "Providers", False),
    21: ("BP",  "The institution", False),
    22: ("BA",  "subject 'The equity holdings which are not deducted'", False),
    23: ("BP",  "subject 'They' -- anaphoric to a party", True),
    24: ("BP",  "the controller", False),
    25: ("BA",  "subject 'which' -- anaphoric to the measures/reporting, not to a party", False),
    26: ("BA",  "subject 'further processing'.  AND: this row is 'shall, in accordance with "
                "Article 89(1), not be considered' -- a second agentless passive the B-FORM rule "
                "missed on intervening material", False),
    27: ("BP",  "subject 'which' -- anaphoric to the designated establishments, which are parties", True),
    28: ("BP",  "The controller or processor", False),
    29: ("BP",  "ESMA", False),
}

# --------------------------------------------------------------------------- 4c, 40 rows, a census
# Session 83's scheme, quoted verbatim from works/2026-09-07-the-exhortation/PREDICTIONS.md §4b:
#   EXHORTATION            -- the sentence urges a named party to act, and the urging is not an
#                             enacted obligation.  This is the class the heading forbids.
#   NOT EXHORTATION -- descriptive -- the sentence reports that someone is or was encouraged,
#                             invited or expected, as a fact about the world, an existing practice,
#                             or another instrument.
#   NOT EXHORTATION -- other      -- anything else, including matches inside a definition, a title,
#                             a quotation, or a construction the pattern misread.
C4 = {i: ("EXH", "") for i in range(40)}
C4[19] = ("OTHER",
          "'the use of administrative records should be encouraged to the extent possible' -- there "
          "is NO named party.  What is encouraged is a practice.  Session 83's scheme requires a "
          "named party for EXHORTATION and has no cell for this, so it falls to OTHER.  The one row "
          "in the census that its own instrument cannot classify is the one where the party has been "
          "deleted, which is this night's object arriving inside last night's audit.")
C4[23] = ("EXH",
          "the only one of the forty in the ARTICLES: Regulation (EU) 2021/241, Article 18, 'Member "
          "States shall be encouraged to foster synergies ...' -- word for word recital 43 of the "
          "same act with 'should' swapped for 'shall'.  Enacted, and imposing no obligation on its "
          "addressee, which is Guideline 12.1's case exactly.  Scored EXHORTATION on the scheme's "
          "sense: the clause 'not an enacted obligation' excludes genuine obligations, and this "
          "obliges the Member States to nothing.")
C4[25] = ("EXH", "subject 'it' is anaphoric to the provider named earlier in the same sentence")


def main():
    a_counts = Counter(v for v, _ in A4.values())
    b_counts = Counter(v for v, _, _ in B4.values())
    c_counts = Counter(v for v, _ in C4.values())

    sample = json.load(open(HERE / "audit-sample.json"))
    part_of_a = {r["i"]: r["part"] for r in sample["4a_agentless_precision"]}
    by_part = {}
    for i, (v, _) in A4.items():
        p = part_of_a[i]
        d = by_part.setdefault(p, Counter())
        d[v] += 1

    precision_a = a_counts["AL"] / len(A4)
    absent_b = b_counts["BA"] + b_counts["UND"]
    precision_c = c_counts["EXH"] / len(C4)

    out = {
        "adjudicator": "one, the session itself; unfixed since Session 82 named it",
        "4a_agentless_precision": {
            "n": len(A4),
            "counts": dict(a_counts),
            "precision": round(precision_a, 4),
            "bar_P4": 0.80,
            "verdict_P4": "WON" if precision_a >= 0.80 else "LOST",
            "by_part": {p: {"counts": dict(c), "n": sum(c.values()),
                            "precision": round(c["AL"] / sum(c.values()), 4)}
                        for p, c in by_part.items()},
            "rows": {str(i): {"verdict": v, "why": w} for i, (v, w) in sorted(A4.items())},
        },
        "4b_bearer_recall": {
            "n": len(B4),
            "counts": dict(b_counts),
            "bearer_absent": absent_b,
            "bar_P5": "at most 8 of 30",
            "verdict_P5": "WON" if absent_b <= 8 else "LOST",
            "anaphoric_subjects_counted_present": sum(1 for _, _, an in B4.values() if an),
            "agentless_passives_the_B_FORM_rule_missed": [19, 26],
            "rows": {str(i): {"verdict": v, "why": w, "anaphoric": an}
                     for i, (v, w, an) in sorted(B4.items())},
        },
        "4c_encouraged_census": {
            "n": len(C4),
            "counts": dict(c_counts),
            "precision": round(precision_c, 4),
            "bar_P6": 0.90,
            "verdict_P6": "WON" if precision_c >= 0.90 else "LOST",
            "note": "a complete census of Session 83's repaired instrument's population, not a "
                    "sample.  Session 83 asked for a fresh sample; a fresh sample of 40 would have "
                    "been drawn from the same 40 matches, so the census answers what the sample "
                    "could not.",
            "rows": {str(i): {"verdict": v, "why": w} for i, (v, w) in sorted(C4.items()) if w},
        },
    }
    json.dump(out, open(HERE / "audit-results.json", "w"), indent=1, ensure_ascii=False)

    print("4a  AGENTLESS precision %d/%d = %.3f   %s   %s"
          % (a_counts["AL"], len(A4), precision_a, dict(a_counts), out["4a_agentless_precision"]["verdict_P4"]))
    for p, d in out["4a_agentless_precision"]["by_part"].items():
        print("      %-9s %d/%d = %.3f" % (p, d["counts"].get("AL", 0), d["n"], d["precision"]))
    print("4b  bearer ABSENT %d/%d   %s   %s"
          % (absent_b, len(B4), dict(b_counts), out["4b_bearer_recall"]["verdict_P5"]))
    print("      agentless passives the B-FORM rule missed, in 30 NON-B rows: 2 (rows 19, 26)")
    print("4c  encouraged census precision %d/%d = %.3f   %s   %s"
          % (c_counts["EXH"], len(C4), precision_c, dict(c_counts),
             out["4c_encouraged_census"]["verdict_P6"]))


if __name__ == "__main__":
    main()
