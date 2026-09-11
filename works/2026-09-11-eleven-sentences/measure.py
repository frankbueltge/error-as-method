#!/usr/bin/env python3
"""The Named Bearer -- Session 87, 2026-09-11.

Session 86's rule, ported from 63 RFCs to 22 WHATWG living standards, because `S86.CONSTANT` asks
for a third corpus and names this kind of document as one of the four it would accept.  The five
rule literals below are lifted byte for byte from `works/2026-09-10-only-when-capitals/measure.py`;
`verify.py` asserts it before this file is allowed to report anything.

  B-FORM      <modal> (not|never)? be <TOKEN>
  AGENTLESS   a B-FORM with no "by" between the slot token and 200 characters later
  AGENTFUL    a B-FORM with one
  NON-B       every other occurrence of shall / should / must

  NORM        prose the document does not mark as non-normative
  NONNORM     prose inside a note, example, advisement or issue, or inside a section opened by
              "This section is non-normative."

The four deviations from Session 86's pipeline -- the sentence unit, the furniture, the absent
boilerplate rule and the substitution of register for case -- are §2 of PREDICTIONS.md, written
before this file existed.
"""

import gzip
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODALS = ("shall", "should", "must")

# ------------------------------------------------- Session 86's rules, verbatim (verify.py asserts)
MODAL_RE = re.compile(r"\b(shall|should|must)\b", re.IGNORECASE)
B_FORM = re.compile(r"^\s+(?:not\s+|never\s+)?be\s+([A-Za-z][A-Za-z\-]*)", re.IGNORECASE)
BY = re.compile(r"\bby\b", re.IGNORECASE)
AGENT_WINDOW = 200
SENT_SPLIT = re.compile(r"(?<=[.;:])\s+(?=[A-Z(‘'‘“])")

# ------------------------------------------------------------------------------- the port's plumbing
RFC2119_BOILERPLATE = "are to be interpreted as described in"


def sentences(block):
    """D1: a prose block is the paragraph; Session 86's splitter applied to it unchanged."""
    flat = re.sub(r"\s+", " ", block).strip()
    for s in SENT_SPLIT.split(flat):
        s = s.strip()
        if s:
            yield s


def classify(sent, doc, register, marked_by, block_index):
    """Session 86's classify(), with `case` replaced by `register` (PREDICTIONS §2, D4)."""
    rows = []
    for m in MODAL_RE.finditer(sent):
        raw = m.group(1)
        rest = sent[m.end():]
        row = {"doc": doc, "block": block_index, "modal": raw.lower(),
               "register": register, "marked_by": marked_by,
               "sentence": sent, "offset": m.start()}
        b = B_FORM.match(rest)
        if not b:
            row["form"] = "NON-B"
            row["slot_token"] = None
            row["agent"] = None
        else:
            tok = b.group(1).lower()
            window = rest[b.end():][:AGENT_WINDOW]
            row["form"] = "B-FORM"
            row["slot_token"] = tok
            row["agent"] = "AGENTFUL" if BY.search(window) else "AGENTLESS"
        rows.append(row)
    return rows


def rate(a, b):
    return round(a / b, 4) if b else None


def tally(rows):
    n = len(rows)
    b = [r for r in rows if r["form"] == "B-FORM"]
    al = [r for r in b if r["agent"] == "AGENTLESS"]
    return {
        "occurrences": n,
        "b_form": len(b),
        "agentless": len(al),
        "agentful": len(b) - len(al),
        "non_b": n - len(b),
        "b_form_share": rate(len(b), n),
        "bearer_deletion_rate": rate(len(al), n),
        "agent_test": rate(len(al), len(b)) if b else None,
    }


