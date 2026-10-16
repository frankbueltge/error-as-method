from PIL import Image
import math
im=Image.open('/tmp/claude-0/s130/mk/m16/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
cols=[]
for x in range(W):
    ws=0;sy=0;syy=0;ys=[]
    for y in range(H):
        d=max(0,200-px[x,y])/200
        if d>0.15:
            ws+=d;sy+=d*y;syy+=d*y*y;ys.append(y)
    m=sy/ws if ws else float('nan')
    sd=math.sqrt(max(0,syy/ws-m*m)) if ws else 0
    cols.append((x,ws,m,sd,min(ys) if ys else -1,max(ys) if ys else -1))
tot=sum(c[1] for c in cols)
print('total ink',tot, 'ink per value', tot/1464)
import json
json.dump(cols,open('/tmp/claude-0/s130/mk/m16/scratch/cols.json','w'))
# periodogram of mean y
dt=1464/W
ms=[c[2] for c in cols]
mu=sum(ms)/len(ms)
res=[]
for i in range(1,600):
    P=6+i*0.5 if i<200 else 106+(i-200)*2
    f=1/P
    a=sum((m-mu)*math.cos(2*math.pi*f*(x+0.5)*dt) for x,m in enumerate(ms))
    b=sum((m-mu)*math.sin(2*math.pi*f*(x+0.5)*dt) for x,m in enumerate(ms))
    res.append((math.hypot(a,b)*2/len(ms),P))
for r in sorted(res,reverse=True)[:25]: print('%.3f px amp at period %.1f h'%r)
# ink per column
print([round(c[1],1) for c in cols[:60]])
print('sd',[round(c[3],1) for c in cols[:60]])
