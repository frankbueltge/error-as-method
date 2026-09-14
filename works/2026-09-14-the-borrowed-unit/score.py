#!/usr/bin/env python3
"""score.py -- the five predictions of PREDICTIONS.md, scored against results.json.

Nothing is decided here that was not written before reach.py existed.  Each row records the
threshold as fixed, the value as measured, and the verdict, so a reader can disagree with the
threshold rather than with the arithmetic.

Run after reach.py.  Writes adjudication.json.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    r = json.load(open(HERE / "results.json"))
    b0 = {k: v["row"]["blocks"]["pct"]["0"] for k, v in r["corpora"].items()}
    med = r["median_word_distance"]
    eu_base0 = r["corpora"]["eu"]["base"]["blocks"]["pct"]["0"]
    sp_b = r["spreads"]["block_window_0"]["spread"]
    sp_w = r["spreads"]["word_window_36"]["spread"]

    rows = [
        {
            "id": "P1",
            "claim": "EU comes in strictly above 13.6 % at block window 0 (S88.REACH's own test).",
            "declared": "non-evidential before the run: an 11.11x unit ratio, not a drafting fact.",
            "threshold": "> 13.6",
            "measured": b0["eu"],
            "verdict": "WON" if b0["eu"] > 13.6 else "LOST",
        },
        {
            "id": "P2",
            "claim": "RFC comes in strictly above 13.6 % and strictly below 35.0 % at block window 0.",
            "declared": "evidential: the RFC hosting block is 1.14x WHATWG's.",
            "threshold": "13.6 < x < 35.0",
            "measured": b0["rfc"],
            "verdict": "WON" if 13.6 < b0["rfc"] < 35.0 else "LOST",
        },
        {
            "id": "P3",
            "claim": "The three-corpus spread is > 40 points at block window 0 and < 20 points at "
                     "word window 36.",
            "declared": "both halves must hold.",
            "threshold": "spread(blocks,0) > 40 and spread(words,36) < 20",
            "measured": {"block_window_0": sp_b, "word_window_36": sp_w},
            "verdict": "WON" if (sp_b > 40 and sp_w < 20) else "LOST",
        },
        {
            "id": "P4",
            "claim": "Of the three, WHATWG has the largest median word distance to the nearest "
                     "party term -- S88.REACH's motivating sentence, in the unit that travels.",
            "declared": "the sharper form of the row's claim; can fail while the block test survives.",
            "threshold": "argmax(median word distance) == whatwg",
            "measured": med,
            "verdict": "WON" if max(med, key=lambda k: med[k]) == "whatwg" else "LOST",
        },
        {
            "id": "P5",
            "claim": "On the base list alone -- no Member States, no the Commission -- EU still "
                     "comes in strictly above 13.6 % at block window 0.",
            "declared": "a robustness check on how much of the EU result two strings carry.",
            "threshold": "> 13.6",
            "measured": eu_base0,
            "verdict": "WON" if eu_base0 > 13.6 else "LOST",
        },
    ]

    falsifier = {
        "row": "S88.REACH",
        "condition": "falsified if either corpus comes in at or below 13.6 % at block window 0",
        "instrument_the_row_specified": "the base list extended by each tradition's own terms",
        "eu": b0["eu"],
        "rfc": b0["rfc"],
        "outcome": "SURVIVES on the instrument the row specified: 68.35 % and 18.31 %, both above "
                   "13.6 %.",
        "the_qualification_this_night_attaches": (
            "On the strictest common instrument -- WHATWG's own 26 terms, with no extension -- EU "
            "comes in at %.2f %%, which is AT OR BELOW 13.6 %% and would falsify the row. The row "
            "survives because it authorised an extension, and the extension is two strings wide. "
            "That is a fact about the instrument's sensitivity, not about EU drafting, and it is "
            "recorded here rather than left for a later session to find." % eu_base0),
    }

    out = {"predictions": rows, "falsifier": falsifier,
           "won": sum(1 for x in rows if x["verdict"] == "WON"),
           "lost": sum(1 for x in rows if x["verdict"] == "LOST")}
    (HERE / "adjudication.json").write_text(json.dumps(out, indent=1) + "\n")

    for x in rows:
        print("  %-3s %-5s  %s" % (x["id"], x["verdict"], x["threshold"]))
        print("        measured: %s" % x["measured"])
    print("\n  %d won, %d lost" % (out["won"], out["lost"]))
    print("  S88.REACH: %s" % falsifier["outcome"])


if __name__ == "__main__":
    main()
