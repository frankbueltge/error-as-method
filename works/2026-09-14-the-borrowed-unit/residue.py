#!/usr/bin/env python3
"""residue.py -- four descriptions, computed AFTER the predictions were scored.

Nothing below is a result.  Each is a description written to explain a loss or to say what the
numbers ride on, and each is marked as such wherever it appears, because a quantity computed after
seeing the answer is not evidence for the answer.

  (a) how deserted each tradition's agentless residue is -- the share of its binding B-FORM
      obligations that delete the bearer.  Offered as the mechanism behind P4's loss, as CONJECTURE.
  (b) which strings actually carry the nearest match, per tradition -- the rejection log.
  (c) how wide, in rows, the EU extension is.
  (d) how many window-0 hits are terms standing AFTER the obligation in its own block
      -- a defect inherited from Session 88's scan, kept so the replication holds,
      measured rather than repaired.

Run after score.py.  Writes residue.json.
"""

import bisect
import gzip
import json
import re
from collections import Counter
from pathlib import Path

import corpora
import reach

HERE = Path(__file__).resolve().parent

REGISTER = {
    "whatwg": (corpora.S87, lambda x: x["register"] == "NORM"),
    "eu": (corpora.S84, lambda x: x["part"] == "articles"),
    "rfc": (corpora.S86, lambda x: x["case"] == "UPPER"),
}


def deserted():
    out = {}
    for name, (src, in_register) in REGISTER.items():
        occ = json.load(gzip.open(src / "occurrences.json.gz"))
        binding = [x for x in occ if in_register(x)]
        bform = [x for x in binding if x["form"] == "B-FORM"]
        agentless = [x for x in bform if x["agent"] == "AGENTLESS"]
        out[name] = {
            "occurrences_in_the_binding_register": len(binding),
            "of_them_B_FORM": len(bform),
            "of_those_AGENTLESS": len(agentless),
            "bearer_deletion_rate_within_B_FORM": round(100.0 * len(agentless) / len(bform), 2),
            "B_FORM_share_of_the_binding_register": round(100.0 * len(bform) / len(binding), 2),
        }
    return out


def carriers():
    """Which string is the nearest party term, per row, in words."""
    base = corpora.base_terms()
    out = {}
    for name in ("whatwg", "eu", "rfc"):
        terms = base + reach.EXTENSIONS[name]
        rows, blocks = corpora.CORPORA[name]()
        party = re.compile(reach.term_pattern(terms), re.IGNORECASE)
        tally = Counter()
        for doc, seq in blocks.items():
            text = reach.SEP.join(seq)
            starts, off = [], 0
            for t in seq:
                starts.append(off)
                off += len(t) + len(reach.SEP)
            ms = [(m.end(), m.group(1).lower()) for m in party.finditer(text)]
            ends = [e for e, _ in ms]
            for r in rows:
                if r["doc"] != doc:
                    continue
                blk = seq[r["block"]]
                pos = starts[r["block"]] + blk.find(r["sentence"]) + r["offset"]
                j = bisect.bisect_right(ends, pos)
                tally[ms[j - 1][1] if j else "(none anywhere)"] += 1
        out[name] = dict(tally.most_common())
    return out


def forwards_only():
    """How many window-0 hits are terms standing AFTER the obligation in its own block.

    Session 88's block scan tests the whole of the obligation's own block, so a party term that
    stands later in the same block counts as "in reach" at window 0.  In a 36-word Bikeshed
    paragraph that is a distinction without a difference.  In a 400-word EU article it is not.  The
    scan is kept exactly as Session 88 wrote it -- the replication in verify.py passes cell for
    cell because of that -- and the cost is measured here instead of being repaired silently.
    """
    base = corpora.base_terms()
    out = {}
    for name in ("whatwg", "eu", "rfc"):
        party = re.compile(reach.term_pattern(base + reach.EXTENSIONS[name]), re.IGNORECASE)
        rows, blocks = corpora.CORPORA[name]()
        at0 = fwd = 0
        for r in rows:
            blk = blocks[r["doc"]][r["block"]]
            if not party.search(blk):
                continue
            at0 += 1
            pos = blk.find(r["sentence"]) + r["offset"]
            if not any(m.end() <= pos for m in party.finditer(blk)):
                fwd += 1
        out[name] = {"window_0_hits": at0, "of_them_only_after_the_obligation": fwd,
                     "share": round(100.0 * fwd / at0, 2) if at0 else None}
    return out


