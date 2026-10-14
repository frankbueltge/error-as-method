#!/usr/bin/env python3
"""Score S120.ACCOUNT from entries.json, practice.json and readers/reader-*.json. Stdlib, no network.

Rules in PREDICTIONS.md: a disagreement is a reader's `wrong` differing from the practice's; a
side-split is a disagreement in which one code is J and the other R; split share per group pooled
over both readers. Falsified if share(A) <= share(S); not testable if pooled disagreements < 5 in a group.
"""
import json, os, collections
H = os.path.dirname(os.path.abspath(__file__))
grp = {r["label"]: r["group"] for r in json.load(open(os.path.join(H, "entries.json")))["rows"]}
st = {r["label"]: r["status"] for r in json.load(open(os.path.join(H, "entries.json")))["rows"]}
me = {r["id"]: r for r in json.load(open(os.path.join(H, "practice.json")))["rows"]}
rd = {k: {r["id"]: r for r in json.load(open(os.path.join(H, "readers", f"reader-{k}.json")))} for k in "AB"}
for k in "AB":
    assert set(rd[k]) == set(me) == set(grp), k
split = lambda a, b: {a, b} == {"J", "R"}
HOLDER = ["implement", "vendor", "author", "working group", "wg", "iesg", "mailing list", "list discussion",
          "reporter", "submitter", "operator", "user", "deploy", "consensus", "editor", "intended", "intent"]
def names_party(t):
    t = t.lower()
    return any((w in t.split()) if w == "wg" else (w in t) for w in HOLDER)
res = {"per_reader": {}, "pooled": {}, "reader_vs_reader": {}, "holder": {}}
for g in "SA":
    ids = [i for i in me if grp[i] == g]
    pool = {"entries": len(ids), "disagreements": 0, "splits": 0, "b_half": 0.0, "list": []}
    for k in "AB":
        dis = [i for i in ids if rd[k][i]["wrong"] != me[i]["wrong"]]
        sp = [i for i in dis if split(rd[k][i]["wrong"], me[i]["wrong"])]
        bh = sum(1 for i in dis if "B" in (rd[k][i]["wrong"], me[i]["wrong"]) and
                 {rd[k][i]["wrong"], me[i]["wrong"]} <= {"J", "R", "B"})
        res["per_reader"][f"{k}-{g}"] = {"agree": len(ids) - len(dis), "disagreements": len(dis), "splits": len(sp),
            "share": round(len(sp) / len(dis), 3) if dis else None,
            "pairs": dict(collections.Counter(f"{me[i]['wrong']}>{rd[k][i]['wrong']}" for i in dis))}
        pool["disagreements"] += len(dis); pool["splits"] += len(sp); pool["b_half"] += 0.5 * bh
        pool["list"] += [{"reader": k, "id": i, "eid": None, "practice": me[i]["wrong"], "reader_code": rd[k][i]["wrong"],
                          "status": st[i], "split": split(rd[k][i]["wrong"], me[i]["wrong"])} for i in dis]
    pool["share"] = round(pool["splits"] / pool["disagreements"], 3) if pool["disagreements"] else None
    pool["share_with_B_half"] = round((pool["splits"] + pool["b_half"]) / pool["disagreements"], 3) if pool["disagreements"] else None
    res["pooled"][g] = pool
    rr = [i for i in ids if rd["A"][i]["wrong"] != rd["B"][i]["wrong"]]
    res["reader_vs_reader"][g] = {"disagreements": len(rr), "splits": sum(split(rd["A"][i]["wrong"], rd["B"][i]["wrong"]) for i in rr)}
    for k in "AB":
        n = sum(names_party(rd[k][i]["held"]) for i in ids)
        res["holder"][f"{k}-{g}"] = {"held_names_party": n, "of": len(ids), "share": round(n / len(ids), 3)}
    res["holder"][f"practice-{g}"] = {"held_names_party": sum(names_party(me[i]["held"]) for i in ids), "of": len(ids)}
pa, ps = res["pooled"]["A"], res["pooled"]["S"]
res["testable"] = pa["disagreements"] >= 5 and ps["disagreements"] >= 5
res["S120_ACCOUNT_falsified"] = (not res["testable"]) or (pa["share"] or 0) <= (ps["share"] or 0)
res["verdict"] = ("not testable" if not res["testable"] else
                  ("falsified" if res["S120_ACCOUNT_falsified"] else "holds"))
res["tallies"] = {k: dict(collections.Counter(r["wrong"] for r in rd[k].values())) for k in "AB"}
res["tallies"]["practice"] = dict(collections.Counter(r["wrong"] for r in me.values()))
json.dump(res, open(os.path.join(H, "results.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ("per_reader", "reader_vs_reader", "holder", "testable", "verdict", "tallies")}, indent=1))
print("pooled A", {k: v for k, v in pa.items() if k != "list"}); print("pooled S", {k: v for k, v in ps.items() if k != "list"})
