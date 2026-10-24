#!/usr/bin/env python3
"""POST HOC, labelled as such: two checks written after P1 was seen, against the obvious objection that
the people's spread is only hand tremor and the family's tightness only clean geometry.

1. TIGHTEST SIX: for every person in a pool, that person and the 5 people nearest them; the smallest D over
   the whole pool. These are six people who drew nearly the same thing, tremor included.
2. TREMOR ADDED: each S drawing resampled every 4 px along its strokes and jittered with Gaussian noise
   (sd 3 px on the 256 canvas, seed 1563), then D recomputed. If the family stays below the people's p5,
   clean lines alone do not explain P1.
Writes posthoc.json."""
import json, os, random
import numpy as np
from render import vector, dist, mean_pairwise
HERE = os.path.dirname(os.path.abspath(__file__))
dr = json.load(open(os.path.join(HERE, "drawings.json")))
res = json.load(open(os.path.join(HERE, "results.json")))
rng = random.Random(1563)

def jitter(d):
    out = []
    for xs, ys in d:
        px, py = [], []
        pts = list(zip(xs, ys))
        if len(pts) == 1: pts = pts * 2
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(1, int(np.hypot(x1 - x0, y1 - y0) / 4))
            for k in range(n):
                t = k / n
                px.append(x0 + t * (x1 - x0) + rng.gauss(0, 3)); py.append(y0 + t * (y1 - y0) + rng.gauss(0, 3))
        px.append(pts[-1][0] + rng.gauss(0, 3)); py.append(pts[-1][1] + rng.gauss(0, 3))
        out.append([px, py])
    return out

out = {}
for c, r in res["things"].items():
    P = json.load(open(os.path.join(HERE, "pools", c.replace(" ", "_") + ".json")))
    pv = np.array([vector(x["drawing"]) for x in P["pool"]])
    sim = pv @ pv.T
    best = 9
    for i in range(len(pv)):
        nn = np.argsort(-sim[i])[:6]
        best = min(best, mean_pairwise(pv[nn]))
    sj = mean_pairwise([vector(jitter(dr[f"S{n}"][c])) for n in range(1, 7)])
    out[c] = {"tightest_six_people": best, "S": r["D"]["S"], "S_with_tremor": sj, "people_p5": r["people_null"]["p5"],
              "S_below_tightest": r["D"]["S"] < best, "S_tremor_below_p5": sj < r["people_null"]["p5"]}
    print(f"{c:12s} tightest six {best:.3f}  S {r['D']['S']:.3f}  S+tremor {sj:.3f}  p5 {r['people_null']['p5']:.3f}")
json.dump(out, open(os.path.join(HERE, "posthoc.json"), "w"), indent=1)
print("S below the tightest six:", sum(v["S_below_tightest"] for v in out.values()), "of 12;",
      "S with tremor below p5:", sum(v["S_tremor_below_p5"] for v in out.values()), "of 12")
