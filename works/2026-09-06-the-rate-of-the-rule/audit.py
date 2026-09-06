#!/usr/bin/env python3
"""The audit: what the rate is actually made of.

Two seeded samples, drawn with random.Random(20260906), the seed fixed in PREDICTIONS.md
before any of this was run:

  PRECISION (P6).  40 matched sentences drawn from the pooled matches of all 28 Stratum B
  acts.  Each is adjudicated by hand in audit.json: is this, on reading, a sentence of a
  recital that tells a party the act commands elsewhere to do something -- or is it a
  statement of reasons that happened to satisfy a regular expression?

  RECALL (P7).  40 recitals drawn from the pooled recitals of Stratum B that the rule did
  NOT match.  Each is adjudicated by hand: does it contain a norm directed at an actor
  that the rule missed?

The hand verdicts are mine, they are unreviewed, and each row carries the text so that a
reader can disagree with a specific row rather than with the number.

`python3 audit.py draw`   writes audit-sample.json, the two samples, unadjudicated.
`python3 audit.py score`  reads audit.json (the hand verdicts) and reports precision,
                          recall-misses, and the corrected rates.

There is also one measurement here that needs no hand at all, and it turned out to matter
more than either sample: for every act, what share of its matches come from an actor that
survives the strict threshold of ten `shall` subjects.  That share is the mechanical
shadow of precision and it can be computed for all 63 acts rather than for 40 sentences.
"""

import gzip
import json
import pathlib
import random
import sys

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


SEED = 20260906
N = 40


def stratum_b(results):
    return [a for a in results["acts"] if a["stratum"] == "B"]


def draw():
    results = load_json(HERE / "results.json")
    corpus = load_json(HERE / "corpus.json")
    acts = stratum_b(results)

    matched, unmatched = [], []
    for act in acts:
        for recital, hits in act["directed"]["detail"].items():
            for hit in hits:
                matched.append({
                    "celex": act["celex"], "domain": act["domain"], "recital": int(recital),
                    "actor": hit["actor"], "verb": hit["verb"], "sentence": hit["sentence"],
                })
        directed = set(act["directed"]["recitals_directed"])
        for number, text in corpus[act["celex"]]["recitals"].items():
            if int(number) not in directed:
                unmatched.append({
                    "celex": act["celex"], "domain": act["domain"], "recital": int(number),
                    "text": text,
                })

    matched.sort(key=lambda r: (r["celex"], r["recital"], r["actor"], r["sentence"]))
    unmatched.sort(key=lambda r: (r["celex"], r["recital"]))

    rng = random.Random(SEED)
    sample = {
        "seed": SEED,
        "pool_sizes": {"matched": len(matched), "unmatched_recitals": len(unmatched)},
        "precision_sample": rng.sample(matched, N),
        "recall_sample": rng.sample(unmatched, N),
    }
    (HERE / "audit-sample.json").write_text(json.dumps(sample, indent=1) + "\n")
    print("pools: %d matched sentences, %d unmatched recitals"
          % (len(matched), len(unmatched)))
    print("drew %d and %d with seed %d -> audit-sample.json" % (N, N, SEED))


def strict_share(results):
    """The mechanical shadow of precision, computable for every act.

    A match is 'strict' where its actor also survives the ten-occurrence threshold.  No
    hand is involved and no sample: this runs over every match in the population.
    """
    out = {}
    for act in results["acts"]:
        strict_actors = set(act["strict"]["actors"])
        total = junk = 0
        for hits in act["directed"]["detail"].values():
            for hit in hits:
                total += 1
                if hit["actor"] not in strict_actors:
                    junk += 1
        out[act["celex"]] = {
            "matches": total,
            "from_actors_below_the_strict_threshold": junk,
            "share": round(junk / total, 3) if total else None,
        }
    return out


def score():
    results = load_json(HERE / "results.json")
    verdicts = load_json(HERE / "audit.json")

    p = verdicts["precision"]
    tp = sum(1 for r in p if r["verdict"] == "directed norm")
    fp = len(p) - tp
    precision = tp / len(p)

    r = verdicts["recall"]
    missed = sum(1 for x in r if x["verdict"] == "missed norm")

    acts = stratum_b(results)
    rates = [a["rate"] for a in acts]
    corrected = [round(a["rate"] * precision, 1) for a in acts]

    shares = strict_share(results)
    b_shares = [shares[a["celex"]]["share"] for a in acts if shares[a["celex"]]["share"] is not None]

    report = {
        "seed": SEED,
        "precision": {
            "n": len(p), "directed_norm": tp, "not_a_directed_norm": fp,
            "precision": round(precision, 3),
            "P6_claim": "precision below 0.85",
            "P6": "WON" if precision < 0.85 else "LOST",
        },
        "recall": {
            "n": len(r), "missed_norms": missed,
            "P7_claim": "at least 2 missed",
            "P7": "WON" if missed >= 2 else "LOST",
        },
        "corrected_rates": {a["celex"]: c for a, c in zip(acts, corrected)},
        "junk_share_per_act": shares,
        "junk_share_stratum_B": {
            "min": min(b_shares), "max": max(b_shares),
            "median": sorted(b_shares)[len(b_shares) // 2],
        },
        "note": (
            "A pooled precision cannot be applied per act, because the junk share is not "
            "constant across acts -- it runs from %.3f to %.3f in Stratum B.  The corrected "
            "rates above are therefore a uniform scaling and are the WEAKEST number in this "
            "work; the per-act junk share beside them is the reason the cross-act comparison "
            "this night set out to make does not survive."
        ) % (min(b_shares), max(b_shares)),
    }
    (HERE / "audit-results.json").write_text(json.dumps(report, indent=1) + "\n")

    print("precision %d/%d = %.3f  -> P6 %s" % (tp, len(p), precision, report["precision"]["P6"]))
    print("recall    %d missed of %d -> P7 %s" % (missed, len(r), report["recall"]["P7"]))
    print("junk share across Stratum B: min %.3f median %.3f max %.3f"
          % (min(b_shares), sorted(b_shares)[len(b_shares) // 2], max(b_shares)))


if __name__ == "__main__":
    {"draw": draw, "score": score}[sys.argv[1] if len(sys.argv) > 1 else "draw"]()
