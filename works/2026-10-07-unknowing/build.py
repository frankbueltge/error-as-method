"""build.py -> data.js for the face (daily values, events, every reading's items and scores, forecast)."""
import json, glob
h = json.load(open('home.json')); r = json.load(open('results.json')); fc = json.load(open('forecast.json'))
reads = []
for f in sorted(glob.glob('readers/*.json')):
    x = json.load(open(f)); s = r['readers'][x['reader']]
    reads.append({'id': x['reader'], 'cond': x['condition'], 't': x['translation'], 'items': x['answer']['singular'],
                  'found': s['found'], 'quarter': x['answer']['quarter'], 'rec': x['answer']['recurrence'],
                  'decided': x['answer']['decided']['singular'], 'guess': x['answer']['guess']})
order = {'fresh': 0, 'sequential': 1}
reads.sort(key=lambda d: (order[d['cond']], d['id'] if d['cond'] == 'sequential' else d['t'] + d['id']))
D = {'dmax': h['daily_max_kp'], 'dap': h['daily_ap'], 'events': h['events'], 'reads': reads, 'forecast': fc['events'],
     'P': {k: r[k]['holds'] for k in ['P1', 'P2', 'P3', 'P4', 'P5']}}
open('data.js', 'w').write('const DATA = ' + json.dumps(D, separators=(',', ':')) + ';\n')
print(len(reads), 'readings')
