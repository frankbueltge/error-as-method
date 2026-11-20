"""Score the hand-backs by the rules committed in predictions.md (f671857). Nothing here is post hoc.

Usage: python3 score.py   (reads makings/<maker>/, canon.npz, shelf.json, KILOGRAM full.json path in FULL below)
"""
import glob
import json
import os
import statistics
import sys

import numpy as np

import canon
import tangram
from words import content

HERE = os.path.dirname(os.path.abspath(__file__))
FULL = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/dl/kilogram/dataset/full.json"
LEAK = {"error", "errors", "mistake", "mistakes", "method", "methods", "norm", "norms"}


def changes(drop, fig):
    d = {p["piece"]: p for p in drop}
    n = 0
    for p in fig:
        q = d[p["piece"]]
        if (abs(p["x"] - q["x"]) > 0.01 or abs(p["y"] - q["y"]) > 0.01
                or abs(((p.get("rot", 0) - q.get("rot", 0)) + 180) % 360 - 180) > 0.5
                or bool(p.get("flip")) != bool(q.get("flip"))):
            n += 1
    return n


def main():
    z = np.load(os.path.join(HERE, "canon.npz"))
    base, ids = z["base"], [str(i) for i in z["ids"]]
    full = json.load(open(FULL))
    shelf = set(json.load(open(os.path.join(HERE, "shelf.json")))["shelf"])
    items = []
    for mdir in sorted(glob.glob(os.path.join(HERE, "makings", "*"))):
        maker = os.path.basename(mdir)
        arm = maker[0].upper()
        mk = json.load(open(os.path.join(mdir, "makings.json")))
        log = open(os.path.join(mdir, "checks.log")).read().splitlines() if os.path.exists(
            os.path.join(mdir, "checks.log")) else []
        for k, f in enumerate(mk["figures"]):
            fig = json.load(open(os.path.join(mdir, f["file"])))
            ok, problems, polys = tangram.check(fig)
            g = canon.normalise(canon.silhouette_of(polys))
            M = canon.iou_matrix(canon.variants(g), base).max(0)
            j = int(M.argmax())
            people = [a["whole"]["wholeAnnotation"] for a in full[ids[j]]["annotations"]]
            pw = set().union(*[content(n) for n in people])
            name_words = content(f["name"])
            stem = os.path.splitext(f["file"])[0]
            checks_fig = [l for l in log if os.path.basename(l.split("\t")[1]).startswith(stem)]
            it = {"maker": maker, "arm": arm, "file": f["file"], "name": f["name"], "how": f.get("how", ""),
                  "first_seen": f.get("first_seen"), "seen_before": f.get("seen_before", ""), "valid": ok,
                  "problems": problems, "nearest_id": ids[j], "nearest_iou": round(float(M[j]), 4),
                  "people_named_nearest": people, "on_shelf": bool(name_words & shelf),
                  "named_as_people": bool(name_words & pw), "shared_with_people": sorted(name_words & pw),
                  "checks_logged_for_file": len(checks_fig),
                  "not_valid_logged_for_file": sum(1 for l in checks_fig if "NOT VALID" in l)}
            if arm == "C":
                drop = json.load(open(os.path.join(mdir, f.get("drop", f"drop{k + 1}.json"))))
                it["changes"] = changes(drop, fig)
                it["first_seen_on_shelf"] = bool(content(f.get("first_seen") or "") & shelf)
            text = " ".join([f["name"], f.get("how", ""), f.get("first_seen") or "", f.get("seen_before", "")]).lower()
            it["leak"] = sorted(w for w in LEAK if w in set(text.replace(".", " ").replace(",", " ").split()))
            items.append(it)
        for it in items:
            if it["maker"] == maker:
                it["maker_checks_total"] = len(log)
                it["maker_not_valid_total"] = sum(1 for l in log if "NOT VALID" in l)
                it["files_opened"] = mk.get("files_opened", [])
    W = [i for i in items if i["arm"] == "W"]
    C = [i for i in items if i["arm"] == "C"]
    r = {}
    medW = statistics.median(i["nearest_iou"] for i in W)
    medC = statistics.median(i["nearest_iou"] for i in C)
    r["P1"] = {"median_W": medW, "holds": medW >= 0.69}
    r["P2"] = {"median_C": medC, "holds": medC <= 0.66}
    sW, sC = sum(i["on_shelf"] for i in W), sum(i["on_shelf"] for i in C)
    r["P3"] = {"W_on_shelf": sW, "of": len(W), "holds": sW >= 9}
    r["P4"] = {"C_on_shelf": sC, "of": len(C), "holds": sC <= 6 and sW - sC >= 3}
    by_word = {}
    for i in W:
        for w in content(i["name"]):
            by_word.setdefault(w, set()).add(i["maker"])
    shared = {w: sorted(m) for w, m in by_word.items() if len(m) >= 2}
    r["P5"] = {"words_in_2plus_W_makers": shared, "holds": any(len(m) >= 3 for m in shared.values())}
    ground = [i for i in W if i["nearest_iou"] >= 0.69]
    named = sum(i["named_as_people"] for i in ground)
    r["P6"] = {"W_on_ground": len(ground), "named_as_people": named,
               "holds": None if len(ground) < 3 else named * 2 >= len(ground)}
    makersW = sorted({i["maker"] for i in W})
    per_fig_W = [i["checks_logged_for_file"] for i in W]
    nv = {m: next(i["maker_not_valid_total"] for i in W if i["maker"] == m) for m in makersW}
    r["P7"] = {"checks_per_W_figure": per_fig_W, "median": statistics.median(per_fig_W), "not_valid_per_maker": nv,
               "holds": statistics.median(per_fig_W) >= 3 and all(v >= 1 for v in nv.values())}
    ch = [i["changes"] for i in C]
    r["P8"] = {"changes": ch, "median": statistics.median(ch), "holds": statistics.median(ch) <= 1}
    leaks = sum(1 for i in items if i["leak"])
    r["P9"] = {"items_with_leak": leaks, "holds": leaks <= 1}
    r["all_valid"] = all(i["valid"] for i in items)
    r["over_cap"] = [i["maker"] + "/" + i["file"] for i in C if i["changes"] > 2]
    json.dump({"items": items, "predictions": r}, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    for k, v in r.items():
        print(k, json.dumps(v))
    print()
    for i in items:
        print(f'{i["maker"]} {i["file"]} {i["nearest_iou"]:.3f} shelf={i["on_shelf"]:d} '
              f'people={i["named_as_people"]:d} ch={i.get("changes", "-")} | {i["first_seen"] or ""} -> {i["name"]} '
              f'|| nearest {i["nearest_id"]}: {", ".join(i["people_named_nearest"][:6])}')


if __name__ == "__main__":
    main()
