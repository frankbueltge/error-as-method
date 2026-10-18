"""extract.py: fetches tonight's source from the NRCS Air and Water Database REST service (National Water and Climate
Center, USDA NRCS; public domain, data.gov record "Soil Climate Analysis Network (SCAN)", licence
https://www.usa.gov/publicdomain/label/1.0/). Station 2064:MS:SCAN (Starkville, Mississippi), element STO (soil
temperature, observed) at -2 inches (5 cm), hourly, 2025-07-15 00:00 to 2025-09-13 23:00 (station local standard
time, as the service stores it). Writes the service's answer unchanged to sources/, the station record beside it,
and URL, byte count and SHA-256 of both to sources/MANIFEST.json."""
import os, json, hashlib, urllib.request, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
URLS = {"sto_2in_hourly.json": "https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/data?stationTriplets=2064:MS:SCAN"
        "&elements=STO:-2&duration=HOURLY&beginDate=2025-07-15%2000:00&endDate=2025-09-13%2023:00",
        "station.json": "https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/stations?stationTriplets=2064:MS:SCAN"}
man = {"fetched_utc": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
       "publisher": "USDA NRCS National Water and Climate Center", "licence": "US public domain "
       "(https://catalog.data.gov/dataset/soil-climate-analysis-network-scan: https://www.usa.gov/publicdomain/label/1.0/)",
       "files": {}}
for name, url in URLS.items():
    with urllib.request.urlopen(url, timeout=90) as r:
        b = r.read(); status = r.status
    open(os.path.join(HERE, "sources", name), "wb").write(b)
    man["files"][name] = {"url": url, "http": status, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
json.dump(man, open(os.path.join(HERE, "sources", "MANIFEST.json"), "w"), indent=1)
print(json.dumps(man, indent=1))
