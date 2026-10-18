from PIL import Image
import json
im=Image.open('/tmp/claude-0/s135/mk/m07/work/record.jpg').convert('L')
w,h=im.size;p=im.load()
ink=[[max(0,255-p[x,y]-12) for x in range(w)] for y in range(h)]
prof=[sum(r) for r in ink]
# refine level centres
c0,step=5.6,4.59
for it in range(5):
    cs=[]
    for k in range(18):
        c=c0+k*step
        ys=[y for y in range(h) if abs(y-c)<=2.3]
        wsum=sum(prof[y] for y in ys); cs.append(sum(y*prof[y] for y in ys)/wsum)
    n=len(cs); mk=sum(range(n))/n; mc=sum(cs)/n
    step=sum((k-mk)*(c-mc) for k,c in enumerate(cs))/sum((k-mk)**2 for k in range(n)); c0=mc-step*mk
print('c0',c0,'step',step)
print([round(c,1) for c in cs])
# column extent
cols=[sum(ink[y][x] for y in range(h)) for x in range(w)]
xs=[x for x in range(w) if cols[x]>200]; x0,x1=xs[0],xs[-1]+1
print('x extent',x0,x1)
D=61; L=18
grid=[[0.0]*L for _ in range(D)]
span=(x1-x0)/D
for x in range(x0,x1):
    # overlap of pixel [x,x+1) with days
    for d in range(D):
        a=max(x,x0+d*span); b=min(x+1,x0+(d+1)*span)
        if b<=a: continue
        f=b-a
        for y in range(h):
            if ink[y][x]==0: continue
            k=round((y-c0)/step)
            if 0<=k<L: grid[d][L-1-k]+=ink[y][x]*f   # level 0 = lowest
# per-day 24 hours, largest remainder
out=[]
for d in range(D):
    t=sum(grid[d]); raw=[24*g/t for g in grid[d]]
    # drop tiny noise (<0.35h) before allocation
    raw=[r if r>=0.35 else 0 for r in raw]; t2=sum(raw); raw=[24*r/t2 for r in raw]
    fl=[int(r) for r in raw]; rem=24-sum(fl)
    order=sorted(range(L),key=lambda k:-(raw[k]-fl[k]))
    for k in order[:rem]: fl[k]+=1
    out.append(fl)
for d,r in enumerate(out):
    print(d+1,''.join('.' if v==0 else (str(v) if v<10 else chr(55+v)) for v in r))
json.dump(out,open('/tmp/claude-0/s135/mk/m07/scratch/grid.json','w'))
# also column-level min/max per pixel column for an envelope
env=[]
for x in range(x0,x1):
    ks=[L-1-round((y-c0)/step) for y in range(h) if ink[y][x]>60]
    ks=[k for k in ks if 0<=k<L]
    env.append([min(ks),max(ks)] if ks else None)
json.dump(env,open('/tmp/claude-0/s135/mk/m07/scratch/env.json','w'))
