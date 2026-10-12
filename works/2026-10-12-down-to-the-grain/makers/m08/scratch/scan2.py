import math, json
cols=json.load(open('/tmp/claude-0/s122/mk/m08/scratch/cols.json'))
A,B=2.9,296.4   # assumed dot-center x of hour 0 and hour 1463 (pixel coords, col center = x+0.5)
def hour_of_col(x): return ((x+0.5)-A-0.5)*1463/(B-A)
xs=list(range(4,296)); v=[cols[x]['mean'] for x in xs]
# remove running mean over 25 cols
sm=[sum(v[max(0,i-12):i+13])/len(v[max(0,i-12):i+13]) for i in range(len(v))]
r=[a-b for a,b in zip(v,sm)]
def amp(P):
    re=sum(r[i]*math.cos(2*math.pi*hour_of_col(xs[i])/P) for i in range(len(r))); im=sum(r[i]*math.sin(2*math.pi*hour_of_col(xs[i])/P) for i in range(len(r)))
    return math.hypot(re,im)*2/len(r)
for lo,hi,st in ((11.6,13.0,0.04),(22.8,27.0,0.2)):
    P=lo
    while P<=hi+1e-9:
        a=amp(P); print('%6.2fh %5.2f'%(P,a),'*'*int(a*10)); P+=st
    print()
for name,P in (('M2',12.4206),('S2',12.0),('N2',12.6583),('K2',11.967),('K1',23.9345),('O1',25.8193),('M4',6.2103)):
    print(name,round(amp(P),2))
