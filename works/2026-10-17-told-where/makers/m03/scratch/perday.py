from PIL import Image
import math, json, sys
g=Image.open(sys.argv[1]).convert('L'); W,H=g.size; p=g.load()
D=[[ max(0,(235-p[x,y]))/235.0 for x in range(W)] for y in range(H)]
P=4.822; x0=-0.988+P  # night centres
Z=83.5; TOP=5.0
segs=[]; k=0
while True:
  a=x0+k*P-P; b=a+P
  if a>W: break
  segs.append((a,b)); k+=1
out=[]
for i,(a,b) in enumerate(segs):
  # fractional column weights
  def w(x): return max(0,min(x+1,b)-max(x,a))
  xs=[x for x in range(max(0,int(a)),min(W,int(b)+2)) if w(x)>0]
  cov=sum(w(x) for x in xs)
  band=sum(w(x)*min(1,(D[83][x]+D[84][x])/1.6) for x in xs)
  gap=cov-band
  ink=0; mom=0; top=None
  for x in xs:
    for y in range(0,82):
      d=D[y][x]*w(x)
      ink+=d; mom+=d*(Z-y)
      if D[y][x]>0.35 and (top is None or y<top): top=y
  out.append(dict(i=i,a=round(a,2),b=round(b,2),cov=round(cov,2),gap=round(gap,2),ink=round(ink,2),mom=round(mom,1),top=top))
for o in out: print(o)
json.dump(out,open('perday.json','w'))
