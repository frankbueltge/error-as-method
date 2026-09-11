#!/usr/bin/env python3
"""bearer -- Session 87, 2026-09-11.  The test F-130 left unbuilt.

Session 86 found that the only part of Session 84's instrument that looks for the agent -- whether a
`by` follows the passive -- is very nearly a constant, so the published "bearer-deletion rate" is a
passive-voice frequency wearing another name.  Its fifth open thread asked the obvious next
question and did not answer it: *what a working test for a deleted bearer would be.*

This file is that test, in the two forms PREDICTIONS.md §3 fixes before any of it ran:

  Rule S   BEARER-NAMED if any member of the lexicon occurs anywhere in the sentence.
  Rule G   BEARER-NAMED if a member stands in the three tokens before the modal.

The lexicon is **not written by me**.  It is derived in two mechanical steps -- a frequency step
over active obligation clauses, then a filter in the corpus's own words (a bearer is a thing the
corpus says can *conform*) -- and both the kept and the rejected lists are published.  The lexicon
is rebuilt separately for each corpus by the same two steps, because scoring RFC sentences against a
WHATWG vocabulary would be a category error.

Scored against two sets: Session 86's 80 hand-adjudicated RFC rows, held out and untouched since
they were published, and a fresh seeded sample of 60 WHATWG rows drawn in `sample.py`.
"""

import gzip
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
S86 = HERE.parent / "2026-09-10-only-when-capitals"

MODAL_RE = re.compile(r"\b(shall|should|must)\b", re.IGNORECASE)
WORD = re.compile(r"[A-Za-z][A-Za-z\-']*")

MIN_ACTIVE = 20          # PREDICTIONS §3 step 1
LOOKBACK = 3             # PREDICTIONS §3, Rule G


# --------------------------------------------------------------------------------- the two mates
def mates(w):
    """A token and its singular/plural partner.  Deliberately crude and published as such."""
    out = {w}
    if w.endswith("ies"):
        out.add(w[:-3] + "y")
    if w.endswith("s"):
        out.add(w[:-1])
    else:
        out.add(w + "s")
    return out


# ----------------------------------------------------------------------------- step 1: candidates
def candidates(sentences, skip_negation=True):
    """Tokens standing immediately before a modal whose clause is active (the next token is not
    `be`).  `skip_negation` steps over a `not`/`never` first; PREDICTIONS §3 did not say so in as
    many words, so both readings are computed and both are published."""
    c = Counter()
    for sent in sentences:
        toks = [(m.group(0), m.start()) for m in WORD.finditer(sent)]
        for i, (t, _) in enumerate(toks):
            if t.lower() not in ("shall", "should", "must"):
                continue
            j = i + 1
            if skip_negation:
                while j < len(toks) and toks[j][0].lower() in ("not", "never"):
                    j += 1
            if j >= len(toks) or toks[j][0].lower() == "be":
                continue
            if i > 0:
                c[toks[i - 1][0].lower()] += 1
    return c


# --------------------------------------------------------------- step 2: the corpus's own filter
FRAMES = {
    "conforming W": lambda w: re.compile(r"\bconforming\s+%s\b" % w, re.I),
    "W that conform": lambda w: re.compile(r"\b%s\s+that\s+conform" % w, re.I),
    "W ... must conform": lambda w: re.compile(r"\b%s\b.{0,40}?\b(?:shall|should|must)\s+conform"
                                               % w, re.I),
    "conformance ... for W": lambda w: re.compile(r"\bconformance\b.{0,40}?\bfor\s+%s\b" % w, re.I),
}


def filter_lexicon(cands, blob):
    kept, rejected = {}, {}
    for w, n in cands.most_common():
        if n < MIN_ACTIVE:
            continue
        hits = []
        for name, build in FRAMES.items():
            for m in mates(w):
                if build(re.escape(m)).search(blob):
                    hits.append("%s (%s)" % (name, m))
                    break
        if hits:
            kept[w] = {"active_subject_count": n, "frames": hits}
        else:
            rejected[w] = {"active_subject_count": n, "frames": []}
    return kept, rejected


# ------------------------------------------------------------------------------------- the rules
def rule_s(sentence, lex_re):
    return "NAMED" if lex_re.search(sentence) else "ABSENT"


def rule_g(sentence, offset, lex):
    toks = [(m.group(0).lower(), m.start()) for m in WORD.finditer(sentence)]
    idx = None
    for i, (t, s) in enumerate(toks):
        if s == offset:
            idx = i
            break
    if idx is None:                       # offsets are the instrument's, not re-derived here
        return "UNLOCATED"
    for k in range(1, LOOKBACK + 1):
        if idx - k < 0:
            break
        if toks[idx - k][0] in lex:
            return "NAMED"
    return "ABSENT"


