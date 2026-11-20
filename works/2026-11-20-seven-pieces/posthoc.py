"""POST HOC, written after scoring (results.json). Not predicted; labelled as such everywhere it is used.

1. Subjects: the head of each name, coded by hand below (the subject noun; adjectives and poses dropped).
2. Arm C: did the final subject differ from what the maker saw first (hand-coded below)?
3. Compactness: silhouette area / convex hull area, to read nearness to the canon against (a compact figure meets many
   canon figures well).
4. Helper instruments: which makers wrote their own scripts to solve the geometry.
"""
import json
import os
import statistics

import tangram

HERE = os.path.dirname(os.path.abspath(__file__))
SUBJECT = {  # hand-coded, one coder (this practice), after the run
    ("w1", "fig1.json"): "fish", ("w1", "fig2.json"): "cat", ("w1", "fig3.json"): "arrow (made as a house)",
    ("w2", "fig1.json"): "cat", ("w2", "fig2.json"): "sailing boat", ("w2", "fig3.json"): "fish",
    ("w3", "fig1.json"): "cat", ("w3", "fig2.json"): "house", ("w3", "fig3.json"): "fish",
    ("w4", "fig1.json"): "cat", ("w4", "fig2.json"): "sailing boat", ("w4", "fig3.json"): "arrow",
    ("c1", "fig1.json"): "bird", ("c1", "fig2.json"): "runner", ("c1", "fig3.json"): "dancer",
    ("c2", "fig1.json"): "shark", ("c2", "fig2.json"): "owl", ("c2", "fig3.json"): "goose",
    ("c3", "fig1.json"): "bird", ("c3", "fig2.json"): "lightning bolt", ("c3", "fig3.json"): "camel",
    ("c4", "fig1.json"): "sailing boat", ("c4", "fig2.json"): "person in a boat", ("c4", "fig3.json"): "runner",
}
# arm C: is the final subject a different thing from the first sighting? (hand-coded from first_seen and name)
TURNED = {
    ("c1", "fig1.json"): False, ("c1", "fig2.json"): False, ("c1", "fig3.json"): False,
    ("c2", "fig1.json"): True,   # small lizard or dragon -> shark
    ("c2", "fig2.json"): True,   # horned or crowned head over a figure falling apart -> horned owl
    ("c2", "fig3.json"): False,  # goose or swan -> goose
    ("c3", "fig1.json"): False,  # bird in flight (or a fish) -> bird
    ("c3", "fig2.json"): False,  # lightning bolt -> lightning bolt
    ("c3", "fig3.json"): True,   # sailing boat -> camel
    ("c4", "fig1.json"): False,  # sailing ship -> sailing boat
    ("c4", "fig2.json"): True,   # a boat -> a person standing in a boat (the square meant as a masthead read as a head)
    ("c4", "fig3.json"): False,
}
HELPERS = {"w1": ["fit.py", "d_fish.py", "d_cat.py", "d_house.py", "d_boat.py"], "w2": ["make.py"],
           "w3": ["build.py"], "w4": ["fit.py", "d1.py", "d2.py", "d3.py"], "c1": ["verts.py"], "c2": ["verts.py"],
           "c3": [], "c4": []}


def main():
    res = json.load(open(os.path.join(HERE, "results.json")))
    out = {"label": "POST HOC", "items": []}
    for it in res["items"]:
        fig = json.load(open(os.path.join(HERE, "makings", it["maker"], it["file"])))
        _, _, polys = tangram.check(fig)
        sil = tangram.silhouette(polys)
        comp = sil.area / sil.convex_hull.area
        out["items"].append({"maker": it["maker"], "file": it["file"], "subject": SUBJECT[(it["maker"], it["file"])],
                             "turned": TURNED.get((it["maker"], it["file"])), "compactness": round(comp, 3),
                             "nearest_iou": it["nearest_iou"]})
    for arm in "wc":
        xs = [i for i in out["items"] if i["maker"][0] == arm]
        subs = [i["subject"].split(" (")[0] for i in xs]
        out[arm.upper() + "_distinct_subjects"] = len(set(subs))
        out[arm.upper() + "_subjects"] = {s: subs.count(s) for s in sorted(set(subs))}
        out[arm.upper() + "_median_compactness"] = statistics.median(i["compactness"] for i in xs)
    out["C_turned"] = sum(1 for i in out["items"] if i["turned"])
    xs = [i["compactness"] for i in out["items"]]
    ys = [i["nearest_iou"] for i in out["items"]]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    r = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / (
        sum((a - mx) ** 2 for a in xs) ** .5 * sum((b - my) ** 2 for b in ys) ** .5)
    out["pearson_compactness_vs_nearest_all24"] = round(r, 3)
    out["helpers_written_by_maker"] = HELPERS
    json.dump(out, open(os.path.join(HERE, "posthoc.json"), "w"), indent=1)
    for k, v in out.items():
        if k != "items":
            print(k, v)


if __name__ == "__main__":
    main()
