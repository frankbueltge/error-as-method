"""fetch.py -> sources/hourly-2025.json, sources/daily-2025.json (API responses verbatim) + MANIFEST.json.
UBA Air Data API v3, station DEBE034 (Berlin Neukoelln, id 145), component 1 (PM10),
scope 2 (one-hour average, 1SMW) and scope 1 (daily average, 1TMW), 2025-01-01 .. 2025-12-31."""
import urllib.request, json, hashlib, datetime
B = 'https://luftdaten.umweltbundesamt.de/api/air-data/v3/measures/json'
Q = 'date_from=2025-01-01&date_to=2025-12-31&time_from=1&time_to=24&station=145&component=1&lang=en'
out = {}
for name, scope in (('hourly', 2), ('daily', 1)):
    url = f'{B}?{Q}&scope={scope}'
    raw = urllib.request.urlopen(url, timeout=120).read()
    open(f'sources/{name}-2025.json', 'wb').write(raw)
    out[name] = {'url': url, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
out.update({'what': 'Umweltbundesamt (German Environment Agency), Air Data API v3: PM10 at Berlin Neukoelln (DEBE034), 2025',
            'licence': 'Datenlizenz Deutschland (Data licence Germany), as stated on https://luftdaten.umweltbundesamt.de/api/air-data/v4/doc; source: Umweltbundesamt with data of the Berlin air quality network',
            'retrieved_utc': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'note': 'Times are CET (MEZ) per the API description; hours 1..24, value is for the hour ending at date_end.'})
json.dump(out, open('sources/MANIFEST.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
