"""fetch.py -> sources/full-moon-2024-2025.json and sources/MANIFEST.json.
Wikimedia REST API, per-article daily pageviews, en.wikipedia, all-access, agent=user,
article "Full_moon", 2024-01-01 .. 2025-12-31. The response is saved verbatim."""
import subprocess, hashlib, json, datetime
URL = ('https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/'
       'all-access/user/Full_moon/daily/20240101/20251231')
# urllib was answered 429 five times running on the night; curl with the same User-Agent got 200.
UA = 'error-as-method nightly research (https://github.com/frankbueltge/error-as-method)'
raw = subprocess.run(['curl', '-sS', '--fail', '-A', UA, URL], capture_output=True, check=True).stdout
open('sources/full-moon-2024-2025.json', 'wb').write(raw)
json.dump({'source': URL,
           'what': 'Wikimedia Analytics, pageviews per article, daily, en.wikipedia, all-access, agent=user, article Full_moon',
           'licence': 'CC0 (https://dumps.wikimedia.org/legal.html: "All Analytics datasets are available under the Creative Commons Zero (CC0) public domain dedication")',
           'docs': 'https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/page-views.html',
           'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
           'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
           'why': 'Session 112 material, committed whole (CC0).'},
          open('sources/MANIFEST.json', 'w'), indent=1)
print(len(raw), hashlib.sha256(raw).hexdigest())
