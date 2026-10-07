"""build.py: results.json + NOTE.md files + control notes -> data.js for the face."""
import json, re
r = json.load(open('results.json'))
def split(note):
    parts = re.split(r'^## (v\d)\s*$', note, flags=re.M)
    return {parts[i]: parts[i + 1].strip() for i in range(1, len(parts), 2)}
D = {'lineages': {}, 'control': {}}
for L in ('P1', 'P2', 'B1', 'B2'):
    notes = split(open(f'lineages/{L}/v4/NOTE.md').read())
    D['lineages'][L] = [{'v': k, 'note': notes.get(f'v{k}', ''), 'bytes': r['bytes'][f'{L}-v{k}'],
                         'folded': r['folded'][f'{L}-v{k}'],
                         'blind': r['blind'].get(f'{L}-{k}'), 'open': r['open'].get(f'{L}-{k}')} for k in range(5)]
for C in ('C1', 'C2'):
    D['control'][C] = split(open(f'control/{C}/NOTE.md').read())['v0']
D['scores'] = {p: r[p]['held'] for p in ('P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7')}
open('data.js', 'w').write('window.BAL=' + json.dumps(D, ensure_ascii=False) + ';\n')
print('ok', len(open('data.js').read()))
