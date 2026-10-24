#!/usr/bin/env python3
"""Score P1-P6 of PREDICTIONS.md exactly as fixed there. Writes results.json.

    python3 -I score.py
"""
import json
import os
import random

import numpy as np

from render import vector, dist, mean_pairwise

HERE = os.path.dirname(os.path.abspath(__file__))
cats = [c["category"] for c in json.load(open(os.path.join(HERE, "plan.json")))["categories"]]
dr = json.load(open(os.path.join(HERE, "drawings.json")))
ARMS = {a: [f"{a}{n}" for n in range(1, 7)] for a in "SFH"}


def pool_of(c):
    return json.load(open(os.path.join(HERE, "pools", c.replace(" ", "_") + ".json")))


res = {"things": {}, "predictions": {}}
rng_null = random.Random(1560)
rng_trace = random.Random(1561)
tally = {k: 0 for k in ("P1", "P2", "P3", "P5", "P6")}
traced, h_cells = 0, 0
for c in cats:
    P = pool_of(c)
    pv = [vector(r["drawing"]) for r in P["pool"]]
    sv = [vector(r["drawing"]) for r in P["shown"]]
    null = [mean_pairwise(rng_null.sample(pv, 6)) for _ in range(2000)]
    p5, p50, p95 = (float(np.percentile(null, q)) for q in (5, 50, 95))
    D = {}
    vecs = {}
    for a, makers in ARMS.items():
        have = [m for m in makers if c in dr.get(m, {})]
        vecs[a] = {m: vector(dr[m][c]) for m in have}
        D[a] = mean_pairwise(vecs[a].values()) if len(have) >= 2 else None
    # P4: tracing in arm H
    trace_null = []
    for _ in range(1000):
        trace_null.append(rng_trace.sample(range(len(pv)), 6))
    cells = {}
    for m, v in vecs["H"].items():
        T = min(dist(v, s) for s in sv)
        ref = [min(dist(v, pv[i]) for i in idx) for idx in trace_null]
        q5 = float(np.percentile(ref, 5))
        cells[m] = {"T": T, "ref_p5": q5, "ref_median": float(np.median(ref)), "traced": T < q5}
        traced += T < q5
        h_cells += 1
    # P6: strokes
    s_strokes = [len(dr[m][c]) for m in ARMS["S"] if c in dr.get(m, {})]
    p_strokes = [len(r["drawing"]) for r in P["pool"]]
    row = {
        "people_null": {"p5": p5, "median": p50, "p95": p95, "draws": 2000},
        "D": D,
        "S_below_p5": D["S"] is not None and D["S"] < p5,
        "H_gt_F": None if None in (D["H"], D["F"]) else D["H"] > D["F"],
        "H_below_p5": D["H"] is not None and D["H"] < p5,
        "F_gt_S": None if None in (D["F"], D["S"]) else D["F"] > D["S"],
        "strokes": {"S_median": float(np.median(s_strokes)) if s_strokes else None,
                    "people_median": float(np.median(p_strokes)),
                    "S": s_strokes, "F": [len(dr[m][c]) for m in ARMS["F"] if c in dr.get(m, {})],
                    "H": [len(dr[m][c]) for m in ARMS["H"] if c in dr.get(m, {})]},
        "H_cells": cells,
        # where each arm's drawings sit inside the people's spread: mean d to the 50 nearest people
        "typicality": {a: (float(np.mean([np.mean(sorted(dist(v, p) for p in pv)[:50])
                                          for v in vecs[a].values()])) if vecs[a] else None) for a in "SFH"},
    }
    row["typicality"]["people"] = float(np.mean([np.mean(sorted(dist(pv[i], p) for j, p in enumerate(pv) if j != i)[:50])
                                                 for i in random.Random(1562).sample(range(len(pv)), 60)]))
    row["S_strokes_gt_people"] = (row["strokes"]["S_median"] or 0) > row["strokes"]["people_median"]
    tally["P1"] += row["S_below_p5"]
    tally["P2"] += bool(row["H_gt_F"])
    tally["P3"] += row["H_below_p5"]
    tally["P5"] += bool(row["F_gt_S"])
    tally["P6"] += row["S_strokes_gt_people"]
    res["things"][c] = row
    print(f"{c:12s} p5 {p5:.3f} med {p50:.3f} | S {D['S']:.3f} F {D['F'] if D['F'] is None else round(D['F'],3)} "
          f"H {D['H'] if D['H'] is None else round(D['H'],3)} | strokes S {row['strokes']['S_median']} "
          f"people {row['strokes']['people_median']} | traced {sum(x['traced'] for x in cells.values())}/{len(cells)}")

need = {"P1": 9, "P2": 8, "P3": 7, "P5": 8, "P6": 8}
for k, n in need.items():
    res["predictions"][k] = {"count": tally[k], "of": len(cats), "needed": n, "held": tally[k] >= n}
res["predictions"]["P4"] = {"count": traced, "of": h_cells, "needed": 24, "held": traced >= 24}
json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)
for k in ("P1", "P2", "P3", "P4", "P5", "P6"):
    p = res["predictions"][k]
    print(k, p["count"], "of", p["of"], "needed", p["needed"], "HELD" if p["held"] else "FAILED")
