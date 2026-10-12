from PIL import Image
im=Image.open('/tmp/claude-0/s122/mk/m12/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
print(W,H)
import collections
hist=collections.Counter(px[x,y]//16 for x in range(W) for y in range(H)); print(sorted(hist.items()))
# threshold & components
T=160
seen=set(); comps=[]
for x in range(W):
  for y in range(H):
    if px[x,y]<T and (x,y) not in seen:
      st=[(x,y)]; seen.add((x,y)); pts=[]
      while st:
        a,b=st.pop(); pts.append((a,b))
        for da in(-1,0,1):
          for db in(-1,0,1):
            c,d=a+da,b+db
            if 0<=c<W and 0<=d<H and (c,d) not in seen and px[c,d]<T:
              seen.add((c,d)); st.append((c,d))
      wsum=sum(255-px[p] for p in pts)
      cx=sum(p[0]*(255-px[p]) for p in pts)/wsum; cy=sum(p[1]*(255-px[p]) for p in pts)/wsum
      comps.append((cx,cy,len(pts),wsum))
print(len(comps))
sz=collections.Counter(c[2] for c in comps); print(sorted(sz.items()))
xs=[c[0] for c in comps]; print(min(xs),max(xs)); ys=[c[1] for c in comps]; print(min(ys),max(ys))
import json; json.dump(comps,open('/tmp/claude-0/s122/mk/m12/scratch/comps.json','w'))
