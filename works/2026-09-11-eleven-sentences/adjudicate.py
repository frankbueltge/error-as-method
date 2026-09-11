#!/usr/bin/env python3
"""adjudicate -- Session 87, 2026-09-11.

The 60 rows of `audit-sample.json`, read one at a time and labelled by hand under the scheme fixed
in PREDICTIONS.md §5, which is Session 86's scheme with one value added to `voice` (ACTIVE), because
this draw is not restricted to the agentless-passive population and Session 86's two values could
not have described it.

**The judgement is about the drawn occurrence, not about the sentence.** Several rows carry more
than one modal; the row is the one at `offset`, and where the two differ the note says so.

`bearer = RECOVERABLE` means: a reader can say from this sentence alone who must act, because a
noun phrase in the sentence denotes that party -- including a pronoun or an elided subject whose
antecedent stands inside the same sentence. An activity that implies a doer without naming one is
not enough; that is Session 86's line and it is kept so the two sets stay comparable.

One adjudicator, who wrote the hypothesis. Unfixed since Session 82 named it. Every row is published.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

# id: (voice, subject, bearer, note)
HAND = {
 "W01": ("PASSIVE", "ARTEFACT", "DELETED", None),
 "W02": ("PASSIVE", "ARTEFACT", "DELETED", None),
 "W03": ("ACTIVE", "ARTEFACT", "DELETED",
         "subject 'it' is the notation, antecedent outside the sentence"),
 "W04": ("ACTIVE", "ARTEFACT", "DELETED",
         "an IDL requirement: the implementation is the bearer and is not in the sentence"),
 "W05": ("ACTIVE", "ARTEFACT", "DELETED", None),
 "W06": ("ACTIVE", "ARTEFACT", "DELETED", None),
 "W07": ("ACTIVE", "PARTY", "RECOVERABLE",
         "subject elided from 'Anyone' in the same sentence; 'should only do so' is also the "
         "adverb gap Session 84 declared and could not repair"),
 "W08": ("PASSIVE", "ARTEFACT", "DELETED", None),
 "W09": ("COPULA", "ARTEFACT", "RECOVERABLE",
         "existential 'there must be'; the user agent is named in the temporal clause and is "
         "plainly the party that must hold the reference"),
 "W10": ("ACTIVE", "ARTEFACT", "DELETED", None),
 "W11": ("PASSIVE", "ARTEFACT", "DELETED", None),
 "W12": ("PASSIVE", "ARTEFACT", "DELETED", None),
 "W13": ("ACTIVE", "ARTEFACT", "DELETED", "the drawn occurrence is the second, 'must contain'"),
 "W14": ("ACTIVE", "PARTY", "RECOVERABLE", None),
 "W15": ("ACTIVE", "PARTY", "RECOVERABLE", None),
 "W16": ("PASSIVE", "ARTEFACT", "DELETED", None),
 "W17": ("PASSIVE", "ARTEFACT", "DELETED", None),
 "W18": ("ACTIVE", "PARTY", "RECOVERABLE", None),
 "W19": ("ACTIVE", "ARTEFACT", "DELETED", None),
 "W20": ("ACTIVE", "ARTEFACT", "DELETED", None),
 "W21": ("ACTIVE", "PARTY", "RECOVERABLE", None),
 "W22": ("ACTIVE", "ARTEFACT", "DELETED", "the drawn occurrence is the second, 'or must have'"),
 "W23": ("ACTIVE", "ARTEFACT", "DELETED", None),
 "W24": ("ACTIVE", "PARTY", "RECOVERABLE", None),
 "W25": ("ACTIVE", "PARTY", "RECOVERABLE", None),
 "W26": ("PASSIVE", "ARTEFACT", "DELETED", None),
 "W27": ("PASSIVE", "ARTEFACT", "DELETED", None),
 "W28": ("PASSIVE", "ARTEFACT", "DELETED", None),
 "W29": ("ACTIVE", "ARTEFACT", "DELETED",
         "'A document must not contain' -- by the HTML Standard's own SS2.1.8 a document IS a "
         "conformance class, so the standard would say this names its bearer; a document does not "
         "act, and the author who must not write it is absent"),
 "W30": ("COPULA", "ARTEFACT", "DELETED", None),
 "W31": ("ACTIVE", "ARTEFACT", "DELETED", None),
 "W32": ("PASSIVE", "ARTEFACT", "DELETED",
         "the drawn occurrence is the second, 'should be presented to the user'"),
 "W33": ("ACTIVE", "PARTY", "RECOVERABLE", None),
 "W34": ("PASSIVE", "ARTEFACT", "DELETED",
         "'the user' appears but erases other site data; the party that must erase the state is "
         "not in the sentence"),
 "W35": ("ACTIVE", "PARTY", "RECOVERABLE", "subject 'it', antecedent 'the user agent' in the "
                                           "conditional clause of the same sentence"),
 "W36": ("PASSIVE", "ARTEFACT", "DELETED", None),
 "W37": ("PASSIVE", "ARTEFACT", "DELETED", None),
 "W38": ("COPULA", "ARTEFACT", "DELETED",
         "the instrument calls this AGENTFUL: 'by the algorithms' falls inside the 200-character "
         "window but belongs to the following clause, not to this one"),
 "W39": ("ACTIVE", "PARTY", "RECOVERABLE", "subject 'it', antecedent in the same sentence"),
 "W40": ("COPULA", "ARTEFACT", "DELETED", None),
 "W41": ("PASSIVE", "ARTEFACT", "DELETED",
         "the instrument calls this AGENTFUL. 'must be followed by a NUMBER SIGN' is a statement "
         "of sequence; the 'by' names no agent at all"),
 "W42": ("ACTIVE", "PARTY", "RECOVERABLE", None),
 "W43": ("ACTIVE", "PARTY", "RECOVERABLE", None),
 "W44": ("ACTIVE", "PARTY", "RECOVERABLE",
         "the drawn occurrence is the second; subject elided from 'user agents' in the first"),
 "W45": ("COPULA", "ARTEFACT", "DELETED", None),
 "W46": ("COPULA", "ARTEFACT", "DELETED",
         "NOT A NORM: the drawn occurrence is the quoted word -- the modal is mentioned, not used"),
 "W47": ("PASSIVE", "ARTEFACT", "DELETED", None),
 "W48": ("ACTIVE", "ARTEFACT", "DELETED", None),
 "W49": ("COPULA", "ARTEFACT", "DELETED", None),
 "W50": ("PASSIVE", "ARTEFACT", "DELETED", None),
 "W51": ("PASSIVE", "ARTEFACT", "DELETED",
         "addressed to the authors of other specifications, who are not in the sentence"),
 "W52": ("ACTIVE", "PARTY", "DELETED",
         "subject 'they' is a party, but its antecedent is outside the sentence -- the one row "
         "where subject and bearer come apart in this direction"),
 "W53": ("PASSIVE", "ARTEFACT", "DELETED",
         "'must only be enabled' -- the adverb gap again; the instrument sees NON-B"),
 "W54": ("COPULA", "ARTEFACT", "DELETED", None),
 "W55": ("ACTIVE", "ARTEFACT", "DELETED", None),
 "W56": ("PASSIVE", "ARTEFACT", "DELETED",
         "borderline: 'when writing specification text' implies a writer, but no noun phrase "
         "denotes them. Counted DELETED to keep Session 86's line. The instrument calls it "
         "AGENTFUL on 'by the script author', which belongs to the causal clause"),
 "W57": ("ACTIVE", "ARTEFACT", "DELETED", None),
 "W58": ("ACTIVE", "ARTEFACT", "DELETED", None),
 "W59": ("PASSIVE", "ARTEFACT", "DELETED", None),
 "W60": ("COPULA", "ARTEFACT", "DELETED", None),
}


def main():
    sample = json.load(open(HERE / "audit-sample.json"))
    rows = []
    for r in sample["rows"]:
        v, s, b, note = HAND[r["id"]]
        rows.append({"id": r["id"], "doc": r["doc"], "url": None, "modal": r["modal"],
                     "form": r["form"], "agent": r["agent"], "slot_token": r["slot_token"],
                     "offset": r["offset"], "voice": v, "subject": s, "bearer": b,
                     "note": note, "sentence": r["sentence"]})
    from collections import Counter
    out = {"session": 87, "date": "2026-09-11",
           "scheme": "PREDICTIONS.md SS5, fixed before the draw",
           "seed": sample["seed"], "n": sample["n"],
           "population": sample["population"], "population_size": sample["population_size"],
           "voice": dict(Counter(r["voice"] for r in rows)),
           "subject": dict(Counter(r["subject"] for r in rows)),
           "bearer": dict(Counter(r["bearer"] for r in rows)),
           "subject_x_bearer": {"%s/%s" % k: v for k, v in
                                Counter((r["subject"], r["bearer"]) for r in rows).items()},
           "instrument_form": dict(Counter(r["form"] for r in rows)),
           "rows": rows}
    (HERE / "adjudication.json").write_text(json.dumps(out, indent=1) + "\n")
    for k in ("voice", "subject", "bearer", "subject_x_bearer", "instrument_form"):
        print("%-18s %s" % (k, out[k]))


if __name__ == "__main__":
    main()
