"""Before any maker runs: measure the shelf against itself. Usage: prepare.py <werke.json> <cache>"""
import sys, json
import numpy as np
from shelf import load_atlas, embedder, mean_pairwise, PRIZE

atlas, sha = load_atlas(sys.argv[1])
embed = embedder(sys.argv[2])
V = embed(x["decisive_move"] for x in atlas)
np.save("atlas_vectors.npy", V.astype(np.float32))
S = V @ V.T
np.fill_diagonal(S, -1)
loo = S.max(1)
rng = np.random.default_rng(179)
null24 = [mean_pairwise(V[rng.choice(len(V), 24, replace=False)]) for _ in range(2000)]
verified = np.array([x.get("verify_status") == "verified" for x in atlas])
prize = np.array([bool(PRIZE.search(x.get("venue_prize") or "")) for x in atlas])
out = {
    "atlas_sha256": sha, "n": len(atlas), "n_verified": int(verified.sum()), "prize_rate": float(prize.mean()),
    "loo_nn_median": float(np.median(loo)), "loo_nn_p10": float(np.percentile(loo, 10)),
    "loo_nn_p90": float(np.percentile(loo, 90)),
    "loo_nn_median_verified_only": float(np.median((V[verified] @ V[verified].T - 2*np.eye(verified.sum())).max(1))),
    "null24_mean_pairwise_median": float(np.median(null24)), "null24_p95": float(np.percentile(null24, 95)),
    "atlas_mean_pairwise": float(mean_pairwise(V)),
}
json.dump(out, open("baseline.json", "w"), indent=1)
print(json.dumps(out, indent=1))
