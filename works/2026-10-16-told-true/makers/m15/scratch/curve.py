from PIL import Image
import json,math
im=Image.open('/tmp/claude-0/s130/mk/m15/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
d=[[max(0,255-p[x,y]-30) for y in range(H)] for x in range(W)]
X0,X1,N=2.5,296.0,1464;pxh=(X1-X0)/(N-1)
sig=0.75
vals=[];sds=[]
for t in range(N):
  xt=X0+t*pxh
  sw=sy=syy=0
  for x in range(max(0,int(xt)-3),min(W,int(xt)+4)):
    k=math.exp(-(x-xt)**2/(2*sig*sig))
    for y in range(H):
      w=d[x][y]*k
      if w: sw+=w;sy+=w*y;syy+=w*y*y
  m=sy/sw;vals.append(90-m);sds.append(math.sqrt(max(0,syy/sw-m*m)))
print(min(vals),max(vals),sum(vals)/N, sum(sds)/N)
# fold check
f=[0]*24
for t,v in enumerate(vals): f[t%24]+=v/61
print([round(q,1) for q in f])
# outliers: blobs well above local curve
b=json.load(open('blobs.json'))
outl=[]
for x,y,v in b:
  t=(x-X0)/pxh;ti=min(N-1,max(0,round(t)))
  # local robust level: median of vals within +-36h
  win=sorted(vals[max(0,ti-36):ti+37]);med=win[len(win)//2]
  if (90-y)-med>14: outl.append([round(t,1),round(90-y,1),round((90-y)-med,1),v])
print(len(outl));print(outl)
json.dump({'v':[round(q,2) for q in vals],'sd':[round(q,2) for q in sds],'out':outl},open('curve.json','w'))
