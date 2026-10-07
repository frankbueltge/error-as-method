"""home.py -> home.json: the true answer to each of the eight questions, by the rules in
PREDICTIONS.md, written before the material was seen. Also the home events for S111.LINE."""
import json, math, statistics as st
from load import load
v, days = load()
missing = [i + 1 for i, x in enumerate(v) if x is None]
v = [x if x is not None else 0 for x in v]
N = len(v)
L = [math.log(max(x, 1)) for x in v]
def runmed(a, w):
    h = w // 2
    return [st.median(a[max(0, i - h):min(len(a), i + h + 1)]) for i in range(len(a))]
def acf(a, k):
    m = st.mean(a); d = sum((x - m) ** 2 for x in a)
    return sum((a[i] - m) * (a[i + k] - m) for i in range(len(a) - k)) / d
out = {'n_days': N, 'missing_days': missing}
# R1 cycle of 20-40 days, on log values with a 91-day running median removed
r = [a - b for a, b in zip(L, runmed(L, 91))]
ac = {k: acf(r, k) for k in range(20, 41)}
p = max(ac, key=ac.get)
out['R1'] = {'best_lag': p, 'acf': round(ac[p], 4), 'present': ac[p] >= 0.3 and 25 <= p <= 35,
             'acf_by_lag': {k: round(x, 4) for k, x in ac.items()}}
# R2 weekly rhythm: log minus centred 7-day mean, mean per weekday position (1 = weekday of day 1)
w = [L[i] - st.mean(L[i - 3:i + 4]) for i in range(3, N - 3)]
pos = [((i) % 7) + 1 for i in range(3, N - 3)]
wd = {k: st.mean(x for x, q in zip(w, pos) if q == k) for k in range(1, 8)}
eff = max(wd.values()) - min(wd.values())
out['R2'] = {'weekday_mean_log_residual': {k: round(x, 4) for k, x in wd.items()}, 'effect': round(eff, 4),
             'present': eff >= 0.05, 'lowest_position': min(wd, key=wd.get)}
# R3 level, year 2 against year 1, by median
m1, m2 = st.median(v[:366]), st.median(v[366:])
ratio = m2 / m1
out['R3'] = {'median_y1': m1, 'median_y2': m2, 'ratio': round(ratio, 4),
             'answer': 'higher' if ratio > 1.10 else 'lower' if ratio < 1 / 1.10 else 'about equal'}
# R4 annual pattern: Spearman between the twelve monthly medians of 2024 and of 2025
def mmed(y):
    return [st.median([x for x, d in zip(v, days) if d[:6] == f'{y}{m:02d}']) for m in range(1, 13)]
a, b = mmed(2024), mmed(2025)
def rank(z):
    s = sorted(range(12), key=lambda i: z[i]); rk = [0] * 12
    for j, i in enumerate(s): rk[i] = j
    return rk
ra, rb = rank(a), rank(b)
rho = 1 - 6 * sum((x - y) ** 2 for x, y in zip(ra, rb)) / (12 * (144 - 1))
out['R4'] = {'monthly_median_2024': a, 'monthly_median_2025': b, 'spearman': round(rho, 4), 'answer': 'yes' if rho >= 0.5 else 'no'}
# S1 highest day; S2 highest day more than 14 days from it; S3 single or run; S4 deep troughs
d1 = max(range(N), key=lambda i: v[i])
d2 = max((i for i in range(N) if abs(i - d1) > 14), key=lambda i: v[i])
run = sum(1 for i in range(max(0, d1 - 3), min(N, d1 + 4)) if v[i] >= 0.5 * v[d1])
med29 = runmed(v, 29)
trough = [i + 1 for i in range(N) if v[i] < med29[i] / 3]
out['S1'] = {'day': d1 + 1, 'date': days[d1], 'views': v[d1]}
out['S2'] = {'day': d2 + 1, 'date': days[d2], 'views': v[d2]}
out['S3'] = {'days_at_half_peak_within_3': run, 'answer': 'single' if run == 1 else 'run'}
out['S4'] = {'days': trough, 'answer': 'none' if not trough else 'some'}
# home events for S111.LINE: runs of days at or above 3x their centred 29-day median
hi = [v[i] >= 3 * med29[i] for i in range(N)]
ev, i = [], 0
while i < N:
    if hi[i]:
        j = i
        while j + 1 < N and hi[j + 1]: j += 1
        pk = max(range(i, j + 1), key=lambda k: v[k])
        ev.append({'id': f'E{len(ev)+1:02d}', 'start': i + 1, 'end': j + 1, 'peak_day': pk + 1, 'peak_date': days[pk], 'peak_views': v[pk],
                   'ratio': round(v[pk] / med29[pk], 2)})
        i = j + 1
    else: i += 1
out['events'] = ev; out['n_events'] = len(ev)
json.dump(out, open('home.json', 'w'), indent=1)
print(json.dumps({k: out[k] for k in ['R1', 'R2', 'R3', 'R4', 'S1', 'S2', 'S3', 'S4']}, default=str)[:1500]); print('events', len(ev))
