import json,math
S=json.load(open('/tmp/claude-0/s122/mk/m12/scratch/series.json')); v=S['v']; N=len(v)
def fit(periods):
  cols=[[1.0]*N]
  for P in periods:
    cols.append([math.cos(2*math.pi*t/P) for t in range(N)]); cols.append([math.sin(2*math.pi*t/P) for t in range(N)])
  n=len(cols)
  A=[[sum(cols[i][t]*cols[j][t] for t in range(N)) for j in range(n)] for i in range(n)]
  b=[sum(cols[i][t]*v[t] for t in range(N)) for i in range(n)]
  # gauss
  for i in range(n):
    p=max(range(i,n),key=lambda r:abs(A[r][i])); A[i],A[p]=A[p],A[i]; b[i],b[p]=b[p],b[i]
    for r in range(n):
      if r!=i:
        f=A[r][i]/A[i][i]; A[r]=[A[r][c]-f*A[i][c] for c in range(n)]; b[r]-=f*b[i]
  c=[b[i]/A[i][i] for i in range(n)]
  model=[sum(c[i]*cols[i][t] for i in range(n)) for t in range(N)]
  res=[v[t]-model[t] for t in range(N)]
  amps=[(P,round(math.hypot(c[1+2*k],c[2+2*k]),1)) for k,P in enumerate(periods)]
  return c,model,res,amps
var=sum((x-sum(v)/N)**2 for x in v)/N
for per in ([12.4206],[12.4206,12.0],[12.4206,12.0,12.6583,23.9345,25.8193,24.0659]):
  c,m,r,a=fit(per); print(a, 'resvar frac',round(sum(x*x for x in r)/N/var,3))
# scan period
best=[]
for P10 in range(110,140):
  P=P10/10; c,m,r,a=fit([P]); best.append((round(sum(x*x for x in r)/N/var,3),P))
print(sorted(best)[:5])
c,m,r,a=fit([12.4206,12.0,12.6583,23.9345,25.8193,24.0659])
json.dump({'v':v,'f':S['f'],'tide':m,'res':r},open('/tmp/claude-0/s122/mk/m12/scratch/fit.json','w'))
for d in range(61): print(d,round(sum(r[d*24:(d+1)*24])/24),end=' ')
