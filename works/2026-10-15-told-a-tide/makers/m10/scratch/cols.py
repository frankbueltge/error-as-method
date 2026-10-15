from PIL import Image
import math, json
im=Image.open('/tmp/claude-0/s128/mk/m10/work/record.jpg').convert('L')
W0,H=im.size; px=im.load(); W=W0
cols=[]
for x in range(1,W-1):
    w=[max(0,230-px[x,y]) for y in range(H)]
    s=sum(w)
    ys=[y for y in range(H) if px[x,y]<170]
    if s==0: continue
    m=sum(y*w[y] for y in range(H))/s
    # percentiles of weight
    acc=0; p={}
    for q in (0.1,0.5,0.9):
        acc=0
        for y in range(H):
            acc+=w[y]
            if acc>=q*s: p[q]=y; break
    cols.append(dict(x=x,mass=s,mean=m,p10=p[0.1],p50=p[0.5],p90=p[0.9],top=min(ys) if ys else None,bot=max(ys) if ys else None))
json.dump(cols,open('cols.json','w'))
W=len(cols)
mass=[c['mass'] for c in cols]; print('mass mean',sum(mass)/W, 'min',min(mass),'max',max(mass))
for name in ('mean','p50','p10','p90','mass'):
    v=[c[name] for c in cols]; mu=sum(v)/len(v); v=[a-mu for a in v]
    den=sum(a*a for a in v)
    out=[]
    for lag in range(1,16):
        out.append('%d:%.2f'%(lag,sum(v[i]*v[i+lag] for i in range(W-lag))/den))
    print(name,' '.join(out))
# DFT of p50 detrended
v=[c['p90']-c['p10'] for c in cols]; mu=sum(v)/W; v=[a-mu for a in v]
pw=[]
for k in range(1,151):
    re=sum(v[i]*math.cos(2*math.pi*k*i/W) for i in range(W)); im_=sum(v[i]*math.sin(2*math.pi*k*i/W) for i in range(W))
    pw.append((re*re+im_*im_,k,W/k))
pw.sort(reverse=True); print('spread spectrum top',[(k,round(p,1)) for _,k,p in pw[:8]])
v=[c['p50'] for c in cols]; mu=sum(v)/W; v=[a-mu for a in v]
pw=[]
for k in range(1,151):
    re=sum(v[i]*math.cos(2*math.pi*k*i/W) for i in range(W)); im_=sum(v[i]*math.sin(2*math.pi*k*i/W) for i in range(W))
    pw.append((re*re+im_*im_,k,W/k))
pw.sort(reverse=True); print('median spectrum top',[(k,round(p,1)) for _,k,p in pw[:8]])
