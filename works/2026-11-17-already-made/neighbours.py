"""After round 1: for each proposal, the three nearest atlas works; writes makings/r2-brief-mN.txt and neighbours.json.
Usage: neighbours.py <werke.json> <cache>"""
import sys, json
import numpy as np
from shelf import load_atlas, embedder, parse_proposals

atlas, sha = load_atlas(sys.argv[1])
embed = embedder(sys.argv[2])
A = np.load("atlas_vectors.npy").astype(np.float64)
tmpl = open("briefs/round2.md").read()
out = {}
for m in range(1, 9):
    props = parse_proposals(open(f"makings/r1-m{m}.txt").read())
    assert len(props) == 3, (m, len(props))
    V = embed(p["move"] for p in props)
    S = V @ A.T
    parts = []
    for i, p in enumerate(props):
        top = np.argsort(-S[i])[:3]
        out[f"m{m}.{i+1}"] = [{"idx": int(j), "sim": float(S[i, j])} for j in top]
        lines = [f"Your proposal {i+1}: {p['title']}"]
        for k, j in enumerate(top, 1):
            a = atlas[j]
            lines.append(f"  {k}. {a['title']} — {a['artist']}, {a['year']}. {a['decisive_move']}")
        parts.append("\n".join(lines))
    open(f"makings/r2-brief-m{m}.txt", "w").write(tmpl.replace("{NEIGHBOURS}", "\n\n".join(parts)))
json.dump(out, open("neighbours.json", "w"), indent=1)
print("ok")
