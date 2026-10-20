"""shelf.py: groups the four shelf lists by publisher+dataset key (hand-written alias table, fixed before any
maker ran) and counts how many of the four agents name each. Writes shelf/groups.json."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
KEYS = [("ghcn", "Global Historical Climatology"), ("usgs-eq", "Earthquake"), ("exoplanet", "Exoplanet"),
 ("gaia", "Gaia"), ("maunaloa", "Mauna Loa"), ("ebird", "eBird"), ("gbif", "GBIF"), ("met", "Metropolitan Museum"),
 ("moma", "Museum of Modern Art"), ("wayback", "Wayback"), ("pageviews", "ageview"), ("gutenberg", "Gutenberg"),
 ("nyctaxi", "Taxi"), ("osm", "OpenStreetMap"), ("gfw", "Global Fishing Watch"), ("migrants", "Missing Migrants"),
 ("ucdp", "UCDP"), ("volcano", "Volcanism"), ("seaice", "Sea Ice Index"), ("berkeley", "Berkeley Earth"),
 ("owid", "Our World in Data"), ("chronam", "Chronicling America"), ("freesound", "Freesound"), ("cern", "CERN"),
 ("fedreg", "Federal Register"), ("gistemp", "GISTEMP"), ("era5", "ERA5"), ("firms", "FIRMS"),
 ("xenocanto", "Xeno-canto"), ("rijks", "Rijksmuseum"), ("wpp", "World Population Prospects"), ("wdi", "World Development"),
 ("hmd", "Human Mortality"), ("silso", "SILSO"), ("blackmarble", "Black Marble"), ("sentinel2", "Sentinel-2"),
 ("mpc", "Minor Planet"), ("nyc311", "311"), ("slavevoyages", "Slave"), ("unhcr", "UNHCR"), ("musicbrainz", "MusicBrainz"),
 ("forest", "Global Forest"), ("cooperhewitt", "Cooper Hewitt"), ("babynames", "Baby Names"), ("commoncrawl", "Common Crawl")]
groups = {}
for i in range(1, 5):
    for line in open(os.path.join(H, "shelf", "S%d.txt" % i)):
        t = re.sub(r"^\d+\.\s*", "", line.strip())
        if not t: continue
        k = next((k for k, s in KEYS if s in t), None)
        assert k, t
        g = groups.setdefault(k, {"key": k, "agents": [], "lines": []}); g["agents"].append(i); g["lines"].append(t)
out = sorted(groups.values(), key=lambda g: (-len(set(g["agents"])), g["key"]))
for g in out: g["n"] = len(set(g["agents"]))
json.dump(out, open(os.path.join(H, "shelf", "groups.json"), "w"), indent=1, ensure_ascii=False)
from collections import Counter
print(len(out), "distinct;", Counter(g["n"] for g in out))
print([g["key"] for g in out if g["n"] == 4])
