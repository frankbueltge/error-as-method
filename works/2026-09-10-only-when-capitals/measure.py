#!/usr/bin/env python3
"""Only When They Appear in All Capitals -- Session 86, 2026-09-10.

Session 84's rule, ported from 63 EU legal acts to 63 RFCs, to find out whether that night measured
drafting or measured English.  The rule is unchanged; what changes is the corpus and one variable:

  B-FORM      <modal> (not|never)? be <TOKEN>
  AGENTLESS   a B-FORM with no "by" between the slot token and the sentence end (max 200 chars)
  AGENTFUL    a B-FORM with one
  NON-B       every other occurrence of shall / should / must

  UPPER       the token is all capitals -- normative, by RFC 8174 and by the document's own boilerplate
  LOWER       the token is all lower case -- ordinary English, by the same
  MIXED       anything else ("Must" at a sentence head); reported, never merged into either side

Everything here is fixed in PREDICTIONS.md, written before this file existed.  The three deviations
from Session 84's pipeline (page furniture, the newline, the boilerplate) are §2 of that file.  The
one repair -- the one-token gap rule -- runs beside the strict rule and publishes its own rejection
log; it scores P4 and nothing else.
"""

import gzip
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODALS = ("shall", "should", "must")

# ------------------------------------------------------------------- Session 84's rules, verbatim
MODAL_RE = re.compile(r"\b(shall|should|must)\b", re.IGNORECASE)
B_FORM = re.compile(r"^\s+(?:not\s+|never\s+)?be\s+([A-Za-z][A-Za-z\-]*)", re.IGNORECASE)
BY = re.compile(r"\bby\b", re.IGNORECASE)
AGENT_WINDOW = 200
SENT_SPLIT = re.compile(r"(?<=[.;:])\s+(?=[A-Z(‘'‘“])")     # the \n+ branch removed: PREDICTIONS §2.2

# --------------------------------------------------------------------------- the one-token gap rule
GAP_FORM = re.compile(r"^\s+(?:not\s+|never\s+)?([A-Za-z][A-Za-z\-']*)\s+be\s+([A-Za-z][A-Za-z\-]*)",
                      re.IGNORECASE)

# ------------------------------------------------------------------------------- the port's plumbing
PAGE_FOOTER = re.compile(r"^.*\[Page \d+\]\s*$")
RUNNING_HEAD = re.compile(r"^RFC \d+\s+.*\b(19|20)\d{2}\s*$")
FORMFEED = "\x0c"
BOILERPLATE = ("appear in all capitals", "are to be interpreted as described in")


def defurniture(text):
    """Strip page breaks, footers and running headers.  Returns (text, lines_removed)."""
    out, removed = [], 0
    for line in text.split("\n"):
        bare = line.replace(FORMFEED, "").rstrip()
        if FORMFEED in line or PAGE_FOOTER.match(bare) or RUNNING_HEAD.match(bare):
            if bare.strip():
                removed += 1
            out.append("")            # a page break is a paragraph break, never a join
            continue
        out.append(line)
    return "\n".join(out), removed


def sentences(text):
    """Paragraph on a blank line; single newlines are line-wraps; then Session 84's splitter."""
    for para in re.split(r"\n\s*\n", text):
        flat = re.sub(r"\s+", " ", para).strip()
        if not flat:
            continue
        for s in SENT_SPLIT.split(flat):
            s = s.strip()
            if s:
                yield s


def case_of(tok):
    if tok.isupper():
        return "UPPER"
    if tok.islower():
        return "LOWER"
    return "MIXED"


