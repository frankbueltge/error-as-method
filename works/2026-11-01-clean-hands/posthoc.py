"""Session 166, experiment 46: POST HOC reading, written after results.json existed. Labelled; predicts nothing.
Category means of the people, the family (A medians) and each arm's account; within-category order; contact category means.
Run: python3 posthoc.py
"""
import json, statistics as st
from pathlib import Path
from score import load, spearman
HERE = Path(__file__).parent
plan, P, S, A, R, room = load()
mk = lambda a: [f"{a}{j}" for j in range(1, 7)]
fam = {k: st.median(A[m][k] for m in A) for k in S}
acc = {a: {k: st.mean(R[m][k] for m in mk(a)) for k in S} for a in "DBS"}
cats = sorted(set(P[k]["category"] for k in S))
out = {"label": "post hoc", "category_means": {}, "within_category_rho_people": {}}
for c in cats:
    ks = [k for k in S if P[k]["category"] == c]
    out["category_means"][c] = {"n": len(ks), "people": round(st.mean(P[k]["mean"] for k in ks), 2),
                                "family": round(st.mean(fam[k] for k in ks), 2),
                                **{a: round(st.mean(acc[a][k] for k in ks), 2) for a in "DBS"}}
contact = [k["id"] for k in plan["keys"] if k["role"] == "contact"]
out["contact_category_means_people"] = {c: round(st.mean(P[k]["mean"] for k in contact if P[k]["category"] == c), 2)
                                        for c in cats if any(P[k]["category"] == c for k in contact)}
# order explained by category alone: rho of people's means with their own category means
cm = {c: st.mean(P[k]["mean"] for k in S if P[k]["category"] == c) for c in cats}
out["rho_people_with_category_mean"] = round(spearman([cm[P[k]["category"]] for k in S], [P[k]["mean"] for k in S]), 3)
# within-category: residual order after removing each source's category means
def resid(vals):
    m = {c: st.mean(vals[k] for k in S if P[k]["category"] == c) for c in cats}
    return [vals[k] - m[P[k]["category"]] for k in S]
pr = resid({k: P[k]["mean"] for k in S})
for name, v in [("family", fam)] + [(a, acc[a]) for a in "DBS"]:
    out["within_category_rho_people"][name] = round(spearman(resid(v), pr), 3)
(HERE / "posthoc.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
