#!/usr/bin/env python3
"""Score S127.DECLINE as PREDICTIONS.md fixes it. Stdlib, no network.

    python3 -I score.py     ->  writes results.json beside this script
"""
import json, os
from collections import Counter
H = os.path.dirname(os.path.abspath(__file__))
L = lambda p: json.load(open(os.path.join(H, p)))
taken = L("order.json")["taken"]
ids = [f"E{i:02d}" for i in range(1, len(taken) + 1)]
refused = {i for i, (_, st) in zip(ids, taken) if st == "NAD"}
coders = {"practice": L("practice.json"), "A": L("readers/reader-A.json"), "B": L("readers/reader-B.json")}
code = {c: {r["id"]: r["wrong"] for r in v} for c, v in coders.items()}
for c in code:
    assert set(code[c]) == set(ids), c
def cnt(c, sub):
    return Counter(code[c][i] for i in sub)
acc = [i for i in ids if i not in refused]
R = {c: cnt(c, refused)["R"] for c in code}
n = len(refused)
fifth = n / 5
gaps = {r: R["practice"] - R[r] for r in ("A", "B")}
falsified = n < 15 or any(g < fifth for g in gaps.values())
pairs = {}
for a, b in (("practice", "A"), ("practice", "B"), ("A", "B")):
    pairs[f"{a}-{b}"] = {
        "agree_all": sum(code[a][i] == code[b][i] for i in ids),
        "agree_refused": sum(code[a][i] == code[b][i] for i in refused),
        "agree_accepted": sum(code[a][i] == code[b][i] for i in acc),
        "disagreements_refused": dict(Counter(f"{code[a][i]}/{code[b][i]}" for i in sorted(refused) if code[a][i] != code[b][i])),
        "disagreements_accepted": dict(Counter(f"{code[a][i]}/{code[b][i]}" for i in acc if code[a][i] != code[b][i])),
    }
res = {
    "refused_n": n, "accepted_n": len(acc),
    "R_on_refused": R, "gap_practice_minus_reader": gaps, "required_gap": fifth,
    "S127.DECLINE": "falsified" if falsified else "holds",
    "rider_practice_share_below_11_of_27": R["practice"] / n < 11 / 27,
    "practice_share": R["practice"] / n, "session127_share": 11 / 27,
    "codes_refused": {c: dict(cnt(c, refused)) for c in code},
    "codes_accepted": {c: dict(cnt(c, acc)) for c in code},
    "all_three_J_on_accepted": sum(all(code[c][i] == "J" for c in code) for i in acc),
    "pairs": pairs,
    "per_entry": [{"id": i, "status": st, "issue": num, **{c: code[c][i] for c in code}} for i, (num, st) in zip(ids, taken)],
}
json.dump(res, open(os.path.join(H, "results.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ("R_on_refused", "gap_practice_minus_reader", "S127.DECLINE", "rider_practice_share_below_11_of_27", "all_three_J_on_accepted")}, indent=1))
for k, v in pairs.items(): print(k, v)
