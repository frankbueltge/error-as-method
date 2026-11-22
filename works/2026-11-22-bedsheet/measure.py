"""Raster measures of a flag PNG, the same for the people's flags and the makers'.
colours: distinct colours (3 bits per channel) that each cover at least 2% of the area
field:   share of the area taken by the single largest colour
edges:   share of horizontally or vertically adjacent pixel pairs that differ by more than 48 (sum of |dRGB|)
usage: python3.13 measure.py OUT.json PNG..."""
import sys, json
import numpy as np
from PIL import Image
out = {}
for f in sys.argv[2:]:
    a = np.asarray(Image.open(f).convert("RGB")).astype(int)
    q = (a >> 5); key = q[..., 0] * 64 + q[..., 1] * 8 + q[..., 2]
    _, counts = np.unique(key, return_counts=True); share = counts / key.size
    dx = np.abs(a[:, 1:] - a[:, :-1]).sum(-1) > 48; dy = np.abs(a[1:] - a[:-1]).sum(-1) > 48
    edges = (dx.sum() + dy.sum()) / (dx.size + dy.size)
    top = int(np.unique(key, return_counts=True)[0][counts.argmax()])
    rgb = [((top >> 6) & 7) * 32 + 16, ((top >> 3) & 7) * 32 + 16, (top & 7) * 32 + 16]
    out[f.split("/")[-1][:-4]] = {"colours": int((share >= 0.02).sum()), "field": round(float(share.max()), 3),
        "field_rgb": rgb, "edges": round(float(edges), 4), "aspect": round(a.shape[1] / a.shape[0], 3)}
json.dump(out, open(sys.argv[1], "w"), indent=1)
