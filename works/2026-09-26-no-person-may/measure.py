#!/usr/bin/env python3
"""measure.py -- three inherited instruments, imported by path and called, over the fifth tradition.

  1. Session 86's classify()      works/2026-09-10-only-when-capitals/measure.py   -> S90.FLOOR, P0, P1
  2. Session 88/90's reach scan    works/2026-09-15-not-part-of-the-act/reach.py    -> S90.LEXICON, P2
  3. Session 91's rules via 94's   works/2026-09-21-three-other-offices/port.py     -> S94.SPREAD, P3, P4
     port, and 94's subjecthood    works/2026-09-21-three-other-offices/inspect.py

Nothing here reimplements a rule.  Vocabularies are the ones declared in PREDICTIONS.md §4,
committed before the harvest.  port.py's calibrate() must reproduce Session 91's published UK
figures before anything new is scanned.

Writes occurrences.json.gz and results.json.
"""

import gzip
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKS = HERE.parent
S86 = WORKS / "2026-09-10-only-when-capitals"
S90 = WORKS / "2026-09-15-not-part-of-the-act"
S94 = WORKS / "2026-09-21-three-other-offices"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M86 = load(S86 / "measure.py", "s86_measure")
R90 = load(S90 / "reach.py", "s90_reach")
sys.path.insert(0, str(S94))            # inspect.py does `import port as P`
P94 = load(S94 / "port.py", "port")
sys.modules["port"] = P94
I94 = load(S94 / "inspect.py", "s94_inspect")

# ---------------------------------------------------------------- PREDICTIONS.md §4, verbatim
CFR_OWN = ["Administrator", "FAA", "Federal Aviation Administration",
           "certificate holder", "certificate holders", "air carrier", "air carriers",
           "operator", "operators", "pilot in command", "pilot", "pilots",
           "crewmember", "crewmembers", "flight crewmember", "flight crewmembers",
           "flight attendant", "flight attendants", "aircraft dispatcher", "dispatcher",
           "dispatchers", "applicant", "applicants", "owner", "owners",
           "air traffic control", "ATC", "manufacturer", "manufacturers"]
CFR_WIDE_ADDS = ["person", "persons"]

# the four earlier points, from works/2026-09-21-three-other-offices/inspection.json
PRIOR = {"EU acts": (29.14, 67.59), "WHATWG standards": (19.88, 55.52),
         "UK Acts": (19.07, 31.42), "RFCs": (13.65, 28.15)}
PRIOR_AGENT_TESTS = {"rfc": 0.9022, "whatwg": 0.9010, "eu": 0.8095, "uk": 0.7763}


def occurrences(corpus):
    rows = []
    for key in corpus:
        for bi, block in enumerate(corpus[key]["act"]):
            for sent in M86.SENT_SPLIT.split(block):
                sent = sent.strip()
                if not sent:
                    continue
                for r in M86.classify(sent, key, bi):
                    r["doc"] = r.pop("rfc")
                    r["block"] = r.pop("para")
                    rows.append(r)
    return rows


def tally(sel):
    n = len(sel)
    b = [r for r in sel if r["form"] == "B-FORM"]
    al = [r for r in b if r["agent"] == "AGENTLESS"]
    return {"occurrences": n, "b_form": len(b), "agentless": len(al),
            "B_FORM_share_pct": round(100.0 * len(b) / n, 2) if n else None,
            "agent_test": round(len(al) / len(b), 4) if b else None,
            "bearer_deletion_rate_pct": round(100.0 * len(al) / n, 2) if n else None}


def rank_verdict(subj, r3b):
    """P4: the row's letter and tonight's declared extension, kept apart."""
    pts = sorted(PRIOR.values())                     # ascending by subjecthood
    subs = [p[0] for p in pts]
    out = {"subjecthood": subj, "R3b": r3b}
    for lo, hi in zip(pts, pts[1:]):
        if lo[0] < subj < hi[0]:
            lo_r, hi_r = sorted((lo[1], hi[1]))
            out.update(position="between %.2f and %.2f" % (lo[0], hi[0]),
                       letter_applies=True, R3b_interval=[lo_r, hi_r],
                       S94_SPREAD_falsified=not (lo_r <= r3b <= hi_r),
                       extension_applies=False)
            return out
    if subj > subs[-1]:
        broken = not (r3b > max(p[1] for p in pts))
        side = "above all four"
    elif subj < subs[0]:
        broken = not (r3b < min(p[1] for p in pts))
        side = "below all four"
    else:
        side, broken = "ties a prior point", None
    out.update(position=side, letter_applies=False, S94_SPREAD_falsified=False,
               extension_applies=True, rank_broken_under_extension=broken)
    return out


