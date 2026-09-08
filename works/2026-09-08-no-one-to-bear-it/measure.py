#!/usr/bin/env python3
"""No One to Bear It -- Session 84, 2026-09-08.

A complete census of the three obligation modals over Session 82's 63-act corpus, classifying every
occurrence by whether the party who must act is recoverable from the sentence.

  B-FORM      <modal> (not|never)? be <TOKEN>
  AGENTLESS   a B-FORM with no "by" between the slot token and the sentence end (max 200 chars)
  AGENTFUL    a B-FORM with one
  NON-B       every other occurrence of shall / should / must

THERE IS NO PARTICIPLE LIST AND NO ACTOR LIST.  Session 82 derived a party vocabulary and got it
wrong twice (F-111, F-112).  Session 83 removed the vocabulary and hand-wrote a list of seven
participles instead, of which one supplied 45 % of the matches and none of the exhortations (F-114).
Its rule: a closed list you wrote yourself is a derived vocabulary with the derivation hidden in your
own head, and it is worse than a computed one because a computed one has a rejection log.  So every
token that turns up in the slot is written to slot-tokens.json with its count, nothing filtered.
That file is the rejection log.

Two over-counts are declared in PREDICTIONS.md §2b rather than discovered afterwards:
  (1) "should be able to" is a copula, not a passive, and this rule counts it as B-FORM.  The §4a
      audit measures how many.
  (2) every "by" counts as an agent phrase, including "by 31 December".  So AGENTFUL is an
      over-count and AGENTLESS a lower bound -- against every prediction that wants AGENTLESS large.

The calibration guards the INPUT and nothing else, and nothing else is claimed of it.
"""

import gzip
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
S82 = HERE.parent / "2026-09-06-the-rate-of-the-rule"

MODALS = ("shall", "should", "must")

# ------------------------------------------------------------------ the rules, from PREDICTIONS.md

MODAL_RE = re.compile(r"\b(shall|should|must)\b", re.IGNORECASE)
B_FORM = re.compile(r"^\s+(?:not\s+|never\s+)?be\s+([A-Za-z][A-Za-z\-]*)", re.IGNORECASE)
BY = re.compile(r"\bby\b", re.IGNORECASE)

AGENT_WINDOW = 200          # chars after the slot token, or sentence end, whichever is shorter
SENT_SPLIT = re.compile(r"(?<=[.;:])\s+(?=[A-Z(‘'‘“])|\n+")


def sentences(text):
    parts = [s.strip() for s in SENT_SPLIT.split(text) if s and s.strip()]
    return parts or ([text.strip()] if text.strip() else [])


def classify(sent, celex, part, division):
    """Every occurrence of the three modals in one sentence, classified."""
    out = []
    for m in MODAL_RE.finditer(sent):
        rest = sent[m.end():]
        b = B_FORM.match(rest)
        row = {
            "celex": celex, "part": part, "division": division,
            "modal": m.group(1).lower(),
            "sentence": sent,
            "offset": m.start(),
        }
        if not b:
            row["form"] = "NON-B"
            row["slot_token"] = None
            row["agent"] = None
        else:
            tok = b.group(1).lower()
            after = rest[b.end():]
            window = after[:AGENT_WINDOW]
            row["form"] = "B-FORM"
            row["slot_token"] = tok
            row["agent"] = "AGENTFUL" if BY.search(window) else "AGENTLESS"
        out.append(row)
    return out


