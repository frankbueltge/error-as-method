#!/usr/bin/env python3
"""The Exhortation -- Session 83, 2026-09-07.

Measures three families over the 63-act corpus committed by Session 82, none of which needs a
derived vocabulary.  Written after PREDICTIONS.md was closed; nothing here was adjusted once a
count was seen.

  Family A  addressed exhortation without a deontic modal
            "<party> is/are encouraged|invited|urged|called upon|recommended|requested|expected to"
            The addressee is the grammatical subject of the passive, so it stands immediately to
            the left of the match.  No actor list is derived, which is why F-111 and F-112 --
            Session 82's two bugs, both bugs in a derived vocabulary -- cannot occur here.

  Family B  "it is necessary|appropriate|desirable|advisable|important|essential to|that|for"
            A CONTROL COLUMN AND NEVER A NUMERATOR.  Guideline 10.3 of the Joint Practical Guide
            prescribes this formula as the ideal conclusion of a statement of reasons: "the
            conclusion that it is therefore necessary or appropriate to adopt the measures set out
            in the enacting terms."  Counting it as a violation would have been refuted by the
            source before the code ran.

  Family C  plain occurrence counts of shall/should/must/may, recomputed from the corpus rather
            than copied from Session 82's results, so that a disagreement would show.

The calibration below guards the INPUT, not the cut.  Session 82's calibration guarded the cut it
had already worried about and passed on all three runs while everything downstream was wrong
(F-111, F-112).  The lesson it drew -- a calibration that passes tells you about the thing you
pointed it at and nothing else -- is why this one is pointed at a different thing and is not
claimed to guard anything else either.
"""

import gzip
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S82 = HERE.parent / "2026-09-06-the-rate-of-the-rule"

# ---------------------------------------------------------------- the patterns, from PREDICTIONS.md

FAMILY_A = re.compile(
    r"\b(is|are|was|were|be)\s+"
    r"(encouraged|invited|urged|called upon|recommended|requested|expected)\s+to\b",
    re.IGNORECASE,
)

FAMILY_B = re.compile(
    r"\bit is\s+(necessary|appropriate|desirable|advisable|important|essential)\s+(to|that|for)\b",
    re.IGNORECASE,
)

MODALS = ("shall", "should", "must", "may")

# The stop list, fixed in PREDICTIONS.md: a negated exhortation is a different act.
NEGATION_WINDOW = 90
NEGATION = re.compile(r"\b(not|no longer)\b", re.IGNORECASE)

# Clause boundary for reading the addressee off the left of the match.  Raw, never normalised.
CLAUSE_BREAK = re.compile(r"[,;:.—]|\band\b|\bor\b|\bthat\b|\bwhich\b|\bwhere\b", re.IGNORECASE)


def sentences(text):
    """Crude sentence split.  Recitals are numbered points of one or more complete sentences
    (Guideline 10.1); the split only has to be good enough to quote the hit back to a reader."""
    parts = re.split(r"(?<=[.;])\s+(?=[A-Z(‘’'])", text)
    return [p.strip() for p in parts if p.strip()]


def addressee(sentence, start):
    """The party being exhorted, taken raw from the left of the match."""
    left = sentence[:start].rstrip()
    breaks = [m.end() for m in CLAUSE_BREAK.finditer(left)]
    cut = breaks[-1] if breaks else 0
    return left[cut:].strip() or left.strip()


def family_a_hits(text, division, celex, part):
    kept, rejected = [], []
    for sent in sentences(text):
        for m in FAMILY_A.finditer(sent):
            window = sent[max(0, m.start() - NEGATION_WINDOW):m.start()]
            row = {
                "celex": celex,
                "part": part,
                "division": division,
                "verb": m.group(2).lower(),
                "addressee": addressee(sent, m.start()),
                "match": m.group(0),
                "sentence": sent,
            }
            if NEGATION.search(window):
                row["rejected_because"] = "negation within %d characters to the left" % NEGATION_WINDOW
                rejected.append(row)
            else:
                kept.append(row)
    return kept, rejected


def family_b_hits(text, division, celex, part):
    out = []
    for sent in sentences(text):
        for m in FAMILY_B.finditer(sent):
            out.append({
                "celex": celex, "part": part, "division": division,
                "head": m.group(1).lower(), "complement": m.group(2).lower(),
                "sentence": sent,
            })
    return out


def counts(text):
    low = text.lower()
    return {w: len(re.findall(r"\b%s\b" % w, low)) for w in MODALS} | {"words": len(text.split())}


