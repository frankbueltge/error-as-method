from PIL import Image
import json, math
im=Image.open('/tmp/claude-0/s130/mk/m14/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
# column centroid profile (weighted by darkness)
cent={}
for x in range(W):
  w=[max(0,200-px[x,y]) for y in range(H)]; s=sum(w)
  if s>0: cent[x]=sum(y*w[y] for y in range(H))/s
# first/last dot centres: darkness-weighted x over first/last 3 columns
def xmass(xs):
  tot=sum(max(0,200-px[x,y]) for x in xs for y in range(H)); return sum(x*max(0,200-px[x,y]) for x in xs for y in range(H))/tot
x0=xmass([2,3]); x1=xmass([296,297]); print('x0,x1',x0,x1)
pass
hpp=(x1-x0)/1463
vals=[]
for i in range(1464):
  x=x0+i*hpp; xa=int(math.floor(x)); f=x-xa
  a=cent.get(xa,cent.get(xa+1)); b=cent.get(xa+1,a)
  vals.append(H-((1-f)*a+f*b))
# blobs: local intensity minima
blobs=[]
for x in range(1,W-1):
  for y in range(1,H-1):
    v=px[x,y]
    if v<170 and all(v<=px[x+dx,y+dy] for dx in(-1,0,1) for dy in(-1,0,1)):
      # subpixel centroid in 3x3
      ws=[(x+dx,y+dy,255-px[x+dx,y+dy]) for dx in(-1,0,1) for dy in(-1,0,1)]
      s=sum(w for *_,w in ws)
      blobs.append((sum(a*w for a,_,w in ws)/s, sum(b*w for _,b,w in ws)/s, 255-v))
print('blobs',len(blobs))
# outliers: blob far above local band (median y of blobs within +-4px)
out=[]
for bx,by,d in blobs:
  near=sorted(b[1] for b in blobs if abs(b[0]-bx)<5)
  med=near[len(near)//2]
  if by<med-22: out.append((bx,by))
print('outliers',len(out), sorted((round(a,1),round(b,1)) for a,b in out))
data={'v':[round(v,2) for v in vals],
      'blobs':[[round(a,1),round(b,1),d] for a,b,d in blobs],
      'out':[[round((a-x0)/hpp),round(H-b,1)] for a,b in out]}
json.dump(data,open('data.json','w'),separators=(',',':'))
vs=sorted(vals); print('v pct',vs[0],vs[73],vs[732],vs[1390],vs[-1])
