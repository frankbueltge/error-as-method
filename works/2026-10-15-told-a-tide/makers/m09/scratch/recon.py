# Recover an hourly sequence from the dot picture.
# Per column: find dark runs, split by ink mass into dots, then order the dots
# so the line runs smoothly from the previous column into the next.
import numpy as np, itertools, json
from PIL import Image
im=np.asarray(Image.open('/tmp/claude-0/s128/mk/m09/work/record.jpg').convert('L')).astype(float)
H,W=im.shape
ink=np.clip(255-im-35,0,None)
cols=[]
masses=[]
for x in range(W):
    c=ink[:,x]; runs=[]; y=0
    while y<H:
        if c[y]>25:
            s=y
            while y<H and c[y]>25: y+=1
            seg=c[s:y]; m=seg.sum(); cen=(seg*np.arange(s,y)).sum()/m
            runs.append([s,y,m,cen])
        else: y+=1
    cols.append(runs); masses+= [r[2] for r in runs]
masses=np.array(masses)
# a single isolated dot's mass: use the median of short runs
unit=sum(r[2] for c in cols for r in c)/1464.0
print('unit dot mass',unit)
vals=[]
for x,runs in enumerate(cols):
    v=[]
    for s,e,m,cen in runs:
        n=max(1,int(round(m/unit)))
        if n==1: v.append(cen)
        else: v+= list(np.linspace(s+0.5*(e-s)/n, e-0.5*(e-s)/n, n)-0.5)
    vals.append(v)
print('dots found',sum(len(v) for v in vals))
def order(v,start,end):
    if len(v)<=1: return v
    if len(v)<=7:
        best=None
        for p in itertools.permutations(v):
            c=abs(p[0]-start)+sum(abs(p[i+1]-p[i]) for i in range(len(p)-1))+abs(end-p[-1])
            if best is None or c<best[0]: best=(c,p)
        return list(best[1])
    rest=list(v); out=[]; cur=start
    while rest:
        j=min(range(len(rest)),key=lambda i:abs(rest[i]-cur)); cur=rest.pop(j); out.append(cur)
    return out
X0,X1=3.0,297.0
seq=[]  # (t_hours, y)
prev=None
for x in range(W):
    v=vals[x]
    if not v: continue
    nxt=[u for u in (vals[x+1] if x+1<W else []) ]
    start=prev if prev is not None else np.median(v)
    end=np.median(nxt) if nxt else np.median(v)
    o=order(v,start,end)
    ta=(x-0.5-X0)/(X1-X0)*1463; tb=(x+0.5-X0)/(X1-X0)*1463
    for i,u in enumerate(o):
        seq.append((ta+(i+0.5)*(tb-ta)/len(o), u))
    prev=o[-1]
# resample to the 1464 hours
t=np.array([s[0] for s in seq]); y=np.array([s[1] for s in seq])
hours=np.arange(1464)
yy=np.interp(hours,t,y)
val=(H-1-yy)   # height in image rows, larger = higher
json.dump({'v':[round(float(a),1) for a in val]},open('/tmp/claude-0/s128/mk/m09/scratch/hourly.json','w'))
# check: fold
for P in (12.42,23.93,24.0,24.84):
    ph=2*np.pi*hours/P; z=np.abs(((val-val.mean())*np.exp(1j*ph)).mean())
    print(P,'amp %.2f'%z)
fold=[val[(hours%24)==h].mean() for h in range(24)]
print(' '.join('%.0f'%f for f in fold))
