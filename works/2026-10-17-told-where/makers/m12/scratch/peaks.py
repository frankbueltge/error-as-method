from PIL import Image
import json
im=Image.open('/tmp/claude-0/s133/mk/m12/work/record.jpg').convert('L')
W,H=im.size
px=[[255-im.getpixel((x,y)) for x in range(W)] for y in range(H)]
g=lambda x,y: px[y][x] if 0<=x<W and 0<=y<H else 0
pk=[]
for y in range(H):
  for x in range(W):
    v=px[y][x]
    if v<70: continue
    nb=[g(x+a,y+b) for a in(-1,0,1) for b in(-1,0,1) if (a,b)!=(0,0)]
    # strict-ish local max with tie-break
    if all(v>n or (v==n and (a,b)<(0,0)) for n,(a,b) in zip(nb,[(a,b) for a in(-1,0,1) for b in(-1,0,1) if (a,b)!=(0,0)])):
      w=[(x+a,y+b,g(x+a,y+b)) for a in(-1,0,1) for b in(-1,0,1)]
      ink=sum(max(0,q[2]-15) for q in w)
      cx=sum(q[0]*max(0,q[2]-15) for q in w)/ink; cy=sum(q[1]*max(0,q[2]-15) for q in w)/ink
      pk.append(dict(x=cx,y=cy,ink=ink,v=v))
up=[p for p in pk if p['y']<81]
ink=sorted(p['ink'] for p in up)
print(len(pk),len(up),[ink[int(len(ink)*q)] for q in(.1,.25,.5,.75,.9)],ink[-5:])
json.dump(pk,open('peaks.json','w'))
