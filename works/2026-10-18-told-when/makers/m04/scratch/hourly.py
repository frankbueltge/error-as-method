import json
d=json.load(open('occ.json')); D=d['D']; first=d['first']; last=d['last']
K=18; N=1464
def m(x):
    t=sum(D[x]); return sum(k*v for k,v in enumerate(D[x]))/t
cols=list(range(first,last+1)); mv=[m(x) for x in cols]
# map hour i -> pixel coordinate (dot centre)
def hv(i):
    x=first+i*(last-first)/(N-1)
    j=x-first; a=int(j); f=j-a
    if a>=len(mv)-1: return mv[-1]
    return mv[a]*(1-f)+mv[a+1]*f
v=[hv(i) for i in range(N)]
# fine phase: hourly residual from 24h running mean
res=[[] for _ in range(24)]
for i in range(12,N-12):
    r=v[i]-sum(v[i-12:i+12])/24; res[i%24].append(r)
for h in range(24): print(h, round(sum(res[h])/len(res[h]),2))
# error-diffusion quantization to levels, value = 17-k (higher = larger value)
q=[];e=0.0
for i in range(N):
    t=v[i]+e; k=int(round(t)); k=max(0,min(17,k)); e=t-k; q.append(17-k)
from collections import Counter
print(sorted(Counter(q).items()))
json.dump(q,open('hourly_levels.json','w'))
print(''.join('%x'%min(15,x) for x in q[:240]))