def main():
    base = corpora.base_terms()
    res = json.load(open(HERE / "results.json"))

    eu_row = res["corpora"]["eu"]["row"]["blocks"]
    eu_base = res["corpora"]["eu"]["base"]["blocks"]
    out = {
        "note": "descriptions, computed after the predictions were scored. Not results, and marked "
                "as such wherever they are used.",
        "a_how_deserted_the_residue_is": {
            "why": "P4 lost: the RFC series, the archetype of drafting around a named addressee, "
                   "keeps its parties FURTHEST from its agentless obligations. CONJECTURE offered "
                   "as the mechanism: where a tradition names the addressee as the subject, the "
                   "obligations that remain agentless are the ones it had no addressee for.",
            "status": "CONJECTURE -- these numbers describe the populations, they do not test it",
            "by_corpus": deserted(),
        },
        "b_which_strings_carry_the_nearest_match": {
            "why": "the rejection log: every term that is ever the nearest one, with its count, "
                   "unfiltered, so a reader can see what the instrument is actually finding.",
            "by_corpus": carriers(),
        },
        "d_window_0_hits_that_stand_after_the_obligation": {
            "why": "Session 88's block scan searches the obligation's own block whole, forwards as "
                   "well as backwards. Kept unaltered so the replication holds; measured here so "
                   "the cost is on the record rather than in the method.",
            "by_corpus": forwards_only(),
        },
        "c_how_wide_the_EU_extension_is": {
            "why": "P5 lost. On the base list alone EU comes in at %.2f %%, below the 13.6 %% that "
                   "would falsify S88.REACH; with the two terms the row itself named it comes in "
                   "at %.2f %%." % (eu_base["pct"]["0"], eu_row["pct"]["0"]),
            "block_window_0_rows_row_list": eu_row["counts"]["0"],
            "block_window_0_rows_base_list": eu_base["counts"]["0"],
            "rows_the_two_strings_add": eu_row["counts"]["0"] - eu_base["counts"]["0"],
            "population": eu_row["population"],
            "points_added": round(eu_row["pct"]["0"] - eu_base["pct"]["0"], 2),
            "base_terms_in_the_common_list": len(base),
            "terms_added": len(reach.EXTENSIONS["eu"]),
        },
    }
    (HERE / "residue.json").write_text(json.dumps(out, indent=1) + "\n")

    print("(a) bearer deletion within B-FORM, binding register only:")
    for k, v in out["a_how_deserted_the_residue_is"]["by_corpus"].items():
        print("    %-7s %5.2f %%  (%d of %d B-FORM; B-FORM is %.2f %% of the register)"
              % (k, v["bearer_deletion_rate_within_B_FORM"], v["of_those_AGENTLESS"],
                 v["of_them_B_FORM"], v["B_FORM_share_of_the_binding_register"]))
    print("\n(b) top nearest-term carriers:")
    for k, v in out["b_which_strings_carry_the_nearest_match"]["by_corpus"].items():
        print("    %-7s %s" % (k, list(v.items())[:6]))
    print("\n(d) window-0 hits whose only party term stands AFTER the obligation:")
    for k, v in out["d_window_0_hits_that_stand_after_the_obligation"]["by_corpus"].items():
        print("    %-7s %5d of %5d  (%.2f %%)" % (k, v["of_them_only_after_the_obligation"],
                                                  v["window_0_hits"], v["share"]))
    c = out["c_how_wide_the_EU_extension_is"]
    print("\n(c) EU block window 0: %d rows on the base list, %d with the two added terms "
          "(+%d rows, +%.2f points)"
          % (c["block_window_0_rows_base_list"], c["block_window_0_rows_row_list"],
             c["rows_the_two_strings_add"], c["points_added"]))


if __name__ == "__main__":
    main()
