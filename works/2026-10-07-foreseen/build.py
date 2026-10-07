"""build.py -> data.js for the face: the series, home events, readers, forecast and scores, phases."""
import json, os
from load import load
v, days = load()
h = json.load(open('home.json')); r = json.load(open('results.json')); p = json.load(open('posthoc.json'))
fc = json.load(open('forecast.json'))
R = {f[2:-5]: json.load(open('readers/' + f))['answer'] for f in sorted(os.listdir('readers')) if f.startswith('F-')}
Q = {'R1': 'a cycle of 20–40 days', 'R2': 'a weekly rhythm', 'R3': 'year 2 against year 1', 'R4': 'the same months high',
     'S1': 'the highest day', 'S2': 'the second event', 'S3': 'peak: one day or a run', 'S4': 'deep drops'}
KEY = {'R1': 'cycle', 'R2': 'week', 'R3': 'level', 'R4': 'year', 'S1': 'highest_day', 'S2': 'second_day', 'S3': 'peak_shape', 'S4': 'drops'}
home_ans = {'R1': f"yes, {h['R1']['best_lag']} days", 'R2': f"yes (weekday spread {h['R2']['effect']})", 'R3': f"{h['R3']['answer']} ({h['R3']['ratio']})",
            'R4': f"{h['R4']['answer']} (rho {h['R4']['spearman']})", 'S1': f"day {h['S1']['day']}", 'S2': f"day {h['S2']['day']}",
            'S3': h['S3']['answer'], 'S4': h['S4']['answer']}
def ans(a, q):
    x = a[KEY[q]]
    if q == 'R1' and x == 'yes': x = f"yes, {a['period_days']} days"
    return x if isinstance(x, str) or x is None else (', '.join(x) if isinstance(x, list) else str(x))
D = {'v': v, 'dates': days, 'events': [[e['start'], e['end'], e['peak_day']] for e in h['events']],
     'phases': [[round(x['offset_days'], 1)] for x in []],
     'full': [], 'q': Q, 'home': home_ans, 'forecast': fc['cells'],
     'cells': {k: c['correct'] for k, c in r['cells'].items()},
     'readers': {k: {'stands_out': a['stands_out'], 'guess': a['guess'], 'decided': a['decided'],
                     'ans': {q: ans(a, q) for q in Q}} for k, a in R.items()},
     'misses': r['misses'], 'matches': r['matches'], 'pair': r['S111']['pairwise_jaccard'],
     'marks': r['S111']['marks'], 'outside': r['S111']['outside'],
     'outside_marks': p['marks_outside']}
# the Moon's phases as day numbers, for the overlay
import re, datetime
mon = {m: i for i, m in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(), 1)}
ph = []
for line in open('sources/moon-phases-2024-2025.txt'):
    y = re.match(r'\s*(2024|2025)\s', line)
    if y: year = int(y.group(1))
    for mm in re.finditer(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d+)\s+(\d\d):(\d\d)\s?([TAPtpn]?)', line):
        col = (mm.start() - 8) // 18
        d = datetime.datetime(year, mon[mm.group(1)], int(mm.group(2)), int(mm.group(3)), int(mm.group(4)))
        ph.append([round((d - datetime.datetime(2024, 1, 1)).total_seconds() / 86400 + 1, 2), col, mm.group(5)])
D['phases'] = ph
del D['full']
D['t5'] = open('renders/T5.txt').read()
open('data.js', 'w').write('window.D=' + json.dumps(D, separators=(',', ':'), ensure_ascii=False) + ';\n')
print(len(open('data.js').read()))
