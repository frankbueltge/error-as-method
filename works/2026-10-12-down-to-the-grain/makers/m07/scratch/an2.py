from PIL import Image
import math
g=Image.open('/tmp/claude-0/s122/mk/m07/work/record.jpg').convert('L')
W,H=g.size
P=[[255-g.getpixel((x,y)) for x in range(W)] for y in range(H)]
cols=[x for x in range(W) if any(P[y][x]>100 for y in range(H))]
print('x extent',cols[0],cols[-1])
rows=[y for y in range(H) if any(P[y][x]>100 for x in range(W))]
print('y extent',rows[0],rows[-1])
# per-day windows: 61 days over extent
x0,x1=cols[0],cols[-1]+1
pp=(x1-x0)/61
def pct(a,q):
  a=sorted(a); return a[min(len(a)-1,int(q*len(a)))]
out=[]
for d in range(61):
  a=int(round(x0+d*pp)); b=int(round(x0+(d+1)*pp))
  ys=[]
  for x in range(a,b):
    for y in range(H):
      if P[y][x]>90: ys+= [y]*(P[y][x]//40)
  lo,hi,med=pct(ys,.05),pct(ys,.95),pct(ys,.5)
  out.append((d,lo,med,hi,hi-lo))
  print(d,a,b,lo,med,hi,hi-lo, '#'*(hi-lo))
