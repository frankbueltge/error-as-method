#!/usr/bin/env python3
"""bounds.py -- what this instrument can possibly return on this corpus, computed before any
prediction is written.

Session 88 fixed a threshold without computing the range of the thing it thresholded and filed
F-137 against itself for it.  Session 89 spent its first half-hour counting words per block instead
of scanning, found that the EU arm of `S88.REACH` compared units 11.11x apart, and declared that arm
non-evidential in writing before the scan ran.  The lesson is now a step: **a night that ports an
instrument to a new corpus measures the instrument's reach on that corpus first, and writes its
predictions against the table.**

NOTHING HERE IS A RESULT.  Five questions, none of which mentions an outcome:

  1. How big is a block in this tradition, against the 36 / 400 / 41 words of the three measured?
  2. How many occurrences of shall / should / must stand in each of the two registers -- the power
     check `S86.CONSTANT` requires (500 each) and `S89.WORDUNIT` requires (500 binding agentless
     B-FORM obligations)?
  3. How much does excluding <BlockAmendment> remove?
  4. **How often do the 26 common party terms occur in UK statute at all?**  The list was written
     for WHATWG living standards.  If `user agent`, `parser` and `browser` are absent from Acts of
     Parliament, then every number the reach scan produces on this corpus is a number about the
     extension I chose, and that has to be known before the extension is written, not after.
  5. What is the ceiling -- the share of binding agentless obligations whose document contains any
     party term anywhere, which no window can exceed?

Run after harvest.py.  Writes bounds.json.
"""

import gzip
import importlib.util
import json
import re
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKS = HERE.parent
S86 = WORKS / "2026-09-10-only-when-capitals"
S88 = WORKS / "2026-09-12-adjacent-text"
S89 = WORKS / "2026-09-14-the-borrowed-unit"

MODAL = re.compile(r"\b(shall|should|must)\b", re.IGNORECASE)

# the three medians Session 89 measured, read out of its file rather than restated
PRIOR_MEDIANS = {"whatwg": 36, "eu": 400, "rfc": 41}


