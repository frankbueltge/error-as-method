"""Post hoc, after both rounds were scored (not one of the fixed rules): place every round-2 answer in GeoNames
cities500 (places of 500 people or more, CC BY 4.0), to measure how far the named place is from the pin and whether
it is the nearest such place. Usage: python3 place500.py <cities500.txt>. Writes place500.json (derived rows only;
the 236,640-row file is not committed, its hash is in sources/MANIFEST.json)."""
import json, os, statistics, sys
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from prepare import hav, load
from score import norm, SYN

_, countries = load()
cc_by = {norm(c["name"]): cc for cc, c in countries.items()}
for k, v in SYN.items():
    for s in v:
        cc_by[norm(s)] = cc_by[norm(k)]
idx, allrows = defaultdict(list), []
for line in open(sys.argv[1], encoding="utf8"):
    f = line.rstrip("\n").split("\t")
    r = {"id": f[0], "name": f[1], "lat": float(f[4]), "lon": float(f[5]), "cc": f[8], "pop": int(f[14] or 0)}
    allrows.append(r)
    for n in {norm(f[1]), norm(f[2])} | {norm(a) for a in f[3].split(",") if a and a.isascii()}:
        idx[(f[8], n)].append(r)
res = json.load(open(os.path.join(HERE, "results2.json"), encoding="utf8"))
out = []
for x in res["pins"]:
    town, _, country = x["answer"].rpartition(",")
    cc = cc_by.get(norm(country))
    pin = tuple(x["pin"])
    near = [r for r in allrows if r["cc"] == cc and abs(r["lat"] - pin[0]) < 1 and abs(r["lon"] - pin[1]) < 1]
    nearest = min(near, key=lambda r: hav(pin, (r["lat"], r["lon"]))) if near else None
    cands = idx.get((cc, norm(town)), [])
    if x["orig"]:
        err = x["err_km"]; named = None
    elif cands:
        b = min(cands, key=lambda r: hav(pin, (r["lat"], r["lon"])))
        err, named = round(hav(pin, (b["lat"], b["lon"])), 1), [b["lat"], b["lon"], b["name"], b["pop"]]
    else:
        err, named = None, None
    rank = None
    if err is not None and near:
        rank = 1 + sum(1 for r in near if hav(pin, (r["lat"], r["lon"])) < err - 0.05)
    out.append({"maker": x["maker"], "j": x["j"], "cond": x["cond"], "answer": x["answer"], "err500_km": err,
                "named500": named, "rank500": rank,
                "nearest500": [nearest["name"], round(hav(pin, (nearest["lat"], nearest["lon"])), 1)] if nearest else None})
summ = {}
for c in ["S2", "S8", "S30"]:
    ps = [o for o in out if o["cond"] == c]
    e = [o["err500_km"] for o in ps if o["err500_km"] is not None]
    summ[c] = {"placed": len(e), "median_err_km": round(statistics.median(e), 1) if e else None,
               "within_10km_of_named": sum(1 for v in e if v <= 10), "rank1": sum(1 for o in ps if o["rank500"] == 1)}
json.dump({"summary": summ, "pins": out}, open(os.path.join(HERE, "place500.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(summ)
for o in out:
    if o["cond"] == "S30" or o["err500_km"] is None:
        print(o["j"], o["cond"], o["answer"], o["err500_km"], o["rank500"], o["nearest500"])
