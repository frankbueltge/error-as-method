#!/usr/bin/env python3
"""inspect.py -- exploratory, computed AFTER the predictions were closed and after results.json
existed.  Everything here is labelled as such in the work.

S91.RULEBOUND's account names a mechanism: R3 fires where a tradition "names its parties as
sentence subjects".  port.py measured the rule's output; this measures the mechanism directly, over
all four traditions, and asks whether the two orderings agree.

subjecthood rate = of every occurrence of a declared party term in the binding register's text, the
share immediately followed by one of R3's own verbs.  It uses R3's verb alternation unchanged, so it
is the rule's own question asked of the corpus rather than of the rows in reach.

Writes inspection.json.
"""

import json
import re
import statistics
from pathlib import Path

import port as P

HERE = Path(__file__).resolve().parent
V = P.V
WORD = P.WORD


def subjecthood(docs, terms):
    party = re.compile(V.term_pattern(terms), re.IGNORECASE)
    subj = re.compile(V.term_pattern(terms) + r"\s+" + V.R3_VERB + r"\b", re.IGNORECASE)
    text = "\n".join("\n".join(seq) for seq in docs.values())
    total = len(party.findall(text))
    acting = len(subj.findall(text))
    words = len(WORD.findall(text))
    blocks = [len(WORD.findall(b)) for seq in docs.values() for b in seq if b.strip()]
    return {"party_term_occurrences": total,
            "of_them_followed_by_an_R3_verb": acting,
            "subjecthood_rate_pct": round(100.0 * acting / total, 2) if total else None,
            "words_of_binding_text": words,
            "party_terms_per_10k_words": round(10000.0 * total / words, 1) if words else None,
            "blocks": len(blocks),
            "median_block_words": statistics.median(blocks) if blocks else None}


def main():
    res = json.load(open(HERE / "results.json"))
    base = res["base_terms"]

    rows = []
    for name, spec in list(P.CORPORA.items()) + [("UK Acts (calibration)", P.CALIBRATION)]:
        docs, _ = spec["build"]()
        narrow = base + spec["own"]
        s = subjecthood(docs, narrow)
        if name == "UK Acts (calibration)":
            r3b = res["calibration_UK_statute"]["lists"]["narrow"]["by_rule"][
                "R3b_active_governor_own_block"]["fire_pct"]
            med = res["calibration_UK_statute"]["lists"]["narrow"]["median_carrier_block_words"]
        else:
            r3b = res["corpora"][name]["lists"]["narrow"]["by_rule"][
                "R3b_active_governor_own_block"]["fire_pct"]
            med = res["corpora"][name]["lists"]["narrow"]["median_carrier_block_words"]
        s.update({"corpus": name, "R3b_fire_pct_narrow": r3b, "median_carrier_block_words": med})
        rows.append(s)

    def order(key, reverse=True):
        return [r["corpus"] for r in sorted(rows, key=lambda r: r[key], reverse=reverse)]

    out = {
        "note": "EXPLORATORY. Computed after PREDICTIONS.md was closed and after results.json "
                "existed. No prediction is scored against anything in this file.",
        "definition": "subjecthood rate = share of declared party-term occurrences in the binding "
                      "register's text immediately followed by one of R3's own verbs "
                      "(may|must|shall|should|will|can|is|are|has|have).",
        "rows": rows,
        "orderings": {
            "by_R3b_fire_rate": order("R3b_fire_pct_narrow"),
            "by_subjecthood_rate": order("subjecthood_rate_pct"),
            "by_median_carrier_block_words": order("median_carrier_block_words"),
            "by_party_terms_per_10k_words": order("party_terms_per_10k_words"),
        },
        "n": len(rows),
        "caution": "Four points. No coefficient is reported and none should be; the orderings are "
                   "the whole of the evidence and a four-point ordering is weak evidence.",
    }
    out["agreement"] = {
        k: (v == out["orderings"]["by_R3b_fire_rate"])
        for k, v in out["orderings"].items() if k != "by_R3b_fire_rate"
    }
    (HERE / "inspection.json").write_text(json.dumps(out, indent=1) + "\n")

    print("%-24s %8s %10s %10s %8s" % ("corpus", "R3b %", "subjecth.%", "terms/10k", "med blk"))
    for r in sorted(rows, key=lambda r: -r["R3b_fire_pct_narrow"]):
        print("%-24s %8.2f %10.2f %10.1f %8s" % (r["corpus"], r["R3b_fire_pct_narrow"],
                                                 r["subjecthood_rate_pct"],
                                                 r["party_terms_per_10k_words"],
                                                 r["median_carrier_block_words"]))
    print()
    for k, v in out["orderings"].items():
        print("  %-32s %s" % (k, " > ".join(x.split(" (")[0] for x in v)))
    print("\n  orderings that agree with R3b: %s"
          % ([k for k, v in out["agreement"].items() if v] or "none"))
    print("  wrote inspection.json")


if __name__ == "__main__":
    main()
