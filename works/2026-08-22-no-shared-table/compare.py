#!/usr/bin/env python3
"""Session 67 adjudicator — read the five runtimes' answers and settle the falsifier.

Session 66 asked for a case where two independent observers with no shared
lineage disagree in a way that LOCATES an error without any norm being
consulted, and its own scoring rule (PREDICTIONS.md) makes the third condition
the hard one: the location must REQUIRE both parties. This file computes that
condition exactly, over 512 doubles and 25 ordered runtime pairs, and writes
results.json. Nothing here decides what an error is; it decides who could have
seen one alone.
"""
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RUNTIMES = ["python", "node", "ruby", "php", "perl"]

PROBES = {
    # id: (family, what is being asked)
    "S1": ("S", "uppercase of U+00DF LATIN SMALL LETTER SHARP S"),
    "S2": ("S", "uppercase of U+FB01 LATIN SMALL LIGATURE FI"),
    "S3": ("S", "lowercase of U+0130 LATIN CAPITAL LETTER I WITH DOT ABOVE"),
    "S4": ("S", "uppercase of U+0131 LATIN SMALL LETTER DOTLESS I"),
    "S5": ("S", "lowercase of GREEK 'ODOS' — word-final sigma or not"),
    "S6": ("S", "uppercase of U+13F8 CHEROKEE SMALL LETTER YE (Unicode 8.0)"),
    "S7": ("S", "uppercase of U+10EF GEORGIAN LETTER JHAN (Mtavruli, Unicode 11.0)"),
    "S8": ("S", "uppercase of U+10428 DESERET SMALL LETTER LONG I (non-BMP)"),
    "S9": ("S", "uppercase of U+01F3 LATIN SMALL LETTER DZ (title/upper split)"),
    "S10": ("S", "lowercase of U+1E9E LATIN CAPITAL LETTER SHARP S"),
    "I1": ("I", "-7 % 3"),
    "I2": ("I", "7 % -3"),
    "I3": ("I", "integer division of -7 by 3"),
    "I4": ("I", "default string of 0.1 + 0.2"),
    "I5": ("I", "default string of 1/3"),
    "I6": ("I", "default string of 1e21"),
    "I7": ("I", "default string of -0.0"),
    "I8": ("I", "round of 0.5, 1.5, 2.5, -0.5"),
    "I9": ("I", "is '10' < '9'"),
    "I10": ("I", "is '' equal to 0"),
    "I11": ("I", "length of the string U+1D11E"),
    "I12": ("I", "is 0.1 + 0.2 == 0.3"),
    "I13": ("I", "default sort of [10, 9, 1]"),
    "I14": ("I", "2 ** 3 ** 2"),
    "I15": ("I", "'0x10' '010' '1e2' ' 12 ' parsed as numbers (bit patterns)"),
}


def probe_table(answers):
    rows = []
    for pid, (family, question) in sorted(PROBES.items(), key=lambda kv: (kv[1][0], kv[0])):
        given = {r: answers[r]["answers"][pid] for r in RUNTIMES}
        # A runtime that answers "n/a:" does not have the operator being asked
        # about. Counting that as disagreement would manufacture a difference
        # out of a missing feature, so it is excluded and recorded.
        speaking = {r: v for r, v in given.items() if not v.startswith("n/a:")}
        distinct = len(set(speaking.values()))
        rows.append({
            "probe": pid, "family": family, "question": question,
            "answers": given,
            "runtimes_with_the_operator": sorted(speaking),
            "distinct_answers": distinct,
            "unanimous": distinct == 1,
            "majority": Counter(speaking.values()).most_common(1)[0] if speaking else None,
        })
    return rows


def family_rates(rows):
    out = {}
    for fam in ("S", "I"):
        sub = [r for r in rows if r["family"] == fam]
        out[fam] = {"probes": len(sub),
                    "unanimous": sum(1 for r in sub if r["unanimous"]),
                    "disagreements": sum(1 for r in sub if not r["unanimous"]),
                    "rate": round(sum(1 for r in sub if r["unanimous"]) / len(sub), 4)}
    return out


