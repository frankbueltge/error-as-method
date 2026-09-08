#!/usr/bin/env python3
"""Draws the three audit samples fixed in PREDICTIONS.md §4, under the seed fixed there.

Nothing here decides anything.  It writes audit-sample.json, which is then read row by row and
adjudicated by hand in verdicts.py under the schemes written before this file ran.
"""

import gzip
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
S83 = HERE.parent / "2026-09-07-the-exhortation"
SEED = 20260908                                  # fixed in PREDICTIONS.md §4


def window(sent, offset, before=None, after=None):
    """The WHOLE sentence, with the modal occurrence marked.

    An earlier draft of this file emitted a 140/220-character window and was replaced before a
    single verdict was written.  The reason is the scheme itself: 4a's third verdict is PASSIVE BUT
    BEARER PRESENT, which asks whether the agent is recoverable *from the sentence*.  Adjudicating
    that over a truncated window would have been adjudicating over less text than the rule saw, and
    every truncation would have pushed a row towards AGENTLESS -- towards the verdict P4 needs.
    The seed and the draw are untouched; only how much of each drawn row is shown.
    """
    return sent[:offset] + "«" + sent[offset:offset + 12] + "»" + sent[offset + 12:]


def main():
    rows = json.load(gzip.open(HERE / "occurrences.json.gz", "rt", encoding="utf-8"))

    agentless = [r for r in rows if r["form"] == "B-FORM" and r["agent"] == "AGENTLESS"]
    non_b = [r for r in rows if r["form"] == "NON-B"]

    rng = random.Random(SEED)
    sample_a = rng.sample(agentless, 40)
    rng_b = random.Random(SEED)
    sample_b = rng_b.sample(non_b, 30)

    # 4c -- the complete census of Session 83's `encouraged` matches, not a sample.
    fam_a = json.load(open(S83 / "family-a.json"))
    encouraged = [h for h in fam_a if h["verb"].lower() == "encouraged"]

    out = {
        "seed": SEED,
        "4a_agentless_precision": [
            {"i": i, "celex": r["celex"], "part": r["part"], "division": r["division"],
             "modal": r["modal"], "slot_token": r["slot_token"],
             "context": window(r["sentence"], r["offset"])}
            for i, r in enumerate(sample_a)
        ],
        "4b_bearer_recall": [
            {"i": i, "celex": r["celex"], "part": r["part"], "division": r["division"],
             "modal": r["modal"], "context": window(r["sentence"], r["offset"])}
            for i, r in enumerate(sample_b)
        ],
        "4c_encouraged_census": [
            {"i": i, "celex": h["celex"], "part": h["part"], "division": h["division"],
             "addressee_raw": h.get("addressee"), "sentence": h["sentence"]}
            for i, h in enumerate(encouraged)
        ],
        "population_sizes": {
            "agentless": len(agentless),
            "non_b": len(non_b),
            "encouraged": len(encouraged),
        },
    }
    json.dump(out, open(HERE / "audit-sample.json", "w"), indent=1, ensure_ascii=False)
    print("agentless population %d, sampled 40" % len(agentless))
    print("non-B population %d, sampled 30" % len(non_b))
    print("encouraged census %d rows (complete, not sampled)" % len(encouraged))


if __name__ == "__main__":
    main()
