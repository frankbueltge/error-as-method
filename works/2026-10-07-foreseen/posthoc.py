"""posthoc.py -> posthoc.json. Written after score.py had run; nothing here changes a score.
(1) Each home event and each reader mark against the Moon's phases (NASA/Espenak table).
(2) Each forecast miss sorted by direction (forecast blind and the readers saw / forecast sight and they did not)
(A split by kind, world against translation, was drafted and dropped: a cell's forecast mixes both and the split was mine to draw.)"""
import json, re, datetime
h = json.load(open('home.json')); r = json.load(open('results.json')); fc = json.load(open('forecast.json'))
mon = {m: i for i, m in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(), 1)}
phase = []  # (day number, kind, flag)
kinds = ['new', 'first quarter', 'full', 'last quarter']
for line in open('sources/moon-phases-2024-2025.txt'):
    m = re.match(r'\s*(\d{4})?\s', line); 
    y = re.match(r'\s*(2024|2025)\s', line)
    if y: year = int(y.group(1)); body = line[:].split(y.group(1), 1)[1]; col0 = len(line) - len(line.lstrip()) + 4
    else: body = line
    # columns are fixed-width, 18 chars from the first column start; parse by position in the raw line
    for mm in re.finditer(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d+)\s+(\d\d):(\d\d)\s?([TAPtpn]?)', line):
        col = (mm.start() - 8) // 18
        d = datetime.datetime(year, mon[mm.group(1)], int(mm.group(2)), int(mm.group(3)), int(mm.group(4)))
        dn = (d - datetime.datetime(2024, 1, 1)).total_seconds() / 86400 + 1
        phase.append((dn, kinds[col], mm.group(5)))
full = [p for p in phase if p[1] == 'full']
def nearest(day):
    p = min(phase, key=lambda p: abs(p[0] - (day + 0.5)))
    return {'phase': p[1], 'eclipse': p[2], 'offset_days': round(day + 0.5 - p[0], 1)}
ev = [{'id': e['id'], 'peak_day': e['peak_day'], 'date': e['peak_date'], **nearest(e['peak_day']),
       'to_full': round(min((e['peak_day'] + 0.5 - f[0] for f in full), key=abs), 1)} for e in h['events']]
outside = []
R = r['S111']['found']
import os
for f in sorted(os.listdir('readers')):
    if not f.startswith('F-'): continue
    a = json.load(open('readers/' + f))['answer']
    for s in a['stands_out']:
        n = [int(x) for x in re.findall(r'\d+', s)]; lo, hi = n[0], n[-1]
        if not any(lo - 1 <= e['end'] and hi + 1 >= e['start'] for e in h['events']):
            outside.append({'reader': f[2:-5], 'mark': s, **nearest(lo)})
# misses
miss = []
for k, c in r['cells'].items():
    if not c['match']:
        q = k.split('.')[0]
        miss.append({'cell': k, 'direction': 'forecast blind, reader saw' if c['correct'] else 'forecast sight, reader did not'})
from collections import Counter
out = {'phases_parsed': len(phase), 'full_moons': len(full), 'events': ev,
       'events_within_1_day_of_full': sum(abs(e['to_full']) <= 1.5 for e in ev),
       'marks_outside': outside, 'misses': miss,
       'miss_counts': {f'{q} {d}': n for (q, d), n in Counter((m['cell'][0], m['direction']) for m in miss).items()},
       'prior_truth_vs_home': {'R1': 'right', 'R2': 'right', 'R3': 'wrong (about equal; home lower, 0.80)', 'R4': 'wrong (no; home yes, rho 0.74)',
                               'S3': 'wrong (single; home run)', 'S4': 'right'}}
json.dump(out, open('posthoc.json', 'w'), indent=1)
print(len(phase), len(full), out['events_within_1_day_of_full']); print(out['miss_counts'])
for o in outside: print(o)
