#!/usr/bin/env python3
"""Post-hoc, declared, scoring nothing -- Session 84, 2026-09-08.

Everything here was written AFTER the predictions were scored and after the audits were adjudicated.
None of it moves a prediction.  It exists because Session 83's rule holds: the repair is committed,
labelled, and kept out of the numerator.

Four things:

  1. THE CONFOUND, QUANTIFIED.  P2 won 28 of 28, and the within-modal table says the win carries no
     information about bearer-deletion.  This puts a number on why.
  2. THE INTERVENING-ADVERBIAL MISS.  Two of the thirty NON-B rows in the 4b audit turned out to be
     agentless passives the B-FORM rule could not see because a word stood between the modal and
     `be`.  This counts the class over the whole corpus.
  3. THE AUDITED HEADLINE.  What the 4a precision does to the raw rate, per part, with the sample
     sizes attached because they are small and the per-part split is smaller.
  4. THE SENTENCE THAT CROSSED.  Row 23 of the 4c census claims Regulation (EU) 2021/241 carries the
     same exhortation in recital 43 and in Article 18.  Checked here against the committed corpus
     rather than left as a reading.
"""

import gzip
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
S82 = HERE.parent / "2026-09-06-the-rate-of-the-rule"

# One or two tokens between the modal and `be` -- the class the B-FORM rule cannot see.
GAPPED = re.compile(
    r"\b(shall|should|must)\s+((?!be\b)[A-Za-z(][^\s]*(?:\s+(?!be\b)[^\s]+)?)\s+be\s+([A-Za-z][A-Za-z\-]*)",
    re.IGNORECASE,
)
BY = re.compile(r"\bby\b", re.IGNORECASE)


def main():
    corpus = json.load(gzip.open(S82 / "corpus.json.gz", "rt"))
    results = json.load(open(HERE / "results.json"))
    audit = json.load(open(HERE / "audit-results.json"))

    out = {"declared": "post-hoc, after scoring; nothing here moves a prediction"}

    # ---------------------------------------------------------------- 1. the confound
    conf = {}
    for part in ("recitals", "articles"):
        w = results["whole_corpus"][part]
        tot = w["modal_occurrences"]
        conf[part] = {
            "modal_share": {m: round(d["total"] / tot, 4) for m, d in w["per_modal"].items()},
            "per_modal_rate": {m: d["rate"] for m, d in w["per_modal"].items()},
            "overall_rate": w["bearer_deletion_rate"],
        }
    out["1_confound"] = {
        "note": "the recitals are 99.2 % `should` and the articles 99.1 % `shall`.  The two halves "
                "of the comparison share almost no modal, so the recital/article contrast and the "
                "should/shall contrast are the same contrast measured twice.  Where the within-modal "
                "comparison has any observations at all it runs the OTHER way.",
        "by_part": conf,
    }

    # ---------------------------------------------------------------- 2. the gapped misses
    gap_rows, gap_tokens = [], {"recitals": Counter(), "articles": Counter()}
    gap_counts = {"recitals": {"total": 0, "agentless": 0}, "articles": {"total": 0, "agentless": 0}}
    for celex, act in sorted(corpus.items()):
        for part in ("recitals", "articles"):
            for division, text in sorted(act[part].items(), key=lambda kv: str(kv[0])):
                for m in GAPPED.finditer(text):
                    tok = m.group(3).lower()
                    window = text[m.end():m.end() + 200]
                    agentless = not BY.search(window)
                    gap_counts[part]["total"] += 1
                    gap_counts[part]["agentless"] += int(agentless)
                    gap_tokens[part][tok] += 1
                    if len(gap_rows) < 300:
                        gap_rows.append({
                            "celex": celex, "part": part, "division": division,
                            "modal": m.group(1).lower(), "gap": m.group(2), "slot_token": tok,
                            "agentless": agentless,
                            "text": text[max(0, m.start() - 60):m.end() + 60],
                        })
    out["2_gapped"] = {
        "rule": "<modal> <one or two tokens, not `be`> be <token>",
        "counts": gap_counts,
        "share_of_the_measured_agentless_class": {
            part: round(gap_counts[part]["agentless"] /
                        results["whole_corpus"][part]["agentless"], 4)
            for part in ("recitals", "articles")
        },
        "top_tokens": {p: dict(c.most_common(15)) for p, c in gap_tokens.items()},
        "first_300_rows": gap_rows,
    }

    # ---------------------------------------------------------------- 3. the audited headline
    prec = audit["4a_agentless_precision"]
    ah = {}
    for part in ("recitals", "articles"):
        p = prec["by_part"][part]
        raw = results["whole_corpus"][part]
        ah[part] = {
            "raw_agentless": raw["agentless"],
            "raw_rate": raw["bearer_deletion_rate"],
            "audit_n": p["n"],
            "audit_precision": p["precision"],
            "audited_agentless_estimate": round(raw["agentless"] * p["precision"]),
            "audited_rate": round(raw["agentless"] * p["precision"] / raw["modal_occurrences"], 4),
        }
    out["3_audited_headline"] = {
        "note": "the per-part precisions rest on 13 and 27 rows.  They are reported because the "
                "over-count is plainly not evenly distributed -- `able`, the single most frequent "
                "recital slot token at 267, is a copula -- and they are not to be read as estimates "
                "with any width worth the name.",
        "by_part": ah,
        "opposite_signs": "the copular over-count (3) shrinks the class; the gapped miss (2) grows "
                          "it.  They are not the same size and they do not cancel; both are reported.",
    }

    # ---------------------------------------------------------------- 4. the sentence that crossed
    act = corpus.get("32021R0241")
    needle = "be encouraged to foster synergies"
    found = []
    if act:
        for part in ("recitals", "articles"):
            for division, text in act[part].items():
                if needle in text:
                    i = text.index(needle)
                    found.append({"part": part, "division": division,
                                  "text": text[max(0, i - 120):i + 160]})
    out["4_the_sentence_that_crossed"] = {
        "celex": "32021R0241",
        "needle": needle,
        "occurrences": found,
        "checked": "found in both halves of the same act" if len(found) >= 2
                   else "NOT confirmed in both halves -- the reading in verdicts.py row 23 is wrong",
    }

    json.dump(out, open(HERE / "residue.json", "w"), indent=1, ensure_ascii=False)

    print("1  modal share  recitals %s" % conf["recitals"]["modal_share"])
    print("               articles %s" % conf["articles"]["modal_share"])
    print("2  gapped B-forms:", gap_counts)
    print("   as a share of the measured agentless class:",
          out["2_gapped"]["share_of_the_measured_agentless_class"])
    print("3  audited headline:")
    for part, d in ah.items():
        print("     %-9s raw %d (%.4f)  x precision %.3f on n=%d  ->  %d (%.4f)"
              % (part, d["raw_agentless"], d["raw_rate"], d["audit_precision"], d["audit_n"],
                 d["audited_agentless_estimate"], d["audited_rate"]))
    print("4  %s -- %d occurrence(s)" % (out["4_the_sentence_that_crossed"]["checked"], len(found)))
    for f in found:
        print("     %-9s %s : ...%s..." % (f["part"], f["division"], f["text"][:150].replace("\n", " ")))


if __name__ == "__main__":
    main()
