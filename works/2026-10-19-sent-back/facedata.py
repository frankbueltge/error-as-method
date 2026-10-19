"""facedata.py -- writes face-data.js for index.html from results.json, versions.jsonl, declines.jsonl and reports/.
Each round's 'said' is the first sentence of the maker's own hand-back for that round, verbatim."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json")))
dec = [json.loads(l) for l in open(os.path.join(HERE, "declines.jsonl"))]
title = {}
for m in R["arms"]:
    t = open(os.path.join(HERE, "makers", m, "v1", "NOTE.md")).read().strip().splitlines()[0]
    title[m] = t.lstrip("# ").strip()


def first(m, r):
    t = open(os.path.join(HERE, "reports", "%s-r%d.md" % (m, r))).read().strip()
    t = re.sub(r"\*\*|`", "", t).split("\n")[0]
    s = re.split(r"(?<=[.!?])\s", t, maxsplit=1)[0]
    return s


out = []
for m in sorted(R["arms"], key=lambda x: (R["arms"][x] != "K", x)):
    rounds = []
    n = max(int(f.split("-r")[1][:-3]) for f in os.listdir(os.path.join(HERE, "reports")) if f.startswith(m + "-r"))
    for r in range(1, n + 1):
        d = any(x["maker"] == m and x["round"] == r for x in dec)
        st = R["steps"].get(m, {}).get(str(r - 1)) or R["steps"].get(m, {}).get(r - 1) if r > 1 and not d else None
        rounds.append({"r": r, "made": not d, "v": None if d else r, "said": first(m, r),
                       "code": st["code"] if st else None, "also": st["also"] if st else None,
                       "sentence": "first brief" if r == 1 else ("may stop" if (R["arms"][m] == "D" or r == 7) else "go on")})
    out.append({"maker": m, "arm": R["arms"][m], "title": title[m], "last": R["last_version"][m], "rounds": rounds,
                "bytes": R["bytes"][m], "pixel": R["pixel_change"][m],
                "best": R["order_best"].get(m, {}).get("best"), "rho": R["order_best"].get(m, {}).get("rho")})
open(os.path.join(HERE, "face-data.js"), "w").write("window.SENT = " + json.dumps(out, ensure_ascii=False, indent=0) + ";\n")
for o in out: print(o["maker"], o["arm"], o["title"], [(x["r"], x["made"], x["code"]) for x in o["rounds"]])