def interop(seeds, iop):
    order = iop["seed_order"]
    truth = {s["name"]: s["bits"] for s in seeds}
    kind = {s["name"]: s["kind"] for s in seeds}
    m = iop["matrix"]

    self_fail = {r: set() for r in RUNTIMES}
    for r in RUNTIMES:
        for i, name in enumerate(order):
            if m[r][r][i] != truth[name]:
                self_fail[r].add(name)

    cross, decisive = [], []
    for producer in RUNTIMES:
        for parser in RUNTIMES:
            if producer == parser:
                continue
            for i, name in enumerate(order):
                got = m[parser][producer][i]
                if got == truth[name]:
                    continue
                rec = {"producer": producer, "parser": parser, "seed": name,
                       "kind": kind[name], "rendered": iop["produced"][producer][i],
                       "true_bits": truth[name], "parsed_bits": got,
                       "producer_self_fails_here": name in self_fail[producer],
                       "parser_self_fails_here": name in self_fail[parser]}
                cross.append(rec)
                if not rec["producer_self_fails_here"] and not rec["parser_self_fails_here"]:
                    decisive.append(rec)

    # A rendering that is not injective loses information before any parser
    # sees it: two distinct doubles arriving as the same text.
    collisions = {}
    for r in RUNTIMES:
        seen = defaultdict(list)
        for i, name in enumerate(order):
            seen[iop["produced"][r][i]].append(name)
        collisions[r] = {"colliding_renderings": sum(1 for v in seen.values() if len(v) > 1),
                         "seeds_involved": sum(len(v) for v in seen.values() if len(v) > 1),
                         "example": next(([k, v] for k, v in seen.items() if len(v) > 1), None)}

    # Session 66 found two observers wrong together and explained it by shared
    # lineage. This counts the same shape here, where there is no shared lineage
    # to explain it: seeds two runtimes render IDENTICALLY while both of them
    # fail their own round-trip on that seed.
    agree_and_wrong = {}
    for i, a in enumerate(RUNTIMES):
        for b in RUNTIMES[i + 1:]:
            same_and_wrong = [n for j, n in enumerate(order)
                              if iop["produced"][a][j] == iop["produced"][b][j]
                              and n in self_fail[a] and n in self_fail[b]]
            same = sum(1 for j in range(len(order))
                       if iop["produced"][a][j] == iop["produced"][b][j])
            agree_and_wrong["%s+%s" % (a, b)] = {
                "identical_renderings": same,
                "identical_and_both_self_fail": len(same_and_wrong),
                "named_examples": [n for n in same_and_wrong if kind[n] == "named"][:8],
            }

    # Independence is a claim, so it gets measured rather than asserted. Strip a
    # rendering down to its significant digits -- no sign, no point, no exponent,
    # no leading or trailing zeros -- and two runtimes that generate the same
    # digits everywhere are running the same digit-generation, however different
    # their dress. This does not prove shared code; it is behavioural evidence,
    # and it is the only kind available here (the binaries carry no provenance
    # strings: see work.md section 8).
    def digits(s):
        s = s.lower().split("e")[0].lstrip("+-").replace(".", "")
        return s.strip("0") or "0"

    digit_agreement = {}
    for i, a in enumerate(RUNTIMES):
        for b in RUNTIMES[i + 1:]:
            same_digits = sum(1 for j in range(len(order))
                              if digits(iop["produced"][a][j]) == digits(iop["produced"][b][j]))
            same_text = sum(1 for j in range(len(order))
                            if iop["produced"][a][j] == iop["produced"][b][j])
            digit_agreement["%s+%s" % (a, b)] = {
                "identical_digit_strings": same_digits, "identical_text": same_text,
                "of": len(order)}

    return {
        "seeds": len(order),
        "named": sum(1 for n in order if kind[n] == "named"),
        "drawn": sum(1 for n in order if kind[n] == "drawn"),
        "ordered_pairs": 20,
        "cells": len(order) * 25,
        "self_roundtrip_failures": {r: {
            "count": len(self_fail[r]),
            "of": len(order),
            "named_examples": sorted(n for n in self_fail[r] if kind[n] == "named")[:12],
        } for r in RUNTIMES},
        "cross_pair_failures": len(cross),
        "cross_pair_failures_by_pair": {
            "%s->%s" % (p, q): sum(1 for c in cross if c["producer"] == p and c["parser"] == q)
            for p in RUNTIMES for q in RUNTIMES if p != q},
        "decisive_failures": len(decisive),
        "decisive_examples": decisive[:10],
        "rendering_collisions": collisions,
        "agreement_without_correctness": agree_and_wrong,
        "digit_agreement": digit_agreement,
    }


def main():
    seeds = json.load(open(os.path.join(HERE, "seeds.json")))
    answers = json.load(open(os.path.join(HERE, "answers.json")))
    iop = json.load(open(os.path.join(HERE, "interop.json")))

    rows = probe_table(answers)
    res = {
        "session": 67,
        "date": "2026-08-22",
        "runtimes": {r: answers[r]["version"] for r in RUNTIMES},
        "unicode_versions": {r: answers[r].get("unicode_version") for r in RUNTIMES},
        "probes": rows,
        "family_agreement": family_rates(rows),
        "internal_checks": {r: answers[r]["checks"] for r in RUNTIMES},
        "interop": interop(seeds, iop),
    }
    sr = os.path.join(HERE, "shipped_rule.json")
    if os.path.exists(sr):
        d = json.load(open(sr))
        res["shipped_rule"] = {
            "perl_unicore_version": d["perl_unicore_version"],
            "shipped_sha256": d.get("shipped_sha256"),
            "remote_identical": d.get("remote", {}).get("identical_to_shipped"),
            "final_sigma_line": d["final_sigma_lines"][0] if d.get("final_sigma_lines") else None,
            "applies_final_sigma": d["applies_final_sigma"],
        }
    json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)

    fa = res["family_agreement"]
    print("Family S unanimous %d/%d   Family I unanimous %d/%d"
          % (fa["S"]["unanimous"], fa["S"]["probes"], fa["I"]["unanimous"], fa["I"]["probes"]))
    for r in RUNTIMES:
        c = res["internal_checks"][r]
        print("%-7s L1 %3d/%d  L2 %2d  L3 %2d  L4 %2d"
              % (r, c["L1_roundtrip"]["violations"], c["L1_roundtrip"]["tested"],
                 c["L2_loose_equality"]["transitivity_violations"],
                 c["L3_relational_coherence"]["violations"],
                 c["L4_division_identity"]["violations"]))
    i = res["interop"]
    print("cross-pair failures %d of %d cells · DECISIVE %d"
          % (i["cross_pair_failures"], i["cells"], i["decisive_failures"]))


if __name__ == "__main__":
    main()
