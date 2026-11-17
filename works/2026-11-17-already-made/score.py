"""Score P1-P5 and P8 as committed in PREDICTIONS.md; P6 and P7 are readings (P6-reading.md, P7-reading.md).
Also writes face-data.js. Usage: score.py <werke.json> <cache>"""
import sys, json, re
import numpy as np
from shelf import load_atlas, embedder, parse_proposals, mean_pairwise, PRIZE

atlas, sha = load_atlas(sys.argv[1])
embed = embedder(sys.argv[2])
A = np.load("atlas_vectors.npy").astype(np.float64)
base = json.load(open("baseline.json"))
nb = json.load(open("neighbours.json"))
assert sha == base["atlas_sha256"]

R = {1: {}, 2: {}}
for r in (1, 2):
    for m in range(1, 9):
        for i, p in enumerate(parse_proposals(open(f"makings/r{r}-m{m}.txt").read()), 1):
            R[r][f"m{m}.{i}"] = p
keys = sorted(R[1])
assert len(keys) == 24 and sorted(R[2]) == keys
V1 = embed(R[1][k]["move"] for k in keys)
V2 = embed(R[2][k]["move"] for k in keys)
S1, S2 = V1 @ A.T, V2 @ A.T
nn1 = S1.max(1)
S2x = S2.copy()
for j, k in enumerate(keys):
    for n in nb[k]:
        S2x[j, n["idx"]] = -1
nn2x = S2x.max(1)
nn2 = S2.max(1)
top1 = S1.argmax(1)
prize = np.array([bool(PRIZE.search(a.get("venue_prize") or "")) for a in atlas])

# P3: material coded by hand from the MATERIAL lines (my coding; see journal)
from score_mat import MAT
makers_by_src = {}
for k, s in MAT.items():
    makers_by_src.setdefault(s, set()).add(k.split(".")[0])
src_counts = {s: len(v) for s, v in sorted(makers_by_src.items(), key=lambda x: -len(x[1]))}

res = {
  "P1": {"r1_nn_median": float(np.median(nn1)), "threshold": base["loo_nn_median"],
         "holds": bool(np.median(nn1) >= base["loo_nn_median"])},
  "P2": {"r1_mean_pairwise": float(mean_pairwise(V1)), "threshold": base["null24_p95"],
         "holds": bool(mean_pairwise(V1) > base["null24_p95"])},
  "P3": {"makers_per_source": src_counts, "holds": max(src_counts.values()) >= 3},
  "P4": {"r2_nn_median_excluding_shown": float(np.median(nn2x)), "threshold": base["loo_nn_p10"],
         "holds": bool(np.median(nn2x) >= base["loo_nn_p10"])},
  "P5": {"r1_mean_pairwise": float(mean_pairwise(V1)), "r2_mean_pairwise": float(mean_pairwise(V2)),
         "holds": bool(mean_pairwise(V2) >= mean_pairwise(V1) - 0.01)},
  "P8": {"top1_prize_rate": float(prize[top1].mean()), "threshold": base["prize_rate"] + 0.10,
         "holds": bool(prize[top1].mean() >= base["prize_rate"] + 0.10)},
  "also": {"r2_nn_median_full_atlas": float(np.median(nn2)),
           "r1_nn_below_atlas_p10": int((nn1 < base["loo_nn_p10"]).sum()),
           "r2x_nn_below_atlas_p10": int((nn2x < base["loo_nn_p10"]).sum()),
           "changed": {c: sum(1 for k in keys if R[2][k].get("changed", "").lower().startswith(c))
                       for c in ("kept", "changed", "replaced")}},
  "per_proposal": {k: {"nn1": float(nn1[j]), "nn2x": float(nn2x[j]), "top1": int(top1[j]),
                       "r1_r2_sim": float(V1[j] @ V2[j])} for j, k in enumerate(keys)},
}
json.dump(res, open("results.json", "w"), indent=1)
for p in ("P1", "P2", "P3", "P4", "P5", "P8"):
    print(p, res[p])
print(res["also"])

# --- the face: a 2-D map by PCA over atlas + both rounds
X = np.vstack([A, V1, V2]); mu = X.mean(0)
U, s, Vt = np.linalg.svd(X - mu, full_matrices=False)
P = (X - mu) @ Vt[:2].T
P = (P - P.min(0)) / (P.max(0) - P.min(0))
na = len(A)
face = {"atlas_sha256": sha, "baseline": base,
        "atlas": [{"t": a["title"], "a": a["artist"], "y": a["year"], "p": bool(prize[i]),
                   "x": round(float(P[i, 0]), 4), "z": round(float(P[i, 1]), 4)} for i, a in enumerate(atlas)],
        "props": []}
for j, k in enumerate(keys):
    face["props"].append({"k": k, "r1": R[1][k], "r2": R[2][k],
        "p1": [round(float(P[na + j, 0]), 4), round(float(P[na + j, 1]), 4)],
        "p2": [round(float(P[na + 24 + j, 0]), 4), round(float(P[na + 24 + j, 1]), 4)],
        "nn1": round(float(nn1[j]), 3), "nn2x": round(float(nn2x[j]), 3),
        "shown": [n["idx"] for n in nb[k]]})
open("face-data.js", "w").write("window.ALREADY=" + json.dumps(face, ensure_ascii=False) + ";\n")
