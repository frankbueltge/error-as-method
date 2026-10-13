from PIL import Image
import math,json
im=Image.open('/tmp/claude-0/s123/mk/m02/work/record.jpg').convert('L')
w,h=im.size; px=im.load()
cols=[]
for x in range(w):
  ws=[max(0,235-px[x,y]) for y in range(h)]
  s=sum(ws)
  m=sum(y*v for y,v in enumerate(ws))/s if s else None
  cols.append((s,m))
ms=[c[1] if c[1] is not None else 45 for c in cols]; print([i for i,c in enumerate(cols) if c[1] is None])
ink=[c[0] for c in cols]
print('ink min/max',min(ink),max(ink), 'zeros',sum(1 for i in ink if i==0))
mean=sum(ms)/len(ms)
d=[m-mean for m in ms]
# periodogram
res=[]
for P10 in range(30,800):
  P=P10/10
  re=sum(v*math.cos(2*math.pi*i/P) for i,v in enumerate(d)); im_=sum(v*math.sin(2*math.pi*i/P) for i,v in enumerate(d))
  res.append((re*re+im_*im_,P))
res.sort(reverse=True)
print(res[:15])
json.dump(cols,open('cols.json','w'))
