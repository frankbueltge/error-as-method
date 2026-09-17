#!/usr/bin/env python3
"""validate.py -- three decision rules, declared in PREDICTIONS.md §3 before this file existed,
scored against the only ground truth this line owns, and then run over the whole population.

Open thread 3 of Session 90 asked whether the precision of the mechanical ceiling -- the share of
rows where the party term in reach is actually the bearer of the obligation -- can be computed
instead of read.  Session 88 read 60 windows and got 0.611; Session 90 read 40 and got 0.425.  A
rule that agrees with those verdicts would give the same quantity over 226 rows, or 336, or 660.

The rules are R1 ADJACENT SUBJECT, R2 NO COMPETING NOMINAL, R3 ACTIVE GOVERNOR.  Their texts are in
PREDICTIONS.md and the commit that carries that file precedes the commit that carries this one; that
ordering is the only warrant a declared rule has.

Writes results.json.  Run after bounds.py.
"""

import bisect
import gzip
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
S88 = HERE.parent / "2026-09-12-adjacent-text"
S90 = HERE.parent / "2026-09-15-not-part-of-the-act"

SEP = "\n"
WORD = re.compile(r"\S+")

UK_NARROW = ["Secretary of State", "Minister", "Ministers", "Treasury",
             "local authority", "local authorities", "authority", "authorities",
             "court", "courts", "tribunal", "tribunals", "constable", "officer", "officers"]
UK_WIDE = UK_NARROW + ["person", "persons"]

# ---------------------------------------------------------------- the three rules, frozen

R1_GAP = re.compile(r"^[\s,;:.()\[\]'‘’“”-]*(?:(?:who|which|that)"
                    r"[\s,;:.()\[\]'‘’“”-]*)?$", re.IGNORECASE)
R2_NOMINAL = re.compile(r"\b(?:the|a|an|any|each|every|such)\s+\w", re.IGNORECASE)
R2_BOUNDARY = re.compile(r"\b(?:and|or|but|if|where|unless|because|which|who|that)\b", re.IGNORECASE)
R3_VERB = r"(?:may|must|shall|should|will|can|is|are|has|have)"


def r1(carrier, gap_text, block_text):
    """ADJACENT SUBJECT: nothing between the carrier and the modal but a relative pronoun."""
    return bool(R1_GAP.match(gap_text))


def r2(carrier, gap_text, block_text):
    """NO COMPETING NOMINAL: nothing in between that could displace the carrier as subject."""
    return not R2_NOMINAL.search(gap_text) and not R2_BOUNDARY.search(gap_text)


def r3(carrier, gap_text, block_text):
    """ACTIVE GOVERNOR: the carrier string acts somewhere in this block."""
    return bool(re.search(r"\b" + re.escape(carrier) + r"\s+" + R3_VERB + r"\b",
                          block_text, re.IGNORECASE))


RULES = {"R1_adjacent_subject": r1, "R2_no_competing_nominal": r2, "R3_active_governor": r3}

# R3b is not one of the three declared in PREDICTIONS.md §3.  It is the repair that §3 says a repair
# must be -- a new rule under a new name, with both reported.  R3 as written asks whether the carrier
# string acts in **the obligation's** block; where the carrier stands in an earlier block that is a
# question about a text the carrier is not in, and 150 of the 226 NARROW rows in reach are of that
# kind.  R3b asks the same question of **the carrier's own** block.  On the 40 hand-read rows the two
# are the same rule, because there the carrier is in the obligation's block by construction; they
# differ only over the population, and that difference is a measurement, not a correction.


def r3b(carrier, gap_text, carrier_block_text):
    """ACTIVE GOVERNOR, asked of the carrier's own block (the repair; not declared in advance)."""
    return r3(carrier, gap_text, carrier_block_text)

# ---------------------------------------------------------------- corpus


def base_terms():
    pat = json.load(open(S88 / "results.json"))["mechanical_ceiling"]["party_terms"]
    return pat[len(r"\b("):-len(r")\b")].split("|")


def term_pattern(names):
    return r"\b(" + "|".join(sorted(names, key=len, reverse=True)) + r")\b"


def occurrences():
    return json.load(gzip.open(S90 / "occurrences.json.gz"))


def population(occ):
    return [{"doc": x["act"], "block": x["block"], "sentence": x["sentence"],
             "modal": x["modal"], "offset": x["offset"]}
            for x in occ
            if x["form"] == "B-FORM" and x["agent"] == "AGENTLESS" and x["register"] == "ACT"]


def blocks():
    corpus = json.load(gzip.open(S90 / "corpus.json.gz", "rt"))
    return {k: d["act"] for k, d in corpus.items()}


def modal_pos_in_block(block_text, sentence, offset):
    """Where the modal stands inside its block."""
    i = block_text.find(sentence)
    return (0 if i < 0 else i) + offset


