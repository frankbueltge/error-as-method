#!/usr/bin/env python3
"""Scores the seven predictions -- and scores them three times.

The instrument was wrong twice before it was right, and both errors were found after the
predictions were closed and after the first numbers were in hand:

  run 1  results-run1-plural-bug.json   the presence test turned `authorities` into
                                        `authoritie`, so the most commanded party in
                                        several acts was rejected as absent (F-111)
  run 2  results-run2-case-bug.json     the derived actor patterns were lowercase and the
                                        search was case-sensitive, so `the Commission`,
                                        `Member States` and every sentence-initial actor
                                        were invisible, and the rule matched only lowercase
                                        junk heads (F-112)
  run 3  results.json                   both repaired

A single scoring against run 3 would be a true statement that hides the thing worth
knowing.  So every prediction is scored against all three, and the table of which
predictions change their verdict between runs is this work's result.  Nothing is scored
against a run the code chose; the run each verdict belongs to is named.

Writes: adjudication.json.
"""

import gzip
import json
import pathlib
import statistics as st

HERE = pathlib.Path(__file__).resolve().parent


def load_json(path):
    """Read a JSON file, transparently accepting the gzipped form.

    corpus.json and the two superseded run files are committed gzipped: they are 12.7 MB
    of largely repeated legal text against an 11 MB repository, and the licence question
    is not the size question.  Gzip keeps every byte checkable offline at a proportionate
    cost, which is the same trade the raw HTML lost.
    """
    path = pathlib.Path(path)
    if path.exists():
        return json.loads(path.read_text())
    gz = path.with_suffix(path.suffix + ".gz")
    with gzip.open(gz, "rt") as fh:
        return json.load(fh)


def dump_json(path, payload, gzipped=False):
    path = pathlib.Path(path)
    text = json.dumps(payload, indent=1) + "\n"
    if gzipped:
        with gzip.open(str(path) + ".gz", "wt") as fh:
            fh.write(text)
        if path.exists():
            path.unlink()
    else:
        path.write_text(text)

RUNS = [
    ("run 1 -- plural bug (F-111)", "results-run1-plural-bug.json"),
    ("run 2 -- case bug (F-112)", "results-run2-case-bug.json"),
    ("run 3 -- both repaired", "results.json"),
]


def stratum(results, which):
    return [a for a in results["acts"] if a["stratum"] == which]


def score_run(results):
    B = stratum(results, "B")
    rates = [a["rate"] for a in B]
    q1, median, q3 = st.quantiles(rates, n=4)
    gdpr = next(a for a in B if a["celex"] == "32016R0679")

    pre = [a["rate"] for a in B if a["adoption_year"] <= 2015]
    post = [a["rate"] for a in B if a["adoption_year"] >= 2016]
    gap = abs(st.mean(pre) - st.mean(post))

    shall_recitals = sum(a["register"]["recitals"]["shall"] for a in B)
    with_directed = sum(1 for a in B if a["directed"]["count"] > 0)
    enc = sum(1 for a in B if a["encouraged"]["recital_only"])

    A10 = [a for a in stratum(results, "A") if a["n_recitals"] >= 10]
    A10d = [a for a in A10 if a["directed"]["count"] > 0]

    return {
        "P1": {
            "claim": "the GDPR's rate is inside the interquartile range of Stratum B",
            "observed": "GDPR %.1f%%, Q1 %.1f, Q3 %.1f" % (gdpr["rate"], q1, q3),
            "verdict": "WON" if q1 <= gdpr["rate"] <= q3 else "LOST",
        },
        "P2": {
            "claim": "|mean rate 2009-2015 - mean rate 2016-2024| < 8 points",
            "observed": "%.1f vs %.1f, gap %.1f" % (st.mean(pre), st.mean(post), gap),
            "verdict": "WON" if gap < 8 else "LOST",
        },
        "P3": {
            "claim": "(a) total `shall` in Stratum B recitals <= 5 AND (b) >= 90% of acts directed",
            "observed": "(a) %d  (b) %d/%d = %.1f%%"
                        % (shall_recitals, with_directed, len(B), 100 * with_directed / len(B)),
            "verdict": "WON" if (shall_recitals <= 5 and with_directed / len(B) >= 0.9) else "LOST",
            "part_a": "WON" if shall_recitals <= 5 else "LOST",
            "part_b": "WON" if with_directed / len(B) >= 0.9 else "LOST",
        },
        "P4": {
            "claim": ">= 80% of Stratum A acts with >= 10 recitals carry a directed sentence",
            "observed": "%d/%d = %.1f%%" % (len(A10d), len(A10), 100 * len(A10d) / len(A10)),
            "verdict": "WON" if len(A10d) / len(A10) >= 0.8 else "LOST",
        },
        "P5": {
            "claim": ">= half of Stratum B has `encourag*` in the recitals and never in the articles",
            "observed": "%d/%d = %.1f%%" % (enc, len(B), 100 * enc / len(B)),
            "verdict": "WON" if enc >= len(B) / 2 else "LOST",
        },
        "_context": {
            "rates": {a["celex"]: a["rate"] for a in B},
            "quartiles": {"q1": round(q1, 1), "median": round(median, 1), "q3": round(q3, 1)},
            "mean": round(st.mean(rates), 1),
        },
    }


def main():
    runs = {}
    for label, filename in RUNS:
        path = HERE / filename
        if path.exists() or path.with_suffix(path.suffix + ".gz").exists():
            runs[label] = score_run(load_json(path))

    audit = load_json(HERE / "audit-results.json")
    final = list(runs)[-1]
    runs[final]["P6"] = {
        "claim": "hand precision below 0.85 on 40 seeded matched sentences",
        "observed": "%d/40 directed norms = %.3f"
                    % (audit["precision"]["directed_norm"], audit["precision"]["precision"]),
        "verdict": audit["precision"]["P6"],
        "note": "scored on run 3 only; the sample was redrawn after each repair",
    }
    runs[final]["P7"] = {
        "claim": ">= 2 missed norms in 40 seeded unmatched recitals",
        "observed": "%d missed" % audit["recall"]["missed_norms"],
        "verdict": audit["recall"]["P7"],
        "note": "scored on run 3 only",
    }

    # Which verdicts move between runs -- the point of scoring three times.
    moved = {}
    for key in ("P1", "P2", "P3", "P4", "P5"):
        verdicts = [(label, runs[label][key]["verdict"]) for label in runs]
        if len({v for _, v in verdicts}) > 1:
            moved[key] = verdicts

    tally = {label: {k: v["verdict"] for k, v in run.items() if k.startswith("P")}
             for label, run in runs.items()}

    payload = {
        "adjudicated": "2026-09-06",
        "runs": runs,
        "verdict_tally": tally,
        "verdicts_that_move_between_runs": moved,
        "reading": (
            "Five predictions were scorable against all three runs.  %d of them return a "
            "different verdict depending on which version of the instrument is asked.  Each "
            "of the three versions ran without error, produced a complete table, and would "
            "have been reported as a result by a night that stopped there."
        ) % len(moved),
    }
    (HERE / "adjudication.json").write_text(json.dumps(payload, indent=1) + "\n")

    for label in runs:
        print("%-30s %s" % (label, "  ".join(
            "%s:%s" % (k, v["verdict"]) for k, v in sorted(runs[label].items())
            if k.startswith("P"))))
    print()
    for key, verdicts in moved.items():
        print("%s moves: %s" % (key, " -> ".join(v for _, v in verdicts)))


if __name__ == "__main__":
    main()
