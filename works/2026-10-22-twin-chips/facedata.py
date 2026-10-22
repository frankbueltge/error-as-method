"""Write face-data.js for index.html from plan.json and results.json."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
r = json.load(open(os.path.join(HERE, "results.json")))
chips = []
for c in r["per_chip"]:
    rows = [x for x in r["rows"] if x["chip"] == c["chip"]]
    def pick(cond, side):
        return [{"m": x["maker"], "name": x["name"], "exact": x["exact"]} for x in rows if x["cond"] == cond and x["side"] == side]
    chips.append({"id": c["chip"], "crowd": c["crowd_name"], "on": c["on"], "off": c["off"],
                  "Non": pick("N", "on"), "Noff": pick("N", "off"), "S": pick("S", "on") + pick("S", "off")})
cells = {k: {"n": v["n"], "exact": v["exact"], "pct": v["exact_pct"]} for k, v in r["cells"].items()}
open(os.path.join(HERE, "face-data.js"), "w").write("window.TWIN=" + json.dumps({"chips": chips, "cells": cells}) + ";\n")
print("ok", len(chips))