def nearest_in_block(party, block_text, pos):
    """The carrier the reader was looking at: the party term nearest the modal, either direction.

    Distance is in words, measured from the term's near edge to the modal.  Ties go backwards,
    because a preceding term is the one a bearer-reading would reach for first.
    """
    spans = [(m.start(), m.end(), m.group(0)) for m in party.finditer(block_text)]
    if not spans:
        return None
    ws = [m.start() for m in WORD.finditer(block_text)]
    wi = bisect.bisect_left(ws, pos)
    best = None
    for s, e, t in spans:
        if e <= pos:
            d, direction, gap = wi - bisect.bisect_left(ws, e), "before", block_text[e:pos]
        elif s > pos:
            d, direction, gap = bisect.bisect_left(ws, s) - wi, "after", block_text[pos:s]
        else:
            d, direction, gap = 0, "overlapping", ""
        key = (d, 0 if direction == "before" else 1)
        if best is None or key < best[0]:
            best = (key, {"carrier": t, "word_distance": d, "direction": direction,
                          "gap_text": gap, "start": s, "end": e})
    return best[1]


# ---------------------------------------------------------------- part one: against the reader


def score_against_reader():
    hand = json.load(open(S90 / "handreading.json"))
    occ = population(occurrences())
    blks = blocks()
    party = re.compile(term_pattern(base_terms() + UK_NARROW), re.IGNORECASE)
    key = {(r["doc"], r["block"], r["modal"], r["sentence"]): r for r in occ}

    rows, unmatched = [], 0
    for h in hand["rows"]:
        k = (h["act"], h["block"], h["modal"], h["sentence"])
        if k not in key:
            unmatched += 1
            continue
        p = key[k]
        bt = blks[h["act"]][h["block"]]
        pos = modal_pos_in_block(bt, p["sentence"], p["offset"])
        c = nearest_in_block(party, bt, pos)
        verdict = h["is_the_nearest_party_term_the_bearer"].strip().upper() == "YES"
        row = {"n": h["n"], "act": h["act"], "block": h["block"], "modal": h["modal"],
               "reader": verdict, "reader_reason": h.get("reason", ""),
               "carrier": None if c is None else c["carrier"],
               "direction": None if c is None else c["direction"],
               "word_distance": None if c is None else c["word_distance"],
               "blind": h["n"] not in (1, 2),
               "rules": {}}
        for name, fn in RULES.items():
            row["rules"][name] = False if c is None else bool(
                fn(c["carrier"], c["gap_text"], bt))
        rows.append(row)

    out = {"n_scored": len(rows), "unmatched_against_the_population": unmatched,
           "reader_yes": sum(1 for r in rows if r["reader"]),
           "reader_no": sum(1 for r in rows if not r["reader"]),
           "carrier_direction": dict(Counter(r["direction"] for r in rows)),
           "by_rule": {}, "blind_only": {}, "pairwise_rule_disagreement": {}}

    def tally(sel, name):
        tp = sum(1 for r in sel if r["rules"][name] and r["reader"])
        fp = sum(1 for r in sel if r["rules"][name] and not r["reader"])
        fn_ = sum(1 for r in sel if not r["rules"][name] and r["reader"])
        tn = sum(1 for r in sel if not r["rules"][name] and not r["reader"])
        fires = tp + fp
        return {"fires": fires, "agreements": tp + tn, "disagreements": fp + fn_,
                "agreement": round((tp + tn) / len(sel), 4) if sel else None,
                "precision_on_yes": round(tp / fires, 4) if fires else None,
                "recall": round(tp / (tp + fn_), 4) if (tp + fn_) else None,
                "tp": tp, "fp": fp, "fn": fn_, "tn": tn}

    for name in RULES:
        out["by_rule"][name] = tally(rows, name)
        out["blind_only"][name] = tally([r for r in rows if r["blind"]], name)

    names = list(RULES)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            d = sum(1 for r in rows if r["rules"][a] != r["rules"][b])
            out["pairwise_rule_disagreement"]["%s vs %s" % (a, b)] = d

    out["max_rule_to_rule_disagreement"] = max(out["pairwise_rule_disagreement"].values())
    out["max_rule_to_reader_disagreement"] = max(v["disagreements"] for v in out["by_rule"].values())
    out["reader_base_rate"] = round(out["reader_yes"] / len(rows), 4) if rows else None
    out["rows"] = rows
    return out


# ---------------------------------------------------------------- part two: over the population