def main():
    corpus = json.load(gzip.open(HERE / "corpus.json.gz", "rt"))
    docs = {k: d["act"] for k, d in corpus.items() if d["act"]}

    # ---------------------------------------------------------------- 1. classify
    rows = occurrences(corpus)
    whole = tally(rows)
    whole["modal_mix"] = dict(Counter(r["modal"] for r in rows))
    text = "\n".join(b for seq in docs.values() for b in seq)
    may = len(re.findall(r"\bmay\b", text, re.IGNORECASE))
    no_person_may = len(re.findall(r"\bno person may\b", text, re.IGNORECASE))
    ssm = whole["occurrences"]
    pop = [{"doc": r["doc"], "block": r["block"], "sentence": r["sentence"],
            "modal": r["modal"], "offset": r["offset"]}
           for r in rows if r["form"] == "B-FORM" and r["agent"] == "AGENTLESS"]
    print("classify: %d modal occurrences, B-FORM %d, agentless %d, agent test %.4f"
          % (ssm, whole["b_form"], whole["agentless"], whole["agent_test"]))
    print("          'may' %d (%.2f x shall+should+must), 'no person may' %d; population %d"
          % (may, may / ssm, no_person_may, len(pop)))
    if len(pop) < 500:
        raise SystemExit("population below 500: PREDICTIONS.md §2's fallback applies; stopping.")

    # ---------------------------------------------------------------- 2. reach, three lists
    base = R90.base_terms()
    lists = {"base": base, "narrow": base + CFR_OWN, "wide": base + CFR_OWN + CFR_WIDE_ADDS}
    reach = {}
    for name, terms in lists.items():
        bd, wd, dup, carrier = R90.scan(pop, docs, terms)
        reach[name] = {"blocks": R90.curve(bd, R90.BLOCK_WINDOWS, len(pop)),
                       "words": R90.curve(wd, R90.WORD_WINDOWS, len(pop)),
                       "carriers": dict(carrier.most_common(15)),
                       "rows_with_a_duplicated_sentence_in_their_block": len(dup)}
        print("reach %-6s w36 %6.2f%%  median %s  none %d"
              % (name, reach[name]["words"]["pct"]["36"],
                 reach[name]["words"]["median_where_present"],
                 reach[name]["words"]["none_anywhere"]))
    w36 = {k: v["words"]["pct"]["36"] for k, v in reach.items()}
    span = round(max(w36.values()) - min(w36.values()), 2)
    lexicon = {"word_window_36_by_list": w36, "span_points": span, "band_points": 20,
               "S90_LEXICON_falsified": span <= 20}

    # ---------------------------------------------------------------- 3. port + subjecthood
    cal, problems = P94.calibrate(base)
    if problems:
        raise SystemExit("CALIBRATION FAILED -- measuring nothing:\n  " + "\n  ".join(problems))
    print("calibration: port.py reproduces Session 91's UK figures exactly.")
    prow = [{"doc": r["doc"], "block": r["block"], "sentence": r["sentence"],
             "offset": int(r["offset"])} for r in pop]
    port = {name: P94.scan(docs, prow, terms) for name, terms in lists.items()}
    for name, r in port.items():
        print("port  %-6s in reach %5d  R3b %s%%" % (name, r["rows_in_reach_at_word_36"],
              r["by_rule"]["R3b_active_governor_own_block"]["fire_pct"]))
    subj = I94.subjecthood(docs, lists["narrow"])
    subj_wide = I94.subjecthood(docs, lists["wide"])
    r3b = port["narrow"]["by_rule"]["R3b_active_governor_own_block"]["fire_pct"]
    spread = rank_verdict(subj["subjecthood_rate_pct"], r3b)
    print("subjecthood narrow %.2f%%, R3b narrow %.2f%% -> %s"
          % (subj["subjecthood_rate_pct"], r3b, spread))

    results = {
        "session": 98, "date": "2026-09-26",
        "corpus": "14 CFR Chapter I, Subchapters F and G, eCFR 2026-09-24; harvest.py",
        "documents": len(docs), "blocks": sum(len(v) for v in docs.values()),
        "words": len(text.split()),
        "classify": {"whole": whole, "population_BFORM_AGENTLESS": len(pop),
                     "may": may, "no_person_may": no_person_may,
                     "may_over_shall_should_must": round(may / ssm, 3),
                     "prior_agent_tests": PRIOR_AGENT_TESTS},
        "reach": {"term_lists": {k: {"n": len(v), "terms": v} for k, v in lists.items()},
                  "lists": reach, "S90_LEXICON": lexicon},
        "port": {"lists": port, "calibration_reproduced": True},
        "subjecthood": {"narrow": subj, "wide": subj_wide},
        "S94_SPREAD": spread, "prior_points": PRIOR,
    }
    results["predictions"] = {
        "P0": {"population": len(pop), "modal_occurrences": ssm,
               "held": len(pop) >= 500 and ssm >= 1000},
        "P1": {"agent_test": whole["agent_test"], "held": whole["agent_test"] < 0.80},
        "P2": {"span_points": span, "held": span > 20},
        "P3": {"subjecthood": subj["subjecthood_rate_pct"],
               "held": subj["subjecthood_rate_pct"] > 29.14},
        "P4": {"held": (not spread["S94_SPREAD_falsified"]) and
                       (not spread.get("rank_broken_under_extension"))},
        "P5": {"may_over_ssm": round(may / ssm, 3), "held": may >= 0.5 * ssm},
    }
    for k, v in results["predictions"].items():
        print("  %s held: %s" % (k, v["held"]))
    with gzip.open(HERE / "occurrences.json.gz", "wt") as fh:
        json.dump(rows, fh)
    (HERE / "results.json").write_text(json.dumps(results, indent=1) + "\n")


if __name__ == "__main__":
    main()