def lex_regex(lex):
    forms = sorted({m for w in lex for m in mates(w)}, key=len, reverse=True)
    return re.compile(r"\b(?:%s)\b" % "|".join(re.escape(f) for f in forms), re.I)


def build(sentences, blob, name):
    with_skip = candidates(sentences, True)
    literal = candidates(sentences, False)
    kept, rejected = filter_lexicon(with_skip, blob)
    print("%s: %d distinct active-clause subjects, %d over the threshold of %d, %d kept by the "
          "corpus's own frames" % (name, len(with_skip),
                                   sum(1 for v in with_skip.values() if v >= MIN_ACTIVE),
                                   MIN_ACTIVE, len(kept)))
    for w, d in sorted(kept.items(), key=lambda kv: -kv[1]["active_subject_count"]):
        print("    keep  %-22s %5d   %s" % (w, d["active_subject_count"], "; ".join(d["frames"])))
    for w, d in sorted(rejected.items(), key=lambda kv: -kv[1]["active_subject_count"])[:14]:
        print("    drop  %-22s %5d" % (w, d["active_subject_count"]))
    return {"kept": kept, "rejected": rejected,
            "candidates_with_negation_skip": dict(with_skip.most_common()),
            "candidates_literal_reading": dict(literal.most_common())}


def main():
    out = {"session": 87, "date": "2026-09-11", "min_active_subject_count": MIN_ACTIVE,
           "lookback_tokens": LOOKBACK, "frames": list(FRAMES)}

    # ------------------------------------------------------------------------ the WHATWG lexicon
    corpus = json.load(gzip.open(HERE / "corpus.json.gz", "rt"))
    wh_sents, wh_blob = [], []
    for key in sorted(corpus):
        for b in corpus[key]["blocks"]:
            wh_sents.append(b["t"])
            wh_blob.append(b["t"])
    out["whatwg"] = build(wh_sents, "\n".join(wh_blob), "WHATWG")

    # --------------------------------------------------------------------------- the RFC lexicon
    rfc = json.load(gzip.open(S86 / "corpus.json.gz", "rt"))
    rfc_sents, rfc_blob = [], []
    for key in sorted(rfc, key=int):
        flat = re.sub(r"\s+", " ", rfc[key]["text"])
        rfc_sents.append(flat)
        rfc_blob.append(flat)
    print()
    out["rfc"] = build(rfc_sents, "\n".join(rfc_blob), "RFC")

    # ------------------------------------------------------- score: the 80 held-out RFC rows
    adj = json.load(open(S86 / "adjudication.json"))
    aud = {r["id"]: r for r in json.load(open(S86 / "audit-sample.json"))["rows"]}
    lex_rfc = out["rfc"]["kept"]
    re_rfc = lex_regex(lex_rfc) if lex_rfc else re.compile(r"(?!x)x")
    held = []
    for row in adj["rows"]:
        a = aud[row["id"]]
        s_ = rule_s(row["sentence"], re_rfc)
        g_ = rule_g(row["sentence"], a["offset"], set(lex_rfc))
        truth = "NAMED" if row["bearer"] == "RECOVERABLE" else "ABSENT"
        held.append({"id": row["id"], "arm": row["arm"], "rfc": row["rfc"],
                     "hand_bearer": row["bearer"], "hand_subject": row["subject"],
                     "rule_s": s_, "rule_g": g_, "truth": truth,
                     "s_agrees": s_ == truth, "g_agrees": g_ == truth,
                     "sentence": row["sentence"]})
    out["held_out"] = score(held, "Session 86's 80 rows")

    # ------------------------------------------------------ score: the 60 fresh WHATWG rows
    lex_wh = out["whatwg"]["kept"]
    re_wh = lex_regex(lex_wh) if lex_wh else re.compile(r"(?!x)x")
    wadj = json.load(open(HERE / "adjudication.json"))
    fresh = []
    for row in wadj["rows"]:
        s_ = rule_s(row["sentence"], re_wh)
        g_ = rule_g(row["sentence"], row["offset"], set(lex_wh))
        truth = "NAMED" if row["bearer"] == "RECOVERABLE" else "ABSENT"
        fresh.append({"id": row["id"], "doc": row["doc"], "hand_bearer": row["bearer"],
                      "hand_subject": row["subject"], "hand_voice": row["voice"],
                      "rule_s": s_, "rule_g": g_, "truth": truth,
                      "s_agrees": s_ == truth, "g_agrees": g_ == truth,
                      "sentence": row["sentence"]})
    out["fresh"] = score(fresh, "tonight's 60 WHATWG rows")

    # ------------------------------------------------- P7: the two rules over the whole corpus
    occ = json.load(gzip.open(HERE / "occurrences.json.gz", "rt"))
    norm = [r for r in occ if r["register"] == "NORM"]
    s_named = sum(1 for r in norm if rule_s(r["sentence"], re_wh) == "NAMED")
    g_named = sum(1 for r in norm if rule_g(r["sentence"], r["offset"], set(lex_wh)) == "NAMED")
    out["corpus_wide"] = {
        "norm_occurrences": len(norm),
        "rule_s_named": s_named, "rule_s_named_share": round(s_named / len(norm), 4),
        "rule_g_named": g_named, "rule_g_named_share": round(g_named / len(norm), 4),
    }
    print("\ncorpus-wide over %d NORM occurrences: Rule S names %d (%.1f %%), "
          "Rule G names %d (%.1f %%)"
          % (len(norm), s_named, 100 * s_named / len(norm), g_named, 100 * g_named / len(norm)))

    # ------------------------------------------- POST HOC, scores nothing: what the filter let in
    posthoc = {}
    for label, drop in (("without 'and'", {"and"}),
                        ("only the two agent words", set(lex_wh) - {"agent", "agents"})):
        lx = {k: v for k, v in lex_wh.items() if k not in drop}
        rx = lex_regex(lx) if lx else re.compile(r"(?!x)x")
        rows = []
        for row in wadj["rows"]:
            truth = "NAMED" if row["bearer"] == "RECOVERABLE" else "ABSENT"
            rows.append({"id": row["id"], "truth": truth,
                         "rule_s": rule_s(row["sentence"], rx),
                         "rule_g": rule_g(row["sentence"], row["offset"], set(lx))})
        for r in rows:
            r["s_agrees"] = r["rule_s"] == r["truth"]
            r["g_agrees"] = r["rule_g"] == r["truth"]
        posthoc[label] = {"lexicon": sorted(lx),
                          "score": score(rows, "POST HOC (scores nothing) -- %s" % label)}
    out["post_hoc_not_scored"] = posthoc

    (HERE / "fresh-sample-scored.json").write_text(json.dumps(
        {"note": "tonight's 60 rows, hand-labelled in adjudicate.py before either rule was run "
                 "over them, then scored.",
         "score": out["fresh"], "corpus_wide": out["corpus_wide"],
         "post_hoc_not_scored": posthoc, "rows": fresh}, indent=1) + "\n")

    (HERE / "lexicon.json").write_text(json.dumps(
        {"note": "Both steps published whole. `candidates_*` are the rejection logs: every token "
                 "that stood before a modal in an active obligation clause, unfiltered and "
                 "unchosen. `kept` is what the corpus's own conformance vocabulary let through.",
         "whatwg": out["whatwg"], "rfc": out["rfc"]}, indent=1) + "\n")
    (HERE / "held-out.json").write_text(json.dumps(
        {"note": "Session 86's 80 hand-adjudicated rows, untouched, scored by two rules that did "
                 "not exist when they were written.",
         "score": out["held_out"], "rows": held}, indent=1) + "\n")
    return 0


