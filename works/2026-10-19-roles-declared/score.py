#!/usr/bin/env python3
"""Score S134.ROLES as PREDICTIONS.md fixes it. Stdlib, no network.

    python3 -I score.py     ->  writes results.json beside this script
"""
import json, os
from collections import Counter
H = os.path.dirname(os.path.abspath(__file__))
L = lambda p: json.load(open(os.path.join(H, p)))
taken = L("../2026-10-18-not-a-defect/order.json")["taken"]
ids = [f"E{i:02d}" for i in range(1, len(taken) + 1)]
refused = [i for i, (_, st) in zip(ids, taken) if st == "NAD"]
accepted = [i for i in ids if i not in refused]
arm = {"D1": "D", "D2": "D", "O1": "O", "O2": "O"}
code = {r: {e["id"]: e["wrong"] for e in L(f"readers/reader-{r}.json")} for r in arm}
for r in code:
    assert set(code[r]) == set(ids), r
PARTY = {"D": {"R": "submitter", "J": "standard"}, "O": {"J": "submitter", "R": "standard"}}
def party(r, i):
    c = code[r][i]
    return {"B": "both", "X": "neither"}.get(c) or PARTY[arm[r]][c]
agree = lambda a, b, sub: sum(code[a][i] == code[b][i] for i in sub)
res = {
    "refused_n": len(refused), "accepted_n": len(accepted),
    "D_agree_refused": agree("D1", "D2", refused),
    "S134.ROLES": "holds" if agree("D1", "D2", refused) >= 20 else "falsified",
    "O_agree_refused": agree("O1", "O2", refused),
    "party_all_four_agree_refused": sum(len({party(r, i) for r in arm}) == 1 for i in refused),
    "submitter_struck_refused": {r: sum(party(r, i) == "submitter" for i in refused) for r in arm},
    "standard_struck_accepted": {r: sum(party(r, i) == "standard" for i in accepted) for r in arm},
    "X_refused": {r: sum(code[r][i] == "X" for i in refused) for r in arm},
    "codes_refused": {r: dict(Counter(code[r][i] for i in refused)) for r in arm},
    "codes_accepted": {r: dict(Counter(code[r][i] for i in accepted)) for r in arm},
    "D_disagreements_refused": dict(Counter(f"{code['D1'][i]}/{code['D2'][i]}" for i in refused if code["D1"][i] != code["D2"][i])),
    "O_disagreements_refused": dict(Counter(f"{code['O1'][i]}/{code['O2'][i]}" for i in refused if code["O1"][i] != code["O2"][i])),
    "per_entry": [{"id": i, "issue": n, "status": st, **{r: code[r][i] for r in arm}, **{r + "_party": party(r, i) for r in arm}} for i, (n, st) in zip(ids, taken)],
}
s = res["submitter_struck_refused"]
res["predictions"] = {
    "P1": res["D_agree_refused"] >= 20,
    "P2": res["O_agree_refused"] >= 20,
    "P3": s["D1"] >= 10 and s["D2"] >= 10,
    "P4": s["O1"] >= 10 and s["O2"] >= 10,
    "P5": all(v >= 13 for v in res["standard_struck_accepted"].values()),
    "P6": any(v >= 8 for v in res["X_refused"].values()),
}
json.dump(res, open(os.path.join(H, "results.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "per_entry"}, indent=1))
