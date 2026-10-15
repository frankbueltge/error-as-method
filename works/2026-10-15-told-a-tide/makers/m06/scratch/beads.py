from PIL import Image
import json
g=Image.open('/tmp/claude-0/s128/mk/m06/work/record.jpg').convert('L'); W,H=g.size; p=g.load()
D=[[max(0,255-p[x,y]-12) for y in range(H)] for x in range(W)]
x0,x1=2.5,297.0   # approx left edge of first hour, right edge of last
dw=(x1-x0)/61
days=[]
for d in range(61):
  a=x0+d*dw; b=a+dw
  prof=[0.0]*H
  for x in range(W):
    ov=max(0,min(b,x+1)-max(a,x))
    if ov>0:
      for y in range(H): prof[y]+=ov*D[x][y]
  tot=sum(prof); cum=0; qs=[]; i=0
  targets=[(k+0.5)/24*tot for k in range(24)]
  for y in range(H):
    nc=cum+prof[y]
    while i<24 and targets[i]<=nc:
      f=(targets[i]-cum)/prof[y] if prof[y] else 0
      qs.append(round(y+f,2)); i+=1
    cum=nc
  days.append(qs)
json.dump(days,open('days.json','w'))
for d in range(0,61,6): print(d, days[d][0], days[d][12], days[d][-1])
flat=[v for q in days for v in q]; print(len(flat), min(flat), max(flat))
