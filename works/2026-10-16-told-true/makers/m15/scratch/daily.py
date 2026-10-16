from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m15/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
x0=2.5;pxh=(296.0-2.5)/1463
rows=[]
for dday in range(61):
  a=x0+dday*24*pxh;b=a+24*pxh
  ws=0;my=0;ys=[]
  for x in range(int(a+0.5),int(b+0.5)):
    for y in range(H):
      w=max(0,200-p[x,y])
      if w: ws+=w;my+=w*y;ys+=[y]*(w//20+1)
  ys.sort()
  rows.append((dday,round(90-my/ws,1),90-ys[int(len(ys)*.9)],90-ys[int(len(ys)*.1)]))
for r in rows: print(r,'#'*int((r[1]-20)))
import math
m=[r[1] for r in rows];mu=sum(m)/61
for P in range(2,16):
  re=sum((v-mu)*math.cos(2*math.pi*i/P) for i,v in enumerate(m));im_=sum((v-mu)*math.sin(2*math.pi*i/P) for i,v in enumerate(m))
  print(P,round(math.hypot(re,im_),1))
