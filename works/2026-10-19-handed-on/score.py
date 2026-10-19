"""score.py -- scores P1-P6 of PREDICTIONS.md, mechanically, from versions.jsonl, coder/answer.json, coder/key.json
and the kept NOTE.md files. Written after all versions were kept and before the coder's answer existed."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
V = [json.loads(l) for l in open(os.path.join(HERE, "versions.jsonl"))]
key = json.load(open(os.path.join(HERE, "coder", "key.json")))
ans = json.load(open(os.path.join(HERE, "coder", "answer.json")))["pairs"]
arms = {"P": [], "T": [], "K": []}
codes = {}
for t, k in key.items():
    c = ans[t]["code"].strip().upper(); codes[(k["lineage"], k["to"])] = c; arms[k["arm"]].append(c)
ss = {a: sum(c in ("SCHEMA", "STRIKE") for c in cs) for a, cs in arms.items()}
schema = {a: sum(c == "SCHEMA" for c in cs) for a, cs in arms.items()}
ver = {(r["lineage"], r["v"]): r for r in V}
decl = {a: sum(1 for (L, v), r in ver.items() if v > 1 and r["arm"] == a and r["changed"] is False) for a in arms}
grew = {L: ver[(L, 4)]["bytes"] > ver[(L, 1)]["bytes"] for L in sorted({r["lineage"] for r in V})}
# P6: a T hand-over 'claims a change of schema' if its NOTE section ## v<k> answers (a), (b) and (c) and index.html changed
claims = []
for (L, v), r in sorted(ver.items()):
    if r["arm"] != "T" or v == 1: continue
    note = open(os.path.join(HERE, "lineages", L, "v%d" % v, "NOTE.md"), encoding="utf-8").read()
    sec = re.split(r"^## v%d\b" % v, note, flags=re.M)
    sec = re.split(r"^## v\d", sec[1], flags=re.M)[0] if len(sec) > 1 else ""
    has = all(re.search(r"\(%s\)" % x, sec) for x in "abc")
    claims.append({"lineage": L, "to": v, "answers_abc": has, "changed": r["changed"], "blind": codes[(L, v)]})
claimed = [c for c in claims if c["answers_abc"] and c["changed"]]
res = {
 "blind_codes": {a: cs for a, cs in arms.items()}, "schema_or_strike": ss, "schema": schema, "declines": decl,
 "bytes_v1_v4": {L: [ver[(L, 1)]["bytes"], ver[(L, 4)]["bytes"]] for L in grew},
 "P1": ss["T"] >= 2 * ss["P"] and decl["T"] <= decl["P"],
 "P2": abs(ss["K"] - ss["P"]) <= 1,
 "P3": ss["T"] - ss["K"] >= 3,
 "P4": all(grew.values()),
 "P5": decl["K"] == 0 and decl["P"] <= 1,
 "P6": len(claimed) >= 5 and sum(c["blind"] == "SCHEMA" for c in claimed) < len(claimed),
 "P6_detail": claims,
}
json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)
for p in ("P1", "P2", "P3", "P4", "P5", "P6"): print(p, "held" if res[p] else "FAILED")
print("SCHEMA+STRIKE", ss, "SCHEMA", schema, "declines", decl)
