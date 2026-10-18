from PIL import Image
import math, json
im=Image.open('/tmp/claude-0/s135/mk/m01/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
d=lambda x,y: max(0,(250-p[x,y]))/250 if 0<=y<H else 0
y0=83.5; sp=78/17
occ=[]  # occ[x][k]
for x in range(W):
    row=[]
    for k in range(18):
        yc=y0-k*sp
        s=sum(d(x,y) for y in range(int(round(yc-2)),int(round(yc+2))+1))
        row.append(round(s,3))
    occ.append(row)
# extent
xs=[x for x in range(W) if sum(occ[x])>0.8]
print('x extent',xs[0],xs[-1])
json.dump(occ,open('occ.json','w'))
# mean level per column
m=[]
for x in range(W):
    t=sum(occ[x]); m.append(sum(k*v for k,v in enumerate(occ[x]))/t if t>0.3 else None)
print([None if v is None else round(v,1) for v in m])
# detrend with 15px running mean, FFT
xs=[x for x in range(W) if m[x] is not None]
r=[]
for x in xs:
    w=[m[j] for j in range(max(0,x-12),min(W,x+13)) if m[j] is not None]
    r.append(m[x]-sum(w)/len(w))
N=len(r)
L=xs[-1]-xs[0]
for f in range(1,150):
    re=sum(r[i]*math.cos(2*math.pi*f*(xs[i]-xs[0])/W) for i in range(N))
    im_=sum(r[i]*math.sin(2*math.pi*f*(xs[i]-xs[0])/W) for i in range(N))
    a=math.hypot(re,im_)/N
    if a>0.06: print(f, round(a,3), 'period px', round(W/f,2))
