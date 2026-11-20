"""Helper: turn target vertex lists into placements. Usage: python3 fit.py design.py out.json"""
import json, sys
from shapely.geometry import Polygon
import tangram

def fit(name, verts):
    target = Polygon(verts)
    c = target.centroid
    best = None
    for flip in (False, True):
        for k in range(8):
            rot = 45 * k
            p = {"piece": name, "x": round(c.x, 6), "y": round(c.y, 6), "rot": rot, "flip": flip}
            d = tangram.place(p).symmetric_difference(target).area
            if best is None or d < best[0]:
                best = (d, p)
    if best[0] > 1e-3:
        raise SystemExit(f"{name}: no fit for {verts} (diff {best[0]:.3f})")
    return best[1]

if __name__ == "__main__":
    design = {}
    exec(open(sys.argv[1]).read(), design)
    fig = [fit(n, v) for n, v in design["PIECES"].items()]
    json.dump(fig, open(sys.argv[2], "w"), indent=1)
    print("wrote", sys.argv[2])
