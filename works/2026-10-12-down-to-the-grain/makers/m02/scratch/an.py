import json,math
v=json.load(open('/tmp/claude-0/s122/mk/m02/scratch/series.json'))['v']; m=len(v)
def fit(periods,data,idx=None):
    # least squares with constant + cos/sin for each period, simple normal eq via gaussian elim
    idx=idx or range(len(data))
    cols=lambda t:[1.0]+sum(([math.cos(2*math.pi*t/P),math.sin(2*math.pi*t/P)] for P in periods),[])
    k=1+2*len(periods); A=[[0]*k for _ in range(k)]; b=[0]*k
    for t in idx:
        c=cols(t)
        for i in range(k):
            b[i]+=c[i]*data[t]
            for j in range(k): A[i][j]+=c[i]*c[j]
    # solve
    M=[A[i]+[b[i]] for i in range(k)]
    for i in range(k):
        p=max(range(i,k),key=lambda r:abs(M[r][i])); M[i],M[p]=M[p],M[i]
        for r in range(k):
            if r!=i:
                f=M[r][i]/M[i][i]; M[r]=[a-f*q for a,q in zip(M[r],M[i])]
    x=[M[i][k]/M[i][i] for i in range(k)]
    res=sum((data[t]-sum(a*q for a,q in zip(cols(t),x)))**2 for t in idx)
    return x,res
best=min(((fit([P],v)[1],P) for P in [12+0.02*i for i in range(50)]))
print('best single',best)
consts={'M2':12.4206,'S2':12.0,'N2':12.6583,'K1':23.9345,'O1':25.8193,'K2':11.967,'M4':6.2103}
x,res=fit(list(consts.values()),v)
tot=sum((a-sum(v)/m)**2 for a in v)
print('R2',1-res/tot)
for i,(k,P) in enumerate(consts.items()):
    a,b=x[1+2*i],x[2+2*i]; print(k,round(math.hypot(a,b),2),round(math.degrees(math.atan2(b,a))))
print('mean',x[0], 'std',math.sqrt(tot/m))
# daily means & ranges
for d in range(61):
    s=v[d*24:(d+1)*24]; print(d,round(sum(s)/24,1),round(max(s)-min(s),1),end=' | ')

print()
P=list(consts.values())
pred=lambda t: x[0]+sum(x[1+2*i]*math.cos(2*math.pi*t/p)+x[2+2*i]*math.sin(2*math.pi*t/p) for i,p in enumerate(P))
r=[v[t]-pred(t) for t in range(m)]
json.dump({'v':v,'pred':[pred(t) for t in range(m)],'res':r},open('/tmp/claude-0/s122/mk/m02/scratch/fit.json','w'))
for t in range(1020,1130): print(t, round(v[t]+250), round(pred(t)+250), round(r[t]))
# 25h running mean of residual per 12h
print([round(sum(r[t:t+25])/25) for t in range(0,m-25,12)])
