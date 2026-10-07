"""cut.py <full Kp_ap_since_1932.txt> -> sources/kp-2025.txt (the window, lines verbatim) + MANIFEST.json"""
import sys, json, hashlib, datetime
src = sys.argv[1]
raw = open(src, 'rb').read()
lines = raw.decode('ascii').splitlines()
win = [l for l in lines if l.startswith('2025 ')]
assert len(win) == 2920, len(win)
out = '\n'.join(win) + '\n'
open('sources/kp-2025.txt', 'w').write(out)
m = {
 'source': 'https://kp.gfz.de/app/files/Kp_ap_since_1932.txt',
 'what': 'GFZ Potsdam, geomagnetic Kp and ap, three-hourly, 1932 to present (hybrid definitive/nowcast)',
 'licence': 'CC BY 4.0 (https://kp.gfz.de/app/format/Kp_ap.txt; DataCite record of doi:10.5880/Kp.0001)',
 'cite': ['Matzka, Stolle, Yamazaki, Bronkalla, Morschhauser 2021, Space Weather, doi:10.1029/2020SW002641',
          'Matzka, Bronkalla, Tornow, Elger, Stolle 2021, GFZ Data Services, doi:10.5880/Kp.0001'],
 'retrieved_utc': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
 'full_file_bytes': len(raw), 'full_file_sha256': hashlib.sha256(raw).hexdigest(),
 'window': '2025-01-01 00 UT .. 2025-12-31 21 UT, lines starting "2025 ", verbatim',
 'window_lines': len(win), 'window_sha256': hashlib.sha256(out.encode()).hexdigest(),
 'why': 'Session 111 material; the full file is not committed (16 MB), the window is.'}
json.dump(m, open('sources/MANIFEST.json', 'w'), indent=1)
print(m['window_sha256'])
