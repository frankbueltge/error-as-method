from PIL import Image
import json,math
im=Image.open('/tmp/claude-0/s133/mk/m12/work/record.jpg').convert('L')
W,H=im.size
px=[[255-im.getpixel((x,y)) for x in range(W)] for y in range(H)]
fl=[px[83][x]+px[84][x] for x in range(W)]
print(''.join(str(min(9,v//50)) for v in fl))
# fit period via phase of fundamental
best=None
for P10 in range(470,510):
  P=P10/100
  s=sum(fl[x]*math.cos(2*math.pi*x/P) for x in range(W)); c=sum(fl[x]*math.sin(2*math.pi*x/P) for x in range(W))
  a=math.hypot(s,c)
  if not best or a>best[0]: best=(a,P,math.atan2(c,s))
print(best, 'floor center at x=', best[2]/(2*math.pi)*best[1])
