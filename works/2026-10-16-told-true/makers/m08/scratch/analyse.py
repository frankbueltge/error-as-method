from PIL import Image
import json, statistics as st
im=Image.open('/tmp/claude-0/s130/mk/m08/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
wt=[[max(0,(215-p[x,y]))/215 for y in range(H)] for x in range(W)]
# per-column robust envelopes: rows containing 10%..90% of ink
def env(col,lo,hi):
    tot=sum(col); 
    if tot==0: return None
    c=0;a=b=None
    for y,v in enumerate(col):
        c+=v
        if a is None and c>=lo*tot: a=y
        if b is None and c>=hi*tot: b=y
    return a,b
E=[env(wt[x],0.1,0.9) for x in range(W)]
# running high envelope over 7 columns
hi=[]
for x in range(W):
    vals=[E[i][0] for i in range(max(0,x-6),min(W,x+7)) if E[i]]
    hi.append(st.median(vals))
lo=[]
for x in range(W):
    vals=[E[i][1] for i in range(max(0,x-6),min(W,x+7)) if E[i]]
    lo.append(st.median(vals))
# outliers: ink more than 7 rows above running high envelope (smaller row = higher)
out=[]; clean=[r[:] for r in wt]
for x in range(W):
    for y in range(H):
        if wt[x][y]>0.25 and y < hi[x]-7:
            out.append((x,y,round(wt[x][y],2)))
    for y in range(H):
        if y < hi[x]-7: clean[x][y]=0
print('outlier px',len(out))
print(sorted(set(x for x,_,_ in out)))
# range per column series
rng=[lo[x]-hi[x] for x in range(W)]
print('hi',hi[::10]); print('lo',lo[::10]); print('rng',rng[::5])
# autocorrelation of range
m=sum(rng)/W
d=[r-m for r in rng]
for lag in range(40,110,4):
    print(lag, round(sum(d[i]*d[i+lag] for i in range(W-lag))/sum(v*v for v in d),2))
ink=[sum(c) for c in wt]
print('ink total', sum(ink), 'per col mean', sum(ink)/W)
# vertical extent of all ink
rows=[sum(wt[x][y] for x in range(W)) for y in range(H)]
print([round(r,1) for r in rows])
json.dump({'W':W,'H':H,'clean':[[round(v,3) for v in c] for c in clean],'out':out,'hi':hi,'lo':lo},open('/tmp/claude-0/s130/mk/m08/scratch/data.json','w'))
