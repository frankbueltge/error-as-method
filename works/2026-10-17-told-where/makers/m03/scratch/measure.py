from PIL import Image
import math, json, sys
g=Image.open(sys.argv[1]).convert('L'); W,H=g.size; p=g.load()
D=[[ (255-p[x,y])/255.0 for x in range(W)] for y in range(H)]
# extent
cols=[x for x in range(W) if max(D[y][x] for y in range(H))>0.3]
rows=[y for y in range(H) if max(D[y])>0.3]
print('x extent',cols[0],cols[-1],'y extent',rows[0],rows[-1])
# zero band row profile
band=[(D[83][x]+D[84][x])/2 for x in range(W)]
# row sums to locate zero line
rs=[sum(D[y]) for y in range(H)]
print('row sums bottom:',[(y,round(rs[y],1)) for y in range(78,90)])
# period by fitting: try periods, maximize |sum band*exp(2pi i x/P)|
best=None
for k in range(4000,5200):
  P=k/1000
  re=sum(band[x]*math.cos(2*math.pi*x/P) for x in range(W)); im=sum(band[x]*math.sin(2*math.pi*x/P) for x in range(W))
  a=math.hypot(re,im)
  if not best or a>best[0]: best=(a,P,math.atan2(im,re))
print('period',best)
