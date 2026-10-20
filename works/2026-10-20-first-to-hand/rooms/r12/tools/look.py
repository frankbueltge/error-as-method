import json,sys,collections
d=json.load(open(sys.argv[1]))['entries']
print(len(d))
ts=sorted(int(e['time']) for e in d if e['q']=='0')
print(len(ts))
iv=[(b-a)/60 for a,b in zip(ts,ts[1:])]
h=collections.Counter(int(x//5)*5 for x in iv if x<200)
for k in sorted(h): print(k,h[k])
print(collections.Counter((e['E'],e['wc'],e['maj'],e['min']) for e in d).most_common(10))
print(sum(1 for e in d if e['durationSec']))
import datetime
days=collections.Counter(datetime.datetime.utcfromtimestamp(t-7*3600).strftime('%m') for t in ts); print(sorted(days.items()))