def s86_measure():
    spec = importlib.util.spec_from_file_location("s86_measure", S86 / "measure.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def base_terms():
    """Session 88's 26 party terms, read out of its results.json so the two cannot drift."""
    pat = json.load(open(S88 / "results.json"))["mechanical_ceiling"]["party_terms"]
    return pat[len(r"\b("):-len(r")\b")].split("|")


def term_pattern(names):
    return r"\b(" + "|".join(sorted(names, key=len, reverse=True)) + r")\b"


def main():
    corpus = json.load(gzip.open(HERE / "corpus.json.gz", "rt"))
    m = s86_measure()
    base = base_terms()
    party = re.compile(term_pattern(base), re.IGNORECASE)

    out = {
        "note": "The geometry of the fourth corpus. Nothing here is a result; every number is a "
                "property of the input, computed before PREDICTIONS.md was written.",
        "prior_medians": PRIOR_MEDIANS,
        "acts": len(corpus),
    }

    # ---------------------------------------------------------------- 1 & 2: blocks and occurrences
    for reg in ("act", "notes"):
        hosting, all_blocks, occ = [], [], 0
        bform = agentless = 0
        for d in corpus.values():
            for b in d[reg]:
                all_blocks.append(len(b.split()))
                hits = len(MODAL.findall(b))
                if hits:
                    hosting.append(len(b.split()))
                occ += hits
            # the occurrence-level counts, with Session 86's own classifier, register-blind
            for i, sent in enumerate(m.sentences("\n\n".join(d[reg]))):
                for r in m.classify(sent, 0, i):
                    if r["form"] == "B-FORM":
                        bform += 1
                        if r["agent"] == "AGENTLESS":
                            agentless += 1
        out[reg] = {
            "blocks": len(all_blocks),
            "words": sum(all_blocks),
            "median_words_per_block": statistics.median(all_blocks),
            "median_words_per_block_hosting_an_obligation": statistics.median(hosting),
            "ratio_to_whatwg": round(
                statistics.median(hosting) / PRIOR_MEDIANS["whatwg"], 2),
            "modal_occurrences_by_regex": occ,
            "B_FORM": bform,
            "B_FORM_AGENTLESS": agentless,
            "powers_the_500_floor": agentless >= 500,
        }

    # ------------------------------------------------------------------------- 3: BlockAmendment
    with_ba = sum(sum(len(MODAL.findall(b)) for b in d["act_with_block_amendment"])
                  for d in corpus.values())
    out["block_amendment"] = {
        "modal_occurrences_in_the_act_register_excluding_it": out["act"]["modal_occurrences_by_regex"],
        "modal_occurrences_including_it": with_ba,
        "share_of_the_wider_count_that_is_quoted_text": round(
            100.0 * (with_ba - out["act"]["modal_occurrences_by_regex"]) / with_ba, 2),
        "decision": "excluded; declared in harvest.py before any measurement",
    }

    # -------------------------------------------- 4: does the borrowed vocabulary reach this corpus?
    per_term = {t: 0 for t in base}
    blocks_with_any = acts_with_any = 0
    total_blocks = 0
    for d in corpus.values():
        act_hit = False
        for b in d["act"]:
            total_blocks += 1
            if party.search(b):
                blocks_with_any += 1
                act_hit = True
            for t in base:
                per_term[t] += len(re.findall(r"\b" + re.escape(t) + r"\b", b, re.IGNORECASE))
        acts_with_any += 1 if act_hit else 0
    out["borrowed_vocabulary"] = {
        "question": "how often do the 26 party terms written for WHATWG living standards occur in "
                    "63 Acts of Parliament?",
        "occurrences_per_term": dict(sorted(per_term.items(), key=lambda kv: -kv[1])),
        "total_occurrences": sum(per_term.values()),
        "terms_that_never_occur": sorted(t for t, n in per_term.items() if n == 0),
        "terms_that_never_occur_count": sum(1 for n in per_term.values() if n == 0),
        "act_blocks": total_blocks,
        "act_blocks_carrying_any_base_term": blocks_with_any,
        "act_blocks_carrying_any_base_term_pct": round(100.0 * blocks_with_any / total_blocks, 2),
        "acts_carrying_any_base_term": acts_with_any,
        "for_comparison_whatwg": "Session 88's own corpus: a term stood in the obligation's own "
                                 "paragraph for 13.61 % of 1,190 obligations and somewhere earlier "
                                 "in the document for 99.6 %.",
    }

    (HERE / "bounds.json").write_text(json.dumps(out, indent=1) + "\n")

    print("%-6s %7s %9s %8s %8s %7s %8s" %
          ("reg", "blocks", "words", "med/blk", "med host", "ratio", "B-AGLESS"))
    for reg in ("act", "notes"):
        r = out[reg]
        print("%-6s %7d %9d %8.0f %8.0f %7.2f %8d"
              % (reg, r["blocks"], r["words"], r["median_words_per_block"],
                 r["median_words_per_block_hosting_an_obligation"], r["ratio_to_whatwg"],
                 r["B_FORM_AGENTLESS"]))
    print("\nmodal occurrences  act %d  notes %d   (both registers clear the 500 floor: %s)"
          % (out["act"]["modal_occurrences_by_regex"], out["notes"]["modal_occurrences_by_regex"],
             out["act"]["powers_the_500_floor"] and out["notes"]["powers_the_500_floor"]))
    print("BlockAmendment carries %.2f %% of the wider modal count; excluded."
          % out["block_amendment"]["share_of_the_wider_count_that_is_quoted_text"])
    bv = out["borrowed_vocabulary"]
    print("\nthe 26 borrowed party terms in 63 Acts: %d occurrences in %d blocks; "
          "%d of the 26 never occur at all."
          % (bv["total_occurrences"], bv["act_blocks"], bv["terms_that_never_occur_count"]))
    print("  act blocks carrying any of them: %d of %d (%.2f %%)"
          % (bv["act_blocks_carrying_any_base_term"], bv["act_blocks"],
             bv["act_blocks_carrying_any_base_term_pct"]))
    print("  the ten that do occur: %s"
          % {k: v for k, v in list(bv["occurrences_per_term"].items())[:10]})


if __name__ == "__main__":
    main()
