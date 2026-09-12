#!/usr/bin/env python3
"""score.py -- score the four pre-registered predictions, and bound the adjudicator.

Two things happen here and they are different in kind.

  1. The hand verdicts of stage 1 and stage 2 are joined and counted.  These are judgements.
  2. A purely mechanical scan asks, of every window and of every whole document, where the nearest
     PARTY TERM stands.  That is not a judgement, and it exists to put a bound on the one above:
     a window with no party term anywhere in it could not have been adjudicated NAMED by any reader,
     so the share of windows that contain one is a ceiling on the hand result, and the gap between
     that ceiling and the hand count is the size of my own discretion.
"""

import gzip
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "2026-09-11-eleven-sentences"

# The vocabulary of parties, fixed before the scan and not tuned: every term this corpus uses for
# somebody who can be asked to act.  It is deliberately generous -- a generous list makes the
# ceiling higher and therefore makes the hand result look worse, not better.
PARTY = re.compile(
    r"\b(user agent|user agents|browser|browsers|author|authors|implementation|implementations|"
    r"implementer|implementers|markup generator|markup generators|conformance checker|"
    r"conformance checkers|parser|parsers|server|servers|client|clients|validator|validators|"
    r"editor|editors|specification author|specification authors)\b", re.IGNORECASE)

WINDOWS = (0, 1, 2, 3, 5, 8, 13, 20, 35, 50, 100, 200)


def load():
    s1 = {r["id"]: r for r in json.load(open(HERE / "stage1-verdicts.json"))["rows"]}
    s2 = {r["id"]: r for r in json.load(open(HERE / "stage2-verdicts.json"))["rows"]}
    ctx = {r["id"]: r for r in json.load(open(HERE / "context.json"))["rows"]}
    return s1, s2, ctx


def nearest_party_term(blocks, index, limit):
    """How many blocks back does the nearest party term stand?  None if none within limit."""
    for d in range(0, min(index, limit) + 1):
        if PARTY.search(blocks[index - d]["t"]):
            return d
    return None


def main():
    ver = json.load(open(HERE / "verification.json"))
    if not ver.get("passed"):
        sys.exit("verify.py has not passed -- refusing to report")

    s1, s2, ctx = load()
    ids = sorted(s1, key=lambda s: int(s[1:]))
    corpus = json.load(gzip.open(SRC / "corpus.json.gz"))

    c1 = Counter(s1[i]["stage1"] for i in ids)
    c2 = Counter(s2[i]["stage2"] for i in ids)

    named1 = [i for i in ids if s1[i]["stage1"] == "NAMED"]
    named2 = [i for i in ids if s2[i]["stage2"] == "NAMED"]
    recovered = [i for i in named2 if i not in named1]

    dist = [s2[i]["distance"] for i in recovered]
    kinds = Counter(s2[i]["kind"] for i in recovered)
    class_anywhere = [i for i in recovered if s2[i].get("class_declaration_in_window")]

    # ---------------------------------------------------------------- the mechanical ceiling
    mech = {}
    for w in WINDOWS:
        hit = {}
        for i in ids:
            r = ctx[i]
            blocks = corpus[r["doc"]]["blocks"]
            d = nearest_party_term(blocks, r["block"], w)
            # a heading in the enclosing chain counts too, at whatever its real distance is
            if d is None:
                for h in r["headings"]:
                    if PARTY.search(h["text"]):
                        d = r["block"] - h["block"]
                        break
            hit[i] = d
        mech[w] = hit

    whole = {}
    for i in ids:
        r = ctx[i]
        blocks = corpus[r["doc"]]["blocks"]
        whole[i] = nearest_party_term(blocks, r["block"], r["block"])

    p = json.load(open(HERE / "predictions.json"))
    results = {
        "P1": {"claim": p["P1"], "value": len(named2), "won": len(named2) > 30},
        "P2": {"claim": p["P2"], "value": len(named1), "won": 0 < len(named1) < 9},
        "P3": {"claim": p["P3"], "value": kinds.get("CLASS", 0), "of": len(recovered),
               "won": kinds.get("CLASS", 0) * 2 > len(recovered)},
        "P4": {"claim": p["P4"], "value": statistics.median(dist) if dist else None,
               "won": bool(dist) and statistics.median(dist) == 0},
    }

    out = {
        "session": 88, "date": "2026-09-12",
        "n": len(ids), "population": ver["population"],
        "stage1": dict(c1), "stage2": dict(c2),
        "named_stage1": named1, "named_stage2": named2, "recovered": recovered,
        "recovery_distances": dict(zip(recovered, dist)),
        "recovery_kinds": dict(kinds),
        "recovered_with_class_declaration_somewhere_in_window": class_anywhere,
        "transitions": dict(Counter("%s->%s" % (s1[i]["stage1"], s2[i]["stage2"]) for i in ids)),
        "predictions": results,
        "mechanical_ceiling": {
            "party_terms": PARTY.pattern,
            "windows": {str(w): {
                "windows_containing_a_party_term": sum(1 for v in mech[w].values() if v is not None),
                "median_distance_where_present": statistics.median(
                    sorted(v for v in mech[w].values() if v is not None)) if any(
                    v is not None for v in mech[w].values()) else None,
            } for w in WINDOWS},
            "whole_document_before_the_sentence":
                sum(1 for v in whole.values() if v is not None),
            "per_row_nearest_party_term_5": mech[5],
            "per_row_nearest_party_term_whole_document": whole,
        },
        # The one rate this night measured rather than assumed: of the windows that DO contain a
        # party term at distance <= 5, how many of them name the bearer of THIS obligation?
        "naming_precision_at_5": {
            "windows_with_a_party_term": sum(1 for v in mech[5].values() if v is not None),
            "hand_named": len(named2),
            "hand_named_among_them": sum(1 for i in named2 if mech[5][i] is not None),
        },
    }
    (HERE / "results.json").write_text(json.dumps(out, indent=1) + "\n")

    print("stage 1 (sentence alone) :", dict(c1))
    print("stage 2 (with context)   :", dict(c2))
    print("recovered by context     :", len(recovered), recovered)
    print("distances                :", dict(zip(recovered, dist)), "median", results["P4"]["value"])
    print("kinds                    :", dict(kinds),
          "| class declaration somewhere in window:", len(class_anywhere))
    print()
    for k in ("P1", "P2", "P3", "P4"):
        r = results[k]
        print("%s  %-5s  value %-6s  %s" % (k, "WON" if r["won"] else "LOST",
                                            r["value"], r["claim"]))
    print()
    for w in WINDOWS:
        d = out["mechanical_ceiling"]["windows"][str(w)]
        print("window %-3d blocks: %2d of 60 contain a party term (median distance %s)"
              % (w, d["windows_containing_a_party_term"], d["median_distance_where_present"]))
    print("whole document before the sentence: %d of 60"
          % out["mechanical_ceiling"]["whole_document_before_the_sentence"])


if __name__ == "__main__":
    main()
