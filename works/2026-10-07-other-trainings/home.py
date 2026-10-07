"""home.py -> home.json: the events (singular) and R2/R3/R4 (regular), by the norms in PREDICTIONS.md."""
import json
from load import daily, hourly
dm = daily(); H = hourly()
n_missing_days = sum(x is None for x in dm)
ex = [x is not None and x > 50 for x in dm]
events, i = [], 0
while i < 365:
    if ex[i]:
        j = i
        while j + 1 < 365 and ex[j+1]: j += 1
        events.append({'id': 'E%d' % (len(events)+1), 'first': i+1, 'last': j+1, 'days': j-i+1,
                       'peak_daily': max(dm[i:j+1])})
        i = j + 1
    else: i += 1
largest = max(events, key=lambda e: e['peak_daily'])['id'] if events else None
q = [(1, 90), (91, 181), (182, 273), (274, 365)]
def qmean(a, b):
    v = [x for x in dm[a-1:b] if x is not None]; return sum(v)/len(v)
qm = [qmean(a, b) for a, b in q]
# R4 weekly recurrence: ACF of the daily means (missing days filled by the year mean)
mu = sum(x for x in dm if x is not None)/(365 - n_missing_days)
z = [(x if x is not None else mu) - mu for x in dm]
var = sum(v*v for v in z)
acf = {L: sum(z[t]*z[t+L] for t in range(365-L))/var for L in range(1, 15)}
r4 = 'yes' if acf[7] > max(acf[6], acf[8]) else 'no'
out = {'events': events, 'n_events': len(events), 'largest': largest, 'n_exceedance_days': sum(ex),
       'R2_highest_quarter': qm.index(max(qm)) + 1, 'R3_lowest_quarter': qm.index(min(qm)) + 1,
       'quarter_means': [round(x, 2) for x in qm], 'R4_weekly': r4, 'acf': {L: round(a, 3) for L, a in acf.items()},
       'missing_days': n_missing_days, 'missing_hours': sum(v is None for d in H for v in d),
       'daily_mean': [None if x is None else round(x, 1) for x in dm]}
json.dump(out, open('home.json', 'w'), indent=1)
print(len(events), 'events,', sum(ex), 'days >50; largest', largest, '; R2', out['R2_highest_quarter'], 'R3', out['R3_lowest_quarter'], 'R4', r4, '; missing days', n_missing_days, 'hours', out['missing_hours'])
