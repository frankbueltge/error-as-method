"""score.py -> results.json. Scores every reader against home.json by the rules in PREDICTIONS.md,
and the forecast (forecast.json) against the fresh readers."""
import json, glob, itertools
h = json.load(open('home.json')); fc = json.load(open('forecast.json'))
E = h['events']; dmax = h['daily_max_kp']
def parse(s):
    s = str(s).replace('–', '-').strip()
    a, _, b = s.partition('-')
    a = int(a); b = int(b) if b else a
    return a, b
def score(ans):
    items = [parse(s) for s in ans['singular']]
    found = {e['id'] for e in E for a, b in items if a <= e['last'] + 1 and b >= e['first'] - 1}
    fa, near = [], []
    for a, b in items:
        if any(a <= e['last'] + 1 and b >= e['first'] - 1 for e in E): continue
        (near if any(dmax[d-1] >= 5.0 - 1e-9 for d in range(max(1, a), min(365, b)+1)) else fa).append(f'{a}-{b}' if a != b else str(a))
    widths = [b - a + 1 for a, b in items]
    q = ans.get('quarter', ''); q = int(q[1]) if q.startswith('Q') else None
    rec = ans.get('recurrence'); per = ans.get('period_days')
    return {'found': sorted(found, key=lambda x: int(x[1:])), 'n_found': len(found), 'n_items': len(items),
            'max_item_width': max(widths) if widths else 0, 'false_alarms': fa, 'near': near,
            'R3': q, 'R3_right': (q == h['R3']) if q else None, 'R2': rec, 'R2_period': per,
            'guess': ans.get('guess', ''), 'files_opened': ans.get('files_opened', [])}
R = {}
for f in sorted(glob.glob('readers/*.json')):
    r = json.load(open(f)); R[r['reader']] = {'condition': r['condition'], 'translation': r['translation'], **score(r['answer'])}
ids = [e['id'] for e in E]; one = {e['id'] for e in E if e['days'] == 1}
out = {'readers': R, 'n_events': len(E)}
# P1: forecast accuracy, event cells vs regular (R3) cells, over the fresh readers
ev_cells = reg_cells = ev_ok = reg_ok = 0; misses = []
for name, r in R.items():
    if r['condition'] != 'fresh': continue
    t = r['translation']
    for e in ids:
        ok = fc['events'][t][e] == (e in r['found']); ev_cells += 1; ev_ok += ok
        if not ok: misses.append(f'{name}:{e}:{"forecast yes" if fc["events"][t][e] else "forecast no"}')
    if r['R3'] is not None:
        reg_cells += 1; reg_ok += (r['R3'] == fc['R3'][t])
    else:
        reg_cells += 1  # "cannot tell" is a miss of a forecast that named a quarter
out['P1'] = {'event_acc': round(ev_ok/ev_cells, 3), 'event_cells': ev_cells, 'regular_acc': round(reg_ok/reg_cells, 3),
             'regular_cells': reg_cells, 'holds': reg_ok/reg_cells - ev_ok/ev_cells >= 0.10, 'event_misses': misses}
# P2: Jaccard of found sets between the two fresh readers per translation
jac = {}
for t in ['T1', 'T2', 'T3', 'T4']:
    a, b = [set(r['found']) for r in R.values() if r['condition'] == 'fresh' and r['translation'] == t]
    jac[t] = round(len(a & b)/len(a | b), 3) if a | b else 1.0
out['P2'] = {'jaccard': jac, 'holds': sum(v >= 0.8 for v in jac.values()) >= 3}
# P3: sequential last translation (T2) vs fresh mean on T2; and every step for the record
fresh_rate = {t: sum(r['n_found'] for r in R.values() if r['condition'] == 'fresh' and r['translation'] == t)/2/len(E) for t in ['T1','T2','T3','T4']}
seq = {n: {'translation': r['translation'], 'rate': round(r['n_found']/len(E), 3), 'fresh_mean': round(fresh_rate[r['translation']], 3)} for n, r in R.items() if r['condition'] == 'sequential'}
out['P3'] = {'sequential': seq, 'holds': any(v['translation'] == 'T2' and v['rate'] - v['fresh_mean'] >= 0.2 for v in seq.values())}
# P4
t4_one = [len(one & set(r['found']))/len(one) for r in R.values() if r['condition'] == 'fresh' and r['translation'] == 'T4']
t3_all = [r['n_found']/len(E) for r in R.values() if r['condition'] == 'fresh' and r['translation'] == 'T3']
out['P4'] = {'T4_one_day_rates': [round(x, 3) for x in t4_one], 'T3_rates': [round(x, 3) for x in t3_all],
             'holds': all(x < 0.5 for x in t4_one) and all(x >= 0.9 for x in t3_all)}
# P5
kw = ('kp', 'geomagnetic')
named = [n for n, r in R.items() if any(k in r['guess'].lower() for k in kw)]
out['P5'] = {'named': named, 'of': len(R), 'holds': len(named) >= 1}
# which events did nobody (fresh) find, which did every fresh reader find
fr = [set(r['found']) for r in R.values() if r['condition'] == 'fresh']
out['events_found_by_n_fresh'] = {e: sum(e in s for s in fr) for e in ids}
json.dump(out, open('results.json', 'w'), indent=1)
for k in ['P1', 'P2', 'P3', 'P4', 'P5']: print(k, {x: y for x, y in out[k].items() if x != 'event_misses'})
print(out['events_found_by_n_fresh'])
