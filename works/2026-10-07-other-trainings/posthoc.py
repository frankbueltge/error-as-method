"""posthoc.py -> posthoc.json. Analyses not pre-registered, kept apart from results.json:
(1) the readers' own singular: days whose hourly maximum stands far above the day's mean (max >= 80
    and daily mean <= 40), and who named each, with the pre-registered tolerance (+-1 day) and a wide one (+-6);
(2) where the T1 items fall against the axis tick labels (1, 30, 60, ..., 360, 365), per kind;
(3) Jaccard over these spike-days per kind pair on each rendering, at both tolerances;
(4) the guesses, by kind."""
import json, itertools
from load import hourly
H = hourly(); h = json.load(open('home.json')); r = json.load(open('results.json')); R = r['readers']
dm = h['daily_mean']
dmax = [max(v for v in d if v is not None) for d in H]
spikes = [k+1 for k in range(365) if dmax[k] >= 80 and dm[k] is not None and dm[k] <= 40]
raw = {n: json.load(open(f'readers/{n}.json'))['answer']['singular'] for n in R}
def parse(s):
    a, _, b = str(s).partition('-'); a = int(a); b = int(b) if b else a; return min(a, b), max(a, b)
def named(n, d, tol): return any(a - tol <= d <= b + tol for a, b in map(parse, raw[n]))
found = {tol: {n: [d for d in spikes if named(n, d, tol)] for n in R} for tol in (1, 6)}
ticks = [1] + list(range(30, 361, 30)) + [365]
def near_tick(a, b): return any(abs((a + b)/2 - t) <= 1 for t in ticks)
tick_share = {}
for k in ('K0', 'K1', 'K2'):
    its = [parse(s) for n in R if R[n]['kind'] == k and R[n]['translation'] == 'T1' for s in raw[n]]
    tick_share[k] = {'items': len(its), 'within_1_day_of_a_tick_label': sum(near_tick(a, b) for a, b in its)}
J = lambda a, b: len(set(a) & set(b))/len(set(a) | set(b)) if set(a) | set(b) else 1.0
pairs = {}
for tol in (1, 6):
    for t in ('T1', 'T3'):
        for k1, k2 in [('K0', 'K0'), ('K1', 'K1'), ('K2', 'K2'), ('K0', 'K1'), ('K0', 'K2'), ('K1', 'K2')]:
            xs = [J(found[tol][a], found[tol][b]) for a, b in itertools.combinations(sorted(R), 2)
                  if R[a]['translation'] == R[b]['translation'] == t and {R[a]['kind'], R[b]['kind']} == {k1, k2} and (k1 != k2 or R[a]['kind'] == k1)]
            pairs[f'tol{tol}:{t}:{k1}-{k2}'] = round(sum(xs)/len(xs), 3)
out = {'spike_days': [{'day': d, 'hour_max': dmax[d-1], 'daily_mean': dm[d-1]} for d in spikes],
       'named_by_reader_tol1': found[1], 'named_by_reader_tol6': found[6],
       'share_naming_each_spike_tol1': {d: sum(d in v for v in found[1].values()) for d in spikes},
       'T1_items_at_tick_labels': tick_share, 'spike_jaccard_by_kind_pair': pairs,
       'guesses': {n: R[n]['guess'] for n in sorted(R)},
       'items_outside_every_event': r['P3']['outside'], 'items': r['P3']['items']}
json.dump(out, open('posthoc.json', 'w'), indent=1, ensure_ascii=False)
print(out['spike_days']); print(out['share_naming_each_spike_tol1']); print(tick_share); print(json.dumps(pairs, indent=0))
for n in sorted(R): print(n, found[1][n], found[6][n])
