from PIL import Image
import json
im=Image.open('/tmp/claude-0/s133/mk/m12/work/record.jpg').convert('L')
W,H=im.size
px=[[255-im.getpixel((x,y)) for x in range(W)] for y in range(H)]
T=50
seen=set();blobs=[]
for y in range(H):
  for x in range(W):
    if px[y][x]>T and (x,y) not in seen:
      st=[(x,y)];seen.add((x,y));pts=[]
      while st:
        a,b=st.pop();pts.append((a,b))
        for da,db in ((1,0),(-1,0),(0,1),(0,-1)):
          c,d=a+da,b+db
          if 0<=c<W and 0<=d<H and (c,d) not in seen and px[d][c]>T:
            seen.add((c,d));st.append((c,d))
      ink=sum(px[b][a] for a,b in pts)
      cx=sum(a*px[b][a] for a,b in pts)/ink; cy=sum(b*px[b][a] for a,b in pts)/ink
      blobs.append(dict(x=cx,y=cy,ink=ink,n=len(pts),ymin=min(b for a,b in pts),ymax=max(b for a,b in pts)))
up=[b for b in blobs if b['ymax']<81]
inks=sorted(b['ink'] for b in up)
print(len(blobs),len(up))
print('ink quantiles',[inks[int(len(inks)*q)] for q in (0.05,.25,.5,.75,.95)], inks[-5:])
json.dump(blobs,open('blobs.json','w'))
