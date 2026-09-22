#!/usr/bin/env python3
"""adjudicate.py -- compute the nearest party term for tonight's forty rows, decide whether the
reader's quoted bearer coincides with it, and score Session 91's rules against those decisions.

Order, fixed in PREDICTIONS.md and checkable by git ancestry: draw.py and sheet.json, then
PREDICTIONS.md, then verdicts.json, then this file.  Nothing here may change a verdict.

Calibration first.  The tally below is pointed back at UK statute -- Session 90's forty hand
verdicts, Session 91's rules, joined by tonight's own plumbing -- and must return Session 91's
fifteen published figures and its three published coefficients exactly.  If one misses, the script
exits and measures nothing.

Writes results.json.
"""

import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKS = HERE.parent
S90 = WORKS / "2026-09-15-not-part-of-the-act"
S91 = WORKS / "2026-09-17-the-second-instrument"
S94 = WORKS / "2026-09-21-three-other-offices"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


V = _load(S91 / "validate.py", "s91_validate")
K = _load(S91 / "kappa.py", "s91_kappa")
P = _load(S94 / "port.py", "s94_port")

# Session 91's published figures for the same scoring, results.json -> against_the_reader, and
# kappa.json -> by_rule.  Nothing new is measured unless all of these return.
#
# TWO OF THESE LITERALS WERE WRONG WHEN THIS FILE WAS FIRST RUN, AND THE WRONG ONES ARE MINE.
# PREDICTIONS.md section 5 tabulates R2's kappa as -0.1611 and R3's as +0.4964.  Session 91
# published -0.1609 and +0.4962; its journal rounds them to three places (-0.161, +0.496) and this
# night's pre-registration extended each by a digit that had not been read.  The calibration
# refused to measure anything and named both.  The literals below are the committed ones, from
# works/2026-09-17-the-second-instrument/kappa.json.  PREDICTIONS.md is NOT edited: its own header
# forbids it once verdicts.json exists, and this record corrects rather than tidies.  P4's bar is
# therefore scored at +0.4962, and score.py reports whether the difference could have mattered.
S91_PUBLISHED = {
    "R1_adjacent_subject":      {"fires": 5,  "agreements": 22, "agreement": 0.55,
                                 "precision_on_yes": 0.4,    "recall": 0.1176, "kappa": -0.0141},
    "R2_no_competing_nominal":  {"fires": 13, "agreements": 18, "agreement": 0.45,
                                 "precision_on_yes": 0.3077, "recall": 0.2353, "kappa": -0.1609},
    "R3_active_governor":       {"fires": 19, "agreements": 30, "agreement": 0.75,
                                 "precision_on_yes": 0.6842, "recall": 0.7647, "kappa": 0.4962},
}

# ------------------------------------------------------------------ the two matching norms


TOKEN = re.compile(r"[a-z0-9]+")


def _tokens(s):
    """Case-folded tokens of four characters or more, one trailing 's' stripped first."""
    out = set()
    for t in TOKEN.findall(s.lower()):
        if len(t) > 1 and t.endswith("s"):
            t = t[:-1]
        if len(t) >= 4:
            out.add(t)
    return out


def m1(bearer, carrier):
    """M1, the decision: either string contains the other, case-folded.  NONE is a NO."""
    if bearer is None or carrier is None or bearer.strip().upper() == "NONE":
        return False
    b, c = bearer.lower(), carrier.lower()
    return c in b or b in c


def m2(bearer, carrier):
    """M2, reported beside M1: M1, or one shared token of four characters or more."""
    if m1(bearer, carrier):
        return True
    if bearer is None or carrier is None or bearer.strip().upper() == "NONE":
        return False
    return bool(_tokens(bearer) & _tokens(carrier))


# ------------------------------------------------------------------ the tally, used on both corpora


