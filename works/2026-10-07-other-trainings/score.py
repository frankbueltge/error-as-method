"""score.py -> results.json. Scores every reader against home.json and the forecast by the rules in PREDICTIONS.md."""
import json, glob, itertools, math
h = json.load(open('home.json')); fc = json.load(open('forecast.json'))
E = h['events']; dm = h['daily_mean']; N = len(E)
def parse(s):
    s = str(s).replace('–', '-').strip(); a, _, b = s.partition('-'); a = int(a); b = int(b) if b else a
    return min(a, b), max(a, b)
def inwin(a, b, e): return a <= e['last'] + 1 and b >= e['first'] - 1
def score(ans):
    items = [parse(s) for s in ans['singular']]
    found = sorted({e['id'] for e in E for a, b in items if inwin(a, b, e)}, key=lambda x: int(x[1:]))
    outside = [(a, b) for a, b in items if not any(inwin(a, b, e) for e in E)]
    near = [f'{a}-{b}' if a != b else str(a) for a, b in outside if any(dm[d-1] is not None and dm[d-1] > 40 for d in range(max(1, a), min(365, b)+1))]
    fa = [f'{a}-{b}' if a != b else str(a) for a, b in outside if (f'{a}-{b}' if a != b else str(a)) not in near]
    q = lambda s: int(s[1]) if str(s).startswith('Q') else None
    rec, per = ans.get('recurrence'), ans.get('period_days')
    r4 = (rec == 'yes' and per is not None and 6 <= float(per) <= 8) if h['R4_weekly'] == 'yes' else (rec == 'no')
    right = {'R2': q(ans['highest_quarter']) == h['R2_highest_quarter'], 'R3': q(ans['lowest_quarter']) == h['R3_lowest_quarter'],
             'R4': r4, 'S1': h['largest'] in found, 'S2': len(found) >= math.ceil(N/2), 'S3': len(fa) == 0}
    return {'found': found, 'n_items': len(items), 'n_outside': len(outside), 'near': near, 'false_alarms': fa, 'right': right,
            'guess': ans.get('guess', '')}
R = {}
for f in sorted(glob.glob('readers/*.json')):
    r = json.load(open(f)); R[r['reader']] = {'kind': r['kind'], 'translation': r['translation'], 'form_kept': r.get('form_kept', True), **score(r['answer'])}
out = {'readers': R, 'n_events': N}
# P1 forecast misses, regular vs singular
miss = {'regular': [], 'singular': []}
for n, r in R.items():
    cell = fc['cells'][f"{r['kind']}-{r['translation']}"]
    for qk, ok in r['right'].items():
        if cell[qk] != ok: miss['regular' if qk[0] == 'R' else 'singular'].append(f'{n}:{qk}:forecast {"right" if cell[qk] else "wrong"}')
out['P1'] = {'regular_misses': len(miss['regular']), 'singular_misses': len(miss['singular']), 'cells_each': 6*6,
             'misses': miss, 'holds': len(miss['singular']) > len(miss['regular'])}
J = lambda a, b: len(set(a) & set(b))/len(set(a) | set(b)) if set(a) | set(b) else 1.0
names = sorted(R)
within = [J(R[a]['found'], R[b]['found']) for a, b in itertools.combinations(names, 2) if R[a]['kind'] == R[b]['kind'] and R[a]['translation'] == R[b]['translation']]
between = [J(R[a]['found'], R[b]['found']) for a, b in itertools.combinations(names, 2) if R[a]['kind'] != R[b]['kind'] and R[a]['translation'] == R[b]['translation']]
mw, mb = sum(within)/len(within), sum(between)/len(between)
out['P2'] = {'within_pairs': len(within), 'within_mean': round(mw, 3), 'between_pairs': len(between), 'between_mean': round(mb, 3), 'holds': mb >= 0.8*mw}
home_ids = [e['id'] for e in E]
jh = sum(J(r['found'], home_ids) for r in R.values())/len(R)
items = sum(r['n_items'] for r in R.values()); outs = sum(r['n_outside'] for r in R.values())
out['P3'] = {'within_mean': round(mw, 3), 'mean_jaccard_with_home': round(jh, 3), 'a_holds': mw >= jh,
             'items': items, 'outside': outs, 'outside_share': round(outs/items, 3), 'b_holds': outs/items < 0.2,
             'holds': mw >= jh and outs/items < 0.2}
kw = ('particulate', 'pm10', 'pm2', 'pm ', 'dust', 'air pollut', 'pollutant')
named = {k: [n for n, r in R.items() if r['kind'] == k and any(w in r['guess'].lower() for w in kw)] for k in ('K0', 'K1', 'K2')}
out['P4'] = {'named_by_kind': named, 'keywords': kw, 'holds': all(len(v) >= 2 for v in named.values())}
fa = {t: sum(len(r['false_alarms']) for r in R.values() if r['translation'] == t) for t in ('T1', 'T3')}
out['P5'] = {'false_alarms': fa, 'holds': fa['T1'] > fa['T3']}
json.dump(out, open('results.json', 'w'), indent=1)
for k in ['P1', 'P2', 'P3', 'P4', 'P5']: print(k, {x: y for x, y in out[k].items() if x != 'misses'})
for n, r in R.items(): print(n, r['found'], 'out', r['n_outside'], '/', r['n_items'], 'FA', r['false_alarms'], {k: int(v) for k, v in r['right'].items()})
print(miss)
