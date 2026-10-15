import json, math
cols=json.load(open('cols.json')); W=len(cols); H=len(cols[0])
thr=40
med=[];lo=[];hi=[];mass=[]
cols=cols[1:299]; W=len(cols)
for c in cols:
  c=[v if v>thr else 0 for v in c]
  s=sum(c); mass.append(s)
  acc=0; m=None
  for y,v in enumerate(c):
    acc+=v
    if m is None and acc>=s/2: m=y
  ys=[y for y,v in enumerate(c) if v>0]
  med.append(H-1-m); hi.append(H-1-min(ys)); lo.append(H-1-max(ys))
print('mass per col mean',sum(mass)/W, 'per value', sum(mass)/1464)
def per(series,name):
  n=len(series); mu=sum(series)/n; s=[v-mu for v in series]
  res=[]
  for k in range(1,n//2):
    re=sum(s[i]*math.cos(2*math.pi*k*i/n) for i in range(n)); im=sum(s[i]*math.sin(2*math.pi*k*i/n) for i in range(n))
    res.append((re*re+im*im,k))
  res.sort(reverse=True)
  print(name,[(k, round(n/k,1), round(n/k*1464/300/24,2)) for p,k in res[:8]])
for s,n in((med,'median'),(lo,'low'),(hi,'high'),(mass,'mass'),([h-l for h,l in zip(hi,lo)],'spread')): per(s,n)
# print daily means: group by ~4.92 px
print(' '.join(str(v) for v in med))
print(' '.join(str(v) for v in lo))
