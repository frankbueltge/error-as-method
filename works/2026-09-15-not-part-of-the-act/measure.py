#!/usr/bin/env python3
"""measure.py -- Session 86's rule, unchanged, over an Act of Parliament and its Explanatory Notes.

The rule is imported from `works/2026-09-10-only-when-capitals/measure.py`, never copied, so it
cannot drift; `verify.py` asserts the five literals that constitute it are byte-identical to what
Session 86 published and what Sessions 87 and 89 ported.

  B-FORM      <modal> (not|never)? be <TOKEN>
  AGENTLESS   a B-FORM with no "by" between the slot token and the sentence end (max 200 chars)
  AGENTFUL    a B-FORM with one
  NON-B       every other occurrence of shall / should / must

  ACT         the Act itself, excluding <BlockAmendment> -- the binding register
  NOTES       the Explanatory Notes, which say "They do not form part of the Act" -- the register
              that declares itself non-binding, and the two-speaking-register corpus
              `S86.CONSTANT` has been open for since Session 87

Sentences are split inside each block, with Session 86's own `SENT_SPLIT`, on text Session 86's own
`sentences()` would have produced -- a block is already a flattened paragraph, so the two routes are
identical and `verify.py` checks that they are, by count, rather than assuming it.

Everything scored here is fixed in PREDICTIONS.md, written before this file existed.

Run after bounds.py.  Writes occurrences.json.gz and results.json.
"""

import gzip
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
S86 = HERE.parent / "2026-09-10-only-when-capitals"
REGISTERS = ("act", "notes")


