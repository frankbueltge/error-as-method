"""Turn target vertex lists into tangram placements. usage: python3 build.py"""
import json
import math
from shapely.geometry import Polygon
from tangram import place

R2 = math.sqrt(2)


def fit(name, verts):
    tgt = Polygon(verts)
    c = tgt.centroid
    for flip in (False, True):
        for rot in range(0, 360, 45):
            p = {"piece": name, "x": round(c.x, 4), "y": round(c.y, 4), "rot": rot, "flip": flip}
            if place(p).symmetric_difference(tgt).area < 1e-3:
                return p
    raise SystemExit(f"no fit for {name} {verts}")


def build(out, targets, scale=1.0):
    fig = [fit(n, [(x * scale, y * scale) for x, y in v]) for n, v in targets.items()]
    json.dump(fig, open(out, "w"), indent=1)
    print("wrote", out)


# fig1: sitting cat (integer grid)
build("fig1.json", {
    "Q": [(0, 1), (-1, 0), (0, -1), (1, 0)],
    "S1": [(-1, 0), (0, 1), (-1, 2)],
    "S2": [(1, 0), (0, 1), (1, 2)],
    "L1": [(0, -5), (0, -1), (-2, -3)],
    "L2": [(0, -5), (-4, -5), (-2, -3)],
    "M": [(0, -3), (0, -5), (2, -5)],
    "P": [(-4, -5), (-3, -4), (-3, -2), (-4, -3)],
})

# fig2: house with chimney (grid unit = sqrt 2)
build("fig2.json", {
    "L1": [(-2.5, 0), (-0.5, 0), (-0.5, 2)],
    "L2": [(-0.5, 0), (1.5, 0), (-0.5, 2)],
    "S1": [(-2, -1), (-1, 0), (-2, 0)],
    "P": [(-2, -1), (-1, -1), (0, 0), (-1, 0)],
    "M": [(-1, -1), (1, -1), (0, 0)],
    "S2": [(0, 0), (1, 0), (1, -1)],
    "Q": [(0.5, 1), (1.5, 1), (1.5, 2), (0.5, 2)],
}, scale=R2)

# fig3: fish facing left (integer grid)
build("fig3.json", {
    "L1": [(-2, 0), (2, 0), (0, 2)],
    "L2": [(-2, 0), (2, 0), (0, -2)],
    "M": [(2, 0), (4, 2), (4, 0)],
    "S1": [(4, 0), (2, 0), (3, -1)],
    "S2": [(4, 0), (4, -2), (3, -1)],
    "P": [(0, 2), (2, 2), (3, 1), (1, 1)],
    "Q": [(0, -2), (1, -1), (2, -2), (1, -3)],
})
