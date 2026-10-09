"""score.py -- P1-P9 from looks.json, coder B, coder C and open.json. Writes results.json."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(H, f)))
looks = {r["maker"]: r for r in J("looks.json")}; op = J("open.json")
kb, ab = J("keys/coder-b.json"), J("coderB/answers-as-returned.json")
kc, ac = J("keys/coder-c.json"), J("coderC/answers-as-returned.json")
arm = lambda a: [m for m, r in looks.items() if r["return"] == a]
reo = lambda a: sum(looks[m]["reopened"] for m in arm(a))
fit = {}
for p, k in kb.items(): fit[(k["maker"], k["stage"])] = ab[p]
share = lambda a: sum(x == "APPLIES" for m in arm(a) for x in fit[(m, "first")]) / (3 * len(arm(a)))
absent = [(m, i) for m in arm("X") for i, x in enumerate(fit[(m, "first")]) if x == "ABSENT"]
acted_absent = [(m, i) for m, i in absent if op["notes"][m]["codes"][i] == "ACTED"]
changers = [m for m in arm("S") + arm("X") if looks[m]["reopened"]]
D = lambda d: sum(d.values())
pairs = {}
for q, k in kc.items():
    a = ac[q]; d = {k["X"]: D(a["defects_X"]), k["Y"]: D(a["defects_Y"])}
    pairs[k["maker"]] = {"rating": a["rating"], "defects_first": d["first"], "defects_second": d["second"],
                         "tags": [t for _, t in a["differences"]]}
r = {
 "P1": {"pred": "H reopened <= 1 of 4", "value": reo("H"), "held": reo("H") <= 1},
 "P2": {"pred": "S reopened >= 3 of 4", "value": reo("S"), "held": reo("S") >= 3},
 "P3": {"pred": "X reopened >= 3 of 4", "value": reo("X"), "held": reo("X") >= 3},
 "P4": {"pred": ">= 2 of 4 X say a note does not describe their work", "value": sum(v > 0 for v in op["absence_said"].values()),
        "held": sum(v > 0 for v in op["absence_said"].values()) >= 2},
 "P5": {"pred": ">= 75% of S/X changers render after return", "value": "%d of %d" % (sum(looks[m]["looks_after_return"] > 0 for m in changers), len(changers)),
        "held": sum(looks[m]["looks_after_return"] > 0 for m in changers) >= 0.75 * len(changers)},
 "P6": {"pred": "<= 2 S/X changers look first", "value": sum(looks[m]["looked_first"] for m in changers), "held": sum(looks[m]["looked_first"] for m in changers) <= 2},
 "P7": {"pred": "S APPLIES >= 2/3 and X APPLIES <= 1/3 on first picture", "value": "S %.2f, X %.2f" % (share("S"), share("X")),
        "held": share("S") >= 2 / 3 and share("X") <= 1 / 3},
 "P8": {"pred": "makers ACT on >= half of X notes rated ABSENT", "value": "%d of %d" % (len(acted_absent), len(absent)),
        "held": len(acted_absent) >= len(absent) / 2},
 "P9": {"pred": "<= 1 changed pair rated 0 or 1", "value": sum(p["rating"] <= 1 for p in pairs.values()), "held": sum(p["rating"] <= 1 for p in pairs.values()) <= 1},
}
extra = {"pairs": pairs,
         "defects_by_return": {a: [sum(pairs[m]["defects_first"] for m in arm(a) if m in pairs), sum(pairs[m]["defects_second"] for m in arm(a) if m in pairs)] for a in "HSX"},
         "S_applies_first_second": [sum(x == "APPLIES" for m in arm("S") for x in fit[(m, st)]) for st in ("first", "second")],
         "X_absent_notes": absent, "X_acted_on_absent": acted_absent,
         "X_partly_notes_acted": [(m, i) for m in arm("X") for i, x in enumerate(fit[(m, "first")]) if x == "PARTLY" and op["notes"][m]["codes"][i] == "ACTED"],
         "X_partly_notes": [(m, i) for m in arm("X") for i, x in enumerate(fit[(m, "first")]) if x == "PARTLY"]}
json.dump({"predictions": r, "derived": extra}, open(os.path.join(H, "results.json"), "w"), indent=1)
for k, v in r.items(): print(k, "HELD" if v["held"] else "FAILED", v["value"], "--", v["pred"])
print(json.dumps(extra, indent=0)[:1500])