def s86():
    spec = importlib.util.spec_from_file_location("s86_measure", S86 / "measure.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def occurrences(corpus, m):
    rows = []
    for key in sorted(corpus, key=lambda k: (corpus[k]["year"], corpus[k]["number"])):
        d = corpus[key]
        for reg in REGISTERS:
            for bi, block in enumerate(d[reg]):
                flat = re.sub(r"\s+", " ", block).strip()
                if not flat:
                    continue
                for sent in m.SENT_SPLIT.split(flat):
                    sent = sent.strip()
                    if not sent:
                        continue
                    for r in m.classify(sent, key, bi):
                        r["act"] = r.pop("rfc")
                        r["block"] = r.pop("para")
                        r["register"] = "ACT" if reg == "act" else "NOTES"
                        rows.append(r)
    return rows


def main():
    corpus = json.load(gzip.open(HERE / "corpus.json.gz", "rt"))
    m = s86()

    # ------------------------------------------------- calibration, on the INPUT only, before counting
    problems = []
    if len(corpus) != 63:
        problems.append("corpus holds %d Acts, expected 63" % len(corpus))
    for k, d in corpus.items():
        if "do not form part of the Act" not in " ".join(d["notes"]):
            problems.append("%s: notes carry no self-declaration" % k)
        if not d["act"] or not d["notes"]:
            problems.append("%s: an empty register" % k)
        if not d["title"]:
            problems.append("%s: no title" % k)
    if problems:
        raise SystemExit("CALIBRATION FAILED -- measuring nothing:\n  " + "\n  ".join(problems))
    print("calibration: 63 Acts, every one with both registers, a title, and the declaration.")

    rows = occurrences(corpus, m)

    def tally(sel):
        n = len(sel)
        b = [r for r in sel if r["form"] == "B-FORM"]
        al = [r for r in b if r["agent"] == "AGENTLESS"]
        return {
            "occurrences": n,
            "b_form": len(b),
            "agentless": len(al),
            "agentful": len(b) - len(al),
            "non_b": n - len(b),
            # the two factors of Session 86's decomposition
            "B_FORM_share_pct": round(100.0 * len(b) / n, 2) if n else None,
            "agent_test": round(len(al) / len(b), 4) if b else None,
            "agent_test_pct": round(100.0 * len(al) / len(b), 2) if b else None,
            # the headline Session 84 published
            "bearer_deletion_rate_pct": round(100.0 * len(al) / n, 2) if n else None,
        }

    by_register = {reg: tally([r for r in rows if r["register"] == reg]) for reg in ("ACT", "NOTES")}
    whole = tally(rows)
    whole["modal_mix"] = {w: sum(1 for r in rows if r["modal"] == w) for w in m.MODALS}
    whole["register_mix"] = {reg: by_register[reg]["occurrences"] for reg in ("ACT", "NOTES")}

    spread = {
        "agent_test_points": round(abs(by_register["ACT"]["agent_test_pct"]
                                       - by_register["NOTES"]["agent_test_pct"]), 2),
        "B_FORM_share_points": round(abs(by_register["ACT"]["B_FORM_share_pct"]
                                         - by_register["NOTES"]["B_FORM_share_pct"]), 2),
    }
    spread["the_other_factor_moves_more"] = \
        spread["B_FORM_share_points"] > spread["agent_test_points"]

    per_modal = {w: {reg: tally([r for r in rows if r["modal"] == w and r["register"] == reg])
                     for reg in ("ACT", "NOTES")} for w in m.MODALS}

    # the rejection log: every token that landed in the slot, unfiltered
    slot = Counter(r["slot_token"] for r in rows if r["slot_token"])
    slot_by_reg = {reg: Counter(r["slot_token"] for r in rows
                                if r["slot_token"] and r["register"] == reg)
                   for reg in ("ACT", "NOTES")}

    results = {
        "session": 90, "date": "2026-09-15",
        "corpus": "63 UK Public General Acts of 2012-2014 and their Explanatory Notes, CLML XML "
                  "from legislation.gov.uk; harvest.py, harvest-log.json, sources/MANIFEST.json",
        "rule": "Session 86's, imported from works/2026-09-10-only-when-capitals/measure.py and "
                "asserted byte-identical by verify.py",
        "registers": {
            "ACT": "the Act, excluding <BlockAmendment>; binding, and not in question",
            "NOTES": "the Explanatory Notes, which declare 'They do not form part of the Act and "
                     "have not been endorsed by Parliament'",
        },
        "modals": m.MODALS, "agent_window_chars": m.AGENT_WINDOW,
        "whole_corpus": whole,
        "by_register": by_register,
        "register_spread": spread,
        "per_modal_register": per_modal,
        "prior_agent_tests": {"eu": 0.8095, "rfc": 0.9022, "whatwg": 0.9010,
                              "source": "S86.CONSTANT's row and Session 87's port"},
        "prior_bearer_deletion": {"eu_recitals_pct": 37.57, "eu_articles_pct": 24.75,
                                  "source": "works/2026-09-08-no-one-to-bear-it/results.json"},
        "acts": [{"act": k, "year": d["year"], "number": d["number"], "title": d["title"],
                  **{reg: tally([r for r in rows
                                 if r["act"] == k and r["register"] == reg.upper()])
                     for reg in ("act", "notes")}}
                 for k, d in sorted(corpus.items(), key=lambda kv: (kv[1]["year"], kv[1]["number"]))],
    }
    (HERE / "results.json").write_text(json.dumps(results, indent=1) + "\n")
    (HERE / "slot-tokens.json").write_text(json.dumps({
        "note": "every token that landed in the '<modal> be ___' slot, unfiltered. The rejection "
                "log: nothing here was chosen by me.",
        "total_distinct": len(slot), "all": dict(slot.most_common()),
        "by_register": {k: dict(v.most_common()) for k, v in slot_by_reg.items()}}, indent=1) + "\n")
    with gzip.open(HERE / "occurrences.json.gz", "wt") as fh:
        json.dump(rows, fh)

    print("\n%-7s %8s %8s %9s %11s %11s %13s"
          % ("reg", "occ", "B-FORM", "agentless", "B-FORM %", "agent test", "bearer del %"))
    for reg in ("ACT", "NOTES"):
        t = by_register[reg]
        print("%-7s %8d %8d %9d %11.2f %11.4f %13.2f"
              % (reg, t["occurrences"], t["b_form"], t["agentless"],
                 t["B_FORM_share_pct"], t["agent_test"], t["bearer_deletion_rate_pct"]))
    t = whole
    print("%-7s %8d %8d %9d %11.2f %11.4f %13.2f"
          % ("WHOLE", t["occurrences"], t["b_form"], t["agentless"],
             t["B_FORM_share_pct"], t["agent_test"], t["bearer_deletion_rate_pct"]))
    print("\nregister spread: agent test %.2f points, B-FORM share %.2f points -- "
          "the other factor moves more: %s"
          % (spread["agent_test_points"], spread["B_FORM_share_points"],
             spread["the_other_factor_moves_more"]))


if __name__ == "__main__":
    main()
