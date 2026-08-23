#!/usr/bin/env python3
"""Apply the scoring rule fixed in PREDICTIONS.md before the first measurement.

Nothing in this script decides whether a party is WRONG -- that is condition 2, and it is
adjudicated by hand in adjudication.json, because it cannot be done mechanically without
smuggling in the very norm whose necessity is the question. What this script decides is
condition 3: whether a divergence could have been found by one party alone.

Cell outcomes: ok | refused | silent
A silent cell is INVISIBLE TO BOTH PARTIES ALONE iff
  - the producer, in the producer's own zone, round-trips that same string, and
  - the parser, in the parser's own zone, round-trips its own rendering of the same instant.
Each party is only ever asked what it could do in its OWN environment, because that is all a
party alone has. Where a self-check is unavailable -- Perl parses nothing, so no Perl-produced
cell has one -- the cell is NOT counted as both-invisible, and the exclusion is reported as its
own number rather than folded into the negative.
"""
import json
import datetime as dt
from collections import Counter
from zoneinfo import ZoneInfo

PRODUCERS = ["python", "node", "ruby", "php", "perl"]
PARSERS = ["python", "node", "ruby", "php"]
FORMS = ["default", "iso"]
FAMILY = {"default": "D0", "iso": "D1"}


def offset_seconds(epoch, tzname):
    """Local UTC offset at an instant, from this machine's tzdata. Used only to NAME the shape
    of a difference, never to decide who is right."""
    if tzname == "UTC":
        return 0
    return int(dt.datetime.fromtimestamp(epoch, ZoneInfo(tzname)).utcoffset().total_seconds())


def classify(delta, epoch, pz, qz):
    """Name the shape of a difference. The harness's vocabulary, not a verdict."""
    if abs(delta) < 1e-6:
        return "none"
    po, qo = offset_seconds(epoch, pz), offset_seconds(epoch, qz)
    if abs(abs(delta) - abs(po - qo)) < 1e-6 and po != qo:
        return "zone-difference"
    if po == qo and abs(abs(delta) - abs(po)) < 1e-6 and po:
        return "zone-offset"
    if abs(delta) < 1.0:
        return "sub-second"
    if abs(delta) % 3600 == 0:
        return "whole-hour"
    if abs(delta) % 60 == 0:
        return "whole-minute"
    return "other"


def unpack(m):
    """matrix.json stores a parse result as a NUMBER (the epoch seconds recovered) or a STRING
    (the parser's refusal message). Restore the two-field form the rest of this script reads."""
    return {tz: {rt: [{"status": "ok", "epoch": v} if isinstance(v, (int, float))
                      else {"status": "refused", "error": v}
                      for v in col]
                 for rt, col in byrt.items()}
            for tz, byrt in m["parse"].items()}


def build(m):
    zones, idx = m["zones"], m["string_index"]
    render, instants = m["render"], m["instants"]
    parse = unpack(m)
    labels, n_chosen = m["labels"], m["n_chosen"]

    def selfclean(rt, zone, i, form):
        """Can rt, alone, in its own zone, see that its own rendering does not come back?
        True = round-trip clean, False = rt can see it itself, None = unavailable."""
        if rt not in PARSERS:
            return None
        s = render[zone][rt][i][form]
        if s is None:
            return None
        r = parse[zone][rt][idx[s]]
        if r["status"] != "ok":
            return False
        return abs(r["epoch"] - instants[i]) < 1e-6

    rows = []
    for form in FORMS:
        for p in PRODUCERS:
            for pz in zones:
                for q in PARSERS:
                    for qz in zones:
                        for i, e in enumerate(instants):
                            s = render[pz][p][i][form]
                            if s is None:
                                continue
                            r = parse[qz][q][idx[s]]
                            c = {"family": FAMILY[form], "producer": p, "producer_zone": pz,
                                 "parser": q, "parser_zone": qz, "instant": i,
                                 "label": labels[i], "chosen": i < n_chosen,
                                 "cross_party": p != q, "same_zone": pz == qz, "string": s}
                            if r["status"] == "refused":
                                c["outcome"], c["error"] = "refused", r["error"]
                            else:
                                d = r["epoch"] - e
                                if abs(d) < 1e-6:
                                    c["outcome"] = "ok"
                                else:
                                    c.update({"outcome": "silent", "delta": d,
                                              "recovered": r["epoch"], "intended": e,
                                              "shape": classify(d, e, pz, qz)})
                            sp, sq = selfclean(p, pz, i, form), selfclean(q, qz, i, form)
                            c["producer_selfclean"], c["parser_selfclean"] = sp, sq
                            c["selfcheck_unavailable"] = sp is None or sq is None
                            c["both_invisible"] = bool(
                                c["outcome"] == "silent" and c["cross_party"]
                                and sp is True and sq is True)
                            rows.append(c)
    return rows