def main():
    corpus = json.load(gzip.open(S82 / "corpus.json.gz", "rt"))
    s82 = json.load(open(S82 / "results.json"))
    meta = {a["celex"]: a for a in s82["acts"]}

    # ------------------------------------------------------------------ calibration on the INPUT
    problems = []
    if len(corpus) != 63:
        problems.append("corpus holds %d acts, expected 63" % len(corpus))
    gdpr = corpus.get("32016R0679")
    if gdpr is None:
        problems.append("32016R0679 absent from the corpus")
    else:
        if len(gdpr["recitals"]) != 173:
            problems.append("GDPR recitals %d, expected 173" % len(gdpr["recitals"]))
        if len(gdpr["articles"]) != 99:
            problems.append("GDPR articles %d, expected 99" % len(gdpr["articles"]))
    for celex, act in corpus.items():
        m = meta.get(celex)
        if m is None:
            problems.append("%s absent from Session 82's results" % celex)
            continue
        if len(act["recitals"]) != m["n_recitals"] or len(act["articles"]) != m["n_articles"]:
            problems.append("%s division counts disagree with Session 82" % celex)
    if problems:
        print("CALIBRATION FAILED -- measuring nothing:", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        sys.exit(1)
    print("calibration: 63 acts, GDPR 173/99, every act's division counts agree with Session 82.")

    acts, all_a, all_b, all_rejected = [], [], [], []
    for celex, act in sorted(corpus.items()):
        m = meta[celex]
        row = {
            "celex": celex, "stratum": m["stratum"], "adoption_year": m["adoption_year"],
            "domain": m["domain"], "title": m["title"],
            "n_recitals": len(act["recitals"]), "n_articles": len(act["articles"]),
        }
        for part in ("recitals", "articles"):
            a_kept, a_rej = [], []
            b_hits = []
            reg = {w: 0 for w in MODALS} | {"words": 0}
            for division, text in act[part].items():
                k, r = family_a_hits(text, division, celex, part)
                a_kept += k
                a_rej += r
                b_hits += family_b_hits(text, division, celex, part)
                c = counts(text)
                for w in reg:
                    reg[w] += c[w]
            all_a += a_kept
            all_b += b_hits
            all_rejected += a_rej
            row[part] = {
                "family_a": len(a_kept),
                "family_a_divisions": sorted({h["division"] for h in a_kept}),
                "family_a_rejected": len(a_rej),
                "family_b": len(b_hits),
                "family_b_divisions": sorted({h["division"] for h in b_hits}),
                "register": reg,
            }
        # Session 82's repaired rule, carried across unchanged so tonight can audit it.
        row["s82_directed"] = m["directed"]["recitals_directed"]
        row["s82_rate"] = m["rate"]
        acts.append(row)

    B = [a for a in acts if a["stratum"] == "B"]
    A = [a for a in acts if a["stratum"] == "A"]

    def tally(pop, part, key):
        return sum(a[part][key] for a in pop)

    def with_any(pop, part, key):
        return sum(1 for a in pop if a[part][key] > 0)

    summary = {
        "strata": {"B": len(B), "A": len(A)},
        "stratum_B": {
            "recitals": sum(a["n_recitals"] for a in B),
            "articles": sum(a["n_articles"] for a in B),
            "family_a_recitals": tally(B, "recitals", "family_a"),
            "family_a_articles": tally(B, "articles", "family_a"),
            "family_a_rejected_recitals": tally(B, "recitals", "family_a_rejected"),
            "family_b_recitals": tally(B, "recitals", "family_b"),
            "family_b_articles": tally(B, "articles", "family_b"),
            "acts_with_family_a_recitals": with_any(B, "recitals", "family_a"),
            "acts_with_family_a_articles": with_any(B, "articles", "family_a"),
            "acts_with_family_b_recitals": with_any(B, "recitals", "family_b"),
            "register_recitals": {w: sum(a["recitals"]["register"][w] for a in B) for w in MODALS},
            "register_articles": {w: sum(a["articles"]["register"][w] for a in B) for w in MODALS},
            "preamble_words": sum(a["recitals"]["register"]["words"] for a in B),
        },
        "stratum_A": {
            "recitals": sum(a["n_recitals"] for a in A),
            "family_a_recitals": tally(A, "recitals", "family_a"),
            "family_b_recitals": tally(A, "recitals", "family_b"),
            "acts_with_family_a_recitals": with_any(A, "recitals", "family_a"),
            "acts_with_family_b_recitals": with_any(A, "recitals", "family_b"),
        },
        "gdpr_family_a_recitals": next(a for a in acts if a["celex"] == "32016R0679")["recitals"]["family_a"],
        "s82_directed_total": sum(len(a["s82_directed"]) for a in acts),
        "s82_directed_total_B": sum(len(a["s82_directed"]) for a in B),
    }

    json.dump({"summary": summary, "acts": acts}, open(HERE / "results.json", "w"), indent=1)
    json.dump(all_a, open(HERE / "family-a.json", "w"), indent=1)
    json.dump(all_b, open(HERE / "family-b.json", "w"), indent=1)
    json.dump(all_rejected, open(HERE / "rejected.json", "w"), indent=1)

    print(json.dumps(summary, indent=1))
    print("\nFamily A kept %d, rejected %d.  Family B %d.  Written." %
          (len(all_a), len(all_rejected), len(all_b)))


if __name__ == "__main__":
    main()
