"""build.py -> data.js for the face (hourly values, daily means, events, every reading, forecast cells)."""
import json, glob
from load import hourly
H = hourly(); h = json.load(open('home.json')); r = json.load(open('results.json')); p = json.load(open('posthoc.json')); fc = json.load(open('forecast.json'))
reads = []
for f in sorted(glob.glob('readers/*.json')):
    x = json.load(open(f)); s = r['readers'][x['reader']]; a = x['answer']
    reads.append({'id': x['reader'], 'k': x['kind'], 't': x['translation'], 'items': a['singular'], 'found': s['found'],
                  'hi': a['highest_quarter'], 'lo': a['lowest_quarter'], 'rec': a['recurrence'], 'guess': a['guess'],
                  'decided': a['decided']['singular'], 'right': s['right'], 'fc': fc['cells'][f"{x['kind']}-{x['translation']}"],
                  'form': x.get('form_kept', True)})
reads.sort(key=lambda d: (d['t'], d['k'], d['id']))
D = {'h': [None if v is None else round(v) for d in H for v in d], 'dm': h['daily_mean'], 'events': h['events'],
     'spikes': [s['day'] for s in p['spike_days']], 'reads': reads,
     'P': {k: r[k]['holds'] for k in ['P1', 'P2', 'P3', 'P4', 'P5']},
     'P1': {k: r['P1'][k] for k in ('regular_misses', 'singular_misses')}, 'outside': [r['P3']['outside'], r['P3']['items']]}
open('data.js', 'w').write('const DATA = ' + json.dumps(D, separators=(',', ':'), ensure_ascii=False) + ';\n')
print(len(reads), 'readings')
