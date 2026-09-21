#!/usr/bin/env python3
"""port.py -- Session 91's bearer-decision rules, imported unchanged, run over three corpora that
are not UK statute.

S91.RULEBOUND says R3 is a rule about UK statutory drafting and that in a tradition which does not
name its parties as sentence subjects it "will fire on almost nothing".  Its check: run the
committed r3/r3b from validate.py, unchanged, over the rows in reach of Session 82's EU acts,
Session 86's RFCs or Session 87's WHATWG standards, restricted to B-FORM and AGENTLESS and that
corpus's own binding register, with its own declared party vocabulary.  Falsified if R3b's fire rate
comes in within 10 points of 31.42 % in any one of the three.

Nothing here reimplements a rule.  validate.py is imported by path and its functions are called;
verify.py asserts the literals it holds are byte-identical to the ones Session 91 published.

Writes results.json.
"""

import bisect
import gzip
import importlib.util
import json
import re
import statistics
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKS = HERE.parent
S82 = WORKS / "2026-09-06-the-rate-of-the-rule"        # EU corpus text
S84 = WORKS / "2026-09-08-no-one-to-bear-it"           # EU occurrences
S86 = WORKS / "2026-09-10-only-when-capitals"          # RFC corpus + occurrences
S87 = WORKS / "2026-09-11-eleven-sentences"            # WHATWG corpus + occurrences
S90 = WORKS / "2026-09-15-not-part-of-the-act"         # UK corpus + occurrences (calibration)
S91 = WORKS / "2026-09-17-the-second-instrument"       # the rules

SEP = "\n"
WORD = re.compile(r"\S+")
WINDOW_WORDS = 36
BAND = (21.42, 41.42)          # PREDICTIONS.md §2 -- 31.42 plus or minus 10 points


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


V = _load(S91 / "validate.py", "s91_validate")          # the rules, unchanged
M86 = _load(S86 / "measure.py", "s86_measure")          # defurniture() and the sentence splitter

# ------------------------------------------------------------------ the vocabularies, from PREDICTIONS.md §4

EU_OWN = ["Commission", "Council", "European Parliament", "Member State", "Member States",
          "Agency", "Agencies", "Authority", "Authorities", "Board", "Committee",
          "Court", "Court of Justice", "Institution", "Institutions", "Body", "Bodies",
          "operator", "operators", "manufacturer", "manufacturers", "importer", "importers",
          "distributor", "distributors", "supplier", "suppliers", "provider", "providers",
          "controller", "controllers", "processor", "processors"]
EU_WIDE_ADDS = ["person", "persons"]

RFC_OWN = ["sender", "senders", "receiver", "receivers", "node", "nodes", "host", "hosts",
           "router", "routers", "peer", "peers", "endpoint", "endpoints", "gateway", "gateways",
           "proxy", "proxies", "responder", "responders", "requester", "requesters",
           "initiator", "initiators", "device", "devices", "application", "applications"]
RFC_WIDE_ADDS = ["party", "parties"]

WHATWG_OWN = ["document", "documents", "element", "elements", "attribute", "attributes"]
WHATWG_WIDE_ADDS = ["party", "parties"]

# ------------------------------------------------------------------ the three corpora, in one shape


def eu():
    """Blocks are an act's article divisions in Session 84's own order; the binding register is the
    articles, as the notes were excluded from Session 90's UK documents."""
    corpus = json.load(gzip.open(S82 / "corpus.json.gz", "rt"))
    occ = json.load(gzip.open(S84 / "occurrences.json.gz"))
    docs, index = {}, {}
    for celex, act in corpus.items():
        order = [k for k, _ in sorted(act["articles"].items(), key=lambda kv: str(kv[0]))]
        docs[celex] = [act["articles"][k] for k in order]
        index[celex] = {k: i for i, k in enumerate(order)}
    rows = []
    for o in occ:
        if o["form"] != "B-FORM" or o["agent"] != "AGENTLESS" or o["part"] != "articles":
            continue
        b = index[o["celex"]].get(str(o["division"]))
        if b is None:
            continue
        rows.append({"doc": o["celex"], "block": b, "sentence": o["sentence"],
                     "offset": int(o["offset"])})
    return docs, rows