def score(rows, label):
    n = len(rows)
    named = sum(1 for r in rows if r["truth"] == "NAMED")
    absent = n - named
    baseline = max(named, absent)
    s = {"n": n, "hand_NAMED": named, "hand_ABSENT": absent,
         "majority_baseline": baseline,
         "majority_baseline_rate": round(baseline / n, 4)}
    for rule in ("rule_s", "rule_g"):
        key = rule[-1] + "_agrees"
        agree = sum(1 for r in rows if r[key])
        tp = sum(1 for r in rows if r["truth"] == "NAMED" and r[rule] == "NAMED")
        fp = sum(1 for r in rows if r["truth"] == "ABSENT" and r[rule] == "NAMED")
        fn = sum(1 for r in rows if r["truth"] == "NAMED" and r[rule] == "ABSENT")
        s[rule] = {"agreements": agree, "rate": round(agree / n, 4),
                   "beats_baseline": agree > baseline,
                   "true_named": tp, "false_named": fp, "missed_named": fn}
    print("\n%s -- %d rows; hand says NAMED %d / ABSENT %d; majority baseline %d"
          % (label, n, named, absent, baseline))
    for rule in ("rule_s", "rule_g"):
        d = s[rule]
        print("  %-7s %3d agreements (%.1f %%)  beats baseline: %-5s  "
              "true-named %d  false-named %d  missed %d"
              % (rule, d["agreements"], 100 * d["rate"], d["beats_baseline"],
                 d["true_named"], d["false_named"], d["missed_named"]))
    return s


if __name__ == "__main__":
    sys.exit(main())
