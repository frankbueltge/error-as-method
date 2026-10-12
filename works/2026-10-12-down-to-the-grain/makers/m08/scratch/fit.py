import math, json
from PIL import Image
g=Image.open('/tmp/claude-0/s122/mk/m08/work/record.jpg').convert('L'); W,H=g.size; p=g.load()
N=1464; A,B=2.9,296.4
xh=lambda t: A+t*(B-A)/(N-1)          # left edge of 2px dot -> covers columns floor(x)..
# darkness weights
D=[[max(0,235-p[x,y]) for y in range(H)] for x in range(W)]
# hours per column (dot centre at xh+0.5 falls in column floor(xh+0.5))
colhours={}
for t in range(N): colhours.setdefault(int(math.floor(xh(t)+0.5)),[]).append(t)
cons={'M2':12.4206012,'S2':12.0,'N2':12.65834824,'K1':23.93447213,'O1':25.81933871,'M4':6.210300601,'MS4':6.103339}
# column observations: darkness-weighted mean y
obs=[]
for x,hs in sorted(colhours.items()):
    s=sum(D[x]); 
    if s<50: continue
    obs.append((x,hs,sum(y*D[x][y] for y in range(H))/s))
# low-frequency basis: piecewise-linear hat functions every K hours
K=18
nodes=list(range(0,N+K,K))
def hat(t,j): return max(0,1-abs(t-nodes[j])/K)
def row(hs):
    r=[]
    for j in range(len(nodes)): r.append(sum(hat(t,j) for t in hs)/len(hs))
    for P in cons.values():
        r.append(sum(math.cos(2*math.pi*t/P) for t in hs)/len(hs)); r.append(sum(math.sin(2*math.pi*t/P) for t in hs)/len(hs))
    return r
X=[row(hs) for x,hs,m in obs]; Y=[m for x,hs,m in obs]
n=len(X[0]); lam=0.5
# normal equations with ridge on 2nd difference of hat coefs
M=[[sum(X[k][i]*X[k][j] for k in range(len(X))) for j in range(n)] for i in range(n)]
v=[sum(X[k][i]*Y[k] for k in range(len(X))) for i in range(n)]
nh=len(nodes)
for j in range(1,nh-1):
    d={j-1:1,j:-2,j+1:1}
    for a,ca in d.items():
        for b,cb in d.items(): M[a][b]+=lam*ca*cb
# solve
def solve(M,v):
    n=len(v); M=[r[:]+[v[i]] for i,r in enumerate(M)]
    for c in range(n):
        piv=max(range(c,n),key=lambda r:abs(M[r][c])); M[c],M[piv]=M[piv],M[c]
        for r in range(n):
            if r!=c:
                f=M[r][c]/M[c][c]
                for k in range(c,n+1): M[r][k]-=f*M[c][k]
    return [M[i][n]/M[i][i] for i in range(n)]
beta=solve(M,v)
res=[Y[k]-sum(X[k][i]*beta[i] for i in range(n)) for k in range(len(Y))]
print('rms resid px',math.sqrt(sum(r*r for r in res)/len(res)))
amp={}
for i,(nm,P) in enumerate(cons.items()):
    a,b=beta[nh+2*i],beta[nh+2*i+1]; amp[nm]=(math.hypot(a,b),math.degrees(math.atan2(b,a))%360)
    print(nm,P,round(amp[nm][0],2),round(amp[nm][1]))
def tide(t): return sum(beta[nh+2*i]*math.cos(2*math.pi*t/P)+beta[nh+2*i+1]*math.sin(2*math.pi*t/P) for i,P in enumerate(cons.values()))
def low(t): return sum(beta[j]*hat(t,j) for j in range(nh) if abs(t-nodes[j])<K)
model=[low(t)+tide(t) for t in range(N)]
# rank-matched reconstruction: for each column, distribute model hours onto observed darkness quantiles
rec=[None]*N
for x,hs in colhours.items():
    s=sum(D[x])
    if s<50:
        for t in hs: rec[t]=model[t]
        continue
    cdf=[];c=0
    for y in range(H): c+=D[x][y]; cdf.append(c/s)
    # order of hours by model value (y pixel; larger y = lower value)
    order=sorted(hs,key=lambda t:model[t])
    k=len(order)
    for i,t in enumerate(order):
        q=(i+0.5)/k
        y=next(yy for yy in range(H) if cdf[yy]>=q)
        lo=cdf[y-1] if y>0 else 0
        frac=(q-lo)/max(1e-9,cdf[y]-lo)
        rec[t]=y-0.5+frac
json.dump(dict(model=model,rec=rec,low=[low(t) for t in range(N)],tide=[tide(t) for t in range(N)],amp=amp),open('/tmp/claude-0/s122/mk/m08/scratch/series.json','w'))
print('rec range',min(rec),max(rec))