def rfc():
    """Blocks are paragraphs, rebuilt from the committed text with Session 86's own defurniture()
    and splitter, because that night's `para` field holds a sentence ordinal (PREDICTIONS.md §3).
    The binding register is the corpus's own: RFC 8174 makes the keyword normative only in capitals,
    so case == UPPER is the binding half."""
    corpus = json.load(gzip.open(S86 / "corpus.json.gz", "rt"))
    occ = json.load(gzip.open(S86 / "occurrences.json.gz"))
    docs, sent_to_block = {}, {}
    for key in sorted(corpus, key=int):
        text, _ = M86.defurniture(corpus[key]["text"])
        paras, mapping, si = [], {}, 0
        for para in re.split(r"\n\s*\n", text):
            flat = re.sub(r"\s+", " ", para).strip()
            if not flat:
                continue
            sents = [s.strip() for s in M86.SENT_SPLIT.split(flat) if s.strip()]
            if not sents:
                continue
            for _ in sents:
                mapping[si] = len(paras)
                si += 1
            paras.append(flat)
        docs[key] = paras
        sent_to_block[key] = mapping
    rows = []
    for o in occ:
        if o["form"] != "B-FORM" or o["agent"] != "AGENTLESS" or o["case"] != "UPPER":
            continue
        d = str(o["rfc"])
        b = sent_to_block[d].get(int(o["para"]))
        if b is None:
            continue
        rows.append({"doc": d, "block": b, "sentence": o["sentence"], "offset": int(o["offset"])})
    return docs, rows


def whatwg():
    """Blocks are the standard's own blocks; the binding register is the block-level NORM flag
    Session 87 derived from each standard's own conformance section."""
    corpus = json.load(gzip.open(S87 / "corpus.json.gz", "rt"))
    occ = json.load(gzip.open(S87 / "occurrences.json.gz"))
    docs = {k: [b["t"] for b in d["blocks"]] for k, d in corpus.items()}
    rows = []
    for o in occ:
        if o["form"] != "B-FORM" or o["agent"] != "AGENTLESS" or o["register"] != "NORM":
            continue
        rows.append({"doc": o["doc"], "block": int(o["block"]), "sentence": o["sentence"],
                     "offset": int(o["offset"])})
    return docs, rows


def uk():
    """The calibration corpus, not one of the three: Session 90's 63 UK Acts, their binding
    register, rebuilt here by tonight's own plumbing so that the port can be asked to reproduce
    Session 91's published figures before it is allowed to measure anything new."""
    corpus = json.load(gzip.open(S90 / "corpus.json.gz", "rt"))
    occ = json.load(gzip.open(S90 / "occurrences.json.gz"))
    docs = {k: d["act"] for k, d in corpus.items()}
    rows = [{"doc": o["act"], "block": int(o["block"]), "sentence": o["sentence"],
             "offset": int(o["offset"])}
            for o in occ
            if o["form"] == "B-FORM" and o["agent"] == "AGENTLESS" and o["register"] == "ACT"]
    return docs, rows


CALIBRATION = {"build": uk, "own": V.UK_NARROW, "wide_adds": ["person", "persons"],
               "binding_register": "the Act, not its Explanatory Notes"}

# Session 91's published figures for the same scan, results.json -> over_the_population.
# The port measures nothing unless it returns these exactly.
S91_PUBLISHED = {
    "base":   {"in_reach": 5,   "R1": 0.0,    "R2": 0.0,    "R3": 0.0,    "R3b": 0.0},
    "narrow": {"in_reach": 226, "R1": 0.0575, "R2": 0.1018, "R3": 0.1903, "R3b": 0.3142},
    "wide":   {"in_reach": 336, "R1": 0.0685, "R2": 0.1429, "R3": 0.1667, "R3b": 0.2619},
}
RULE_KEYS = {"R1": "R1_adjacent_subject", "R2": "R2_no_competing_nominal",
             "R3": "R3_active_governor", "R3b": "R3b_active_governor_own_block"}


