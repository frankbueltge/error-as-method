"""Compare the gazetteer's point for each drawn place with Wikidata's (P625 via P1566), and the twin's step with that gap.
Reads plan.json and sources/wikidata-p625.json (Wikidata Query Service, CC0, fetched 2026-10-23). Writes canons.json."""
import json, os, re, statistics, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
from prepare import hav
plan = json.load(open(os.path.join(HERE, "plan.json"), encoding="utf8"))
wd = json.load(open(os.path.join(HERE, "sources", "wikidata-p625.json"), encoding="utf8"))
by = {}
for b in wd["results"]["bindings"]:
    lon, lat = map(float, re.findall(r"-?[\d.]+", b["coord"]["value"]))
    by.setdefault(b["g"]["value"], []).append((b["item"]["value"], lat, lon))
out = []
for p in sorted(plan["places"], key=lambda p: p["j"]):
    rows = by.get(p["id"], [])
    gap = min((hav((p["lat"], p["lon"]), (la, lo)) for _, la, lo in rows), default=None)
    out.append({"j": p["j"], "name": p["name"], "twin_km": p["twin_km"], "wikidata": [r[0] for r in rows],
                "gap_km": None if gap is None else round(gap, 3)})
gaps = [o["gap_km"] for o in out if o["gap_km"] is not None]
summary = {"places_with_wikidata_point": len(gaps), "median_gap_km": round(statistics.median(gaps), 3),
           "median_twin_km": round(statistics.median(o["twin_km"] for o in out), 3),
           "twin_smaller_than_gap": sum(1 for o in out if o["gap_km"] is not None and o["twin_km"] < o["gap_km"])}
json.dump({"summary": summary, "places": out}, open(os.path.join(HERE, "canons.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(summary)
for o in out: print(o["j"], o["name"], o["twin_km"], o["gap_km"])
