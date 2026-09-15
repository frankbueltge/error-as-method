#!/usr/bin/env python3
"""verify.py -- the warrant. A port that cannot reproduce what it ports is measuring something else.

Four checks, all of which must pass before any number in this work is read as a result.

  1. THE RULE IS THE SAME RULE.  The five literals that constitute Session 86's classifier are
     asserted byte-identical to the strings Session 86 published and Sessions 87 and 89 ported.
     The rule is imported, never copied, so this check is against drift in the source itself.

  2. THE SCAN IS THE SAME SCAN.  `reach.py`'s own `scan` and `curve` are run over Session 87's 22
     WHATWG living standards, through Session 89's own corpus loader, and every cell of Session 89's
     published WHATWG curve -- twelve block windows and thirteen word windows, plus the median --
     must come back identical.  This is the only thing that licenses tonight's numbers: the
     instrument reproduces a published result on a corpus it did not gather.

  3. THE TWO SENTENCE ROUTES AGREE.  `measure.py` splits sentences inside each block rather than
     calling Session 86's `sentences()` on the joined text, and claims the two are identical because
     a block is already a flattened paragraph. Checked by count over the whole corpus, not assumed.

  4. EVERY OCCURRENCE IS WHERE IT SAYS IT IS.  For all 8,795 rows, the stored sentence must occur in
     the block the row points at, in the register the row names.

Writes verification.json.  Exits non-zero on any failure.
"""

import gzip
import importlib.util
import json
import re
import sys
from pathlib import Path

import reach

HERE = Path(__file__).resolve().parent
WORKS = HERE.parent
S86 = WORKS / "2026-09-10-only-when-capitals"
S87 = WORKS / "2026-09-11-eleven-sentences"
S89 = WORKS / "2026-09-14-the-borrowed-unit"

# Session 86's rule, as published. Byte strings, not descriptions.
EXPECTED = {
    "MODAL_RE": r"\b(shall|should|must)\b",
    "B_FORM": r"^\s+(?:not\s+|never\s+)?be\s+([A-Za-z][A-Za-z\-]*)",
    "BY": r"\bby\b",
    "SENT_SPLIT": "(?<=[.;:])\\s+(?=[A-Z(‘'‘“])",
    "AGENT_WINDOW": 200,
}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.pop(0)
    return mod


def check_rule(m):
    got = {"MODAL_RE": m.MODAL_RE.pattern, "B_FORM": m.B_FORM.pattern, "BY": m.BY.pattern,
           "SENT_SPLIT": m.SENT_SPLIT.pattern, "AGENT_WINDOW": m.AGENT_WINDOW}
    bad = {k: {"expected": EXPECTED[k], "found": got[k]} for k in EXPECTED if got[k] != EXPECTED[k]}
    return {"literals_checked": len(EXPECTED), "identical": not bad, "mismatches": bad}


def check_scan():
    """Reproduce Session 89's published WHATWG curve with this work's own scan and curve."""
    corpora = load(S89 / "corpora.py", "s89_corpora")
    rows, blks = corpora.whatwg()
    terms = corpora.base_terms()                     # S89's extension for whatwg is []
    bd, wd, _dup, _c = reach.scan(rows, blks, terms)
    mine = {"blocks": reach.curve(bd, reach.BLOCK_WINDOWS, len(rows)),
            "words": reach.curve(wd, reach.WORD_WINDOWS, len(rows))}
    theirs = json.load(open(S89 / "results.json"))["corpora"]["whatwg"]["row"]

    cells, mismatches = 0, []
    for unit, windows in (("blocks", reach.BLOCK_WINDOWS), ("words", reach.WORD_WINDOWS)):
        for w in windows:
            cells += 1
            a, b = mine[unit]["pct"][str(w)], theirs[unit]["pct"][str(w)]
            if a != b:
                mismatches.append({"unit": unit, "window": w, "mine": a, "published": b})
        for field in ("population", "whole_document", "none_anywhere", "median_where_present"):
            cells += 1
            if mine[unit][field] != theirs[unit][field]:
                mismatches.append({"unit": unit, "field": field,
                                   "mine": mine[unit][field], "published": theirs[unit][field]})
    return {"corpus": "Session 87's 22 WHATWG living standards, through Session 89's own loader",
            "cells_compared": cells, "identical": not mismatches, "mismatches": mismatches,
            "reproduced_block_window_0_pct": mine["blocks"]["pct"]["0"],
            "reproduced_word_window_36_pct": mine["words"]["pct"]["36"],
            "reproduced_median_word_distance": mine["words"]["median_where_present"]}


def check_sentence_routes(m, corpus):
    per_block, joined = 0, 0
    for d in corpus.values():
        for reg in ("act", "notes"):
            for block in d[reg]:
                flat = re.sub(r"\s+", " ", block).strip()
                if not flat:
                    continue
                per_block += sum(1 for s in m.SENT_SPLIT.split(flat) if s.strip())
            joined += sum(1 for _ in m.sentences("\n\n".join(d[reg])))
    return {"sentences_split_inside_each_block": per_block,
            "sentences_from_session_86_s_own_sentences_on_the_joined_text": joined,
            "identical": per_block == joined}


def check_placement(corpus):
    occ = json.load(gzip.open(HERE / "occurrences.json.gz"))
    bad = 0
    for x in occ:
        reg = "act" if x["register"] == "ACT" else "notes"
        block = corpus[x["act"]][reg][x["block"]]
        if x["sentence"] not in re.sub(r"\s+", " ", block).strip():
            bad += 1
    return {"rows": len(occ), "rows_whose_sentence_is_not_in_its_block": bad, "identical": bad == 0}


def main():
    m = load(S86 / "measure.py", "s86_measure")
    corpus = json.load(gzip.open(HERE / "corpus.json.gz", "rt"))

    out = {
        "note": "The four checks a port owes. Every number in this work is void unless all four pass.",
        "1_the_rule_is_the_same_rule": check_rule(m),
        "2_the_scan_reproduces_session_89_s_published_whatwg_curve": check_scan(),
        "3_the_two_sentence_routes_agree": check_sentence_routes(m, corpus),
        "4_every_occurrence_is_where_it_says_it_is": check_placement(corpus),
    }
    ok = all(v["identical"] for k, v in out.items() if k != "note")
    out["all_four_pass"] = ok
    (HERE / "verification.json").write_text(json.dumps(out, indent=1) + "\n")

    for k, v in out.items():
        if k == "note" or k == "all_four_pass":
            continue
        print("%-58s %s" % (k[:58], "OK" if v["identical"] else "FAILED"))
    s = out["2_the_scan_reproduces_session_89_s_published_whatwg_curve"]
    print("  (%d cells compared; block w0 %.2f %%, word w36 %.2f %%, median %s)"
          % (s["cells_compared"], s["reproduced_block_window_0_pct"],
             s["reproduced_word_window_36_pct"], s["reproduced_median_word_distance"]))
    if not ok:
        sys.exit("VERIFICATION FAILED -- nothing in this work is a result.")


if __name__ == "__main__":
    main()
