import json
from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m19/work/record.jpg').convert('L'); p=im.load()
W,H=im.size
FLOOR=83.5; TOP=5.5
mean=[];mx=[];ink=[]
for x in range(W):
  sw=0;sv=0;m=0
  for y in range(H):
    d=(255-p[x,y])-60
    if d<=0: continue
    v=max(0.0,min(1.0,(FLOOR-y)/(FLOOR-TOP)))
    sw+=d; sv+=d*v
    if d>60: m=max(m,v)
  mean.append(round(sv/sw,3) if sw else None); mx.append(round(m,3)); ink.append(sw)
out={'x0':2.6,'pxPerDay':4.8227,'nightX':3.818,'mean':mean,'max':mx}
json.dump(out,open('cols.json','w'))
print(mean[:30]); print(mx[:30])
