import json
v=json.load(open('series.json'))
N=len(v)
for h in range(24):
    a=[v[d*24+h] for d in range(61)]
    print(h, round(sum(a)/61,1), '#'*int(sum(a)/61-10))
dm=[sum(v[d*24:(d+1)*24])/24 for d in range(61)]
print([round(x,1) for x in dm])
amp=[max(v[d*24:(d+1)*24])-min(v[d*24:(d+1)*24]) for d in range(61)]
print([round(x) for x in amp])
