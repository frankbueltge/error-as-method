"""POST HOC (written after score.py ran): what can the committed text measure see?
Usage: posthoc.py <werke.json> <cache>"""
import sys, json, re, itertools
import numpy as np
from shelf import load_atlas, embedder, parse_proposals
from score_mat import MAT

atlas, sha = load_atlas(sys.argv[1]); embed = embedder(sys.argv[2])
A = np.load("atlas_vectors.npy").astype(np.float64)
R = {r: {} for r in (1, 2)}
for r in (1, 2):
    for m in range(1, 9):
        for i, p in enumerate(parse_proposals(open(f"makings/r{r}-m{m}.txt").read()), 1):
            R[r][f"m{m}.{i}"] = p
keys = sorted(R[1]); V1 = embed(R[1][k]["move"] for k in keys)
S = V1 @ V1.T
same = [S[i, j] for i, j in itertools.combinations(range(24), 2) if MAT[keys[i]] == MAT[keys[j]]]
diff = [S[i, j] for i, j in itertools.combinations(range(24), 2) if MAT[keys[i]] != MAT[keys[j]]]
# calibration: two atlas entries describing versions of one work
lib = [i for i, a in enumerate(atlas) if a["title"].startswith("The Library of Missing Datasets")]
cal = float(A[lib[0]] @ A[lib[1]]) if len(lib) >= 2 else None
# theme: a record's errors, gaps, revisions, flags, withdrawals (regex, crude)
TH = re.compile(r"\b(error|errat|retract|withdraw|revis|revert|undo|undone|correct|flag|missing|gap|absen|silen|offline|outage|rejected|declined|set aside|threw out|left out|did not|no reading|never existed|not confirmed|fell below|threshold)", re.I)
rate = lambda texts: sum(bool(TH.search(t)) for t in texts) / len(texts)
out = {"same_source_pairwise_mean": float(np.mean(same)), "n_same": len(same),
       "different_source_pairwise_mean": float(np.mean(diff)),
       "atlas_same_work_calibration": {"titles": [atlas[i]["title"] for i in lib], "sim": cal},
       "theme_rate_atlas": rate([a["decisive_move"] for a in atlas]),
       "theme_rate_r1": rate([R[1][k]["move"] for k in keys]),
       "theme_rate_r2": rate([R[2][k]["move"] for k in keys])}
json.dump(out, open("posthoc.json", "w"), indent=1); print(json.dumps(out, indent=1))
