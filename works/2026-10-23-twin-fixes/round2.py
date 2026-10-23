"""Experiment 36, Twin Fixes, round 2: move the same 24 pins further, to find where the makers' holding stops.

Written after round 1 came back at its ceiling (results.json) and before any round-2 maker ran.
Seed 1522. Steps of 2, 8 and 30 km on seeded bearings, printed in decimal degrees to five places, like key E.
Writes plan2.json and briefs2/. Same brief template as round 1. Standard library only.
"""
import json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from prepare import hav, move, load, MAKERS

SEED = 1522
STEPS = {"S2": 2.0, "S8": 8.0, "S30": 30.0}
CONDS = list(STEPS)


def main():
    plan = json.load(open(os.path.join(HERE, "plan.json"), encoding="utf8"))
    rows, _ = load()
    rng = random.Random(SEED)
    places = sorted(plan["places"], key=lambda p: p["j"])
    for p in places:
        p["round2"] = {}
        for c, km in STEPS.items():
            b = rng.uniform(0, 360)
            q = move((p["lat"], p["lon"]), km, b)
            qs = ("%.5f" % q[0], "%.5f" % q[1])
            qp = (float(qs[0]), float(qs[1]))
            near = min(rows, key=lambda o: hav(qp, (o["lat"], o["lon"])))
            p["round2"][c] = {"key": "%s, %s" % qs, "lat": qp[0], "lon": qp[1], "bearing": round(b, 1),
                              "km_from_town": round(hav((p["lat"], p["lon"]), qp), 2),
                              "nearest_id": near["id"], "nearest_name": near["name"],
                              "nearest_km": round(hav(qp, (near["lat"], near["lon"])), 2)}
    deal = {}
    for i, m in enumerate(MAKERS):
        items = [{"j": p["j"], "cond": CONDS[(i + p["j"]) % 3]} for p in places]
        for it in items:
            it["key"] = places[it["j"] - 1]["round2"][it["cond"]]["key"]
        rng.shuffle(items)
        for k, it in enumerate(items):
            it["line"] = k + 1
        deal[m] = items
    os.makedirs(os.path.join(HERE, "briefs2"), exist_ok=True)
    head = open(os.path.join(HERE, "brief-template.txt"), encoding="utf8").read()
    for m, items in deal.items():
        open(os.path.join(HERE, "briefs2", m + ".txt"), "w", encoding="utf8").write(
            head.replace("{POINTS}", "\n".join("%d: %s" % (it["line"], it["key"]) for it in items)))
    json.dump({"seed": SEED, "steps_km": STEPS,
               "places": [{"j": p["j"], "id": p["id"], "name": p["name"], "round2": p["round2"]} for p in places],
               "deal": deal}, open(os.path.join(HERE, "plan2.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    for p in places:
        print(p["j"], p["name"], {c: (v["nearest_name"], v["nearest_km"]) for c, v in p["round2"].items()})


if __name__ == "__main__":
    main()
