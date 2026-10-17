from PIL import Image
import math
im=Image.open('/tmp/claude-0/s133/mk/m07/work/record.jpg').convert('L')
w,h=im.size;p=im.load()
f=[sum((255-p[x,y])/255 for y in (83,84)) for x in range(w)]
best=None
for P in [4.6+i*0.005 for i in range(100)]:
  for a in [i*0.05 for i in range(int(P/0.05))]:
    s=sum(f[x]*math.cos(2*math.pi*(x-a)/P) for x in range(w))
    if best is None or s>best[0]: best=(s,P,a)
print(best)
# the ink extent of the plotted data
cols=[x for x in range(w) if any(p[x,y]<200 for y in range(h))]
rows=[y for y in range(h) if any(p[x,y]<200 for x in range(w))]
print(cols[0],cols[-1],rows[0],rows[-1])
