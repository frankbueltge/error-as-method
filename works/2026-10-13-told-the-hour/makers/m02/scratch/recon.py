from PIL import Image
import json
im=Image.open('/tmp/claude-0/s123/mk/m02/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
N=1464; X1=298
prof=[]
for x in range(W):
  prof.append([max(0,230-px[x,y]) for y in range(H)])
colhours={}
for i in range(N):
  c=round(i*X1/(N-1)); colhours.setdefault(c,[]).append(i)
def quantiles(p,k):
  s=sum(p)
  if s==0: return None
  out=[]
  cum=0; targets=[(j+0.5)/k*s for j in range(k)]; t=0
  for y,v in enumerate(p):
    while t<k and cum+v>=targets[t]:
      frac=(targets[t]-cum)/v if v else 0
      out.append(y+frac); t+=1
    cum+=v
  while len(out)<k: out.append(out[-1])
  return out
means=[]
for x in range(W):
  s=sum(prof[x]); means.append(sum(y*v for y,v in enumerate(prof[x]))/s if s else None)
vals=[None]*N
for c,hs in colhours.items():
  q=quantiles(prof[c],len(hs))
  if q is None: q=quantiles(prof[c-1],len(hs))
  v=[H-1-y for y in q]  # larger = higher
  pm=means[c-1] if c>0 and means[c-1] is not None else means[c]
  nm=means[c+1] if c+1<W and means[c+1] is not None else means[c]
  rising = (pm-nm)>0   # y decreases => value rises
  v.sort(reverse=not rising)
  for h,val in zip(hs,v): vals[h]=round(val,2)
json.dump(vals,open('vals.json','w'))
print(min(vals),max(vals))
# daily profile by hour, all days
for start in (0,):
  acc=[0]*24; n=[0]*24
  for i,v in enumerate(vals): acc[i%24]+=v; n[i%24]+=1
  print([round(a/b,1) for a,b in zip(acc,n)])
# weekday-only (days with week offset 2..6) excluding days 35-48
acc=[0]*24; n=[0]*24
for i,v in enumerate(vals):
  d=i//24
  if d%7>=2 and not 35<=d<=48: acc[i%24]+=v; n[i%24]+=1
print('wkday',[round(a/b,1) for a,b in zip(acc,n)])
acc=[0]*24; n=[0]*24
for i,v in enumerate(vals):
  d=i//24
  if d%7<2 and not 35<=d<=48: acc[i%24]+=v; n[i%24]+=1
print('wkend',[round(a/b,1) for a,b in zip(acc,n)])
