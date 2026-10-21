"""score.py: Session 145. Unmasks the three blind codes with coder/key.json and scores P1-P8 as PREDICTIONS.md
registered them, plus S144.CHANCE's falsifying test as a side test. Writes results.json and prints the table."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); L = lambda p: json.load(open(os.path.join(H, p)))
key, X, W, V, PV = L("coder/key.json"), L("coder/codes-X.json"), L("coder/codes-W.json"), L("coder/codes-V.json"), L("practice-verdict.json")["M"]
x = {key["X_variants"][c["id"]]: dict(c, nearest_work=key["X_family"].get(c["nearest"])) for c in X}
w = {key["W"][c["id"]]: c for c in W["items"]}; v = {key["V"][c["id"]]: c for c in V}
C = ["c1", "c2", "c3", "c4"]; arm = lambda a: [a + str(i) for i in range(1, 9)]; U, T, S = arm("u"), arm("t"), arm("s"); M = U + T + S
yes = lambda k: w[k]["works"].lower().startswith("y"); broken = lambda k: x[k]["broken"].lower().startswith("y")
dist = lambda k: x[k]["distance"] if isinstance(x[k]["distance"], int) else -1
info = lambda k: (not broken(k)) and dist(k) >= 2 and yes(k)
false = lambda k: v[k]["agrees"].lower().startswith("n")
n = lambda f, ks: sum(1 for k in ks if f(k))
far = [k for k in M if not broken(k) and dist(k) >= 2]
acc1 = [k for k in M if yes(k) and dist(k) >= 1]
WORDS = ["wrong", "false", "incorrect", "mislabel", "mismatch", "not the", "should be", "actually", "error", "nonsens", "inaccura"]
named = [k for k in M if yes(k) and any(t in w[k]["why"].lower() for t in WORDS)]
agree = [k for k in M if (PV[k][0] == "works") == yes(k)]
I = {a: [k for k in ks if info(k)] for a, ks in (("U", U), ("T", T), ("S", S))}
P = {
 "P1": {"held": n(broken, U) >= 3 and n(broken, S) <= 1, "count": "broken: U %d of 8, S %d of 8" % (n(broken, U), n(broken, S))},
 "P2": {"held": n(lambda k: dist(k) == 0, T) >= 2 and n(lambda k: dist(k) == 0, S) <= 1,
        "count": "distance 0: T %d of 8, S %d of 8" % (n(lambda k: dist(k) == 0, T), n(lambda k: dist(k) == 0, S))},
 "P3": {"held": len(far) <= 4, "count": "not broken and distance >= 2: %d of 24 %s" % (len(far), far)},
 "P4": {"held": sum(map(len, I.values())) >= 1 and not I["U"], "count": "information: %s" % I},
 "P5": {"held": len(I["S"]) >= len(I["T"]) >= len(I["U"]), "count": "information S %d, T %d, U %d" % (len(I["S"]), len(I["T"]), len(I["U"]))},
 "P6": {"held": None if not acc1 else n(false, acc1) >= len(acc1) / 2, "count": "W accepts and distance >= 1: %d %s; V says no to %d" % (len(acc1), acc1, n(false, acc1))},
 "P7": {"held": len(named) <= 1, "count": "accepted mutants whose W reason names a false value (word list in score.py): %d %s" % (len(named), named)},
 "P8": {"held": len(agree) >= 18, "count": "practice agrees with W on %d of 24; disagrees on %s" % (len(agree), [k for k in M if k not in agree])},
}
side = {"S144.CHANCE_test_fires": bool(far and any(yes(k) for k in far)), "far_and_accepted": [k for k in far if yes(k)],
        "note": "Side test only: tonight's operator acts on the table, not on code, so this is not the row's event."}
rows = {k: {"arm": "C" if k[0] == "c" else k[0].upper(), "x_broken": x.get(k, {}).get("broken"), "x_nearest": x.get(k, {}).get("nearest_work"),
            "x_distance": x.get(k, {}).get("distance"), "x_seen": x.get(k, {}).get("seen"), "w_works": w[k]["works"], "w_why": w[k]["why"],
            "v_agrees": v[k]["agrees"], "v_why": v[k]["why"], "practice": PV.get(k, [None, None])[:2],
            "information": info(k) if k in x else None} for k in C + M}
json.dump({"parent": L("plan.json")["parent"], "w_meaning": W["meaning"], "predictions": P, "side_test": side, "rows": rows},
          open(os.path.join(H, "results.json"), "w"), indent=1, ensure_ascii=False)
for k, p in P.items(): print(k, {True: "HELD", False: "FAILED", None: "UNTESTABLE"}[p["held"]], "-", p["count"])
print("side:", side)
for k, r in rows.items(): print(k, r["x_broken"], r["x_nearest"], r["x_distance"], r["w_works"], r["v_agrees"], r["practice"], "INFO" if r["information"] else "", "|", r["w_why"][:80], "|", r["v_why"][:80])
