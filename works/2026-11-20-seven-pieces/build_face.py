"""Write face-data.js for index.html from results.json, the makers' figures and the reference distributions.
No canon figure is drawn or exported (KILOGRAM's images are for research use only); the people's names are text (MIT).
"""
import json
import os

import tangram

HERE = os.path.dirname(os.path.abspath(__file__))


def pieces(fig):
    out = []
    for p in sorted(fig, key=lambda q: tangram.NAMES.index(q["piece"])):
        poly = tangram.place(p)
        out.append([[round(x, 3), round(y, 3)] for x, y in list(poly.exterior.coords)[:-1]])
    return out


def main():
    res = json.load(open(os.path.join(HERE, "results.json")))
    base = json.load(open(os.path.join(HERE, "canon_baseline.json")))
    null = json.load(open(os.path.join(HERE, "null_nearest.json")))
    items = []
    for it in res["items"]:
        d = os.path.join(HERE, "makings", it["maker"])
        fig = json.load(open(os.path.join(d, it["file"])))
        row = {k: it.get(k) for k in ("maker", "arm", "file", "name", "how", "first_seen", "seen_before",
                                      "nearest_iou", "on_shelf", "named_as_people", "changes",
                                      "checks_logged_for_file", "not_valid_logged_for_file")}
        row["people"] = it["people_named_nearest"][:10]
        row["fig"] = pieces(fig)
        if it["arm"] == "C":
            k = int(it["file"][3]) - 1
            row["drop"] = pieces(json.load(open(os.path.join(d, f"drop{k + 1}.json"))))
        items.append(row)
    data = {"items": items,
            "canon_nn": sorted(v[1] for v in base["nearest"].values()),
            "chance": sorted(v["nearest"][0]["iou"] for v in null.values()),
            "predictions": res["predictions"]}
    with open(os.path.join(HERE, "face-data.js"), "w") as f:
        f.write("var D=" + json.dumps(data, separators=(",", ":")) + ";\n")
    print(len(items), "items written")


if __name__ == "__main__":
    main()
