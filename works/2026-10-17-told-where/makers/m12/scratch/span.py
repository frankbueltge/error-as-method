import json
from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m12/work/record.jpg').convert('L')
W,H=im.size
px=[[255-im.getpixel((x,y)) for x in range(W)] for y in range(H)]
B=json.load(open('blobs.json'))
P=4.82; c0=3.89-P; k=294/1463
up=[b for b in B if b['ymax']<=81]
# floor width per period: ink in rows 83-84 by column -> width at half max, subpixel
fl=[px[83][x]+px[84][x] for x in range(W)]
out=[]
for n in range(1,62):
  a=c0+n*P; b=a+P
  bs=[q for q in up if a<=q['x']<b]
  if not bs: continue
  span=(max(q['x'] for q in bs)-min(q['x'] for q in bs))/k+1
  # floor cluster around center c=a (night center) : columns within +-2.4
  c=a
  cols=[x for x in range(W) if abs(x-c)<=2.4]
  w=sum(fl[x] for x in cols)/max(fl[x] for x in cols) if cols else 0
  out.append((n,round(span,1),round(w,2)))
for o in out: print(o)
