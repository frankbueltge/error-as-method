"""score.py: Session 144. Unmasks the two blind codes with coder/key.json and scores P1-P7 as PREDICTIONS.md
registered them. Writes results.json and prints the table."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); L = lambda p: json.load(open(os.path.join(H, p)))
key, X, W, PV = L("coder/key.json"), L("coder/codes-X.json"), L("coder/codes-W.json"), L("practice-verdict.json")
parent = L("plan.json")["parent"]
x = {key["X_variants"][c["id"]]: dict(c, nearest_work=key["X_family"].get(c["nearest"])) for c in X}
w = {key["W"][c["id"]]: c for c in W["items"]}
C = ["c1", "c2", "c3", "c4"]; A = ["a1", "a2", "a3", "a4"]; M = ["m%02d" % i for i in range(1, 13)]
yes = lambda k: w[k]["works"].lower().startswith("y"); broken = lambda k: x[k]["broken"].lower().startswith("y")
dist = lambda k: x[k]["distance"]
info = lambda k: (not broken(k)) and (dist(k) or 0) >= 2 and yes(k)
mnb = [k for k in M if not broken(k)]; mfar = [k for k in mnb if (dist(k) or 0) >= 2]
pv = {**PV["M"], **PV["A"]}; agree = [k for k in A + M if (pv[k][0] == "works") == yes(k)]
P = {
 "P1": {"held": sum(1 for k in A if x[k]["nearest_work"] == parent and dist(k) <= 1) >= 3,
        "count": "A with parent nearest and distance <= 1: %d of 4" % sum(1 for k in A if x[k]["nearest_work"] == parent and dist(k) <= 1)},
 "P2": {"held": len(mfar) <= len(mnb) / 3, "count": "M not broken %d, of them distance >= 2: %d" % (len(mnb), len(mfar))},
 "P3": {"held": sum(map(broken, M)) >= 3, "count": "M broken: %d of 12" % sum(map(broken, M))},
 "P4": {"held": sum(map(yes, C)) >= 3 and sum(map(yes, A)) >= 3 and sum(map(yes, M)) <= 6,
        "count": "W works: C %d/4, A %d/4, M %d/12" % (sum(map(yes, C)), sum(map(yes, A)), sum(map(yes, M)))},
 "P5": {"held": None if not mfar else sum(map(yes, mfar)) <= 1, "count": "M far and not broken: %d (untestable if 0)" % len(mfar)},
 "P6": {"held": len(agree) >= 13, "count": "practice agrees with W on %d of 16; disagrees on %s" % (len(agree), [k for k in A + M if k not in agree])},
 "P7": {"held": sum(map(info, A)) >= sum(map(info, M)), "count": "information: A %d, M %d" % (sum(map(info, A)), sum(map(info, M)))},
}
rows = {k: {"arm": k[0].upper(), "x_broken": x.get(k, {}).get("broken"), "x_nearest": x.get(k, {}).get("nearest_work"),
            "x_distance": x.get(k, {}).get("distance"), "w_works": w[k]["works"], "w_why": w[k]["why"],
            "practice": pv.get(k, [None])[0], "information": info(k) if k in x else None} for k in C + A + M}
json.dump({"parent": parent, "w_meaning": W["meaning"], "predictions": P, "rows": rows}, open(os.path.join(H, "results.json"), "w"), indent=1)
for k, v in P.items(): print(k, {True: "HELD", False: "FAILED", None: "UNTESTABLE"}[v["held"]], "-", v["count"])
for k, r in rows.items(): print(k, r["x_broken"], r["x_nearest"], r["x_distance"], r["w_works"], r["practice"], "INFO" if r["information"] else "", "|", r["w_why"][:90])
