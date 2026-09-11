#!/usr/bin/env python3
"""agentful -- Session 87, 2026-09-11.  **POST HOC. Scores no prediction. Marked at every use.**

F-130 argued from a counterfactual that Session 84's `by`-test does no work: replace it with a
constant and the published headline comes back. It never checked the other half -- what the test
finds when it *does* fire. Neither could Session 86's hand sample, which was drawn entirely from
AGENTLESS rows, so not one of its 80 sentences contained a `by` for the instrument to have been
right or wrong about.

This corpus has 133 AGENTFUL occurrences, which is few enough to read **all of them** rather than
sample. Each is labelled with one question: *does the `by`-phrase the instrument found name the
party that must act?* One adjudicator, who wrote the hypothesis; every row is published with its
sentence, so disagreeing costs a reader nothing.

  BEARER            yes -- the by-phrase names the party bound by this obligation
  NOT-AGENTIVE      the `by` is not an agent phrase at all: followed by, separated by, surrounded
                    by, sorted by, accompanied by, by default, by <gerund> (means)
  AGENT-IS-ARTEFACT a grammatical agent, but an object, a class or an interface -- not a party who
                    could be asked to act
  OTHER-CLAUSE      the `by` lies inside the 200-character window but belongs to a different
                    predicate than the modal's
  AGENT-NOT-BEARER  a party, but the one who *may* act or who benefits -- "should be editable by
                    the user" binds the user agent, not the user
"""

import gzip
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

BEARER = {15, 21, 45, 56, 62, 63, 93, 97, 98, 103, 104}
AGENT_NOT_BEARER = {38, 39, 40, 44}
AGENT_IS_ARTEFACT = {1, 2, 3, 4, 5, 6, 7, 10, 12, 28, 31, 32, 33, 37, 50, 55, 58, 60, 61,
                     64, 65, 66, 67, 68, 69, 73, 75, 76, 78, 79, 80, 82, 101, 102, 132, 133}
OTHER_CLAUSE = {16, 24, 26, 35, 42, 43, 49, 51, 53, 57, 71, 72, 77, 81, 87, 96,
                125, 126, 127, 128, 129, 130, 131}


def verdict(i):
    if i in BEARER:
        return "BEARER"
    if i in AGENT_NOT_BEARER:
        return "AGENT-NOT-BEARER"
    if i in AGENT_IS_ARTEFACT:
        return "AGENT-IS-ARTEFACT"
    if i in OTHER_CLAUSE:
        return "OTHER-CLAUSE"
    return "NOT-AGENTIVE"


def main():
    occ = json.load(gzip.open(HERE / "occurrences.json.gz", "rt"))
    af = [r for r in occ if r["form"] == "B-FORM" and r["agent"] == "AGENTFUL"]
    rows = []
    for i, r in enumerate(af, 1):
        rows.append({"id": "A%03d" % i, "doc": r["doc"], "modal": r["modal"],
                     "slot_token": r["slot_token"], "register": r["register"],
                     "verdict": verdict(i),
                     "window": r["sentence"][r["offset"]:r["offset"] + 260],
                     "sentence": r["sentence"]})
    c = Counter(x["verdict"] for x in rows)
    total_occ = len(occ)
    out = {"session": 87, "date": "2026-09-11",
           "status": "POST HOC; scores no prediction",
           "question": "does the by-phrase the instrument found name the party that must act?",
           "n_agentful": len(rows),
           "n_occurrences": total_occ,
           "agentful_share_of_all_occurrences": round(len(rows) / total_occ, 4),
           "verdicts": dict(c),
           "precision_bearer_named": round(c["BEARER"] / len(rows), 4),
           "bearer_named_share_of_all_occurrences": round(c["BEARER"] / total_occ, 5),
           "rows": rows}
    (HERE / "agentful.json").write_text(json.dumps(out, indent=1) + "\n")
    print("%d AGENTFUL occurrences of %d (%.2f %%), read whole:"
          % (len(rows), total_occ, 100 * len(rows) / total_occ))
    for k, v in c.most_common():
        print("  %-18s %3d  (%.1f %%)" % (k, v, 100 * v / len(rows)))
    print("\nthe by-test names the bound party in %d of %d occurrences it flags (%.1f %%), "
          "and in %d of %d occurrences in the corpus (%.2f %%)"
          % (c["BEARER"], len(rows), 100 * c["BEARER"] / len(rows),
             c["BEARER"], total_occ, 100 * c["BEARER"] / total_occ))


if __name__ == "__main__":
    main()
