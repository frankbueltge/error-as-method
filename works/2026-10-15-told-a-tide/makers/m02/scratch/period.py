import json,math
cols=json.load(open('/tmp/claude-0/s128/mk/m02/scratch/cols.json'))
W=len(cols); hpp=1464/300
for idx,name in ((4,'mean'),(3,'q90'),(1,'q10')):
    v=[c[idx] for c in cols]; m=sum(v)/W; d=[a-m for a in v]
    res=[]
    P=2.2
    while P<160:
        c=sum(d[i]*math.cos(2*math.pi*i/P) for i in range(W)); s=sum(d[i]*math.sin(2*math.pi*i/P) for i in range(W))
        res.append((c*c+s*s,P)); P*=1.004
    res.sort(reverse=True)
    print(name,[ '%.2fpx=%.1fh'%(P,P*hpp) for _,P in res[:12]])
# fold on 24h
v=[c[4] for c in cols]
for per_h in (24.0,24.84,23.93):
    P=per_h/hpp; bins=[[] for _ in range(12)]
    for i,a in enumerate(v): bins[int(((i+0.5)/P%1)*12)].append(a)
    print(per_h,' '.join('%.1f'%(sum(b)/len(b)) for b in bins))
