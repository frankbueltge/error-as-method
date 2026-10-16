from PIL import Image
import math, json
im=Image.open('/tmp/claude-0/s130/mk/m14/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
cols=[]
for x in range(W):
  w=[max(0,200-px[x,y]) for y in range(H)]
  s=sum(w)
  if s==0: cols.append(None); continue
  c=sum(y*w[y] for y in range(H))/s
  dark=[y for y in range(H) if px[x,y]<150]
  cols.append((c,s,min(dark) if dark else None,max(dark) if dark else None))
xs=[x for x in range(W) if cols[x]]
print('x range',xs[0],xs[-1], 'empty cols',[x for x in range(W) if not cols[x]])
# overall rows
rows=[sum(max(0,200-px[x,y]) for x in range(W)) for y in range(H)]
print('row mass', [round(r/1000,1) for r in rows])
# detrend centroid series, robust: median within band
c=[cols[x][0] for x in range(2,298)]; W=len(c)
# fill
m=sum(c)/len(c); c=[v-m for v in c]
# periodogram
res=[]
p=2.05
while p<120:
  f=1/p
  a=sum(c[x]*math.cos(2*math.pi*f*x) for x in range(W)); b=sum(c[x]*math.sin(2*math.pi*f*x) for x in range(W))
  res.append((p,(a*a+b*b)/W)); p*=1.01
res.sort(key=lambda r:-r[1])
for p,pw in res[:25]: print('period px %.2f  = %.1f h  = %.2f d  power %.1f'%(p,p*1464/300,p*1464/300/24,pw))
json.dump(c,open('cent.json','w'))