def fire_rates():
    """Each rule's fire rate over every row in reach, under each of the three vocabularies."""
    occ = population(occurrences())
    blks = blocks()
    base = base_terms()
    lists = {"base": base, "narrow": base + UK_NARROW, "wide": base + UK_WIDE}
    w36 = {"base": 0.76, "narrow": 34.24, "wide": 50.91}   # Session 90's published reach

    out = {}
    for lname, terms in lists.items():
        party = re.compile(term_pattern(terms), re.IGNORECASE)
        # the rows this list puts in reach at word window 36, with their nearest PRECEDING carrier
        docs = {}
        for doc, seq in blks.items():
            text = SEP.join(seq)
            starts, off = [], 0
            for t in seq:
                starts.append(off)
                off += len(t) + len(SEP)
            docs[doc] = {"text": text, "starts": starts,
                         "spans": [(m.start(), m.end(), m.group(0)) for m in party.finditer(text)],
                         "word_starts": [m.start() for m in WORD.finditer(text)]}
        allnames = list(RULES) + ["R3b_active_governor_own_block"]
        fired = {name: 0 for name in allnames}
        by_carrier = {name: Counter() for name in allnames}
        carrier_total = Counter()
        n_in_reach = same_block = 0
        for r in occ:
            d = docs[r["doc"]]
            sb = blks[r["doc"]][r["block"]]
            pos = d["starts"][r["block"]] + sb.find(r["sentence"]) + r["offset"]
            ends = [e for _, e, _ in d["spans"]]
            j = bisect.bisect_right(ends, pos)
            if j == 0:
                continue
            s, e, t = d["spans"][j - 1]
            ws = d["word_starts"]
            if bisect.bisect_left(ws, pos) - bisect.bisect_left(ws, e) > 36:
                continue
            n_in_reach += 1
            gap = d["text"][e:pos]
            carrier_total[t.lower()] += 1
            cb = blks[r["doc"]][bisect.bisect_right(d["starts"], s) - 1]
            if s >= d["starts"][r["block"]]:
                same_block += 1
            for name, fn in RULES.items():
                if fn(t, gap, sb):
                    fired[name] += 1
                    by_carrier[name][t.lower()] += 1
            if r3b(t, gap, cb):
                fired["R3b_active_governor_own_block"] += 1
                by_carrier["R3b_active_governor_own_block"][t.lower()] += 1
        out[lname] = {
            "rows_in_reach_at_word_36": n_in_reach,
            "of_them_carrier_in_the_obligation_s_own_block": same_block,
            "session_90_published_reach_pct": w36[lname],
            "by_rule": {name: {
                "fires": fired[name],
                "fire_rate": round(fired[name] / n_in_reach, 4) if n_in_reach else None,
                "corrected_reach_pct": round(w36[lname] * fired[name] / n_in_reach, 2)
                if n_in_reach else None,
            } for name in allnames},
            "carriers_in_reach": dict(carrier_total.most_common(12)),
            "R3_fire_share_by_carrier": {
                c: round(by_carrier["R3_active_governor"][c] / n, 4)
                for c, n in carrier_total.most_common(12)},
            "R3b_fire_share_by_carrier": {
                c: round(by_carrier["R3b_active_governor_own_block"][c] / n, 4)
                for c, n in carrier_total.most_common(12)},
        }
    return out


def main():
    reader = score_against_reader()
    pop = fire_rates()

    print("against the reader -- %d rows scored, %d YES / %d NO, base rate %.3f"
          % (reader["n_scored"], reader["reader_yes"], reader["reader_no"],
             reader["reader_base_rate"]))
    print("  carrier direction: %s" % reader["carrier_direction"])
    for name, v in reader["by_rule"].items():
        print("  %-24s fires %2d  agree %2d/%d = %.3f  precision-on-YES %s  recall %s"
              % (name, v["fires"], v["agreements"], reader["n_scored"], v["agreement"],
                 v["precision_on_yes"], v["recall"]))
    print("  rule-to-rule disagreement: %s" % reader["pairwise_rule_disagreement"])

    print("\nover the population")
    for lname, v in pop.items():
        print("  %-7s in reach %4d (S90 reach %5.2f%%)" % (lname, v["rows_in_reach_at_word_36"],
                                                           v["session_90_published_reach_pct"]))
        for name, r in v["by_rule"].items():
            print("      %-24s fire rate %s  corrected reach %s%%"
                  % (name, r["fire_rate"], r["corrected_reach_pct"]))

    out = {
        "note": "Three decision rules declared in PREDICTIONS.md §3, in a commit that precedes this "
                "file, scored against Session 90's 40 hand verdicts and then run over every row in "
                "reach under each of Session 90's three vocabularies.",
        "rules": dict([(name, fn.__doc__.strip()) for name, fn in RULES.items()]
                      + [("R3b_active_governor_own_block", r3b.__doc__.strip())]),
        "rule_literals": {
            "R1_gap_pattern": R1_GAP.pattern,
            "R2_nominal_pattern": R2_NOMINAL.pattern,
            "R2_boundary_pattern": R2_BOUNDARY.pattern,
            "R3_verb_alternation": R3_VERB,
        },
        "against_the_reader": reader,
        "over_the_population": pop,
    }
    (HERE / "results.json").write_text(json.dumps(out, indent=1) + "\n")
    print("\n  wrote results.json")


if __name__ == "__main__":
    main()
