"""prepare.py -- builds data.js from the City of Seattle file and lays out the twelve makers' folders.

python3 prepare.py <scratch-root>

The makers work outside this repository, in <scratch-root>/<id>/..., so that nothing of this
experiment's own name is in reach of them (F-195, Session 114). Only the surround varies by
condition; data.js, the brief and the viewport are the same bytes for every maker, except that
condition E adds one first line to data.js and condition F adds one sentence to the brief.
"""
import json, os, random, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
WORD = "orchard"
CONDITIONS = ["A", "A", "B", "B", "C", "C", "D", "D", "E", "E", "F", "F"]
SEED = 115


def data_js():
    rows = json.load(open(os.path.join(HERE, "sources", "fremont-2025.json")))
    assert len(rows) == 8760
    hours = []
    for r in rows:
        if "fremont_bridge" not in r:
            hours.append(None)
        else:
            hours.append([int(r["fremont_bridge"]), int(r["fremont_bridge_nb"]), int(r["fremont_bridge_sb"])])
    body = "window.COUNTS = " + json.dumps({"first": "2025-01-01T00:00", "step": "1 hour",
                                             "fields": ["total", "northbound", "southbound"],
                                             "hours": hours}, separators=(",", ":")) + ";\n"
    return body


def layout(root):
    rnd = random.Random(SEED)
    conds = CONDITIONS[:]
    rnd.shuffle(conds)
    plan = []
    body = data_js()
    for i, c in enumerate(conds, 1):
        mid = "m%02d" % i
        if c == "B":
            folder = os.path.join(root, mid, WORD)
        elif c == "C":
            folder = os.path.join(root, mid, WORD, "work")
        else:
            folder = os.path.join(root, mid, "work")
        os.makedirs(folder, exist_ok=True)
        js = ("// " + WORD + "\n" + body) if c == "E" else body
        open(os.path.join(folder, "data.js"), "w").write(js)
        if c == "D":
            open(os.path.join(folder, WORD + ".txt"), "w").close()
        plan.append({"maker": mid, "condition": c, "folder": folder,
                     "data_sha256": hashlib.sha256(js.encode()).hexdigest()})
    return plan


if __name__ == "__main__":
    root = sys.argv[1]
    open(os.path.join(HERE, "data.js"), "w").write(data_js())
    plan = layout(root)
    json.dump(plan, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
    for p in plan:
        print(p["maker"], p["condition"], p["folder"])
