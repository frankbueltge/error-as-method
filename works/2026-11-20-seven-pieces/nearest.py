"""Hold figures against the canon: for each figure, the people's figure whose silhouette is nearest (IoU, best over
24 turns x 2 mirrorings), and the names people gave that figure (KILOGRAM full.json, MIT).

Usage: python3 nearest.py CANON_NPZ FULL_JSON OUT_JSON FIGURE.json [FIGURE.json ...]
"""
import json
import os
import sys

import numpy as np

import canon
import tangram


def main(npz, full_json, out, paths):
    z = np.load(npz)
    base, ids = z["base"], [str(i) for i in z["ids"]]
    full = json.load(open(full_json))
    res = {}
    for p in paths:
        fig = json.load(open(p))
        ok, problems, polys = tangram.check(fig)
        g = canon.normalise(canon.silhouette_of(polys))
        M = canon.iou_matrix(canon.variants(g), base).max(0)
        top = np.argsort(-M)[:3]
        res[os.path.relpath(p)] = {
            "valid": ok,
            "nearest": [{"id": ids[j], "iou": round(float(M[j]), 4),
                         "people_named_it": [a["whole"]["wholeAnnotation"] for a in full[ids[j]]["annotations"]]}
                        for j in top]}
    json.dump(res, open(out, "w"), indent=1)
    v = [r["nearest"][0]["iou"] for r in res.values()]
    print(len(v), "figures; nearest-IoU percentiles 10/25/50/75/90:",
          [round(float(x), 3) for x in np.percentile(v, [10, 25, 50, 75, 90])])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
