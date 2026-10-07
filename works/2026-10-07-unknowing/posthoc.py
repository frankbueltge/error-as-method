"""posthoc.py -> posthoc.json. Analyses not pre-registered, kept apart from results.json:
(1) find rate by peak Kp (the readers' shared threshold), (2) what the sequential readers found beyond
both fresh readers of the same translation, and how much of it they had named at an earlier step,
(3) precision (no item outside every event window)."""
import json
r = json.load(open('results.json')); h = json.load(open('home.json'))
pk = {e['id']: e['peak_kp'] for e in h['events']}; R = r['readers']
by_level = {}
for lv in sorted(set(pk.values())):
    ids = [e for e in pk if pk[e] == lv]
    by_level[f'{lv:.3f}'] = {'events': ids, 'readings': len(R),
        'find_rate': round(sum(e in x['found'] for e in ids for x in R.values())/(len(ids)*len(R)), 3)}
carry = {}
for s in ('S1', 'S2'):
    prev = set()
    for n in sorted(k for k in R if k.startswith(s)):
        x = R[n]
        fresh = set().union(*[set(y['found']) for y in R.values() if y['condition'] == 'fresh' and y['translation'] == x['translation']])
        extra = set(x['found']) - fresh
        carry[n] = {'beyond_both_fresh': sorted(extra, key=lambda e: int(e[1:])), 'named_at_earlier_step': sorted(extra & prev, key=lambda e: int(e[1:]))}
        prev |= set(x['found'])
tot = sum(len(v['beyond_both_fresh']) for v in carry.values()); car = sum(len(v['named_at_earlier_step']) for v in carry.values())
out = {'find_rate_by_peak_kp': by_level, 'carry': carry, 'carry_totals': {'beyond_both_fresh': tot, 'named_earlier': car},
       'items_outside_every_event_window': sum(len(x['false_alarms']) + len(x['near']) for x in R.values()),
       'items_total': sum(x['n_items'] for x in R.values()),
       'note': 'An item can overlap two adjacent event windows (e.g. 310-311 touches E17 and E18); wide T4 ranges (up to 11 days) find more than one event. Both are the pre-registered rule.'}
json.dump(out, open('posthoc.json', 'w'), indent=1)
print(json.dumps({k: v['find_rate'] for k, v in by_level.items()}), out['carry_totals'], out['items_outside_every_event_window'], out['items_total'])
