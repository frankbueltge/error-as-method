import json
B=json.load(open('blobs.json'))
x0,x1=3.0,296.0
step=(x1-x0)/1463
base=83.5; top=5.3
pts=[]
for b in B:
  if b['ymax']>=82: continue
  k=max(1,round(b['mass']/330))
  pts.append(((b['x']-x0)/step,(base-b['y'])/(base-top),k,b['mass']))
cw=sum(h*v*k for h,v,k,_ in pts); 
# circular mean of hour mod 24
import math
sx=sum(v*k*math.cos(h/24*2*math.pi) for h,v,k,_ in pts); sy=sum(v*k*math.sin(h/24*2*math.pi) for h,v,k,_ in pts)
noon=(math.atan2(sy,sx)/(2*math.pi)*24)%24
print('solar noon at series hour',round(noon,2))
S=noon-12
days=[[] for _ in range(61)]
for h,v,k,m in pts:
  t=h-S; d=int(t//24); 
  if 0<=d<61: days[d].append([round(t-24*d,2),round(v,3),k])
res=[]
for d,L in enumerate(days):
  L.sort()
  n=sum(k for *_,k in L); s=sum(v*k for _,v,k in L); mx=max([v for _,v,_ in L] or [0])
  lo=min(h for h,v,k in L); hi=max(h for h,v,k in L)
  res.append((d,n,round(s,2),round(mx,2),lo,hi,round(hi-lo,1)))
  print(*res[-1])
json.dump(dict(noon=noon,days=days),open('days2.json','w'))
import statistics as st
for a,b in((0,20),(20,40),(40,61)):
  r=res[a:b];print(a,b,'tot',round(st.mean(x[2] for x in r),2),'max',round(st.mean(x[3] for x in r),2),'top5max',sorted(x[3] for x in r)[-5:],'span',round(st.median(x[6] for x in r),1))