def summarise(rows, **filt):
    sel = [r for r in rows if all(r.get(k) == v for k, v in filt.items())]
    out = {"n": len(sel)}
    for o in ("ok", "refused", "silent"):
        out[o] = sum(1 for r in sel if r["outcome"] == o)
    out["both_invisible"] = sum(1 for r in sel if r["both_invisible"])
    out["silent_excluded_no_selfcheck"] = sum(
        1 for r in sel if r["outcome"] == "silent" and r["selfcheck_unavailable"])
    return out


def main():
    m = json.load(open("matrix.json"))
    rows = build(m)
    zones = m["zones"]
    cross = [r for r in rows if r["cross_party"]]
    same = [r for r in cross if r["same_zone"]]
    diff = [r for r in cross if not r["same_zone"]]

    rep = {
        "cells_total": len(rows),
        "cross_party": summarise(rows, cross_party=True),
        "cross_party_same_zone": {**summarise(same),
                                  "note": "the matrix as first designed, now over three zones"},
        "cross_party_cross_zone": {**summarise(diff),
                                   "note": "the repair: producer and parser in different zones"},
        "by_family": {f: summarise(cross, family=f) for f in ("D0", "D1")},
        "by_family_same_zone": {f: summarise(same, family=f) for f in ("D0", "D1")},
        "by_zone_same": {z: summarise([r for r in same if r["producer_zone"] == z])
                         for z in zones},
    }

    bi = [r for r in rows if r["both_invisible"]]
    rep["both_invisible"] = {
        "n": len(bi),
        "same_zone": sum(1 for r in bi if r["same_zone"]),
        "cross_zone": sum(1 for r in bi if not r["same_zone"]),
        "by_family": dict(Counter(r["family"] for r in bi)),
        "shapes": dict(Counter(r["shape"] for r in bi).most_common()),
        "pairs": dict(Counter(f"{r['producer']}->{r['parser']}" for r in bi).most_common()),
        "shapes_same_zone": dict(
            Counter(r["shape"] for r in bi if r["same_zone"]).most_common()),
    }

    # ---- P6: same producer, parser, instant, form and BYTE-IDENTICAL string; different zone;
    #          different outcome. The purest form of the question.
    bykey = {}
    for r in rows:
        if not r["cross_party"] or not r["same_zone"]:
            continue
        bykey.setdefault((r["family"], r["producer"], r["parser"], r["instant"]), {})[
            r["producer_zone"]] = r
    flips, flips_same_string = [], []
    for k, byzone in bykey.items():
        outs = {z: byzone[z]["outcome"] for z in byzone}
        if len(set(outs.values())) > 1:
            rec = {"family": k[0], "producer": k[1], "parser": k[2],
                   "label": byzone[next(iter(byzone))]["label"], "outcomes": outs,
                   "strings": {z: byzone[z]["string"] for z in byzone}}
            flips.append(rec)
            if len(set(rec["strings"].values())) == 1:
                flips_same_string.append(rec)
    ok_then_silent = [f for f in flips
                      if "ok" in f["outcomes"].values() and "silent" in f["outcomes"].values()]
    rep["zone_flips"] = {
        "cells_whose_outcome_depends_on_TZ": len(flips),
        "of_those_ok_in_one_zone_and_silent_in_another": len(ok_then_silent),
        "of_those_on_a_byte_identical_string": len(
            [f for f in ok_then_silent if len(set(f["strings"].values())) == 1]),
        "examples": [f for f in ok_then_silent
                     if len(set(f["strings"].values())) == 1][:4],
    }

    # ---- refusals
    rep["refusals"] = dict(Counter(
        f"{r['producer']}->{r['parser']}" for r in cross if r["outcome"] == "refused").most_common())

    # ---- family N (identical under every zone; taken from the first)
    z0 = zones[0]
    rep["family_N"] = [
        {"string": s, **{rt: m["numparse"][z0][rt][i] for rt in PRODUCERS}}
        for i, s in enumerate(m["numbers"])]

    # ---- prediction scoring, thresholds exactly as written in PREDICTIONS.md
    d0 = rep["by_family_same_zone"]["D0"]["silent"]
    d1 = rep["by_family_same_zone"]["D1"]["silent"]
    top = next(iter(rep["both_invisible"]["shapes"]), None)
    rep["predictions"] = {
        "P1  D0 cross-party silent cells > 100":
            {"value": d0, "verdict": "confirmed" if d0 > 100 else "refuted"},
        "P2  at least one both-invisible cell":
            {"value": rep["both_invisible"]["n"],
             "verdict": "confirmed" if rep["both_invisible"]["n"] >= 1 else "refuted"},
        "P3  zero both-invisible cells LOCATE an error":
            {"value": "hand-adjudicated", "verdict": "see adjudication.json"},
        "P4  largest both-invisible shape is a zone difference":
            {"value": rep["both_invisible"]["shapes"],
             "verdict": "confirmed" if top in ("zone-difference", "zone-offset") else "refuted"},
        "P5  D1 silent < one tenth of D0 silent":
            {"value": {"D0": d0, "D1": d1},
             "verdict": "confirmed" if d1 * 10 < d0 else "refuted"},
        "P6  at least one cell ok in one zone and silent in another":
            {"value": rep["zone_flips"]["of_those_ok_in_one_zone_and_silent_in_another"],
             "verdict": "confirmed"
                        if rep["zone_flips"]["of_those_ok_in_one_zone_and_silent_in_another"]
                        else "refuted"},
        "P7  every refusal is the parser's own report":
            {"value": True, "verdict": "confirmed by construction"},
        "P8  two runtimes agree and are both wrong in family N":
            {"value": "hand-adjudicated", "verdict": "see adjudication.json"},
        "P9  no runtime is defective":
            {"value": "hand-adjudicated", "verdict": "see adjudication.json"},
        "P10 falsifier not met, failing at condition 2 rather than condition 3":
            {"value": "condition 3 satisfied iff P2 confirmed; condition 2 by hand",
             "verdict": "see adjudication.json"},
    }

    with open("verdict.json", "w") as fh:
        json.dump(rep, fh, indent=1)
    with open("both-invisible.json", "w") as fh:
        json.dump({"n": len(bi), "note": "first 500 rows", "rows": bi[:500]}, fh, indent=1)

    print(f"cells {rep['cells_total']}  cross-party {rep['cross_party']}")
    print(f"  same-zone  {rep['cross_party_same_zone']}")
    print(f"  cross-zone {rep['cross_party_cross_zone']}")
    print(f"  D0 {rep['by_family_same_zone']['D0']}  D1 {rep['by_family_same_zone']['D1']}")
    print(f"  both-invisible {rep['both_invisible']['n']} "
          f"(same-zone {rep['both_invisible']['same_zone']}, "
          f"cross-zone {rep['both_invisible']['cross_zone']})")
    print(f"  shapes {rep['both_invisible']['shapes']}")
    print(f"  pairs  {rep['both_invisible']['pairs']}")
    print(f"  flips  {  {k: v for k, v in rep['zone_flips'].items() if k != 'examples'} }")
    print(f"  refusals {rep['refusals']}")


if __name__ == "__main__":
    main()
