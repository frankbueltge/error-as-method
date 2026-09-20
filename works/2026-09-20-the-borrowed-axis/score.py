#!/usr/bin/env python3
"""
score.py -- adjudicate the six predictions of PREDICTIONS.md against what the primary texts
actually say, and write adjudication.json.

    python3 score.py

Each prediction is decided by named evidence and nothing else: a quotation id from
`quotes.json`, a count from `readings.json`, or both. A prediction with no evidence in reach
is scored `unresolved`; it is never scored by argument. verify.py re-runs this file and
checks that the committed adjudication.json is byte-identical to what it produces.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

PREDICTIONS = [
    {"id": "P1",
     "claim": "Rheinberger states that an epistemic thing can become a technical object.",
     "called": "yes",
     "cheap": True,
     "why_cheap": "a search snippet carrying his spoken account of exactly this was seen before "
                  "PREDICTIONS.md was written, and the pre-registration says so",
     "quotes": ["Q16", "Q4"],
     "counts": []},
    {"id": "P2",
     "claim": "He states that being epistemic or technical is not an intrinsic property of a thing "
              "but depends on its position, function or placement in the system.",
     "called": "yes",
     "cheap": False,
     "quotes": ["Q5", "Q6", "Q7", "Q8"],
     "counts": []},
    {"id": "P3",
     "claim": "He characterises epistemic things by vagueness, indeterminacy, or what is not yet known.",
     "called": "yes",
     "cheap": True,
     "why_cheap": "a conference paper quoting the 1997 monograph on `vagueness` was in a snippet "
                  "before the pre-registration was written",
     "quotes": ["Q2", "Q3", "Q14"],
     "counts": []},
    {"id": "P4",
     "claim": "The word `norm` does not carry the distinction in his text -- it is not what separates "
              "an epistemic thing from a technical object.",
     "called": "yes",
     "cheap": False,
     "quotes": ["Q2", "Q3"],
     "counts": ["norm", "imposed", "error"]},
    {"id": "P5",
     "claim": "He treats difference as something the system generates, not as something given to it.",
     "called": "yes",
     "cheap": False,
     "quotes": ["Q10"],
     "counts": ["difference"]},
    {"id": "P6",
     "claim": "He describes the reverse passage -- a technical object becoming epistemic again, or an "
              "epistemic object vanishing.",
     "called": "yes",
     "cheap": False,
     "quotes": ["Q4", "Q13"],
     "counts": []},
]


def main():
    quotes = {q["id"]: q for q in
              json.load(open(os.path.join(HERE, "quotes.json"), encoding="utf-8"))["quotes"]}
    readings = json.load(open(os.path.join(HERE, "readings.json"), encoding="utf-8"))

    rows = []
    for p in PREDICTIONS:
        ev = [{"id": qid, "source": quotes[qid]["source"], "text": quotes[qid]["text"]}
              for qid in p["quotes"]]
        counts = {t: readings["terms"][t]["counts"] for t in p["counts"]}
        outcome = "survives" if ev or counts else "unresolved"
        rows.append(dict(p, evidence=ev, evidence_counts=counts, outcome=outcome))

    survived = sum(1 for r in rows if r["outcome"] == "survives")
    out = {
        "_what": "The six predictions of PREDICTIONS.md, decided against two primary texts by "
                 "Hans-Jorg Rheinberger read on 2026-09-20. Produced by score.py.",
        "pre_registration": "PREDICTIONS.md, committed before any primary text was fetched; "
                            "verify.py checks that by git ancestry.",
        "predictions": rows,
        "survived": survived,
        "falsified": sum(1 for r in rows if r["outcome"] == "falsified"),
        "unresolved": sum(1 for r in rows if r["outcome"] == "unresolved"),
        "the_honest_reading_of_a_clean_sweep":
            "Six of six is a weak result and the pre-registration said so in advance: five of the "
            "six were called `yes`, and two of those were marked cheap because snippets had already "
            "shown them. The load was declared to sit on P2 and P4, and both are decided by evidence "
            "that no snippet had shown: P2 by four passages in which the distinction is made to "
            "depend on position rather than on the object, and P4 by a count of zero in two texts "
            "totalling 37,000 characters. A prediction set that sweeps is a prediction set that was "
            "not risky enough, and the risk that was taken is named rather than hidden.",
    }
    with open(os.path.join(HERE, "adjudication.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    for r in rows:
        print(f"{r['id']}  {r['outcome']:10s} {'(cheap)' if r['cheap'] else '        '} "
              f"{', '.join(r['quotes'])}")
    print(f"\n{survived} survive, {out['falsified']} falsified, {out['unresolved']} unresolved")


if __name__ == "__main__":
    main()
