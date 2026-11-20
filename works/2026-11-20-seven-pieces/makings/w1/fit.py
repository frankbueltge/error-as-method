"""Turn target piece outlines (vertex lists) into placements. Usage: python3 fit.py design.py out.json"""
import json, sys, math
from shapely.geometry import Polygon
import tangram as T

def fit(name, verts):
    tgt = Polygon(verts)
    c = tgt.centroid
    for flip in (False, True):
        for rot in range(0, 360, 45):
            p = {"piece": name, "x": c.x, "y": c.y, "rot": rot, "flip": flip}
            g = T.place(p)
            if g.symmetric_difference(tgt).area < 1e-6:
                return {"piece": name, "x": round(c.x, 4), "y": round(c.y, 4), "rot": rot, "flip": flip}
    raise SystemExit(f"{name}: no fit for {verts} (area {tgt.area:.3f})")

if __name__ == "__main__":
    design = {}
    exec(open(sys.argv[1]).read(), {"r2": math.sqrt(2)}, design)
    fig = [fit(n, design["D"][n]) for n in T.NAMES]
    json.dump(fig, open(sys.argv[2], "w"), indent=1)
    print("wrote", sys.argv[2])
