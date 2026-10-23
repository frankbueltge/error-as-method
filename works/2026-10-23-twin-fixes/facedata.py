"""Experiment 36, Twin Fixes: gather what the face shows into face-data.js.
Reads plan.json, plan2.json, results.json, results2.json, place500.json. Standard library only."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda f: json.load(open(os.path.join(HERE, f), encoding="utf8"))
plan, plan2, r1, r2, p5 = J("plan.json"), J("plan2.json"), J("results.json"), J("results2.json"), J("place500.json")
r2p = {p["j"]: p["round2"] for p in plan2["places"]}
places = []
for p in sorted(plan["places"], key=lambda p: p["j"]):
    steps = []
    for c, km, lat, lon, key in [("E", 0, p["lat"], p["lon"], p["key_E"]), ("D", 0, p["lat"], p["lon"], p["key_D"]),
                                 ("T", p["twin_km"], p["twin_lat"], p["twin_lon"], p["key_T"])]:
        ans = [x for x in r1["pins"] if x["j"] == p["j"] and x["cond"] == c]
        steps.append({"c": c, "km": km, "pin": [lat, lon], "key": key,
                      "a": [{"t": x["answer"], "o": x["town_hit"] or x["answer"].startswith("Shearia"),
                             "at": [p["lat"], p["lon"]] if (x["town_hit"] or x["answer"].startswith("Shearia")) else None} for x in ans]})
    for c in ["S2", "S8", "S30"]:
        k = r2p[p["j"]][c]
        ans = [(x, y) for x, y in zip(r2["pins"], p5["pins"]) if x["j"] == p["j"] and x["cond"] == c]
        a = []
        for x, y in ans:
            at = [p["lat"], p["lon"]] if x["orig"] else (y["named500"][:2] if y["named500"] and y["err500_km"] < 200 else None)
            a.append({"t": x["answer"], "o": x["orig"], "at": at, "near": y["rank500"] == 1})
        steps.append({"c": c, "km": k["km_from_town"], "pin": [k["lat"], k["lon"]], "key": k["key"], "a": a,
                      "nearest": [k["nearest_name"], k["nearest_km"]]})
    places.append({"j": p["j"], "name": p["name"], "country": p["country"], "pop": p["pop"], "lat": p["lat"], "lon": p["lon"], "steps": steps})
out = {"places": places,
       "r1": {c: r1["summary"][c] for c in "EDT"}, "r2": {c: r2["summary"][c] for c in ["S2", "S8", "S30"]},
       "captured": r2["summary"]["captured_S30"], "p500": p5["summary"],
       "chips": {"exact": 27.8, "twin": 12.5}}
open(os.path.join(HERE, "face-data.js"), "w", encoding="utf8").write("window.TF = " + json.dumps(out, ensure_ascii=False) + ";\n")
print(len(json.dumps(out)))
