#!/usr/bin/env python3
"""Score C4 (S113.SIDE) from census.json, readers/reader-*.json and splits.json. Stdlib, no network."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
me = {r["id"]: r for r in json.load(open(os.path.join(H, "census.json")))["rows"]}
splits = json.load(open(os.path.join(H, "splits.json")))
res = {}
for k in "AB":
    rd = {r["id"]: r for r in json.load(open(os.path.join(H, "readers", f"reader-{k}.json")))}
    assert set(rd) == set(me)
    dis = sorted(i for i in me if rd[i]["wrong"] != me[i]["wrong"])
    assert set(dis) == set(splits[k]), (k, dis)
    n_split = sum(splits[k][i]["split"] for i in dis)
    tally = {c: sum(1 for r in rd.values() if r["wrong"] == c) for c in "JRBX"}
    res[k] = {"agree": 21 - len(dis), "disagreements": dis, "splits": n_split,
              "split_share": round(n_split / len(dis), 3) if dis else 0, "tally": tally,
              "P5_holds": 21 - len(dis) >= 14, "P4_holds": n_split * 3 <= len(dis)}
res["practice_tally"] = {c: sum(1 for r in me.values() if r["wrong"] == c) for c in "JRBX"}
res["held_named_all"] = all(r["held_named"] == "y" for r in me.values())
res["S113_SIDE_a_fires"] = not (res["A"]["P4_holds"] and res["B"]["P4_holds"])
res["S113_SIDE_b_fires"] = not res["held_named_all"]
json.dump(res, open(os.path.join(H, "results.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