def classify(sent, rfc, para_index):
    rows = []
    for m in MODAL_RE.finditer(sent):
        raw = m.group(1)
        rest = sent[m.end():]
        row = {"rfc": rfc, "para": para_index, "modal": raw.lower(), "case": case_of(raw),
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
        # the gap rule, computed for every occurrence, used only where PREDICTIONS says
        g = GAP_FORM.match(rest) if not b else None
        if g:
            gtok, stok = g.group(1).lower(), g.group(2).lower()
            gwindow = rest[g.end():][:AGENT_WINDOW]
            row["gap_token"] = gtok
            row["gap_slot_token"] = stok
            row["gap_agent"] = "AGENTFUL" if BY.search(gwindow) else "AGENTLESS"
        else:
            row["gap_token"] = row["gap_slot_token"] = row["gap_agent"] = None
        rows.append(row)
    return rows


def rate(agentless, total):
    return round(agentless / total, 4) if total else None


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
        "bearer_deletion_rate": rate(len(al), n),
        "agentless_share_of_b_form": rate(len(al), len(b)) if b else None,
    }


def main():
    corpus = json.load(gzip.open(HERE / "corpus.json.gz", "rt"))

    # ---------------------------------------------------------------- calibration, on the INPUT only
    problems = []
    if len(corpus) != 63:
        problems.append("corpus holds %d documents, expected 63" % len(corpus))
    windows = Counter(d["window"] for d in corpus.values())
    for seed in (8175, 8800, 9400):
        if windows.get(seed) != 21:
            problems.append("window %d holds %d, expected 21" % (seed, windows.get(seed, 0)))
    for k, d in corpus.items():
        if not d.get("title") or not d.get("date") or not d.get("category"):
            problems.append("rfc%s missing publisher metadata" % k)
        if "appear in all capitals" not in re.sub(r"\s+", " ", d["text"]):
            problems.append("rfc%s does not carry the RFC 8174 boilerplate" % k)
    if problems:
        print("CALIBRATION FAILED -- measuring nothing:", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        sys.exit(1)
    print("calibration: 63 documents, 21 per window, every one carrying the RFC 8174 boilerplate.")

    rows, docs = [], []
    furniture_removed = 0
    dropped_sentences = 0
    dropped_occurrences = 0
    for key in sorted(corpus, key=int):
        d = corpus[key]
        text, removed = defurniture(d["text"])
        furniture_removed += removed
        doc_rows = []
        for i, sent in enumerate(sentences(text)):
            if any(b in sent for b in BOILERPLATE):
                dropped_sentences += 1
                dropped_occurrences += len(MODAL_RE.findall(sent))
                continue
            doc_rows.extend(classify(sent, int(key), i))
        t = tally(doc_rows)
        t.update({"rfc": int(key), "title": d["title"], "date": d["date"],
                  "category": d["category"], "window": d["window"],
                  "upper": sum(1 for r in doc_rows if r["case"] == "UPPER"),
                  "lower": sum(1 for r in doc_rows if r["case"] == "LOWER"),
                  "mixed": sum(1 for r in doc_rows if r["case"] == "MIXED")})
        docs.append(t)
        rows.extend(doc_rows)
        print("  rfc%-5d %5d occ  %5.1f%%  %s" % (int(key), t["occurrences"],
                                                  100 * (t["bearer_deletion_rate"] or 0),
                                                  (d["title"] or "")[:44]))

    # ------------------------------------------------------------------------------ the aggregations
    by_case = {c: tally([r for r in rows if r["case"] == c]) for c in ("UPPER", "LOWER", "MIXED")}
    per_modal_case = {}
    for w in MODALS:
        per_modal_case[w] = {}
        for c in ("UPPER", "LOWER", "MIXED"):
            per_modal_case[w][c] = tally([r for r in rows if r["modal"] == w and r["case"] == c])

    # P4: the one-token gap adds these, over and above the strict rule
    gap_rows = [r for r in rows if r["form"] == "NON-B" and r["gap_agent"] == "AGENTLESS"]
    strict_agentless = by_case["UPPER"]["agentless"] + by_case["LOWER"]["agentless"] + \
        by_case["MIXED"]["agentless"]
    gap = {
        "strict_agentless": strict_agentless,
        "gap_rule_extra_agentless": len(gap_rows),
        "gap_rule_extra_agentful": sum(1 for r in rows
                                       if r["form"] == "NON-B" and r["gap_agent"] == "AGENTFUL"),
        "relative_increase": rate(len(gap_rows), strict_agentless),
        "by_case": {c: sum(1 for r in gap_rows if r["case"] == c)
                    for c in ("UPPER", "LOWER", "MIXED")},
    }

    whole = tally(rows)
    whole["modal_mix"] = {w: sum(1 for r in rows if r["modal"] == w) for w in MODALS}
    whole["case_mix"] = {c: sum(1 for r in rows if r["case"] == c)
                         for c in ("UPPER", "LOWER", "MIXED")}

    # the rejection logs
    slot = Counter(r["slot_token"] for r in rows if r["slot_token"])
    slot_by_case = defaultdict(Counter)
    for r in rows:
        if r["slot_token"]:
            slot_by_case[r["case"]][r["slot_token"]] += 1
    gaptok = Counter(r["gap_token"] for r in rows if r["gap_token"])

    results = {
        "session": 86, "date": "2026-09-10",
        "corpus": "63 RFCs carrying the RFC 8174 boilerplate; harvest.py",
        "modals": MODALS, "agent_window_chars": AGENT_WINDOW,
        "page_furniture_lines_removed": furniture_removed,
        "boilerplate_sentences_dropped": dropped_sentences,
        "boilerplate_occurrences_dropped": dropped_occurrences,
        "whole_corpus": whole,
        "by_case": by_case,
        "per_modal_case": per_modal_case,
        "gap_rule": gap,
        "eu_reference": {
            "source": "works/2026-09-08-no-one-to-bear-it/results.json, whole_corpus",
            "recitals": {"occurrences": 6942, "agentless": 2608, "rate": 0.3757},
            "articles": {"occurrences": 15612, "agentless": 3864, "rate": 0.2475},
        },
        "documents": docs,
    }
    (HERE / "results.json").write_text(json.dumps(results, indent=1) + "\n")
    (HERE / "slot-tokens.json").write_text(json.dumps(
        {"note": "every token that landed in the '<modal> be ___' slot, unfiltered. "
                 "This file is the rejection log: nothing here was chosen by me.",
         "total_distinct": len(slot),
         "all": dict(slot.most_common()),
         "by_case": {c: dict(v.most_common()) for c, v in slot_by_case.items()}}, indent=1) + "\n")
    (HERE / "gap-tokens.json").write_text(json.dumps(
        {"note": "every token that stood between the modal and 'be' under the one-token gap rule, "
                 "unfiltered. The second rejection log; there is no adverb list.",
         "total_distinct": len(gaptok),
         "all": dict(gaptok.most_common())}, indent=1) + "\n")
    with gzip.open(HERE / "occurrences.json.gz", "wt") as fh:
        json.dump(rows, fh)

    print("\n%d occurrences  |  UPPER %d  LOWER %d  MIXED %d"
          % (whole["occurrences"], whole["case_mix"]["UPPER"],
             whole["case_mix"]["LOWER"], whole["case_mix"]["MIXED"]))
    print("whole corpus bearer-deletion rate: %.4f" % whole["bearer_deletion_rate"])
    for w in MODALS:
        u, l = per_modal_case[w]["UPPER"], per_modal_case[w]["LOWER"]
        print("  %-7s UPPER %6d %s   LOWER %6d %s"
              % (w, u["occurrences"], u["bearer_deletion_rate"],
                 l["occurrences"], l["bearer_deletion_rate"]))
    print("gap rule: +%d agentless on %d strict (%.4f)"
          % (gap["gap_rule_extra_agentless"], strict_agentless, gap["relative_increase"] or 0))
    print("furniture lines removed %d | boilerplate sentences dropped %d (%d occurrences)"
          % (furniture_removed, dropped_sentences, dropped_occurrences))


if __name__ == "__main__":
    main()
