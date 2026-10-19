import json
from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m14/work/record.jpg').convert('L');px=im.load()
W,H=im.size
cmin={};cmax={}
for x in range(W):
    ys=[y for y in range(H) if px[x,y]<140 and px[x,y]<=min(px[x,max(0,y-1)],px[x,min(H-1,y+1)])]
    if ys: cmin[x]=min(ys);cmax[x]=max(ys)
xs=sorted(cmin); X0,X1=xs[0],xs[-1]
peaks=[]
for x in xs:
    win=[cmin[k] for k in range(x-2,x+3) if k in cmin]
    if cmin[x]==min(win) and (not peaks or x-peaks[-1]>=3): peaks.append(x)
    elif cmin[x]==min(win) and peaks and cmin[x]<cmin[peaks[-1]]: peaks[-1]=x
print(len(peaks)); print(peaks)
anchors=[]
for i,p in enumerate(peaks):
    anchors.append((p,cmin[p]))
    if i+1<len(peaks):
        q=peaks[i+1]
        t=max(range(p+1,q), key=lambda k:cmax.get(k,-1)) if q-p>1 else p
        anchors.append((t+0.3,cmax[t]))
# ensure start/end
if anchors[0][0]>X0: anchors.insert(0,(X0,cmin[X0]))
if anchors[-1][0]<X1: anchors.append((X1,(cmin[X1]+cmax[X1])/2))
anchors.sort()
N=1464;vals=[];j=0
import math
for h in range(N):
    xt=X0+(X1-X0)*h/(N-1)
    while j<len(anchors)-2 and anchors[j+1][0]<xt: j+=1
    (xa,ya),(xb,yb)=anchors[j],anchors[j+1]
    t=0 if xb==xa else min(1,max(0,(xt-xa)/(xb-xa)))
    t=(1-math.cos(math.pi*t))/2   # ease between extremes
    vals.append(round((90-(ya+(yb-ya)*t))/90,4))
json.dump(vals,open('vals.json','w'))
json.dump({'peaks':peaks,'anchors':anchors},open('anchors.json','w'))
for d in range(61):
    day=vals[d*24:(d+1)*24]
    print(d, f"{min(day):.2f} {max(day):.2f}", ''.join(' .:-=+*#%@'[min(9,int(v*12))] for v in day))
