import json,datetime
d=open('px.raw','rb').read();W,H=480,220
X0,X1,N=6.5,472.5,5478
pts=[]
for y in range(H):
  for x in range(W):
    v=d[y*W+x]
    if v<215 and 3<=x<=476: pts.append((x,y,255-v))
print(len(pts))
# seasonal check: mean y of upper band (y<=112) per month
import collections
acc=collections.defaultdict(lambda:[0,0])
for x,y,w in pts:
  if y>112: continue
  day=(x-X0)*N/(X1-X0)
  dt=datetime.date(2000,1,1)+datetime.timedelta(days=max(0,min(N,int(round(day)))))
  a=acc[dt.month]; a[0]+=y*w; a[1]+=w
for m in sorted(acc): print(m, round(acc[m][0]/acc[m][1],1))
# compact: string of x,y,w as bytes -> base64
import base64
b=bytearray()
for x,y,w in pts: b+=bytes([x>>1, ((x&1)<<7)|y, w])
open('pts.b64','w').write(base64.b64encode(bytes(b)).decode())
