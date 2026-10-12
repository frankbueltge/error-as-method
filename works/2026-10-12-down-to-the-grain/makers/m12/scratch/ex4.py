import json,math
pk=json.load(open('/tmp/claude-0/s122/mk/m12/scratch/peaks.json'))
x0,k=11.4,(1187.45-11.4)/1463
N=1464; slot=[None]*N
# greedy: sort by fractional distance
cands=sorted(pk,key=lambda p:abs((p[0]-x0)/k-round((p[0]-x0)/k)))
lost=0
for p in cands:
  h=round((p[0]-x0)/k)
  for dh in (0,1,-1,2,-2):
    j=h+dh
    if 0<=j<N and slot[j] is None and abs((p[0]-x0)/k-j)<2.2: slot[j]=p[1]; break
  else: lost+=1
print('lost',lost,'empty',sum(s is None for s in slot))
# interpolate
v=[None if s is None else 360-s for s in slot]
filled=[0 if s is not None else 1 for s in v]
for i in range(N):
  if v[i] is None:
    a=i-1
    while a>=0 and slot[a] is None: a-=1
    b=i+1
    while b<N and slot[b] is None: b+=1
    va=360-slot[a] if a>=0 else 360-slot[b]; vb=360-slot[b] if b<N else va
    v[i]=va+(vb-va)*(i-a)/(b-a) if a>=0 and b<N else va
json.dump({'v':v,'f':filled},open('/tmp/claude-0/s122/mk/m12/scratch/series.json','w'))
m=sum(v)/N
def ac(L): 
  return sum((v[i]-m)*(v[i+L]-m) for i in range(N-L))/sum((x-m)**2 for x in v)
print([ (L,round(ac(L),2)) for L in (1,2,3,6,12,24,48,72,168)])
# per-lag acf scan for peak
best=sorted(((ac(L),L) for L in range(5,400)),reverse=True)[:10]; print(best)
# daily means
for d in range(61):
  seg=v[d*24:(d+1)*24]; print(d,round(sum(seg)/24),round(min(seg)),round(max(seg)),end=' | ')
print()
# hour-of-day profile
prof=[sum(v[d*24+h] for d in range(61))/61 for h in range(24)]; print([round(p) for p in prof])
print(max(v), v.index(max(v)), min(v))
