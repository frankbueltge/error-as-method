from PIL import Image
import math, json
im=Image.open('/tmp/claude-0/s128/mk/m02/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
cols=[]
for x in range(W):
    w=[max(0,235-px[x,y]) for y in range(H)]
    s=sum(w)
    if s==0: cols.append(None); continue
    mean=sum(y*w[y] for y in range(H))/s
    # weighted quantiles
    acc=0;q={}
    for y in range(H):
        acc+=w[y]
        for p in (0.1,0.5,0.9):
            if p not in q and acc>=p*s: q[p]=y
    cols.append(dict(x=x,s=s,mean=mean,q10=q[0.1],q50=q[0.5],q90=q[0.9],w=w))
print('empty cols',sum(c is None for c in cols))
# periodicity: autocorr of q90 (lower edge) and q10
def series(k): return [c[k] if c else float('nan') for c in cols]
for k in ('q10','q50','q90','mean','s'):
    v=series(k); m=sum(x for x in v if x==x)/sum(1 for x in v if x==x)
    d=[ (x-m) if x==x else 0 for x in v]
    var=sum(a*a for a in d)
    ac=[sum(d[i]*d[i+L] for i in range(W-L))/var for L in range(1,40)]
    print(k,' '.join('%d:%.2f'%(L+1,a) for L,a in enumerate(ac)))
json.dump([[c['x'],c['q10'],c['q50'],c['q90'],round(c['mean'],2)] if c else None for c in cols],open('/tmp/claude-0/s128/mk/m02/scratch/cols.json','w'))
