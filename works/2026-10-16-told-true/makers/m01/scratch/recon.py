from PIL import Image
import json
im=Image.open('/tmp/claude-0/s130/mk/m01/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
D=[[255-px[x,y] for y in range(H)] for x in range(W)]
print('edge ink',[sum(D[x]) for x in (1,2,3,295,296,297,298)])
N=1464
a,b=2.3,(297.4-2.3)/(N-1)
cols={}
for i in range(N):
    x=int(round(a+i*b)); cols.setdefault(x,[]).append(i)
thr=75
def runs(x):
    r=[];cur=None
    for y in range(H):
        if D[x][y]>=thr:
            if cur is None: cur=[y,y]
            else: cur[1]=y
        else:
            if cur: r.append(cur); cur=None
    if cur: r.append(cur)
    return r
colmean={}
for x in cols:
    ys=[(y,D[x][y]) for y in range(H) if D[x][y]>=thr]
    colmean[x]=sum(y*w for y,w in ys)/sum(w for y,w in ys) if ys else None
vals=[None]*N
deficit=0
for x,hrs in sorted(cols.items()):
    n=len(hrs); r=runs(x)
    if not r: continue
    # allocate
    if len(r)>n:
        r=sorted(r,key=lambda s:-(s[1]-s[0]+1)*max(D[x][s[0]:s[1]+1]))[:n]
    alloc=[1]*len(r); rest=n-len(r)
    L=[s[1]-s[0]+1 for s in r]
    for _ in range(rest):
        k=max(range(len(r)),key=lambda j:L[j]/alloc[j]); alloc[k]+=1
    ys=[]
    for s,k in zip(r,alloc):
        if k==1: ys.append((s[0]+s[1])/2)
        else: ys+= [s[0]+(s[1]-s[0])*j/(k-1) for j in range(k)]
    # order: going toward next column's mean
    nxt=colmean.get(x+1); prv=colmean.get(x-1)
    trend=(nxt if nxt is not None else colmean[x])-(prv if prv is not None else colmean[x])
    ys.sort(reverse=(trend<0))  # trend<0: next higher(smaller y) -> want descending y
    for i,y in zip(hrs,ys): vals[i]=y
miss=[i for i,v in enumerate(vals) if v is None]
print('missing',len(miss),miss[:20])
for i in miss:
    vals[i]=vals[i-1] if i else vals[i+1]
v=[round(88-y,1) for y in vals]
print(min(v),max(v))
json.dump(v,open('series.json','w'))
