import json,sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); px=im.load(); W,H=im.size
pts=json.load(open('pts.json'))
x0,x1=1.0,296.0; per=24*(x1-x0)/1463
g0=1.16  # gap (daytime) centre for day 0
FLOOR=83.5
rows=[]
for k in range(-1,62):
  c=g0+k*per
  b=[p for p in pts if p[2]>=90 and p[1]<81.5 and abs(p[0]-c)<=per/2]
  if not b: continue
  top=min(p[1] for p in b)
  # floor columns between this gap and next
  fl=[x for x in range(W) if c<=x<c+per and (255-px[x,83])>150]
  rows.append((k,round(c,1),len(b),round((FLOOR-top)/(FLOOR-2),2),round(sum(FLOOR-p[1] for p in b)/(FLOOR-2),2),len(fl)))
for r in rows: print(r)
