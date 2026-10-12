from PIL import Image
im=Image.open('/tmp/claude-0/s122/mk/m09/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
print(W,H)
import collections
hist=collections.Counter(px[x,y]//16 for x in range(W) for y in range(H)); print(sorted(hist.items()))
thr=160
seen=set(); comps=[]
for x in range(W):
  for y in range(H):
    if px[x,y]<thr and (x,y) not in seen:
      st=[(x,y)]; seen.add((x,y)); pts=[]
      while st:
        a,b=st.pop(); pts.append((a,b))
        for dx in(-1,0,1):
          for dy in(-1,0,1):
            c,d=a+dx,b+dy
            if 0<=c<W and 0<=d<H and (c,d) not in seen and px[c,d]<thr:
              seen.add((c,d)); st.append((c,d))
      wsum=sum(255-px[p] for p in pts)
      cx=sum((255-px[p])*p[0] for p in pts)/wsum; cy=sum((255-px[p])*p[1] for p in pts)/wsum
      comps.append((cx,cy,len(pts),wsum))
print(len(comps))
sizes=collections.Counter(c[2] for c in comps); print(sorted(sizes.items()))
xs=sorted(c[0] for c in comps); print(xs[:5],xs[-5:])
ys=sorted(c[1] for c in comps); print(ys[:5],ys[-5:])
import json; json.dump(comps,open('/tmp/claude-0/s122/mk/m09/scratch/comps.json','w'))
