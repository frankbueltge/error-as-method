import json,math
d=json.load(open('/tmp/claude-0/s122/mk/m02/scratch/dots.json'))
n=len(d); m=1464
x0,x1=d[0][0],d[-1][0]; dx=(x1-x0)/(m-1)
X=[x0+i*dx for i in range(m)]
INF=1e18
# dp[i][j]: first i dots placed in first j slots
import array
prev=[0.0]*(m+1)
back=[]
for i in range(1,n+1):
    cur=[INF]*(m+1); bk=bytearray(m+1)
    xi=d[i-1][0]
    for j in range(i,m-(n-i)+1):
        a=cur[j-1]  # skip slot j
        b=prev[j-1]+(xi-X[j-1])**2
        if b<=a: cur[j]=b; bk[j]=1
        else: cur[j]=a; bk[j]=0
    back.append(bk); prev=cur
vals=[None]*m; j=m
for i in range(n,0,-1):
    while back[i-1][j]==0: j-=1
    vals[j-1]=d[i-1][1]; j-=1
missing=[k for k,v in enumerate(vals) if v is None]
print('dx',dx,'missing',missing)
# interpolate missing
for k in missing:
    a=k-1
    while a>=0 and vals[a] is None and a not in missing: a-=1
for k in range(m):
    if vals[k] is None:
        lo=k-1; hi=k+1
        while hi<m and vals[hi] is None: hi+=1
        vals[k]=vals[lo] if hi>=m else (vals[hi] if lo<0 else vals[lo]+(vals[hi]-vals[lo])*(k-lo)/(hi-lo))
v=[-y for y in vals]  # higher = larger
json.dump({'v':v,'missing':missing},open('/tmp/claude-0/s122/mk/m02/scratch/series.json','w'))
mu=sum(v)/m
def ac(l): return sum((v[i]-mu)*(v[i+l]-mu) for i in range(m-l))/sum((x-mu)**2 for x in v)
print([ (l,round(ac(l),2)) for l in (1,2,3,6,12,24,48,168,12*1,25,23)])
best=sorted(range(2,400),key=lambda l:-ac(l))[:10]; print(best)
