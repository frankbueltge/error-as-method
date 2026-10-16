import numpy as np, json
y=np.load('y.npy'); N=1464
xi=3.0+np.arange(N)*(296.5-3.0)/(N-1); ci=np.floor(xi).astype(int)
v=90-y
groups=[np.where(ci==c)[0] for c in np.unique(ci)]
for p in range(6):
    for g in groups:
        a,b=g[0],g[-1]
        best=None
        for s in (np.sort(v[g]),np.sort(v[g])[::-1]):
            cost=np.abs(np.diff(s)).sum()
            if a>0: cost+=abs(s[0]-v[a-1])
            if b<N-1: cost+=abs(s[-1]-v[b+1])
            if best is None or cost<best[0]: best=(cost,s)
        v[g]=best[1]
for d in [0,1,15,39]: print(d, np.round(v[d*24:(d+1)*24]).astype(int).tolist())
p=v.reshape(61,24)
print('max hr',np.bincount(p.argmax(1),minlength=24)); print('min hr',np.bincount(p.argmin(1),minlength=24))
amp=p.max(1)-p.min(1); print(np.round(amp).astype(int).tolist())
# normalise 0..1 over whole range
n=(v-v.min())/(v.max()-v.min())
json.dump([round(float(t),4) for t in n],open('vals.json','w'))
print(v.min(),v.max())
