import json
B=json.load(open('blobs.json'))
x0,x1=3.0,296.0
step=(x1-x0)/1463
base=83.5; top=5.3
pts=[]
for b in B:
  if b['ymax']>=82: continue
  k=max(1,round(b['mass']/330))
  v=(base-b['y'])/(base-top)
  h=(b['x']-x0)/step
  pts.append((h,v,k))
print('dots est',sum(k for _,_,k in pts))
days=[[] for _ in range(61)]
for h,v,k in pts:
  d=int(h//24); d=min(max(d,0),60)
  days[d].append((h-24*d,v,k))
out=[]
for d,L in enumerate(days):
  n=sum(k for *_,k in L); s=sum(v*k for _,v,k in L); mx=max([v for _,v,_ in L] or [0])
  hs=[h for h,_,_ in L]
  print(d,n,round(s,2),round(mx,2), round(min(hs),1) if hs else '-', round(max(hs),1) if hs else '-')
  out.append(L)
json.dump(out,open('days.json','w'))
