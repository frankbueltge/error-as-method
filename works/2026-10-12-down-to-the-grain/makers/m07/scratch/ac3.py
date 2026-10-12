from PIL import Image
import math
g=Image.open('/tmp/claude-0/s122/mk/m07/work/record.jpg').convert('L')
W,H=g.size
P=[[max(0,255-g.getpixel((x,y))-30) for x in range(W)] for y in range(H)]
def ac(dx,xa=3,xb=296):
  s=0;n=0
  for y in range(1,89):
    for x in range(xa,xb-dx):
      s+=P[y][x]*(P[y][x+dx]+0.5*(P[y-1][x+dx]+P[y+1][x+dx])); n+=1
  return s/n
a=[ac(d) for d in range(0,200)]
m=sum(a[1:])/199
hpp=1464/(296-2)  # hours per pixel approx
print('h/px',hpp)
for lo,hi in ((2.2,2.8),(4.4,5.6)):
  best=[]
  p=lo
  while p<hi:
    s=sum((a[d]-m)*math.cos(2*math.pi*d/p) for d in range(3,200))
    best.append((s,p)); p+=0.002
  best.sort(reverse=True)
  for s,p in best[:3]: print(round(p,3),'px =',round(p*hpp,2),'h',round(s,1))
