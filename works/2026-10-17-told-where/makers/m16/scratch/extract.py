import json
from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m16/work/record.jpg').convert('L');px=im.load()
W,H=im.size
I=lambda x,y:max(0,235-px[x,y]) if 0<=x<W and 0<=y<H else 0
P=4.824;n0=6.16;ZERO=83.5;TOP=5.0
dots=[]
for x in range(W):
  for y in range(2,81):
    v=I(x,y)
    if v<70: continue
    nb=[(I(x+a,y+b),a,b) for a in(-1,0,1) for b in(-1,0,1) if (a,b)!=(0,0)]
    # strict local max with tie-break
    if any(n>v or (n==v and (a,b)<(0,0)) for n,a,b in nb): continue
    s=sx=sy=0
    for a in(-1,0,1):
      for b in(-1,0,1):
        w=I(x+a,y+b); s+=w; sx+=w*(x+a); sy+=w*(y+b)
    cx,cy=sx/s+0.5,sy/s+0.5   # pixel-centre coords
    d=(cx-0.5-n0)/P
    k=round(d); ph=d-k
    val=(ZERO-(cy-0.5))/(ZERO-TOP)
    dots.append([k,round(ph*24,2),round(max(0,min(1.05,val)),3),round(min(1,s/900),2)])
print(len(dots))
import collections
c=collections.Counter(d[0] for d in dots);print(sorted(c.items()))
json.dump(dots,open('dots.json','w'))
# daily max and sum
for k in range(61):
  ds=[d for d in dots if d[0]==k]
  print(k,len(ds),max([d[2] for d in ds] or [0]),round(sum(d[2] for d in ds),2), sorted(d[1] for d in ds)[:1], sorted(d[1] for d in ds)[-1:])
