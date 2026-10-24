#!/usr/bin/env python3
"""Session 155 (the seventh night): is "typical of people" the same as "the people's answer"?

Andueza Rodriguez, Candito & Huyghe (arXiv:2603.18171, section 4.1) measure how human-typical a
model's word associations are by the standardized strength SS1: for cue c and response r,
S1(c, r) is the share of people whose first response to c was r, and
SS1(c, r) = (S1(c, r) - mean S1(c, *)) / SD(S1(c, *)), the mean and SD taken over the unique human
responses to c. tok-SS1 averages SS1 over a respondent's response tokens (eq. 2). They read a high
tok-SS1 as one "prototypical" participant giving "the associations most commonly produced".

Session 153 (works/2026-10-23-the-blank/) found the family's modal word to be the people's
commonest on only 8 of 24 USF cues. This script applies the paper's measure, unchanged in form, to
the same 24 cues and the same 144 maker answers, to see whether the measure can tell the two apart.

Inputs are committed by Session 153: plan.json (the people's listed responses and counts per cue,
quoted from USF Appendix A) and results.json (the six makers' normalised answers per cue).
Two adaptations, both forced by USF and declared:
  * USF Appendix A lists only responses written by two or more people. The rest of each cue's
    G participants wrote idiosyncratic responses, one person each (Appendix A's own description,
    as usf.py records it). They are restored here as G - sum(listed) singletons.
  * SD is the population SD over unique responses. The paper does not say which; the sample SD
    is also computed and reported, and no verdict below changes with it.
Post hoc, on data already scored. Nothing here was predicted.
"""
import json
import os
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BLANK = os.path.join(HERE, "..", "..", "..", "..", "..", "works", "2026-10-23-the-blank")


def strengths(G, people):
    listed = [n for _, n in people]
    singles = G - sum(listed)
    assert singles >= 0
    s = [n / G for n in listed] + [1 / G] * singles
    return {w: n / G for w, n in people}, s


def main(sd_kind="pop"):
    plan = json.load(open(os.path.join(BLANK, "plan.json")))
    res = json.load(open(os.path.join(BLANK, "results.json")))
    sdf = st.pstdev if sd_kind == "pop" else st.stdev
    rows = []
    for k in plan["keys"]["S"]:
        cid, G, people = k["id"], k["G"], k["people"]
        S1, dist = strengths(G, people)
        mu, sd = st.mean(dist), sdf(dist)
        ss = lambda w: ((S1.get(w, 0.0)) - mu) / sd
        makers = res["cells"][cid]["norm"]
        tok_family = st.mean(ss(w) for w in makers)
        # the people's own tok-SS1: every person's token, singletons included
        tok_people = (sum(n * ss(w) for w, n in people) + (G - sum(n for _, n in people)) * ((1 / G - mu) / sd)) / G
        top = people[0][0]
        modal = res["cells"][cid]["modal"]
        rows.append({
            "id": cid, "cue": k["cue"], "G": G, "unique_human_responses": len(dist),
            "people_top": top, "people_top_SS1": round(ss(top), 2),
            "family_modal": modal, "modal_is_top": modal == top,
            "family_tok_SS1": round(tok_family, 2), "people_tok_SS1": round(tok_people, 2),
            "family_above_people": tok_family > tok_people,
        })
    off = [r for r in rows if not r["modal_is_top"]]
    on = [r for r in rows if r["modal_is_top"]]
    summary = {
        "sd": sd_kind,
        "cues": len(rows),
        "family_mean_tok_SS1": round(st.mean(r["family_tok_SS1"] for r in rows), 2),
        "people_mean_tok_SS1": round(st.mean(r["people_tok_SS1"] for r in rows), 2),
        "cues_family_above_people": sum(r["family_above_people"] for r in rows),
        "modal_is_people_top": len(on),
        "off_top_cues": len(off),
        "off_top_family_mean_tok_SS1": round(st.mean(r["family_tok_SS1"] for r in off), 2),
        "off_top_cues_family_above_people": sum(r["family_above_people"] for r in off),
        "on_top_family_mean_tok_SS1": round(st.mean(r["family_tok_SS1"] for r in on), 2),
        "paper_reference": "arXiv:2603.18171 Table 1: human tok-SS1 1.67 (490 SWOW cues); largest model 2.56 at temperature 1",
    }
    return {"summary": summary, "rows": rows}


if __name__ == "__main__":
    out = {"population_sd": main("pop"), "sample_sd": main("sample")}
    json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    for k, v in out.items():
        print(k, json.dumps(v["summary"], indent=1))
    for r in out["population_sd"]["rows"]:
        print(r["id"], r["cue"], r["people_top"], r["family_modal"], r["modal_is_top"], r["family_tok_SS1"], r["people_tok_SS1"])
