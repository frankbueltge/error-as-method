"""Fetch every ComCat event worldwide, 2026-09-03 to 2026-10-03 UTC, in daily windows (the service
caps one query at 20,000 events), and write data.js (compact records) and harvest-log.json."""
import json, hashlib, time, urllib.request, datetime as dt
BASE = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&orderby=time-asc"
start = dt.datetime(2026, 9, 3); log = []; recs = {}
for d in range(30):
    a = start + dt.timedelta(days=d); b = a + dt.timedelta(days=1)
    url = f"{BASE}&starttime={a:%Y-%m-%dT%H:%M:%S}&endtime={b:%Y-%m-%dT%H:%M:%S}"
    raw = urllib.request.urlopen(url, timeout=120).read()
    j = json.loads(raw); n = len(j["features"])
    log.append({"url": url, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "events": n,
                "fetched": dt.datetime.utcnow().isoformat() + "Z"})
    for f in j["features"]:
        p = f["properties"]; c = f["geometry"]["coordinates"]
        recs[f["id"]] = [p["time"], c[1], c[0], c[2], p["mag"], p["magType"], p["type"], p["status"], p["net"], p["place"]]
    print(a.date(), n); time.sleep(1)
D = sorted(recs.values(), key=lambda r: r[0])
open("data.js", "w").write("const D=" + json.dumps(D, separators=(",", ":")) + ";\n")
json.dump({"query": BASE, "windows": log, "unique_events": len(D)}, open("harvest-log.json", "w"), indent=1)
print("unique", len(D))
