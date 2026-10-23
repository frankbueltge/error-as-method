"""Experiment 36, Twin Fixes, round 2: score by the rules added to PREDICTIONS.md before round 2 ran.
Reads plan.json, plan2.json, rooms2/<maker>/REPLY.txt, sources/cities15000-columns.tsv. Writes results2.json."""
import json, os, statistics, sys
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from prepare import hav, load
from score import norm, parse, SYN

CAPTURE_KM = 10.0


def main():
    plan = json.load(open(os.path.join(HERE, "plan.json"), encoding="utf8"))
    plan2 = json.load(open(os.path.join(HERE, "plan2.json"), encoding="utf8"))
    rows, countries = load()
    byid = {r["id"]: r for r in rows}
    names_by_cc = defaultdict(lambda: defaultdict(list))
    for r in rows:
        for n in {norm(r["name"]), norm(r["ascii"])}:
            names_by_cc[r["cc"]][n].append(r)
    cc_by_country = {norm(c["name"]): cc for cc, c in countries.items()}
    for cname, syns in SYN.items():
        for s in syns:
            cc_by_country[norm(s)] = cc_by_country[norm(cname)]
    places = {p["j"]: p for p in plan["places"]}
    r2 = {p["j"]: p["round2"] for p in plan2["places"]}
    pins, makers = [], {}
    for m, items in plan2["deal"].items():
        ans, how, tools = parse(open(os.path.join(HERE, "rooms2", m, "REPLY.txt"), encoding="utf8").read())
        makers[m] = {"how": how, "tools": tools}
        for it in items:
            p, k = places[it["j"]], r2[it["j"]][it["cond"]]
            raw = ans.get(it["line"], "")
            town, _, country = raw.rpartition(",") if "," in raw else (raw, "", "")
            nt, nc = norm(town), norm(country)
            okn = {norm(p["name"]), norm(p["ascii"])} | {norm(a) for a in p.get("alternatenames", [])}
            if p["id"] == "13132453":
                okn.add("shearia")
            orig = nt in okn
            captured = k["nearest_id"] != p["id"] and k["nearest_km"] <= CAPTURE_KM
            near = k["nearest_id"] != p["id"] and nt in {norm(byid[k["nearest_id"]]["name"]), norm(byid[k["nearest_id"]]["ascii"])}
            err, at = None, None
            cands = names_by_cc[cc_by_country[nc]].get(nt, []) if nc in cc_by_country else []
            if orig:
                cands = [byid[p["id"]]]
            if cands:
                best = min(cands, key=lambda o: hav((k["lat"], k["lon"]), (o["lat"], o["lon"])))
                err, at = round(hav((k["lat"], k["lon"]), (best["lat"], best["lon"])), 1), [best["lat"], best["lon"], best["name"]]
            pins.append({"maker": m, "line": it["line"], "j": it["j"], "cond": it["cond"], "key": k["key"],
                         "pin": [k["lat"], k["lon"]], "answer": raw, "orig": orig, "captured": captured,
                         "near": near, "nearest": k["nearest_name"], "nearest_km": k["nearest_km"],
                         "err_km": err, "named_at": at, "country_hit": cc_by_country.get(nc) == p["cc"]})
    summ = {}
    for c in ["S2", "S8", "S30"]:
        ps = [x for x in pins if x["cond"] == c]
        errs = [x["err_km"] for x in ps if x["err_km"] is not None]
        summ[c] = {"n": len(ps), "orig": sum(x["orig"] for x in ps), "country": sum(x["country_hit"] for x in ps),
                   "orig_rate": round(100 * sum(x["orig"] for x in ps) / len(ps), 1),
                   "placed": len(errs), "median_err_km": round(statistics.median(errs), 1) if errs else None}
    cap = [x for x in pins if x["cond"] == "S30" and x["captured"]]
    summ["captured_S30"] = {"n": len(cap), "near": sum(x["near"] for x in cap), "orig": sum(x["orig"] for x in cap)}
    preds = {"Q1": summ["S2"]["orig_rate"] >= 90, "Q2": summ["S8"]["orig_rate"] >= 75,
             "Q3": cap and sum(x["near"] for x in cap) >= 0.5 * len(cap) and sum(x["orig"] for x in cap) <= 0.2 * len(cap),
             "Q4": summ["S30"]["median_err_km"] is not None and summ["S30"]["median_err_km"] <= 15,
             "Q5": "read by hand"}
    json.dump({"summary": summ, "predictions": preds, "makers": makers, "pins": pins},
              open(os.path.join(HERE, "results2.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print(json.dumps(summ, indent=1)); print(preds)
    for x in sorted(pins, key=lambda x: (x["j"], x["cond"])):
        print(x["j"], places[x["j"]]["name"][:12], x["cond"], "|", x["answer"], "|", "ORIG" if x["orig"] else ("NEAR" if x["near"] else "-"), x["err_km"], "cap" if x["captured"] else "", x["nearest"], x["nearest_km"])


if __name__ == "__main__":
    main()
