#!/usr/bin/env python3
"""score.py -- the seven predictions of PREDICTIONS.md §5, scored mechanically against results.json.

Nothing here is a judgement call.  Each prediction is a function of the committed numbers; the
verdict strings are generated, not typed.  Writes adjudication.json.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOW, HIGH = 21.42, 41.42
R3B = "R3b_active_governor_own_block"
ORDER = ["R1_adjacent_subject", "R2_no_competing_nominal", "R3_active_governor", R3B]


def main():
    res = json.load(open(HERE / "results.json"))
    C = res["corpora"]
    names = list(C)

    narrow = {n: C[n]["lists"]["narrow"] for n in names}
    r3b = {n: narrow[n]["by_rule"][R3B]["fire_pct"] for n in names}
    blk = {n: narrow[n]["median_carrier_block_words"] for n in names}
    span = {n: round(C[n]["lists"]["wide"]["reach_pct"] - C[n]["lists"]["base"]["reach_pct"], 2)
            for n in names}

    P = []

    inside = [n for n in names if LOW <= r3b[n] <= HIGH]
    P.append({"id": "P1", "called": "yes",
              "claim": "All three R3b fire rates fall outside [21.42, 41.42] on the narrow list.",
              "observed": r3b, "won": not inside,
              "why": ("none of the three lands in the band" if not inside
                      else "%s lands in the band" % ", ".join(inside))})

    top = max(names, key=lambda n: r3b[n])
    P.append({"id": "P2", "called": "yes",
              "claim": "WHATWG standards give the highest R3b fire rate of the three.",
              "observed": r3b, "won": top == "WHATWG standards",
              "why": "highest is %s at %.2f %%" % (top, r3b[top])})

    above = [n for n in names if r3b[n] > HIGH]
    P.append({"id": "P3", "called": "yes",
              "claim": "At least one corpus comes in above 41.42 %, i.e. above the band.",
              "observed": r3b, "won": bool(above),
              "why": "above the band: %s" % (", ".join(above) or "none")})

    below = [n for n in names if r3b[n] < 10.0]
    P.append({"id": "P4", "called": "yes",
              "claim": "No corpus comes in below 10 % on the narrow list.",
              "observed": r3b, "won": not below,
              "why": "lowest is %s at %.2f %%" % (min(names, key=lambda n: r3b[n]),
                                                  min(r3b.values()))})

    by_rate = sorted(names, key=lambda n: -r3b[n])
    by_block = sorted(names, key=lambda n: -blk[n])
    P.append({"id": "P5", "called": "yes",
              "claim": "The three rank by R3b fire rate in the same order as by median in-reach "
                       "carrier-block length in words.",
              "observed": {"by_R3b": by_rate, "by_median_carrier_block_words": by_block,
                           "median_carrier_block_words": blk},
              "won": by_rate == by_block,
              "why": "%s against %s" % (" > ".join(by_rate), " > ".join(by_block))})

    wide_span = [n for n in names if span[n] > 20.0]
    P.append({"id": "P6", "called": "yes",
              "claim": "The reach span across base/narrow/wide at word window 36 exceeds 20 points "
                       "in at least two of the three corpora.",
              "observed": span, "won": len(wide_span) >= 2,
              "why": "%d of 3 exceed 20 points (%s)" % (
                  len(wide_span), "; ".join("%s %.2f" % (n, span[n]) for n in names))})

    holds = {n: [narrow[n]["by_rule"][k]["fire_pct"] for k in ORDER] for n in names}
    strict = {n: all(v[i] < v[i + 1] for i in range(3)) for n, v in holds.items()}
    all_hold = all(strict.values())
    P.append({"id": "P7", "called": "no",
              "claim": "The fire-rate ordering R1 < R2 < R3 < R3b holds in all three corpora. "
                       "Called NO: the prediction was that it would break somewhere.",
              "observed": {"fire_pcts_in_rule_order": holds, "strictly_increasing": strict},
              "won": not all_hold,
              "why": ("the ordering holds in all three, so the call of NO is lost"
                      if all_hold else "it breaks in %s"
                      % ", ".join(n for n, ok in strict.items() if not ok))})

    won = [p["id"] for p in P if p["won"]]
    lost = [p["id"] for p in P if not p["won"]]

    falsified = bool(inside)
    out = {
        "note": "Scored mechanically from results.json. PREDICTIONS.md was committed before "
                "port.py existed; git ancestry is asserted by verify.py.",
        "predictions": P,
        "won": won, "lost": lost,
        "tally": "%d of %d won" % (len(won), len(P)),
        "S91.RULEBOUND": {
            "condition": "falsified if R3b's fire rate over the rows in reach comes in within 10 "
                         "points of 31.42 % in any one of the three",
            "band": [LOW, HIGH],
            "narrow_R3b_by_corpus": r3b,
            "inside_the_band": inside,
            "verdict": "FALSIFIED" if falsified else "not falsified",
            "margin": {n: round(r3b[n] - 31.42, 2) for n in names},
        },
    }
    (HERE / "adjudication.json").write_text(json.dumps(out, indent=1) + "\n")

    for p in P:
        print("  %s  %-4s  %s" % (p["id"], "WON" if p["won"] else "LOST", p["why"]))
    print("\n  %s" % out["tally"])
    print("  S91.RULEBOUND: %s -- %s" % (out["S91.RULEBOUND"]["verdict"],
                                         ", ".join("%s %+.2f" % (n, out["S91.RULEBOUND"]["margin"][n])
                                                   for n in names)))
    print("  wrote adjudication.json")


if __name__ == "__main__":
    main()
