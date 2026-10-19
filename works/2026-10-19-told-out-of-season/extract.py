"""extract.py: fetches tonight's source from the USGS Water Services instantaneous-values service (US Geological
Survey, National Water Information System; US public domain, https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits).
Site 06221400, Dinwoody Creek above lakes near Burris, Wyoming (a proglacial stream fed by Dinwoody and Gannett
Glaciers, Wind River Range; Barkdull et al. 2021, doi:10.3389/feart.2021.727575), parameter 00060 (discharge, cubic
feet per second), every 15 minutes, 2025-08-01 07:00 UTC to 2025-10-01 07:00 UTC (1 August to 30 September 2025 in
local standard time, UTC-7). Writes the service's answer unchanged to sources/, and URL, byte count and SHA-256 to
sources/MANIFEST.json."""
import os, json, hashlib, urllib.request, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
URLS = {"usgs_06221400_00060_iv.json": "https://nwis.waterservices.usgs.gov/nwis/iv/?format=json&sites=06221400"
        "&parameterCd=00060&startDT=2025-08-01T07:00Z&endDT=2025-10-01T07:00Z"}
man = {"fetched_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
       "publisher": "US Geological Survey, National Water Information System",
       "licence": "US public domain (https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits)",
       "files": {}}
for name, url in URLS.items():
    with urllib.request.urlopen(url, timeout=120) as r:
        b = r.read(); status = r.status
    open(os.path.join(HERE, "sources", name), "wb").write(b)
    man["files"][name] = {"url": url, "http": status, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
json.dump(man, open(os.path.join(HERE, "sources", "MANIFEST.json"), "w"), indent=1)
print(json.dumps(man, indent=1))
