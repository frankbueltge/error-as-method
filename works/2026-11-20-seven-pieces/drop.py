"""The chance drop: seven pieces put down one after another, each touching what lies there, nothing overlapping.

Each piece gets a random turn in steps of 45 degrees (the parallelogram a random flip) and comes in from a random
direction towards the centre of what lies there, stopping at first contact (bisection to 0.01 units).
Order of pieces is shuffled. Deterministic from the seed.

Usage: python3 drop.py SEED N OUTDIR  -> N arrangements as JSON figures (tangram.py's format)
"""
import json
import math
import os
import random
import sys

from shapely.ops import unary_union

import tangram


def drop(rng):
    order = tangram.NAMES[:]
    rng.shuffle(order)
    placed = []
    for name in order:
        rot = 45 * rng.randrange(8)
        flip = name == "P" and rng.random() < 0.5
        if not placed:
            placed.append({"piece": name, "x": 0.0, "y": 0.0, "rot": rot, "flip": flip})
            continue
        u = unary_union([tangram.place(p) for p in placed])
        c = u.centroid
        th = rng.uniform(0, 2 * math.pi)
        dx, dy = math.cos(th), math.sin(th)

        def at(t):
            return {"piece": name, "x": c.x + dx * t, "y": c.y + dy * t, "rot": rot, "flip": flip}

        lo, hi = 0.0, 20.0     # at hi the piece is clear of the union
        while hi - lo > 0.01:
            mid = (lo + hi) / 2
            if tangram.place(at(mid)).intersection(u).area > 0.005:
                lo = mid
            else:
                hi = mid
        placed.append(at(hi))
    for p in placed:
        p["x"], p["y"] = round(p["x"], 3), round(p["y"], 3)
    return placed


def main(seed, n, outdir):
    rng = random.Random(seed)
    os.makedirs(outdir, exist_ok=True)
    made = 0
    while made < n:
        fig = drop(rng)
        ok, problems, _ = tangram.check(fig)
        if not ok:          # contact by bisection can leave a hair's gap; such drops are redrawn, and counted
            print("redrawn:", problems)
            continue
        json.dump(fig, open(os.path.join(outdir, f"drop-{made:03d}.json"), "w"), indent=1)
        made += 1


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
