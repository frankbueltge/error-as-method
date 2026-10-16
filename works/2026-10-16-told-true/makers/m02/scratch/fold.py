from PIL import Image
import math
im=Image.open('/tmp/claude-0/s130/mk/m02/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
# find exact x extent with ink sum profile
prof=[sum(max(0,(255-p[x,y])/255-0.15) for y in range(H)) for x in range(W)]
print([round(v,2) for v in prof[:8]],[round(v,2) for v in prof[-8:]])
x0,x1=3.0,296.5
dxh=(x1-x0)/1463
best=None
for P in [x/1000 for x in range(4700,4950,5)]:
    # phase-fold column mean-y with period P
    bins=[[0,0] for _ in range(24)]
    for x in range(2,298):
        for y in range(H):
            w=(255-p[x,y])/255
            if w<0.25: continue
            b=int(((x-x0)/P%1)*24)%24
            bins[b][0]+=w*y; bins[b][1]+=w
    m=[a/b if b else 45 for a,b in bins]
    amp=max(m)-min(m)
    if best is None or amp>best[0]: best=(amp,P,m)
print('best period px',best[1],'expected',24*dxh)
P=24*dxh
bins=[[0,0,0] for _ in range(24)]
for x in range(2,298):
    for y in range(H):
        w=(255-p[x,y])/255
        if w<0.25: continue
        b=int(((x-x0)/P%1)*24)%24
        bins[b][0]+=w*y; bins[b][1]+=w
for h,(a,b,_) in enumerate(bins): print(h, round(a/b,1), '#'*int((90-a/b)))
