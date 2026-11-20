"""The canon: KILOGRAM's 1,013 tangram figures (Slocum's book, digitised by Ji et al. 2022) as silhouettes, and the
similarity measure every figure tonight is held against.

The SVGs are NOT committed: KILOGRAM's README says the tangram images are for educational and research use only
(Princeton Library notice), so this script reads them from a local clone of github.com/lil-lab/kilogram at commit
f2cd80201eedc5f4882bd88ba32de39195d9e9f3 and commits only derived numbers (ids, similarities). The people's names
(full.json annotations) are MIT-licensed text.

Usage: python3 canon.py /path/to/kilogram  -> canon.npz (rasters, not committed) and canon_baseline.json
"""
import json
import os
import re
import sys

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon
from shapely.ops import unary_union

GRID = 64
EXTENT = 9.0           # rasters cover [-9, 9]^2 in tangram units (the set has area 16)
ROTS = list(range(0, 360, 15))


def parse_svg(path):
    txt = open(path).read()
    polys = []
    for m in re.finditer(r"<polygon[^>]*>", txt):
        tag = m.group(0)
        pts = [float(v) for v in re.search(r'points="([^"]+)"', tag).group(1).replace(",", " ").split()]
        xy = list(zip(pts[0::2], pts[1::2]))
        t = re.search(r'transform="matrix\(([^)]+)\)"', tag)
        if t:
            a, b, c, d, e, f = [float(v) for v in t.group(1).replace(",", " ").split()]
            xy = [(a * x + c * y + e, b * x + d * y + f) for x, y in xy]
        polys.append(Polygon([(x, -y) for x, y in xy]))   # SVG y runs down; flip so up is up
    return polys


def normalise(geom):
    """Centre on the centroid and scale to area 16."""
    c = geom.centroid
    g = affinity.translate(geom, -c.x, -c.y)
    k = (16.0 / g.area) ** 0.5
    return affinity.scale(g, k, k, origin=(0, 0))


def raster(geom):
    from PIL import Image, ImageDraw
    img = Image.new("1", (GRID, GRID), 0)
    d = ImageDraw.Draw(img)
    s = GRID / (2 * EXTENT)
    geoms = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
    for g in geoms:
        d.polygon([((x + EXTENT) * s, (EXTENT - y) * s) for x, y in g.exterior.coords], fill=1)
        for hole in g.interiors:
            d.polygon([((x + EXTENT) * s, (EXTENT - y) * s) for x, y in hole.coords], fill=0)
    return np.array(img, dtype=np.float32).reshape(-1)


def variants(geom):
    """The figure in 24 rotations x 2 mirrorings, each re-centred: a viewer may turn or flip a figure."""
    out = []
    for mirror in (False, True):
        g0 = affinity.scale(geom, -1, 1, origin=(0, 0)) if mirror else geom
        for r in ROTS:
            out.append(raster(affinity.rotate(g0, r, origin=(0, 0))))
    return np.stack(out)


def iou_matrix(A, B):
    inter = A @ B.T
    sa = A.sum(1)[:, None]
    sb = B.sum(1)[None, :]
    return inter / (sa + sb - inter)


def silhouette_of(polys):
    return unary_union([p.buffer(1e-3) for p in polys]).buffer(-1e-3)


def main(root):
    svgdir = os.path.join(root, "dataset", "tangrams-svg")
    full = json.load(open(os.path.join(root, "dataset", "full.json")))
    ids = sorted(full)
    base = []
    for i in ids:
        g = normalise(silhouette_of(parse_svg(os.path.join(svgdir, i + ".svg"))))
        base.append(raster(g))
    base = np.stack(base)
    # nearest neighbour among the people's figures: each figure's 48 variants against all others in canonical pose
    nn, nn_id = [], []
    for k, i in enumerate(ids):
        g = normalise(silhouette_of(parse_svg(os.path.join(svgdir, i + ".svg"))))
        M = iou_matrix(variants(g), base).max(0)
        M[k] = -1
        j = int(M.argmax())
        nn.append(float(M[j]))
        nn_id.append(ids[j])
    np.savez_compressed(os.path.join(os.path.dirname(os.path.abspath(__file__)), "canon.npz"), base=base,
                        ids=np.array(ids))
    q = np.percentile(nn, [10, 25, 50, 75, 90])
    out = {"source": "github.com/lil-lab/kilogram @ f2cd80201eedc5f4882bd88ba32de39195d9e9f3, dataset/tangrams-svg",
           "n": len(ids), "grid": GRID, "extent": EXTENT, "rotations": ROTS, "mirror": True,
           "nn_iou_percentiles_10_25_50_75_90": [round(float(v), 4) for v in q],
           "nearest": {i: [nn_id[k], round(nn[k], 4)] for k, i in enumerate(ids)}}
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "canon_baseline.json"), "w"),
              indent=0)
    print("n", len(ids), "nn IoU percentiles 10/25/50/75/90:", [round(float(v), 3) for v in q])


if __name__ == "__main__":
    main(sys.argv[1])
