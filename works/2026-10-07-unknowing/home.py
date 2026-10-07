"""home.py -> home.json: the events (singular) and R2/R3 (regular), by the norms in PREDICTIONS.md."""
import json
from load import load
kp, ap, d = load()
dmax = [max(x) for x in kp]
dap = [sum(x)/8 for x in ap]
storm = [m >= 5.667 - 1e-9 for m in dmax]
events, i = [], 0
while i < 365:
    if storm[i]:
        j = i
        while j + 1 < 365 and storm[j+1]: j += 1
        events.append({'id': 'E%d' % (len(events)+1), 'first': i+1, 'last': j+1, 'days': j-i+1,
                       'peak_kp': max(dmax[i:j+1]), 'peak_day_ap': round(max(dap[i:j+1]), 1)})
        i = j + 1
    else: i += 1
n = 365; mu = sum(dap)/n; var = sum((x-mu)**2 for x in dap)
acf = {L: sum((dap[t]-mu)*(dap[t+L]-mu) for t in range(n-L))/var for L in range(1, 61)}
best = max(range(24, 31), key=lambda L: acf[L]); a_rec = acf[best]; a_mid = max(acf[L] for L in range(8, 19))
r2 = 'yes' if (a_rec >= 0.15 and a_rec > a_mid) else ('no' if a_rec < 0.05 else 'undecided')
q = [(1, 91), (92, 182), (183, 273), (274, 365)]
qm = [sum(dap[a-1:b])/(b-a+1) for a, b in q]
r3 = qm.index(max(qm)) + 1
g1 = [k+1 for k in range(365) if dmax[k] >= 5.0 - 1e-9]
out = {'events': events, 'n_events': len(events), 'one_day_events': sum(e['days'] == 1 for e in events),
       'g1_days': g1, 'R2': r2, 'R2_acf_best_lag': best, 'R2_acf_best': round(a_rec, 3), 'R2_acf_8_18_max': round(a_mid, 3),
       'R3': r3, 'R3_quarter_means': [round(x, 2) for x in qm],
       'definitive_flags': {str(v): d.count(v) for v in sorted(set(d))},
       'daily_max_kp': dmax, 'daily_ap': [round(x, 2) for x in dap]}
json.dump(out, open('home.json', 'w'), indent=1)
print(len(events), 'events;', out['one_day_events'], 'one-day; R2', r2, best, round(a_rec, 3), '; R3', r3)
