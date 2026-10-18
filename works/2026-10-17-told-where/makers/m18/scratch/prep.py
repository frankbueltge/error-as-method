import json,math
D=json.load(open('days2.json'))
days={int(k):[(a,b) for a,b,_ in v] for k,v in D['days'].items()}
N=len(days)
mx=[max(b for a,b in days[k]) for k in range(N)]
env=[max(mx[max(1,k-3):min(N-1,k+4)]) for k in range(N)]
def lin(xs,ys):
  n=len(xs);mx_=sum(xs)/n;my=sum(ys)/n
  s=sum((x-mx_)*(y-my) for x,y in zip(xs,ys))/sum((x-mx_)**2 for x in xs);return s,my-s*mx_
ks=list(range(1,N-1))
s,i=lin(ks,[env[k] for k in ks]); print('env fit',i+s*1,i+s*60)
s2,i2=lin(ks,[mx[k] for k in ks]); print('max fit',i2+s2*1,i2+s2*60)
hl=[]
for k in ks:
  nz=[a for a,b in days[k] if b>=2]
  hl.append((max(nz)-min(nz))/2)
s3,i3=lin(ks,hl); print('halfspan fit',i3+s3*1,i3+s3*60)
# daily sums (approx energy) using hourly interp
out=[]
for k in range(N):
  pts=sorted(days[k])
  # merge nearly coincident points: average t, keep both values ordered by t
  out.append([[round(a,2),round(max(0,b),1)] for a,b in pts])
json.dump({'days':out,'env':[i+s*k for k in range(N)],'half':[i3+s3*k for k in range(N)],'max':mx},open('data.json','w'))
print(mx)
