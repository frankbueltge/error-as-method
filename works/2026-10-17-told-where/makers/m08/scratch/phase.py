import math
from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m08/work/record.jpg').convert('L')
W,H=im.size; p=im.load(); pd=W/61
# x span of data 2..296 -> hourly spacing
fl=[(255-p[x,83])+(255-p[x,84]) for x in range(W)]
best=None
for k in range(100):
    ph=k/100*pd
    s=sum(fl[x]*math.cos(2*math.pi*(x+0.5-ph)/pd) for x in range(5,292))
    if best is None or s<best[0]: best=(s,ph)
print(best)
