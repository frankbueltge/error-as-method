"""Experiment 36, Twin Fixes: score the replies by the rules fixed in PREDICTIONS.md.

Reads plan.json, rooms/<maker>/REPLY.txt, sources/cities15000-columns.tsv. Writes results.json.
Standard library only.
"""
import json, math, os, re, statistics, sys, unicodedata
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from prepare import hav, load

SYN = {"United States": ["usa", "us", "united states of america", "america"], "Russia": ["russian federation"],
       "Turkey": ["turkiye"], "Papua New Guinea": ["png"]}


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"[’'\-.]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def parse(text):
    out, how, tools = {}, "", ""
    for line in text.splitlines():
        m = re.match(r"\s*(\d+)\s*:\s*(.+)$", line)
        if m:
            out[int(m.group(1))] = m.group(2).strip()
        elif line.startswith("HOW:"):
            how = line[4:].strip()
        elif line.startswith("TOOLS:"):
            tools = line[6:].strip()
    return out, how, tools


def main():
    plan = json.load(open(os.path.join(HERE, "plan.json"), encoding="utf8"))
    rows, countries = load()
    names_by_cc = defaultdict(lambda: defaultdict(list))
    for r in rows:
        for n in {norm(r["name"]), norm(r["ascii"])}:
            names_by_cc[r["cc"]][n].append(r)
    cc_by_country = {}
    for cc, c in countries.items():
        cc_by_country[norm(c["name"])] = cc
    for cname, syns in SYN.items():
        cc = cc_by_country[norm(cname)]
        for s in syns:
            cc_by_country[norm(s)] = cc
    places = {p["j"]: p for p in plan["places"]}
    pins = []
    makers = {}
    for m, items in plan["deal"].items():
        text = open(os.path.join(HERE, "rooms", m, "REPLY.txt"), encoding="utf8").read()
        ans, how, tools = parse(text)
        makers[m] = {"how": how, "tools": tools}
        for it in items:
            p = places[it["j"]]
            raw = ans.get(it["line"], "")
            town, _, country = raw.rpartition(",") if "," in raw else (raw, "", "")
            nt, nc = norm(town), norm(country)
            okn = {norm(p["name"]), norm(p["ascii"])} | {norm(a) for a in p.get("alternatenames", [])}
            town_hit = nt in okn
            country_hit = cc_by_country.get(nc) == p["cc"]
            dist = 0.0 if town_hit else None
            named_at = None
            if not town_hit and nc in cc_by_country:
                cands = names_by_cc[cc_by_country[nc]].get(nt, [])
                if cands:
                    best = min(cands, key=lambda o: hav((p["lat"], p["lon"]), (o["lat"], o["lon"])))
                    dist = round(hav((p["lat"], p["lon"]), (best["lat"], best["lon"])), 1)
                    named_at = [best["lat"], best["lon"]]
            pins.append({"maker": m, "line": it["line"], "j": it["j"], "cond": it["cond"], "key": it["key"],
                         "answer": raw, "town_hit": town_hit, "country_hit": country_hit,
                         "dist_km": dist, "named_at": named_at})
    summ = {}
    for c in "EDT":
        ps = [x for x in pins if x["cond"] == c]
        misses = [x["dist_km"] for x in ps if not x["town_hit"] and x["dist_km"] is not None]
        placed = [x["dist_km"] for x in ps if x["dist_km"] is not None]
        summ[c] = {"n": len(ps), "town": sum(x["town_hit"] for x in ps), "country": sum(x["country_hit"] for x in ps),
                   "placed_misses": len(misses), "unplaced_misses": sum(1 for x in ps if x["dist_km"] is None),
                   "median_dist_placed_misses": round(statistics.median(misses), 1) if misses else None,
                   "median_dist_all_placed": round(statistics.median(placed), 1) if placed else None}
        summ[c]["town_rate"] = round(100 * summ[c]["town"] / len(ps), 1)
        summ[c]["country_rate"] = round(100 * summ[c]["country"] / len(ps), 1)
    E, D, T = (summ[c]["town_rate"] for c in "EDT")
    cr = [summ[c]["country_rate"] for c in "EDT"]
    preds = {
        "P1": {"holds": T >= (2 / 3) * E, "detail": "T %.1f%% vs two thirds of E %.1f%% = %.1f%%" % (T, E, 2 / 3 * E)},
        "P2": {"holds": abs(E - D) < 10, "detail": "E %.1f%%, D %.1f%%" % (E, D)},
        "P3": {"holds": max(cr) - min(cr) <= 5, "detail": "country E/D/T %s" % cr},
        "P4": {"holds": 20 <= E <= 80, "detail": "E %.1f%%" % E},
        "P5": {"holds": None, "detail": "read by hand from the HOW lines; see journal"},
    }
    per_place = []
    for j in sorted(places):
        p = places[j]
        d = {"j": j, "name": p["name"], "country": p["country"], "continent": p["continent"], "pop": p["pop"]}
        for c in "EDT":
            ps = [x for x in pins if x["j"] == j and x["cond"] == c]
            d[c] = {"town": sum(x["town_hit"] for x in ps), "country": sum(x["country_hit"] for x in ps),
                    "answers": [x["answer"] for x in ps]}
        per_place.append(d)
    per_maker = {m: {c: sum(x["town_hit"] for x in pins if x["maker"] == m and x["cond"] == c) for c in "EDT"}
                 for m in plan["deal"]}
    json.dump({"summary": summ, "predictions": preds, "per_place": per_place, "per_maker": per_maker,
               "makers": makers, "pins": pins}, open(os.path.join(HERE, "results.json"), "w", encoding="utf8"),
              ensure_ascii=False, indent=1)
    print(json.dumps(summ, indent=1))
    print(json.dumps(preds, indent=1))
    print(per_maker)
    for d in per_place:
        print(d["j"], d["name"], d["country"], "E", d["E"]["town"], "D", d["D"]["town"], "T", d["T"]["town"])


if __name__ == "__main__":
    main()
