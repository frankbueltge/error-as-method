"""Score Before the Verdict against PREDICTIONS.md. Reads verdicts.jsonl and NORMS.md; writes results.json.
Age classes: A = decisive norm in N0 (committed before the material); B = minted at an earlier variant;
C = minted at this very variant. Revision lines (those with 'revises') are reported apart and do not enter Q1-Q5."""
import json, re, os
V = [json.loads(l) for l in open("verdicts.jsonl")]
prim = [v for v in V if "revises" not in v]
minted_at = {}
for v in prim:
    for n in v.get("minted", []): minted_at[n] = v["order"]
def age(v):
    d = v["decisive"]
    if d.startswith("N0"): return "A"
    return "C" if minted_at[d] == v["order"] else "B"
for v in prim: v["age"] = age(v)
grid = [v for v in prim if v["variant"] < 24]
fails = [v for v in grid if v["verdict"] == "fails"]
cnt = lambda xs, k: sum(1 for x in xs if x["age"] == k)
n0 = [n for n in re.findall(r"\*\*(N0\.\d)\*\*", open("NORMS.md").read())]
decided = {v["decisive"] for v in prim}
minted_grid = [n for n, o in minted_at.items() if o <= 24]
r = {
 "verdicts_grid": {k: sum(1 for v in grid if v["verdict"] == k) for k in ("works", "fails", "unsure")},
 "fails_by_age": {k: cnt(fails, k) for k in "ABC"},
 "all_grid_by_age": {k: cnt(grid, k) for k in "ABC"},
 "minted": minted_at,
 "n0_never_decisive": [n for n in n0 if n not in decided],
 "revisions": [v for v in V if "revises" in v],
 "per_verdict": [{k: v[k] for k in ("order", "variant", "verdict", "decisive", "age")} for v in prim],
}
Q = {}
Q["Q1"] = {"pred": "at most 6 of 24 work", "value": r["verdicts_grid"]["works"], "held": r["verdicts_grid"]["works"] <= 6}
fa = r["fails_by_age"]["A"]; Q["Q2"] = {"pred": "fewer than half of fails decided by N0", "value": f"{fa} of {len(fails)}", "held": fa < len(fails) / 2}
Q["Q3"] = {"pred": ">= 3 norms minted while judging (grid)", "value": len(minted_grid), "held": len(minted_grid) >= 3}
early = sum(1 for n in minted_grid if minted_at[n] <= 12)
Q["Q4"] = {"pred": ">= 2/3 of grid-minted norms in batches 1-2", "value": f"{early} of {len(minted_grid)}", "held": early >= 2 / 3 * len(minted_grid)}
Q["Q5"] = {"pred": "at least one N0 norm decides nothing", "value": r["n0_never_decisive"], "held": len(r["n0_never_decisive"]) >= 1}
v24 = [v for v in prim if v["variant"] == 24][0]
Q["Q6"] = {"pred": "V24 mints no new norm", "value": v24.get("minted", []), "held": not v24.get("minted")}
Q["R1"] = {"rule": "any fails with decisive norm of class C -> Session 60 falsifier 2 fires", "value": r["fails_by_age"]["C"], "fires": r["fails_by_age"]["C"] + (1 if v24["age"] == "C" and v24["verdict"] == "fails" else 0) > 0}
r["predictions"] = Q
json.dump(r, open("results.json", "w"), indent=1)
for k, q in Q.items(): print(k, q)
print("fails by age", r["fails_by_age"], "| all grid by age", r["all_grid_by_age"], "| verdicts", r["verdicts_grid"])