def main():
    corpus = json.load(gzip.open(S82 / "corpus.json.gz", "rt"))
    s82 = json.load(open(S82 / "results.json"))
    meta = {a["celex"]: a for a in s82["acts"]}

    # -------------------------------------------------------------- calibration on the INPUT
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

    acts, rows = [], []
    for celex, act in sorted(corpus.items()):
        m = meta[celex]
        row = {
            "celex": celex, "stratum": m["stratum"], "adoption_year": m["adoption_year"],
            "domain": m["domain"], "title": m["title"],
            "n_recitals": len(act["recitals"]), "n_articles": len(act["articles"]),
        }
        for part in ("recitals", "articles"):
            hits = []
            for division, text in sorted(act[part].items(), key=lambda kv: str(kv[0])):
                for sent in sentences(text):
                    hits += classify(sent, celex, part, division)
            rows += hits
            tot = len(hits)
            bform = [h for h in hits if h["form"] == "B-FORM"]
            less = [h for h in bform if h["agent"] == "AGENTLESS"]
            full = [h for h in bform if h["agent"] == "AGENTFUL"]
            per_modal = {}
            for w in MODALS:
                mh = [h for h in hits if h["modal"] == w]
                ml = [h for h in mh if h["form"] == "B-FORM" and h["agent"] == "AGENTLESS"]
                per_modal[w] = {
                    "total": len(mh),
                    "agentless": len(ml),
                    "rate": round(len(ml) / len(mh), 4) if mh else None,
                }
            row[part] = {
                "modal_occurrences": tot,
                "b_form": len(bform),
                "agentless": len(less),
                "agentful": len(full),
                "non_b": tot - len(bform),
                "bearer_deletion_rate": round(len(less) / tot, 4) if tot else None,
                "per_modal": per_modal,
            }
        acts.append(row)

    # -------------------------------------------------------------- aggregates
    def agg(subset, part):
        tot = sum(a[part]["modal_occurrences"] for a in subset)
        bf = sum(a[part]["b_form"] for a in subset)
        al = sum(a[part]["agentless"] for a in subset)
        af = sum(a[part]["agentful"] for a in subset)
        pm = {}
        for w in MODALS:
            t = sum(a[part]["per_modal"][w]["total"] for a in subset)
            l = sum(a[part]["per_modal"][w]["agentless"] for a in subset)
            pm[w] = {"total": t, "agentless": l, "rate": round(l / t, 4) if t else None}
        return {
            "acts": len(subset),
            "modal_occurrences": tot, "b_form": bf, "agentless": al, "agentful": af,
            "non_b": tot - bf,
            "bearer_deletion_rate": round(al / tot, 4) if tot else None,
            "agentful_share_of_b_form": round(af / bf, 4) if bf else None,
            "per_modal": pm,
        }

    B = [a for a in acts if a["stratum"] == "B"]
    A = [a for a in acts if a["stratum"] == "A"]

    # P2: per-act comparison, Stratum B
    higher, equal, lower, undefined = [], [], [], []
    for a in B:
        r, c = a["recitals"]["bearer_deletion_rate"], a["articles"]["bearer_deletion_rate"]
        if r is None or c is None:
            undefined.append(a["celex"])
        elif r > c:
            higher.append(a["celex"])
        elif r == c:
            equal.append(a["celex"])
        else:
            lower.append(a["celex"])

    slot = {
        part: Counter(h["slot_token"] for h in rows
                      if h["part"] == part and h["form"] == "B-FORM")
        for part in ("recitals", "articles")
    }

    results = {
        "session": 84,
        "date": "2026-09-08",
        "modals": list(MODALS),
        "agent_window_chars": AGENT_WINDOW,
        "total_modal_occurrences": len(rows),
        "stratum_B": {"recitals": agg(B, "recitals"), "articles": agg(B, "articles")},
        "stratum_A": {"recitals": agg(A, "recitals"), "articles": agg(A, "articles")},
        "whole_corpus": {"recitals": agg(acts, "recitals"), "articles": agg(acts, "articles")},
        "p2_per_act_stratum_B": {
            "recitals_higher": higher, "equal": equal, "articles_higher": lower,
            "undefined": undefined,
            "n_recitals_higher": len(higher),
        },
        "acts": acts,
    }

    json.dump(results, open(HERE / "results.json", "w"), indent=1, ensure_ascii=False)
    json.dump(rows, gzip.open(HERE / "occurrences.json.gz", "wt", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    json.dump(
        {part: dict(c.most_common()) for part, c in slot.items()},
        open(HERE / "slot-tokens.json", "w"), indent=1, ensure_ascii=False,
    )

    wb, wa = results["whole_corpus"]["recitals"], results["whole_corpus"]["articles"]
    bb, ba = results["stratum_B"]["recitals"], results["stratum_B"]["articles"]
    print()
    print("occurrences of shall/should/must, whole corpus: %d" % len(rows))
    for name, r in (("recitals", wb), ("articles", wa)):
        print("  %-9s n=%-6d B-FORM=%-5d AGENTLESS=%-5d AGENTFUL=%-4d  rate=%s  agentful/B=%s"
              % (name, r["modal_occurrences"], r["b_form"], r["agentless"], r["agentful"],
                 r["bearer_deletion_rate"], r["agentful_share_of_b_form"]))
    print()
    print("P1  Stratum B recitals bearer-deletion rate : %s   (bar 0.20)"
          % bb["bearer_deletion_rate"])
    print("P2  Stratum B acts, recitals > articles     : %d of 28   (bar 20)" % len(higher))
    print("P3  agentful share of B-FORM  recitals %s / articles %s   (bar < 0.15)"
          % (wb["agentful_share_of_b_form"], wa["agentful_share_of_b_form"]))
    print()
    print("within-modal control (whole corpus, bearer-deletion rate):")
    for w in MODALS:
        print("  %-7s recitals n=%-6d rate=%-8s   articles n=%-6d rate=%s"
              % (w, wb["per_modal"][w]["total"], wb["per_modal"][w]["rate"],
                 wa["per_modal"][w]["total"], wa["per_modal"][w]["rate"]))
    print()
    print("P7 (unscorable) most frequent recital slot token: %s"
          % (slot["recitals"].most_common(3),))


if __name__ == "__main__":
    main()
