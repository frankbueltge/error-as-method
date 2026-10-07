"""score.py -> results.json: every cell-reading scored by the rules in PREDICTIONS.md, against
forecast.json; P1-P5. Nothing here is tuned after the readings: rules as pre-registered."""
import json, os, re
h = json.load(open('home.json')); fc = json.load(open('forecast.json'))['cells']
R = {f[2:-5]: json.load(open('readers/' + f))['answer'] for f in sorted(os.listdir('readers')) if f.startswith('F-')}
def day(x):
    try: return int(x)
    except (TypeError, ValueError): return None
def correct(q, a):
    if q == 'R1':
        if h['R1']['present']: return a['cycle'] == 'yes' and a['period_days'] is not None and abs(float(a['period_days']) - h['R1']['best_lag']) <= 2
        return a['cycle'] == 'no'
    if q == 'R2': return a['week'] == ('yes' if h['R2']['present'] else 'no')
    if q == 'R3': return a['level'] == h['R3']['answer']
    if q == 'R4': return a['year'] == h['R4']['answer']
    if q == 'S1': return day(a['highest_day']) is not None and abs(day(a['highest_day']) - h['S1']['day']) <= 1
    if q == 'S2': return day(a['second_day']) is not None and abs(day(a['second_day']) - h['S2']['day']) <= 1
    if q == 'S3': return a['peak_shape'] == h['S3']['answer']
    if q == 'S4':
        d = a['drops']
        if not h['S4']['days']: return d == 'none' or d == []
        return isinstance(d, list) and any(abs(int(x) - t) <= 1 for s in d for x in re.findall(r'\d+', s) for t in h['S4']['days'])
cells = {}; miss = {'regular': 0, 'singular': 0}; hits = 0
for q in fc:
    for t in fc[q]:
        for r in ('a', 'b'):
            ok = correct(q, R[t + r]); f = fc[q][t] == 'C'
            cells[f'{q}.{t}{r}'] = {'correct': ok, 'forecast': fc[q][t], 'match': ok == f}
            if ok != f: miss['regular' if q[0] == 'R' else 'singular'] += 1
            else: hits += 1
# S111.LINE on question 9
def rng(s):
    n = [int(x) for x in re.findall(r'\d+', s)]; return (n[0], n[-1])
E = h['events']
found, outside, marks = {}, 0, 0
for k, a in R.items():
    fs = set()
    for s in a['stands_out']:
        lo, hi = rng(s); marks += 1
        m = [e['id'] for e in E if lo - 1 <= e['end'] and hi + 1 >= e['start']]
        if m: fs |= set(m)
        else: outside += 1
    found[k] = sorted(fs)
def jac(x, y):
    x, y = set(x), set(y); return 1.0 if not (x | y) else len(x & y) / len(x | y)
pair = {t: jac(found[t + 'a'], found[t + 'b']) for t in ('T1', 'T2', 'T3', 'T4', 'T5')}
home = {k: len(v) / len(E) for k, v in found.items()}
mp, mh = sum(pair.values()) / 5, sum(home.values()) / 10
guess_moon = sum(1 for a in R.values() if re.search(r'moon|lunar', a['guess'], re.I))
t3drop = [k for k in ('T3a', 'T3b') if isinstance(R[k]['drops'], list) and any('729' in s or '105' in s for s in R[k]['drops'])]
res = {'cells': cells, 'misses': miss, 'matches': hits,
       'correct_by_q_t': {q: {t: sum(cells[f'{q}.{t}{r}']['correct'] for r in 'ab') for t in fc[q]} for q in fc},
       'P1': {'holds': miss['singular'] > miss['regular'], 'regular_misses': miss['regular'], 'singular_misses': miss['singular']},
       'P2': {'holds': hits >= 56, 'matches': hits},
       'S111': {'found': found, 'pairwise_jaccard': pair, 'mean_pairwise': round(mp, 4), 'home_jaccard': home, 'mean_home': round(mh, 4),
                'marks': marks, 'outside': outside},
       'P3': {'holds': mp > mh and outside * 5 < marks},
       'P4': {'holds': guess_moon >= 5, 'moon_guesses': guess_moon},
       'P5': {'holds': bool(t3drop), 't3_readers_naming_week_105': t3drop}}
json.dump(res, open('results.json', 'w'), indent=1)
for k in ('P1', 'P2', 'P3', 'P4', 'P5'): print(k, res[k])
print(json.dumps(res['correct_by_q_t'])); print(json.dumps(res['S111']['pairwise_jaccard']), res['S111']['mean_home'], marks, outside)
