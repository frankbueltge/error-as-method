"""prepare.py: NSIDC G02135 v4 daily NH extent CSV -> data/extent.js. Usage: python3 prepare.py <csv>"""
import sys, json, hashlib
raw = open(sys.argv[1], 'rb').read()
rows = []
for line in raw.decode().splitlines()[2:]:
    f = [x.strip() for x in line.split(',')[:4]]
    if len(f) == 4 and f[0].isdigit():
        rows.append([int(f[0]), int(f[1]), int(f[2]), float(f[3])])
open('data/extent.js', 'w').write('window.EXTENT=' + json.dumps(rows, separators=(',', ':')) + ';\n')
print(len(rows), rows[0], rows[-1], hashlib.sha256(raw).hexdigest())
