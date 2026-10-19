import json
from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m14/work/record.jpg').convert('L')
W,H=im.size;px=im.load()
TH=200
path=[];prev=None
for x in range(W):
    blobs=[];cur=None
    for y in range(H):
        v=max(0,TH-px[x,y])
        if v>15:
            if cur is None: cur=[0,0]
            cur[0]+=v;cur[1]+=v*y
        elif cur is not None: blobs.append(cur[1]/cur[0]);cur=None
    if cur: blobs.append(cur[1]/cur[0])
    if not blobs: continue
    asc=sorted(blobs);desc=asc[::-1]
    o=asc if prev is None else ([b for b in asc if b>=prev-2]+[b for b in asc if b<prev-2])
    n=len(o)
    for i,y in enumerate(o): path.append((x-0.5+(i+0.5)/n,y))
    prev=o[-1]
x0,x1=path[0][0],path[-1][0]
N=1464;vals=[];j=0
for h in range(N):
    xt=x0+(x1-x0)*h/(N-1)
    while j<len(path)-2 and path[j+1][0]<xt: j+=1
    (xa,ya),(xb,yb)=path[j],path[j+1]
    t=0 if xb==xa else min(1,max(0,(xt-xa)/(xb-xa)))
    y=ya+(yb-ya)*t
    vals.append(round((90-y)/90,4))  # 0..1, up = larger
json.dump(vals,open('vals.json','w'))
# daily summary
for d in range(61):
    day=vals[d*24:(d+1)*24]
    mx=max(day);mn=min(day)
    print(d, f"{mn:.2f} {mx:.2f} peakhr={day.index(mx):2d} minhr={day.index(mn):2d}", ''.join(' .:-=+*#%@'[min(9,int(v*12))] for v in day))
