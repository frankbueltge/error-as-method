import json
from PIL import Image, ImageDraw
bl=json.load(open('blobs.json'))
a=3.6; s=0.20090; N=1464; SM=1.2
X=lambda i:a+s*i
vals=[0.0]*N
pts=[(x,83.5-y) for x,y,v in bl if 83.5-y>1.2]
for d in range(-1,62):
  lo=24*d+SM; hi=lo+24
  bs=[(x,v) for x,v in pts if X(lo)<=x<X(hi)]
  if not bs: continue
  xmin=min(x for x,v in bs); xmax=max(x for x,v in bs)
  hrs=[i for i in range(int(lo)+1,int(hi)+1) if 0<=i<N and xmin-0.08<=X(i)<=xmax+0.08]
  noon=lo+12
  for part in (0,1):
    H=[i for i in hrs if (i<noon)==(part==0)]
    V=sorted([v for x,v in bs if (x<X(noon))==(part==0)], reverse=(part==1))
    if not H: continue
    if not V: V=[2.0]
    for j,i in enumerate(H):
      t=j*(len(V)-1)/(len(H)-1) if len(H)>1 else (len(V)-1)/2
      k=int(t); f=t-k
      vals[i]=V[k]*(1-f)+(V[min(k+1,len(V)-1)])*f
mx=max(vals)
print('max',mx, 'nonzero',sum(1 for v in vals if v>0))
q=[round(v/80*100) for v in vals]
json.dump(q,open('series.json','w'))
im=Image.new('L',(300,90),255);dr=ImageDraw.Draw(im)
for i,v in enumerate(vals):
  x=X(i);y=83.5-v
  dr.ellipse([x-0.7,y-0.7,x+0.7,y+0.7],fill=0)
im.resize((1200,360),Image.NEAREST).save('recon.png')
# daily stats
for d in range(61):
  day=vals[24*d:24*d+24]
  print(d, sum(1 for v in day if v>0), round(max(day)), round(sum(day)), end=' | ')
