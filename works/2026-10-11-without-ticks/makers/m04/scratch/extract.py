import json, math
d=json.load(open('gray.json'));g=d['g'];w,h=d['w'],d['h']
X0,X1=81,1080; Y0,Y1=18,449
# ink with gridline background removed: per-row median background
ink={}
for y in range(Y0,Y1):
    row=[g[y][x] for x in range(X0,X1)]
    bg=sorted(row)[len(row)//2]
    for x in range(X0,X1):
        v=(bg-g[y][x])/(bg-34) if bg>34 else 0
        if v>0.08: ink[(x,y)]=min(1.0,v)
# components (8-connected)
seen=set(); comps=[]
for p in ink:
    if p in seen: continue
    st=[p]; seen.add(p); c=[]
    while st:
        q=st.pop(); c.append(q)
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                r=(q[0]+dx,q[1]+dy)
                if r in ink and r not in seen: seen.add(r); st.append(r)
    comps.append(c)
mass=[sum(ink[p] for p in c) for c in comps]
import statistics
small=sorted(m for m,c in zip(mass,comps) if len(c)<=12)
print('ncomps',len(comps),'total mass',sum(mass))
print('mass quantiles of small comps',[round(small[int(len(small)*q)],2) for q in (0.1,0.25,0.5,0.75,0.9)])
# histogram of masses
from collections import Counter
print(sorted(Counter(round(m) for m in mass).items())[:30])
json.dump({'ink':[[x,y,v] for (x,y),v in ink.items()],'comps':[[list(p) for p in c] for c in comps]},open('comps.json','w'))
