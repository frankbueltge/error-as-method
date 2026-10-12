import math, json
from PIL import Image
g=Image.open('/tmp/claude-0/s122/mk/m08/work/record.jpg').convert('L'); W,H=g.size; p=g.load()
cols=[]
for x in range(W):
    w=[max(0,235-p[x,y]) for y in range(H)]
    s=sum(w)
    m=sum(y*w[y] for y in range(H))/s
    sd=math.sqrt(sum((y-m)**2*w[y] for y in range(H))/s)
    # quantiles
    c=0;q={}
    for y in range(H):
        c+=w[y]
        for qq in (0.05,0.5,0.95):
            if qq not in q and c>=qq*s: q[qq]=y
    cols.append(dict(x=x,mass=s,mean=m,sd=sd,q05=q[0.05],q50=q[0.5],q95=q[0.95]))
json.dump(cols,open('/tmp/claude-0/s122/mk/m08/scratch/cols.json','w'))
def dft(v):
    n=len(v); mu=sum(v)/n; v=[a-mu for a in v]
    out=[]
    for k in range(1,n//2):
        re=sum(v[i]*math.cos(2*math.pi*k*i/n) for i in range(n)); im=sum(v[i]*math.sin(2*math.pi*k*i/n) for i in range(n))
        out.append((math.hypot(re,im),k,n/k))
    return sorted(out,reverse=True)[:8]
for key in ('mean','sd','q05','q95','mass'):
    print(key,[ (round(a),k,round(per,2)) for a,k,per in dft([c[key] for c in cols])])
print('mass', [round(c['mass']/1000) for c in cols])
print('q05',[c['q05'] for c in cols])
print('q95',[c['q95'] for c in cols])
