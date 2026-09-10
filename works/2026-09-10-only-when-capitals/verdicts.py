#!/usr/bin/env python3
"""My hand verdicts on the 80 drawn rows.  Session 86, 2026-09-10.

The scheme is PREDICTIONS.md §3 and was fixed before the draw:

  VOICE    PASSIVE | COPULA | OTHER
  SUBJECT  PARTY | ARTEFACT | NONE
  BEARER   RECOVERABLE | DELETED     -- "can a reader say, from this sentence alone, who must act?"

ONE ADJUDICATOR, WHO WROTE THE HYPOTHESIS.  Unfixed since Session 82 named it, named again in
PREDICTIONS.md §4, and not answered tonight either.  Every row's sentence is in audit-sample.json
and on the work's page, so disagreeing costs a reader nothing but reading.

`note` is a POST-HOC field.  It did not exist when the scheme was fixed; it was added while reading
the rows, because a class turned up that the scheme has no bucket for -- lowercase modals that are
not norms addressed to anybody: predictions, definitions, arithmetic, strings inside code and inside
YANG modules.  It scores NOTHING.  P6 is scored on BEARER alone, exactly as pre-registered.
"""

V = {
    # ---------------------------------------------------------------- UPPER: normative by the key
    "U01": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U02": ("PASSIVE", "ARTEFACT", "DELETED", "slot token is the adverb 'silently', not a participle"),
    "U03": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U04": ("PASSIVE", "ARTEFACT", "DELETED", "borderline: 'the node' appears, but as a possessor"),
    "U05": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U06": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U07": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U08": ("COPULA", "ARTEFACT", "DELETED", None),
    "U09": ("PASSIVE", "PARTY", "DELETED", "the party in subject position is the beneficiary, "
                                           "not the bearer: who must allow the operator is unwritten"),
    "U10": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U11": ("PASSIVE", "ARTEFACT", "DELETED", "borderline: the purpose clause implies an implementer"),
    "U12": ("PASSIVE", "PARTY", "DELETED", "as U09: the servers are given protections by nobody named"),
    "U13": ("COPULA", "ARTEFACT", "DELETED", None),
    "U14": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U15": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U16": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U17": ("COPULA", "ARTEFACT", "DELETED", "a pass criterion: nobody acts at all"),
    "U18": ("COPULA", "ARTEFACT", "DELETED", None),
    "U19": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U20": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U21": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U22": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U23": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U24": ("COPULA", "ARTEFACT", "DELETED", None),
    "U25": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U26": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U27": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U28": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U29": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U30": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U31": ("COPULA", "ARTEFACT", "DELETED", None),
    "U32": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U33": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U34": ("COPULA", "ARTEFACT", "DELETED", None),
    "U35": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U36": ("PASSIVE", "ARTEFACT", "DELETED", "near-mention: 'the list of header extensions that "
                                              "SHOULD/MUST be supported is specified in [RFC8834]'"),
    "U37": ("COPULA", "ARTEFACT", "DELETED", "slot token is 'either', not a participle"),
    "U38": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U39": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "U40": ("PASSIVE", "ARTEFACT", "DELETED", None),

    # ------------------------------------------------- LOWER: ordinary English, by the same key
    "L01": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "L02": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "L03": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "L04": ("COPULA", "ARTEFACT", "DELETED", None),
    "L05": ("COPULA", "ARTEFACT", "DELETED", "NOT DEONTIC: 'This time should be sufficient' is a "
                                             "prediction about the protocol, not a norm"),
    "L06": ("COPULA", "ARTEFACT", "DELETED", "NOT DEONTIC: definitional 'shall be' = 'is'"),
    "L07": ("COPULA", "ARTEFACT", "DELETED", "NOT DEONTIC: definitional 'shall be' = 'is'"),
    "L08": ("PASSIVE", "ARTEFACT", "DELETED", "commentary on a worked example, not a norm of this doc"),
    "L09": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "L10": ("PASSIVE", "ARTEFACT", "DELETED", "a lowercase 'should' beside an uppercase MUST in one "
                                              "sentence, same author, same clause chain"),
    "L11": ("COPULA", "ARTEFACT", "DELETED", "NOT DEONTIC: an arithmetic constraint in a worked sum"),
    "L12": ("PASSIVE", "ARTEFACT", "RECOVERABLE", "'Feed publishers assume the responsibility of "
                                                  "determining which data should be made public'"),
    "L13": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "L14": ("COPULA", "ARTEFACT", "DELETED", "NOT PROSE: an error string inside Python source"),
    "L15": ("COPULA", "ARTEFACT", "DELETED", "NOT PROSE: an error string inside Python source"),
    "L16": ("COPULA", "PARTY", "RECOVERABLE", None),
    "L17": ("COPULA", "PARTY", "RECOVERABLE", None),
    "L18": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "L19": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "L20": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "L21": ("PASSIVE", "ARTEFACT", "DELETED", "NOT PROSE: a description string inside a YANG module"),
    "L22": ("COPULA", "ARTEFACT", "DELETED", None),
    "L23": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "L24": ("PASSIVE", "ARTEFACT", "RECOVERABLE", "'if the server attempts to parse ... only hardened "
                                                  "parsers should be used'"),
    "L25": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "L26": ("COPULA", "ARTEFACT", "DELETED", None),
    "L27": ("COPULA", "ARTEFACT", "DELETED", None),
    "L28": ("COPULA", "ARTEFACT", "DELETED", "NOT PROSE: a description string inside a YANG module"),
    "L29": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "L30": ("PASSIVE", "ARTEFACT", "RECOVERABLE", "'allow a recipient to know which group secrets "
                                                  "should be used'"),
    "L31": ("PASSIVE", "ARTEFACT", "RECOVERABLE", "'based on the policy and configuration of the "
                                                  "verifier'"),
    "L32": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "L33": ("COPULA", "ARTEFACT", "DELETED", None),
    "L34": ("PASSIVE", "ARTEFACT", "DELETED", "'to unauthorized persons' is the recipient, not the agent"),
    "L35": ("COPULA", "PARTY", "RECOVERABLE", None),
    "L36": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "L37": ("PASSIVE", "ARTEFACT", "DELETED", "about the document's own future work, not a protocol norm"),
    "L38": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "L39": ("PASSIVE", "ARTEFACT", "DELETED", None),
    "L40": ("PASSIVE", "ARTEFACT", "DELETED", None),
}
