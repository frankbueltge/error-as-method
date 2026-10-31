"""Session 165, experiment 45 (Paired): POST HOC readings, written after results.json existed. Nothing here is a
prediction or a test of one; it says where the scored numbers came from.

1. Per maker: Spearman rho of its stated means with the people's means and with the family medians, and the SD of
   its stated means (how much order it dared to state).
2. The S arm split by whether the maker said its contact numbers did not fit the pictures (hand coding, PREDICTIONS.md
   P6, quoted in the journal): noticed S1, S3, S5, S6; borderline S2; not S4.
3. Within-kind order: rho over the scored keys of the release's two largest categories (dogs and cats, file digits 1
   and 2) and over the rest, for the family and each arm, so that 'order' is not only 'cats above crocodiles'.
4. Where the family and the people part most: the keys with the largest |people mean - family median|.
Run: python3 posthoc.py
"""
import json, statistics as st
from pathlib import Path
from score import load, spearman

HERE = Path(__file__).parent
plan, P, S, A, R, room = load()
fam = {k: st.median(A[m][k] for m in A) for k in S}
pm = {k: P[k]["mean"] for k in S}
out = {"makers": {}}
for m in list(A) + list(R):
    v = {k: (A[m][k] if m in A else R[m][k]["mean"]) for k in S}
    out["makers"][m] = {"rho_people": round(spearman([v[k] for k in S], [pm[k] for k in S]), 3),
                        "rho_family": round(spearman([v[k] for k in S], [fam[k] for k in S]), 3),
                        "sd_of_stated": round(st.pstdev(v.values()), 3),
                        "mae": None if m in A else round(st.mean(abs(v[k] - pm[k]) for k in S), 3)}
out["people_sd_of_means"] = round(st.pstdev(pm.values()), 3)
groups = {"S_noticed": ["S1", "S3", "S5", "S6"], "S_borderline": ["S2"], "S_not": ["S4"]}
for g, ms in groups.items():
    acc = {k: st.mean(R[m][k]["mean"] for m in ms) for k in S}
    out[g] = {"rho_people": round(spearman([acc[k] for k in S], [pm[k] for k in S]), 3),
              "sd_of_stated_mean": round(st.mean(out["makers"][m]["sd_of_stated"] for m in ms), 3),
              "mae": round(st.mean(out["makers"][m]["mae"] for m in ms), 3)}
kind = {"dogs_cats": [k for k in S if P[k]["file"][0] in "12"], "other": [k for k in S if P[k]["file"][0] not in "12"]}
out["within_kind"] = {}
for g, ks in kind.items():
    row = {"n": len(ks), "family": round(spearman([fam[k] for k in ks], [pm[k] for k in ks]), 3)}
    for a in "DBS":
        acc = {k: st.mean(R[f"{a}{j}"][k]["mean"] for j in range(1, 7)) for k in ks}
        row[a] = round(spearman([acc[k] for k in ks], [pm[k] for k in ks]), 3)
    out["within_kind"][g] = row
gap = sorted(S, key=lambda k: -abs(pm[k] - fam[k]))[:8]
out["largest_gaps"] = [{"key": k, "species": P[k]["species"], "people": round(pm[k], 2), "family": fam[k],
                        **{a: round(st.mean(R[f"{a}{j}"][k]["mean"] for j in range(1, 7)), 2) for a in "DBS"}} for k in gap]
(HERE / "posthoc.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
for k, v in out.items():
    if k != "makers": print(k, v)
for m, v in out["makers"].items(): print(m, v)