def calibrate(base):
    """Run the scan over UK statute and refuse to go on unless every published figure returns."""
    docs, rows = CALIBRATION["build"]()
    lists = {"base": base,
             "narrow": base + CALIBRATION["own"],
             "wide": base + CALIBRATION["own"] + CALIBRATION["wide_adds"]}
    out, problems = {}, []
    for lname, terms in lists.items():
        r = scan(docs, rows, terms)
        out[lname] = r
        want = S91_PUBLISHED[lname]
        if r["rows_in_reach_at_word_36"] != want["in_reach"]:
            problems.append("%s: %d rows in reach, Session 91 published %d"
                            % (lname, r["rows_in_reach_at_word_36"], want["in_reach"]))
        for short, key in RULE_KEYS.items():
            got = r["by_rule"][key]["fire_rate"]
            if got != want[short]:
                problems.append("%s/%s: fire rate %s, Session 91 published %s"
                                % (lname, short, got, want[short]))
    return out, problems


CORPORA = {
    "EU acts": {"build": eu, "own": EU_OWN, "wide_adds": EU_WIDE_ADDS,
                "binding_register": "articles (the enacting terms)"},
    "RFCs": {"build": rfc, "own": RFC_OWN, "wide_adds": RFC_WIDE_ADDS,
             "binding_register": "the keyword in all capitals (RFC 8174)"},
    "WHATWG standards": {"build": whatwg, "own": WHATWG_OWN, "wide_adds": WHATWG_WIDE_ADDS,
                         "binding_register": "blocks flagged NORM"},
}

# ------------------------------------------------------------------ the reach scan


def scan(docs, rows, terms):
    """Session 91's fire_rates() over one corpus and one vocabulary.  Nearest PRECEDING carrier in
    the joined document, word window 36; R1/R2/R3 asked of the obligation's block, R3b of the
    carrier's own block."""
    party = re.compile(V.term_pattern(terms), re.IGNORECASE)
    built = {}
    for doc, seq in docs.items():
        text = SEP.join(seq)
        starts, off = [], 0
        for t in seq:
            starts.append(off)
            off += len(t) + len(SEP)
        built[doc] = {"text": text, "starts": starts,
                      "spans": [(m.start(), m.end(), m.group(0)) for m in party.finditer(text)],
                      "word_starts": [m.start() for m in WORD.finditer(text)]}

    names = list(V.RULES) + ["R3b_active_governor_own_block"]
    fired = {n: 0 for n in names}
    by_carrier = {n: Counter() for n in names}
    carrier_total = Counter()
    n_in_reach = same_block = 0
    carrier_block_words, obligation_block_words, distances = [], [], []

    for r in rows:
        d = built[r["doc"]]
        sb = docs[r["doc"]][r["block"]]
        i = sb.find(r["sentence"])
        pos = d["starts"][r["block"]] + (0 if i < 0 else i) + r["offset"]
        ends = [e for _, e, _ in d["spans"]]
        j = bisect.bisect_right(ends, pos)
        if j == 0:
            continue
        s, e, t = d["spans"][j - 1]
        ws = d["word_starts"]
        dist = bisect.bisect_left(ws, pos) - bisect.bisect_left(ws, e)
        if dist > WINDOW_WORDS:
            continue
        n_in_reach += 1
        distances.append(dist)
        gap = d["text"][e:pos]
        carrier_total[t.lower()] += 1
        cb_index = bisect.bisect_right(d["starts"], s) - 1
        cb = docs[r["doc"]][cb_index]
        if s >= d["starts"][r["block"]]:
            same_block += 1
        carrier_block_words.append(len(WORD.findall(cb)))
        obligation_block_words.append(len(WORD.findall(sb)))
        for name, fn in V.RULES.items():
            if fn(t, gap, sb):
                fired[name] += 1
                by_carrier[name][t.lower()] += 1
        if V.r3b(t, gap, cb):
            fired["R3b_active_governor_own_block"] += 1
            by_carrier["R3b_active_governor_own_block"][t.lower()] += 1

    pct = lambda x, n: round(100.0 * x / n, 2) if n else None
    return {
        "terms_in_list": len(terms),
        "population": len(rows),
        "rows_in_reach_at_word_36": n_in_reach,
        "reach_pct": pct(n_in_reach, len(rows)),
        "of_them_carrier_in_the_obligation_s_own_block": same_block,
        "carrier_in_own_block_pct": pct(same_block, n_in_reach),
        "median_carrier_block_words": (statistics.median(carrier_block_words)
                                       if carrier_block_words else None),
        "median_obligation_block_words": (statistics.median(obligation_block_words)
                                          if obligation_block_words else None),
        "median_word_distance_to_carrier": (statistics.median(distances) if distances else None),
        "by_rule": {n: {"fires": fired[n],
                        "fire_rate": round(fired[n] / n_in_reach, 4) if n_in_reach else None,
                        "fire_pct": pct(fired[n], n_in_reach)} for n in names},
        "carriers_in_reach": dict(carrier_total.most_common(12)),
        "R3b_fire_share_by_carrier": {c: round(by_carrier["R3b_active_governor_own_block"][c] / n, 4)
                                      for c, n in carrier_total.most_common(12)},
    }


