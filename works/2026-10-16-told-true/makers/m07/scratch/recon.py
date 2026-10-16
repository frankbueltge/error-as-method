import json
cols=json.load(open('cols.json'))
W=300; N=1464; H=90; X0=2; XW=296
# hours per column
hours=[[] for _ in range(W)]
for t in range(N):
    x=X0+min(XW-1,int((t+0.5)*XW/N)); hours[x].append(t)
def wq(ink,q):
    tot=sum(a for _,a in ink); acc=0
    for y,a in sorted(ink):
        acc+=a
        if acc>=q*tot: return y
    return sorted(ink)[-1][0]
# column mean per x  (value = H - y, bigger higher)
colmean=[]
for c in cols:
    s=sum(a for _,a in c)
    colmean.append(H-sum(y*a for y,a in c)/s if s else None)
# fill gaps
for i,v in enumerate(colmean):
    if v is None and X0<=i<X0+XW:
        nb=[colmean[j] for j in (i-1,i+1) if 0<=j<W and colmean[j] is not None]; colmean[i]=sum(nb)/len(nb)
# mean diurnal profile by hour-of-day from column means minus local mean
def ma(a,k): return [sum(a[max(0,i-k):i+k+1])/len(a[max(0,i-k):i+k+1]) for i in range(len(a))]
colmean=[v if v is not None else 0 for v in colmean]
base=ma(colmean,5)
prof=[0]*24; cnt=[0]*24
for x in range(X0,X0+XW):
    for t in hours[x]:
        prof[t%24]+=colmean[x]-base[x]; cnt[t%24]+=1
prof=[p/c for p,c in zip(prof,cnt)]
print('profile',[round(p,1) for p in prof])
# rank-matched assignment
vals=[0]*N
for x in range(X0,X0+XW):
    hs=hours[x]; k=len(hs)
    c=cols[x] or cols[x-1]
    qs=sorted(H-wq(c,(i+0.5)/k) for i in range(k))
    order=sorted(hs,key=lambda t:prof[t%24])
    for t,v in zip(order,qs): vals[t]=v
json.dump({'vals':vals,'prof':prof},open('recon.json','w'))
print(min(vals),max(vals))
# daily stats
for d in range(61):
    day=vals[d*24:(d+1)*24]
    print(d, round(min(day)),round(sum(day)/24,1),round(max(day)))
