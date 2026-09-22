#!/usr/bin/env python3
"""draw.py -- build the reading frame for tonight and draw forty rows from it, blind.

Session 94 ran Session 91's bearer-decision rules over three traditions they were not written for.
R3b fired at 28.15 % in the RFC series against 31.42 % in UK statute -- 3.27 points apart, which
falsified S91.RULEBOUND.  A fire rate says how often a rule answers YES.  It says nothing about
whether the YES is right, and this line has a reader's verdicts for UK statute only (Session 90,
forty rows, precision 0.425 for the nearest party term; Session 91 scored R1/R2/R3 against them).

Tonight asks the other half of the question in the corpus where the rate matched: read forty RFC
rows by hand and see whether the same rate is made of the same decisions.

This file draws the sample and writes `sheet.json` -- and nothing else.  It does NOT compute the
carrier, and it does NOT run a rule.  The reader's verdicts are written against `sheet.json`
alone, into `verdicts.json`; `adjudicate.py`, which does not exist when this runs, computes the
nearest party term afterwards and scores the rules against those verdicts.  Git ancestry is the
warrant: verify.py asserts the commit carrying this file and `sheet.json` precedes the commit
carrying `PREDICTIONS.md`, which precedes `verdicts.json`, which precedes `adjudicate.py`.

Nothing here is reimplemented.  The population comes from Session 94's port.rfc(), the vocabulary
and the nearest-term function from Session 91's validate.py, both imported by path and called.
"""

import importlib.util
import json
import random
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKS = HERE.parent
S86 = WORKS / "2026-09-10-only-when-capitals"
S91 = WORKS / "2026-09-17-the-second-instrument"
S94 = WORKS / "2026-09-21-three-other-offices"

SEED = 95          # the session number, as Session 90 used its own
SAMPLE = 40        # the size of the only ground truth this line owns, matched deliberately


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


V = _load(S91 / "validate.py", "s91_validate")      # term_pattern, base_terms, nearest_in_block
P = _load(S94 / "port.py", "s94_port")              # the RFC population builder, unchanged


def modal_lookup():
    """(rfc, sentence, offset) -> the modal, from Session 86's committed occurrences.

    port.rfc() drops the modal; the reading sheet needs it, and it is a property of the sentence
    at that offset, so joining it back is a lookup and not a decision.
    """
    import gzip
    occ = json.load(gzip.open(S86 / "occurrences.json.gz"))
    return {(str(o["rfc"]), o["sentence"], int(o["offset"])): o["modal"] for o in occ}


def frame():
    """Tonight's population: RFC rows that are B-FORM, AGENTLESS and in the binding register
    (RFC 8174: the keyword in capitals), whose OWN paragraph holds at least one term of the
    NARROW list -- Session 94's block window 0, the frame Session 90 read UK statute in.
    """
    docs, rows = P.rfc()
    party = re.compile(V.term_pattern(V.base_terms() + P.RFC_OWN), re.IGNORECASE)
    modals = modal_lookup()
    frame_rows = []
    for r in rows:
        block_text = docs[r["doc"]][r["block"]]
        pos = V.modal_pos_in_block(block_text, r["sentence"], r["offset"])
        if V.nearest_in_block(party, block_text, pos) is None:
            continue                      # no party term in the obligation's own block
        frame_rows.append({
            "rfc": r["doc"], "block": r["block"], "offset": r["offset"],
            "modal": modals.get((r["doc"], r["sentence"], r["offset"])),
            "sentence": r["sentence"], "block_text": block_text,
        })
    return len(rows), frame_rows


def main():
    population, rows = frame()
    rows.sort(key=lambda r: (int(r["rfc"]), r["block"], r["offset"], r["sentence"]))
    random.seed(SEED)
    picked = random.sample(rows, SAMPLE)
    sheet = {
        "note": "Forty rows drawn blind from the RFC block-window-0 frame with random.seed(95), "
                "before any verdict was written and before any rule was run over them. The "
                "nearest party term is NOT named here on purpose: the reader names the bearer "
                "in their own words, and whether that answer coincides with the term the rule "
                "reads is decided afterwards, mechanically, by adjudicate.py.",
        "corpus": "Session 86's 63 RFCs, binding register (the keyword in capitals, RFC 8174)",
        "frame": "B-FORM, AGENTLESS, block window 0 under the NARROW list "
                 "(Session 88's base terms + Session 94's RFC_OWN)",
        "population_b_form_agentless_binding": population,
        "population_in_frame": len(rows),
        "sampled": SAMPLE,
        "seed": SEED,
        "rows": [dict(n=i + 1, **r) for i, r in enumerate(picked)],
    }
    (HERE / "sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
    print("RFC B-FORM/AGENTLESS/binding population : %d" % population)
    print("of them, block window 0 under NARROW    : %d" % len(rows))
    print("drawn with seed %d                      : %d" % (SEED, SAMPLE))
    print("wrote sheet.json -- no carrier, no rule verdict")


if __name__ == "__main__":
    main()