def main():
    corpus = json.load(gzip.open(HERE / "corpus.json.gz", "rt"))

    # ------------------------------------------------------------- calibration, on the INPUT only
    problems = []
    if not corpus:
        problems.append("corpus is empty")
    for key, d in corpus.items():
        if not d.get("title"):
            problems.append("%s has no publisher title" % key)
        if not d.get("blocks"):
            problems.append("%s has no prose blocks" % key)
    if problems:
        print("CALIBRATION FAILED -- measuring nothing:", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        return 1
    print("calibration: %d documents, every one with a publisher title and prose." % len(corpus))

    rows, docs = [], []
    boilerplate_hits = 0
    for key in sorted(corpus):
        d = corpus[key]
        doc_rows = []
        for i, b in enumerate(d["blocks"]):
            if RFC2119_BOILERPLATE in b["t"]:
                boilerplate_hits += 1          # D3: counted, never dropped
            for sent in sentences(b["t"]):
                doc_rows.extend(classify(sent, key, b["r"], b.get("m"), i))
        t = tally(doc_rows)
        t.update({"doc": key, "title": d["title"], "updated": d["updated"], "url": d["url"],
                  "norm": sum(1 for r in doc_rows if r["register"] == "NORM"),
                  "nonnorm": sum(1 for r in doc_rows if r["register"] == "NONNORM")})
        docs.append(t)
        rows.extend(doc_rows)
        print("  %-14s %5d occ   B-FORM %5.1f%%   agent test %s   %s"
              % (key, t["occurrences"], 100 * (t["b_form_share"] or 0), t["agent_test"],
                 (d["title"] or "")[:34]))

    by_register = {r: tally([x for x in rows if x["register"] == r]) for r in ("NORM", "NONNORM")}
    per_modal = {w: tally([x for x in rows if x["modal"] == w]) for w in MODALS}
    per_modal_register = {w: {r: tally([x for x in rows if x["modal"] == w and x["register"] == r])
                              for r in ("NORM", "NONNORM")} for w in MODALS}

    whole = tally(rows)
    whole["modal_mix"] = {w: sum(1 for r in rows if r["modal"] == w) for w in MODALS}
    whole["register_mix"] = {r: sum(1 for x in rows if x["register"] == r)
                             for r in ("NORM", "NONNORM")}
    whole["nonnorm_marked_by"] = dict(Counter(x["marked_by"] for x in rows
                                              if x["register"] == "NONNORM"))

    slot = Counter(r["slot_token"] for r in rows if r["slot_token"])
    slot_by_register = defaultdict(Counter)
    for r in rows:
        if r["slot_token"]:
            slot_by_register[r["register"]][r["slot_token"]] += 1

    results = {
        "session": 87, "date": "2026-09-11",
        "corpus": "22 WHATWG living standards served to this session on 2026-09-11; harvest.py",
        "modals": MODALS, "agent_window_chars": AGENT_WINDOW,
        "rfc2119_boilerplate_blocks": boilerplate_hits,
        "whole_corpus": whole,
        "by_register": by_register,
        "per_modal": per_modal,
        "per_modal_register": per_modal_register,
        "prior_corpora": {
            "source": "works/2026-09-10-only-when-capitals/decomposition.json",
            "EU_all": {"occurrences": 22554, "b_form_share": 0.3545, "agent_test": 0.8095,
                       "rate": 0.2870},
            "EU_recitals": {"occurrences": 6942, "b_form_share": 0.4657, "agent_test": 0.8067,
                            "rate": 0.3757},
            "EU_articles": {"occurrences": 15612, "b_form_share": 0.3062, "agent_test": 0.8109,
                            "rate": 0.2475},
            "RFC_all": {"occurrences": 2952, "b_form_share": 0.4468, "agent_test": 0.9022,
                        "rate": 0.4031},
            "RFC_upper": {"occurrences": 2360, "b_form_share": 0.4449, "agent_test": 0.9105,
                          "rate": 0.4051},
            "RFC_lower": {"occurrences": 581, "b_form_share": 0.4544, "agent_test": 0.8674,
                          "rate": 0.3941},
        },
        "documents": docs,
    }
    (HERE / "results.json").write_text(json.dumps(results, indent=1) + "\n")
    (HERE / "slot-tokens.json").write_text(json.dumps(
        {"note": "every token that landed in the '<modal> be ___' slot, unfiltered. The rejection "
                 "log: nothing here was chosen by me.",
         "total_distinct": len(slot),
         "all": dict(slot.most_common()),
         "by_register": {k: dict(v.most_common()) for k, v in slot_by_register.items()}},
        indent=1) + "\n")
    with gzip.open(HERE / "occurrences.json.gz", "wt") as fh:
        json.dump(rows, fh)

    print("\n%d occurrences  |  NORM %d  NONNORM %d  (%s)"
          % (whole["occurrences"], whole["register_mix"]["NORM"],
             whole["register_mix"]["NONNORM"], whole["nonnorm_marked_by"]))
    print("modal mix: %s" % whole["modal_mix"])
    print("B-FORM share %.4f   agent test %.4f   bearer-deletion rate %.4f"
          % (whole["b_form_share"], whole["agent_test"], whole["bearer_deletion_rate"]))
    for r in ("NORM", "NONNORM"):
        t = by_register[r]
        print("  %-8s %5d occ   B-FORM %s   agent test %s   rate %s"
              % (r, t["occurrences"], t["b_form_share"], t["agent_test"],
                 t["bearer_deletion_rate"]))
    print("blocks carrying the RFC 2119 boilerplate string: %d" % boilerplate_hits)
    return 0


if __name__ == "__main__":
    sys.exit(main())
