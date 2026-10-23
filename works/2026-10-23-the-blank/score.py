"""Score The Blank against PREDICTIONS.md. Reads plan.json and rooms/<maker>.txt; writes results.json.

usage: python3 score.py
"""
import collections
import json
import random
import re

from usf import norm

plan = json.load(open("plan.json"))
keys = {k["id"]: k for arm in plan["keys"].values() for k in arm}


def parse(path):
    text = open(path).read()
    words = {}
    for m in re.finditer(r"^\s*(\d{1,2})\s*:\s*(.+?)\s*$", text, re.M):
        words[int(m.group(1))] = m.group(2)
    how = re.search(r"^HOW:\s*(.*)$", text, re.M)
    tools = re.search(r"^TOOLS:\s*(.*)$", text, re.M)
    return words, how.group(1) if how else None, tools.group(1) if tools else None


answers = collections.defaultdict(dict)  # key id -> maker -> raw word
makers = {}
for maker, order in plan["deal"].items():
    words, how, tools = parse(f"rooms/{maker}.txt")
    assert sorted(words) == list(range(1, 25)), (maker, sorted(words))
    makers[maker] = {"how": how, "tools": tools}
    for i, kid in enumerate(order):
        answers[kid][maker] = words[i + 1]


def human_distinct6(k, rng, n=20000):
    """Expected distinct words among six people drawn without replacement from a cue's group."""
    urn = []
    for w, c in k["people"]:
        urn += [w] * c
    urn += [f"_idio{i}" for i in range(k["G"] - len(urn))]
    return sum(len(set(rng.sample(urn, 6))) for _ in range(n)) / n


rng = random.Random(1530)
cells = {}
for kid, k in keys.items():
    arm = kid[0]
    raw = [answers[kid][f"{arm}{m}"] for m in range(1, 7)]
    w = [norm(x) for x in raw]
    count = collections.Counter(w)
    modal, modal_n = sorted(count.items(), key=lambda kv: (-kv[1], kv[0]))[0]
    c = {"arm": arm, "raw": raw, "norm": w, "unanimous": len(set(w[:3])) == 1,
         "unanimous6": len(set(w)) == 1, "modal": modal, "modal_n": modal_n,
         "modal_tie": list(count.values()).count(modal_n) > 1, "distinct6": len(count)}
    if arm == "S":
        c["people_top"] = k["people"][0][0]
        c["modal_is_people_top"] = modal == k["people"][0][0] and not c["modal_tie"]
        c["p_three_agree"] = k["p_three_agree"]
        c["people_distinct6"] = round(human_distinct6(k, rng), 3)
        G = k["G"]
        c["people_share"] = {x: round(n / G, 3) for x, n in k["people"]}
        c["makers_in_people"] = sum(1 for x in w if x in dict(k["people"]))
    if arm == "N":
        c["excluded"] = k["excluded"]
        c["used_excluded"] = sum(1 for x in w if x == k["excluded"])
        c["people_second"] = k["second"]
        c["modal_is_people_second"] = modal == k["second"] and not c["modal_tie"]
        S = cells.get("S" + kid[1:])
        c["modal_is_S_second"] = None  # filled below
    if arm == "P":
        c["kind"] = k["kind"]
        c["shared"] = k["shared"]
        c["modal_is_shared"] = k["shared"] is not None and modal == k["shared"] and not c["modal_tie"]
    cells[kid] = c

# N against the makers' own S answers: is the N word the family's second word on S?
for kid, c in cells.items():
    if c["arm"] == "N":
        s = cells["S" + kid[1:]]
        sc = collections.Counter(s["norm"])
        ranked = [x for x, _ in sorted(sc.items(), key=lambda kv: (-kv[1], kv[0]))]
        c["S_makers_words"] = ranked
        c["modal_in_S_makers"] = c["modal"] in sc

S = [c for k, c in sorted(cells.items()) if c["arm"] == "S"]
P = [c for k, c in sorted(cells.items()) if c["arm"] == "P"]
N = [c for k, c in sorted(cells.items()) if c["arm"] == "N"]
U = lambda cs: sum(c["unanimous"] for c in cs)
E = sum(c["p_three_agree"] for c in S)
mean = lambda xs: sum(xs) / len(xs)

summary = {
    "S_unanimous": U(S), "P_unanimous": U(P), "N_unanimous": U(N),
    "P_forced_unanimous": U([c for c in P if c["kind"] == "FORCED"]),
    "P_unforced_unanimous": U([c for c in P if c["kind"] == "UNFORCED"]),
    "S_unanimous6": sum(c["unanimous6"] for c in S),
    "P_unanimous6": sum(c["unanimous6"] for c in P),
    "N_unanimous6": sum(c["unanimous6"] for c in N),
    "people_E_three_agree_S": round(E, 3),
    "S_modal_is_people_top": sum(c["modal_is_people_top"] for c in S),
    "S_mean_distinct6_makers": round(mean([c["distinct6"] for c in S]), 3),
    "S_mean_distinct6_people": round(mean([c["people_distinct6"] for c in S]), 3),
    "S_maker_words_in_people_list": sum(c["makers_in_people"] for c in S),
    "N_modal_is_people_second": sum(c["modal_is_people_second"] for c in N),
    "N_used_excluded": sum(c["used_excluded"] for c in N),
    "N_modal_in_S_makers_words": sum(c["modal_in_S_makers"] for c in N),
    "P_forced_modal_is_shared": sum(c["modal_is_shared"] for c in P),
}
s = summary
verdicts = {
    "R1": {"rule": ">=24 of 48 P+N unanimous (falsifies below); predicted >=30",
           "value": s["P_unanimous"] + s["N_unanimous"],
           "row_holds": s["P_unanimous"] + s["N_unanimous"] >= 24,
           "prediction_held": s["P_unanimous"] + s["N_unanimous"] >= 30},
    "R2": {"rule": ">=4 of 12 UNFORCED unanimous (falsifies below); predicted >=5",
           "value": s["P_unforced_unanimous"],
           "row_holds": s["P_unforced_unanimous"] >= 4,
           "prediction_held": s["P_unforced_unanimous"] >= 5},
    "H1": {"rule": "S unanimous >= 2E (and predicted >=12)", "value": s["S_unanimous"],
           "two_E": round(2 * E, 2), "held": s["S_unanimous"] >= 2 * E and s["S_unanimous"] >= 12},
    "H2": {"rule": "S modal = people's top on >=16", "value": s["S_modal_is_people_top"],
           "held": s["S_modal_is_people_top"] >= 16},
    "H3": {"rule": "makers' mean distinct6 <= half people's",
           "value": [s["S_mean_distinct6_makers"], s["S_mean_distinct6_people"]],
           "held": s["S_mean_distinct6_makers"] <= s["S_mean_distinct6_people"] / 2},
    "H4": {"rule": "N unanimous >=12 and N modal = people's second on >=8",
           "value": [s["N_unanimous"], s["N_modal_is_people_second"]],
           "held": s["N_unanimous"] >= 12 and s["N_modal_is_people_second"] >= 8},
    "H5": {"rule": "FORCED unanimous > UNFORCED unanimous",
           "value": [s["P_forced_unanimous"], s["P_unforced_unanimous"]],
           "held": s["P_forced_unanimous"] > s["P_unforced_unanimous"]},
}
json.dump({"summary": summary, "verdicts": verdicts, "cells": cells, "makers": makers},
          open("results.json", "w"), indent=1)
print(json.dumps(summary, indent=1))
print(json.dumps(verdicts, indent=1))
