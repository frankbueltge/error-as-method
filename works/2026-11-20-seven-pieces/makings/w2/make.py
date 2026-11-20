"""Turn target piece outlines (absolute vertices) into placements."""
import json
import math
import sys

from shapely.geometry import Polygon

from tangram import NAMES, place

R = math.sqrt(2)


def fit(name, verts):
    target = Polygon(verts)
    c = target.centroid
    for flip in (False, True):
        for rot in range(0, 360, 45):
            p = {"piece": name, "x": round(c.x, 4), "y": round(c.y, 4), "rot": rot, "flip": flip}
            if place(p).symmetric_difference(target).area < 1e-3:
                return p
    raise SystemExit(f"{name}: no fit for {verts}")


def cat():
    return {
        "L1": [(-2, 0), (2, 0), (0, 2)],
        "L2": [(0, 2), (2, 0), (2, 4)],
        "M": [(0, 2), (2, 4), (0, 4)],
        "Q": [(1, 4), (2, 5), (1, 6), (0, 5)],
        "S1": [(0, 5), (1, 6), (0, 7)],
        "S2": [(2, 5), (1, 6), (2, 7)],
        "P": [(2, 0), (2 + R, R), (2 + R, 2 * R), (2, R)],
    }


def boat():
    m = 4 * R - 2.35
    return {
        "S1": [(0, R), (R, R), (R, 0)],
        "Q": [(R, 0), (2 * R, 0), (2 * R, R), (R, R)],
        "S2": [(2 * R, 0), (2 * R, R), (3 * R, R)],
        "P": [(2 * R, 0), (3 * R, 0), (4 * R, R), (3 * R, R)],
        "L1": [(m, R), (m, R + 4), (m - 2, R + 2)],
        "L2": [(m, R), (m - 2, R + 2), (m - 4, R)],
        "M": [(m + 0.35, R), (m + 0.35, R + 2), (m + 2.35, R)],
    }


def fish():
    return {
        "L1": [(-2, 0), (2, 0), (0, 2)],
        "L2": [(-2, 0), (2, 0), (0, -2)],
        "M": [(2, 0), (4, 2), (4, 0)],
        "S1": [(2, 0), (4, 0), (3, -1)],
        "S2": [(3, -1), (4, 0), (4, -2)],
        "P": [(-1, 1), (0, 2), (0, 4), (-1, 3)],
        "Q": [(0, -2), (1, -1), (2, -2), (1, -3)],
    }


if __name__ == "__main__":
    shape = globals()[sys.argv[1]]()
    fig = [fit(n, shape[n]) for n in NAMES]
    json.dump(fig, open(sys.argv[2], "w"), indent=1)
    print("wrote", sys.argv[2])