def main():
    base = V.base_terms()

    cal, problems = calibrate(base)
    if problems:
        print("CALIBRATION FAILED -- measuring nothing:")
        for p in problems:
            print("  " + p)
        raise SystemExit(1)
    print("calibration: the port reproduces Session 91's three reach counts and twelve fire rates "
          "over UK statute exactly (narrow R3b = %.4f).\n"
          % cal["narrow"]["by_rule"]["R3b_active_governor_own_block"]["fire_rate"])

    out = {
        "note": "Session 91's r1/r2/r3/r3b imported from works/2026-09-17-the-second-instrument/"
                "validate.py and called, not reimplemented. Vocabularies and the decision band are "
                "declared in PREDICTIONS.md, committed before this file.",
        "band_that_would_falsify_S91.RULEBOUND": {"low_pct": BAND[0], "high_pct": BAND[1],
                                                  "session_91_narrow_R3b_pct": 31.42},
        "base_terms": base,
        "base_term_count": len(base),
        "corpora": {},
        "calibration_UK_statute": {
            "note": "Not one of the three. Session 90's corpus rebuilt by tonight's plumbing and "
                    "required to return Session 91's published counts and fire rates exactly "
                    "before any new corpus is scanned.",
            "binding_register": CALIBRATION["binding_register"],
            "session_91_published": S91_PUBLISHED,
            "lists": cal,
        },
    }
    for name, spec in CORPORA.items():
        docs, rows = spec["build"]()
        lists = {"base": base,
                 "narrow": base + spec["own"],
                 "wide": base + spec["own"] + spec["wide_adds"]}
        print("== %s -- %d documents, population %d" % (name, len(docs), len(rows)))
        entry = {"documents": len(docs), "population": len(rows),
                 "binding_register": spec["binding_register"],
                 "own_terms": spec["own"], "wide_adds": spec["wide_adds"], "lists": {}}
        for lname, terms in lists.items():
            r = scan(docs, rows, terms)
            entry["lists"][lname] = r
            print("   %-7s in reach %5d (%5.2f%%)  R1 %5.2f  R2 %5.2f  R3 %5.2f  R3b %5.2f  "
                  "median carrier block %s words"
                  % (lname, r["rows_in_reach_at_word_36"], r["reach_pct"],
                     r["by_rule"]["R1_adjacent_subject"]["fire_pct"],
                     r["by_rule"]["R2_no_competing_nominal"]["fire_pct"],
                     r["by_rule"]["R3_active_governor"]["fire_pct"],
                     r["by_rule"]["R3b_active_governor_own_block"]["fire_pct"],
                     r["median_carrier_block_words"]))
        n = entry["lists"]["narrow"]["by_rule"]["R3b_active_governor_own_block"]["fire_pct"]
        entry["decision"] = {
            "narrow_R3b_pct": n,
            "inside_the_band": bool(n is not None and BAND[0] <= n <= BAND[1]),
            "distance_from_31.42": round(n - 31.42, 2) if n is not None else None,
        }
        print("   -> narrow R3b = %s %%, inside the band: %s"
              % (n, entry["decision"]["inside_the_band"]))
        out["corpora"][name] = entry

    falsifying = [k for k, v in out["corpora"].items() if v["decision"]["inside_the_band"]]
    out["S91.RULEBOUND"] = {
        "corpora_inside_the_band": falsifying,
        "falsified": bool(falsifying),
    }
    print("\nS91.RULEBOUND -- corpora inside the band: %s" % (falsifying or "none"))
    (HERE / "results.json").write_text(json.dumps(out, indent=1) + "\n")
    print("wrote results.json")


if __name__ == "__main__":
    main()
