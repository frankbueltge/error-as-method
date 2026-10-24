"""The one measure of form this experiment uses, fixed before any maker ran.

A drawing is a list of strokes, each [[x...], [y...]], as in the simplified Quick, Draw! files.
`vector()` centres it on its bounding box, scales the longer side to 56 px inside a 64 x 64
canvas (aspect kept), draws the strokes 2 px wide, blurs with a Gaussian of radius 2 px and
returns the unit-length vector. `dist()` is 1 minus the cosine of two such vectors: 0 for the
same picture, larger for pictures whose ink lies in different places. It knows nothing of what
is drawn. It sees where the ink is, after position and size are taken away.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SIZE = 64
SPAN = 56


def _points(drawing):
    xs = [x for s in drawing for x in s[0]]
    ys = [y for s in drawing for y in s[1]]
    return min(xs), min(ys), max(xs), max(ys)


def raster(drawing, size=SIZE, span=SPAN, width=2, ink=255, bg=0):
    x0, y0, x1, y1 = _points(drawing)
    w, h = max(x1 - x0, 1e-6), max(y1 - y0, 1e-6)
    k = span / max(w, h)
    ox = (size - w * k) / 2 - x0 * k
    oy = (size - h * k) / 2 - y0 * k
    im = Image.new("L", (size, size), bg)
    dr = ImageDraw.Draw(im)
    for s in drawing:
        pts = [(x * k + ox, y * k + oy) for x, y in zip(s[0], s[1])]
        if len(pts) == 1:
            pts = pts * 2
        dr.line(pts, fill=ink, width=width, joint="curve")
    return im


def vector(drawing):
    im = raster(drawing).filter(ImageFilter.GaussianBlur(2))
    v = np.asarray(im, dtype=np.float64).ravel()
    n = np.linalg.norm(v)
    return v / n if n else v


def dist(a, b):
    return float(1.0 - np.dot(a, b))


def mean_pairwise(vs):
    vs = list(vs)
    d = [dist(vs[i], vs[j]) for i in range(len(vs)) for j in range(i + 1, len(vs))]
    return float(np.mean(d))


def contact_sheet(drawings, path, cell=220, pad=10):
    """Six drawings side by side, black on white, no words: what an F or H maker is shown."""
    n = len(drawings)
    sheet = Image.new("L", (n * cell + (n + 1) * pad, cell + 2 * pad), 255)
    for i, d in enumerate(drawings):
        im = raster(d, size=cell, span=cell - 20, width=3, ink=0, bg=255)
        sheet.paste(im, (pad + i * (cell + pad), pad))
        ImageDraw.Draw(sheet).rectangle(
            [pad + i * (cell + pad), pad, pad + i * (cell + pad) + cell - 1, pad + cell - 1], outline=200)
    sheet.save(path)