def tally(rows, rule, reader_key):
    tp = sum(1 for r in rows if r["rules"][rule] and r[reader_key])
    fp = sum(1 for r in rows if r["rules"][rule] and not r[reader_key])
    fn = sum(1 for r in rows if not r["rules"][rule] and r[reader_key])
    tn = sum(1 for r in rows if not r["rules"][rule] and not r[reader_key])
    n = len(rows)
    coef = K.coefficients(tp, fp, fn, tn)
    return {"fires": tp + fp, "agreements": tp + tn, "disagreements": fp + fn,
            "agreement": round((tp + tn) / n, 4) if n else None,
            "precision_on_yes": round(tp / (tp + fp), 4) if (tp + fp) else None,
            "recall": round(tp / (tp + fn), 4) if (tp + fn) else None,
            "tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "cohens_kappa": coef["cohens_kappa"], "scotts_pi": coef["scotts_pi"]}


def baseline(rows, reader_key):
    """Always answering NO -- the majority class in both corpora, and the bar R1 and R2 failed."""
    no = sum(1 for r in rows if not r[reader_key])
    return {"always_no_agreements": no, "always_no_agreement": round(no / len(rows), 4)}


# ------------------------------------------------------------------ calibration: UK statute


def uk_rows():
    """Session 90's forty hand-read rows, carriers and rules recomputed by tonight's plumbing."""
    hand = json.load(open(S90 / "handreading.json"))
    occ = V.population(V.occurrences())
    blks = V.blocks()
    party = re.compile(V.term_pattern(V.base_terms() + V.UK_NARROW), re.IGNORECASE)
    key = {(r["doc"], r["block"], r["modal"], r["sentence"]): r for r in occ}
    rows = []
    for h in hand["rows"]:
        p = key[(h["act"], h["block"], h["modal"], h["sentence"])]
        bt = blks[h["act"]][h["block"]]
        pos = V.modal_pos_in_block(bt, p["sentence"], p["offset"])
        c = V.nearest_in_block(party, bt, pos)
        rows.append({
            "n": h["n"], "carrier": None if c is None else c["carrier"],
            "reader": h["is_the_nearest_party_term_the_bearer"].strip().upper() == "YES",
            "rules": {name: (False if c is None else bool(fn(c["carrier"], c["gap_text"], bt)))
                      for name, fn in V.RULES.items()},
        })
    return rows


def calibrate():
    rows = uk_rows()
    problems, got = [], {}
    if len(rows) != 40:
        problems.append("UK calibration joined %d rows, Session 90 read 40" % len(rows))
    for rule, want in S91_PUBLISHED.items():
        t = tally(rows, rule, "reader")
        got[rule] = t
        for field, expected in want.items():
            mine = t["cohens_kappa"] if field == "kappa" else t[field]
            if mine != expected:
                problems.append("%s/%s: tonight %s, Session 91 published %s"
                                % (rule, field, mine, expected))
    return rows, got, problems


# ------------------------------------------------------------------ the RFC rows


def rfc_rows():
    sheet = json.load(open(HERE / "sheet.json"))
    verdicts = {r["n"]: r for r in json.load(open(HERE / "verdicts.json"))["rows"]}
    docs, _ = P.rfc()
    party = re.compile(V.term_pattern(V.base_terms() + P.RFC_OWN), re.IGNORECASE)
    rows = []
    for s in sheet["rows"]:
        bt = docs[s["rfc"]][s["block"]]
        if bt != s["block_text"]:
            sys.exit("row %d: the paragraph has moved since the sheet was drawn" % s["n"])
        pos = V.modal_pos_in_block(bt, s["sentence"], s["offset"])
        c = V.nearest_in_block(party, bt, pos)
        if c is None:
            sys.exit("row %d: no carrier, but the frame guaranteed one" % s["n"])
        v = verdicts[s["n"]]
        named = v["bearer"].strip().upper() != "NONE"
        rows.append({
            "n": s["n"], "rfc": s["rfc"], "block": s["block"], "modal": s["modal"],
            "sentence": s["sentence"],
            "bearer": v["bearer"], "reason": v["reason"], "bearer_named": named,
            "carrier": c["carrier"], "direction": c["direction"],
            "word_distance": c["word_distance"],
            "m1": m1(v["bearer"], c["carrier"]), "m2": m2(v["bearer"], c["carrier"]),
            "rules": {name: bool(fn(c["carrier"], c["gap_text"], bt))
                      for name, fn in V.RULES.items()},
            "r3b_same_block": bool(V.r3b(c["carrier"], c["gap_text"], bt)),
        })
    return sheet, rows


def main():
    uk, uk_scores, problems = calibrate()
    if problems:
        print("CALIBRATION FAILED -- nothing measured")
        for p in problems:
            print("   " + p)
        sys.exit(1)
    print("calibration: 18 of 18 of Session 91's published figures returned")

    sheet, rows = rfc_rows()
    named = sum(1 for r in rows if r["bearer_named"])
    out = {
        "note": "Forty RFC rows, read blind by one reader, adjudicated against Session 91's rules. "
                "M1 is the decision fixed in PREDICTIONS.md; M2 is reported beside it. The UK "
                "figures are Session 91's, reproduced by tonight's plumbing before anything new "
                "was measured.",
        "calibration": {"corpus": "UK statute, Session 90's 40 hand verdicts",
                        "figures_reproduced": 18, "figures_missed": 0,
                        "by_rule": uk_scores,
                        "baseline": baseline(uk, "reader"),
                        "reader_yes": sum(1 for r in uk if r["reader"]),
                        "rows": [{"n": r["n"], "carrier": r["carrier"], "reader": r["reader"],
                                  "R3": r["rules"]["R3_active_governor"]} for r in uk]},
        "frame": {k: sheet[k] for k in ("corpus", "frame", "population_b_form_agentless_binding",
                                        "population_in_frame", "sampled", "seed")},
        "reading": {
            "bearer_named": named, "bearer_none": len(rows) - named,
            "named_share": round(named / len(rows), 4),
            "m1_yes": sum(1 for r in rows if r["m1"]),
            "m2_yes": sum(1 for r in rows if r["m2"]),
            "m1_m2_disagreements": sum(1 for r in rows if r["m1"] != r["m2"]),
            "m1_m2_disagreeing_rows": [r["n"] for r in rows if r["m1"] != r["m2"]],
            "m1_precision_of_the_nearest_term": round(
                sum(1 for r in rows if r["m1"]) / len(rows), 4),
            "carrier_direction": dict(Counter(r["direction"] for r in rows)),
            "carriers": dict(Counter(r["carrier"].lower() for r in rows).most_common()),
            "carriers_in_rows_the_reader_called_NONE": dict(
                Counter(r["carrier"].lower() for r in rows if not r["bearer_named"]).most_common()),
        },
        "against_the_reader": {
            "M1": {rule: tally(rows, rule, "m1") for rule in V.RULES},
            "M2": {rule: tally(rows, rule, "m2") for rule in V.RULES},
            "baseline_M1": baseline(rows, "m1"),
            "baseline_M2": baseline(rows, "m2"),
        },
        "r3b_equals_r3_on_these_rows": all(r["rules"]["R3_active_governor"] == r["r3b_same_block"]
                                           for r in rows),
        "rows": rows,
    }
    (HERE / "results.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")

    print("bearer named by the reader : %d of 40" % named)
    print("M1 (the decision)          : %d of 40 -- the nearest term IS the reader's bearer"
          % out["reading"]["m1_yes"])
    print("M2                         : %d of 40, disagreeing with M1 on %s"
          % (out["reading"]["m2_yes"], out["reading"]["m1_m2_disagreeing_rows"] or "nothing"))
    for rule in ("R1_adjacent_subject", "R2_no_competing_nominal", "R3_active_governor"):
        t = out["against_the_reader"]["M1"][rule]
        u = uk_scores[rule]
        print("%-26s fires %2d  agrees %2d/40 (%.4f)  precision %s  kappa %s   "
              "[UK: %2d, %2d/40, %s, %s]"
              % (rule, t["fires"], t["agreements"], t["agreement"], t["precision_on_yes"],
                 t["cohens_kappa"], u["fires"], u["agreements"], u["precision_on_yes"],
                 u["cohens_kappa"]))
    print("always-NO baseline         : %d of 40" % out["against_the_reader"]["baseline_M1"]
          ["always_no_agreements"])
    print("R3b == R3 on these rows    : %s" % out["r3b_equals_r3_on_these_rows"])
    print("wrote results.json")


if __name__ == "__main__":
    main()
