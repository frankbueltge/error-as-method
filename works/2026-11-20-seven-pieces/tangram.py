"""The seven pieces: definition, placement, the check, and pictures.

Session 182, 2026-11-20. Written on the night (standing finding 5: this is where errors land).

A figure is a JSON list of seven placements, one per piece:
  {"piece": "L1", "x": 2.0, "y": 0.67, "rot": 0, "flip": false}
x, y is where the piece's centroid goes; rot is degrees counter-clockwise about the centroid; flip mirrors the
piece left-right before rotating (it matters only for the parallelogram P). Pieces: L1, L2 (large triangles, area 4),
M (medium triangle, 2), S1, S2 (small triangles, 1), Q (square, 2), P (parallelogram, 2). Total area 16.

Command line (for makers):
  python3 tangram.py check  FIGURE.json [OUT.png]   -> validity report, and a picture if OUT.png is given
  python3 tangram.py square OUT.json                 -> writes the seven pieces assembled as the 4x4 square
"""
import json
import math
import sys

from shapely import affinity
from shapely.geometry import Polygon
from shapely.ops import unary_union

# the standard square [0,4]^2, cut into the seven pieces
STANDARD = {
    "L1": [(0, 0), (4, 0), (2, 2)],
    "L2": [(0, 0), (2, 2), (0, 4)],
    "M": [(4, 2), (4, 4), (2, 4)],
    "S1": [(4, 0), (4, 2), (3, 1)],
    "S2": [(2, 2), (3, 3), (1, 3)],
    "Q": [(2, 2), (3, 1), (4, 2), (3, 3)],
    "P": [(0, 4), (1, 3), (3, 3), (2, 4)],
}
NAMES = list(STANDARD)
OVERLAP_TOL = 0.02   # area two pieces may share and still count as touching (rounding)
GAP_TOL = 0.05       # distance at which pieces count as touching


def _local(name):
    poly = Polygon(STANDARD[name])
    c = poly.centroid
    return affinity.translate(poly, -c.x, -c.y), (c.x, c.y)


LOCAL = {n: _local(n)[0] for n in NAMES}
CENTRE = {n: _local(n)[1] for n in NAMES}


def place(p):
    poly = LOCAL[p["piece"]]
    if p.get("flip"):
        poly = affinity.scale(poly, xfact=-1, yfact=1, origin=(0, 0))
    poly = affinity.rotate(poly, float(p.get("rot", 0)), origin=(0, 0))
    return affinity.translate(poly, float(p["x"]), float(p["y"]))


def square_figure():
    return [{"piece": n, "x": round(CENTRE[n][0], 4), "y": round(CENTRE[n][1], 4), "rot": 0, "flip": False}
            for n in NAMES]


def check(fig):
    """Return (ok, problems, polygons)."""
    problems = []
    if isinstance(fig, dict):
        fig = fig.get("pieces", fig)
    names = [p.get("piece") for p in fig]
    if sorted(names) != sorted(NAMES):
        problems.append(f"pieces must be exactly {NAMES}, got {names}")
        return False, problems, []
    polys = {p["piece"]: place(p) for p in fig}
    for i, a in enumerate(NAMES):
        for b in NAMES[i + 1:]:
            ov = polys[a].intersection(polys[b]).area
            if ov > OVERLAP_TOL:
                problems.append(f"{a} and {b} overlap by {ov:.3f} square units")
    grown = unary_union([g.buffer(GAP_TOL) for g in polys.values()])
    parts = 1 if grown.geom_type == "Polygon" else len(grown.geoms)
    if parts > 1:
        # name the islands
        groups = []
        geoms = [grown] if grown.geom_type == "Polygon" else list(grown.geoms)
        for g in geoms:
            groups.append([n for n in NAMES if g.intersects(polys[n].representative_point().buffer(1e-6))])
        problems.append(f"the figure falls apart into {parts} islands: {groups}")
    return not problems, problems, [polys[n] for n in NAMES]


def silhouette(polys):
    return unary_union([p.buffer(1e-4) for p in polys]).buffer(-1e-4)


def render_png(polys, path, outline=True, size=480, labels=None):
    from PIL import Image, ImageDraw
    u = unary_union(polys)
    minx, miny, maxx, maxy = u.bounds
    span = max(maxx - minx, maxy - miny)
    pad = 0.08 * span
    s = (size - 1) / (span + 2 * pad)
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2

    def tr(x, y):
        return ((x - cx) * s + size / 2, size / 2 - (y - cy) * s)

    img = Image.new("RGB", (size, size), "white")
    d = ImageDraw.Draw(img)
    for i, p in enumerate(polys):
        pts = [tr(x, y) for x, y in p.exterior.coords]
        d.polygon(pts, fill=(40, 40, 40), outline=(255, 255, 255) if outline else None)
        if outline:
            d.line(pts, fill=(255, 255, 255), width=2)
        if labels:
            c = p.centroid
            d.text(tr(c.x, c.y), labels[i], fill=(255, 200, 80))
    img.save(path)


def main(argv):
    if len(argv) >= 3 and argv[1] == "square":
        json.dump(square_figure(), open(argv[2], "w"), indent=1)
        print("wrote", argv[2])
        return 0
    if len(argv) >= 3 and argv[1] == "check":
        fig = json.load(open(argv[2]))
        ok, problems, polys = check(fig)
        print("VALID" if ok else "NOT VALID")
        with open("checks.log", "a") as log:      # every check a maker runs is counted (iterating, erring)
            import datetime
            log.write(f"{datetime.datetime.utcnow().isoformat()}Z\t{argv[2]}\t{'VALID' if ok else 'NOT VALID'}"
                      f"\t{len(problems)}\n")
        for p in problems:
            print("  -", p)
        if polys:
            sil = silhouette(polys)
            print(f"  silhouette area {sil.area:.2f} (16 when nothing overlaps); bounds "
                  + ", ".join(f"{v:.2f}" for v in sil.bounds))
        if len(argv) >= 4 and polys:
            render_png(polys, argv[3], outline=True, labels=NAMES)
            out2 = argv[3].replace(".png", "-silhouette.png")
            render_png(polys, out2, outline=False)
            print("  pictures:", argv[3], "(pieces labelled) and", out2, "(silhouette, as a viewer sees it)")
        return 0 if ok else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
