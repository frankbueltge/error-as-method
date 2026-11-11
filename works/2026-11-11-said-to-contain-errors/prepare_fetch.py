"""Fetch October 2026 daily mean discharge (USGS 00060, statistic 00003) for a fixed candidate list of gauges.
The candidate list was written from memory before any value was seen; USGS returns each site's own name, which is
what the briefs use. Raw response kept in sources/usgs-dv-2026-10.json."""
import json, urllib.request, sys
SITES = """07289000 07374000 05587450 05331000 03611500 03294500 06934500 06610000 14105700 14246900 04264331 07381490
07263450 03593500 13269000 13334300 01578310 01646500 01463500 01358000 01184000 09380000 09421500 08364000 08313000
11447650 11303500 14211720 12340500 06191500 06214500 02489500 02467000 02358000 02226000 02198500 02131000 02037500
01570500 03049500 03085000 04193500 05082500 07355500 08116650 08158000 08167500 15565447 15515500 12113000 12200500
09315000 09163500 11264500 01104500 11103000 02336000 01481000 06730500 09402500 05420500 05344500 04087000 01638500
13317000 12422500 10350000 11477000 14321000 06090800 06054500 07069000 07010000 01100000 01034500 01010500 02087500
04119000 04208000 03234500 03377500 06892350 06486000 06805500 08057000 08074000 11152500 11169000 09506000 09498500
13013650 06043500 12301933""".split()
url = ("https://waterservices.usgs.gov/nwis/dv/?format=json&parameterCd=00060&statCd=00003"
       "&startDT=2026-10-01&endDT=2026-10-31&sites=" + ",".join(SITES))
raw = urllib.request.urlopen(url, timeout=120).read()
open("sources/usgs-dv-2026-10.json", "wb").write(raw)
d = json.loads(raw)
out = {}
for ts in d["value"]["timeSeries"]:
    site = ts["sourceInfo"]["siteCode"][0]["value"]
    name = ts["sourceInfo"]["siteName"]
    vals = [v for v in ts["values"][0]["value"]]
    nums = [float(v["value"]) for v in vals if float(v["value"]) >= 0]
    quals = sorted({q for v in vals for q in v.get("qualifiers", [])})
    out[site] = {"name": name, "n": len(nums), "mean_cfs": (sum(nums) / len(nums)) if nums else None, "qualifiers": quals}
json.dump({"url": url, "candidates": SITES, "sites": out}, open("sources/october-2026.json", "w"), indent=1)
print(len(SITES), "candidates,", len(out), "returned,", sum(1 for s in out.values() if s["n"] == 31), "with 31 days")
missing = [s for s in SITES if s not in out]
print("not returned:", missing)
