#!/usr/bin/env python3
"""inspect.py -- EXPLORATORY, written after results.json existed and after S94.SPREAD had come back
falsified.  No prediction is scored against anything here.

Reading twelve non-firing rows by hand (journal, 2026-09-26) suggested one reason why this corpus
sits in the middle by subjecthood and at the bottom by R3b: US federal regulation often puts a
qualifier between its party and its modal -- "Each operator subject to § 91.865 ... shall submit",
"Each operator ... desiring to establish ... must submit".  Both subjecthood and R3 only see a party
**immediately** followed by a verb.

This measures that directly in all five traditions, with Session 94's builders for the four and
tonight's corpus for the fifth, on each tradition's NARROW list:

  immediate  term + R3 verb                                   (Session 94's subjecthood numerator)
  delayed    term + 1-12 words with no sentence end + R3 verb, and not immediate

It is a new instrument built after the fact, so it can only suggest.  Writes inspection.json.
"""

import gzip
import json
import re
from pathlib import Path

import measure as M

HERE = Path(__file__).resolve().parent
P, V = M.P94, M.P94.V


def rates(docs, terms):
    party = re.compile(V.term_pattern(terms), re.IGNORECASE)
    verb = re.compile(r"^" + V.R3_VERB + r"\b", re.IGNORECASE)
    stop = re.compile(r"[.;:\n]")
    text = "\n".join("\n".join(seq) for seq in docs.values())
    total = i = d = 0
    for m in party.finditer(text):
        total += 1
        tail = text[m.end():m.end() + 400]
        cut = stop.search(tail)
        words = (tail[:cut.start()] if cut else tail).split()[:13]
        hit = [k for k, w in enumerate(words) if verb.match(w)]
        if hit and hit[0] == 0:
            i += 1
            d += 1
        elif hit:
            d += 1
    return {"party_term_occurrences": total, "immediate": i,
            "immediate_pct": round(100.0 * i / total, 2),
            "immediate_or_within_12_words": d,
            "within_12_pct": round(100.0 * d / total, 2),
            "delayed_share_of_acting_pct": round(100.0 * (d - i) / d, 2) if d else None}


def main():
    res = json.load(open(HERE / "results.json"))
    base = res["reach"]["term_lists"]["base"]["terms"]
    rows = {}
    for name, spec in list(P.CORPORA.items()) + [("UK Acts", P.CALIBRATION)]:
        docs, _ = spec["build"]()
        rows[name] = rates(docs, base + spec["own"])
    corpus = json.load(gzip.open(HERE / "corpus.json.gz", "rt"))
    rows["14 CFR F+G"] = rates({k: d["act"] for k, d in corpus.items() if d["act"]},
                               base + M.CFR_OWN)
    r3b = {k: v[1] for k, v in M.PRIOR.items()}
    r3b["14 CFR F+G"] = res["S94_SPREAD"]["R3b"]
    for k in rows:
        rows[k]["R3b_narrow_pct"] = r3b[k]
    order = lambda key: [k for k, _ in sorted(rows.items(), key=lambda kv: -kv[1][key])]
    out = {"note": "EXPLORATORY, post hoc. See the docstring.",
           "rows": rows,
           "orderings": {"by_R3b": order("R3b_narrow_pct"),
                         "by_immediate": order("immediate_pct"),
                         "by_within_12": order("within_12_pct"),
                         "by_delayed_share": order("delayed_share_of_acting_pct")}}
    (HERE / "inspection.json").write_text(json.dumps(out, indent=1) + "\n")
    print("%-18s %8s %9s %10s %9s" % ("corpus", "R3b", "immed.%", "within12%", "delayed%"))
    for k, v in sorted(rows.items(), key=lambda kv: -kv[1]["R3b_narrow_pct"]):
        print("%-18s %8.2f %9.2f %10.2f %9.2f" % (k, v["R3b_narrow_pct"], v["immediate_pct"],
                                                 v["within_12_pct"],
                                                 v["delayed_share_of_acting_pct"]))
    for k, v in out["orderings"].items():
        print("  %-18s %s" % (k, " > ".join(v)))


if __name__ == "__main__":
    main()
