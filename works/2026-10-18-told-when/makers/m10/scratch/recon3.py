from PIL import Image
import json,sys
im=Image.open('/tmp/claude-0/s135/mk/m10/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
N=1464;K=18
yc=[5.5+4.588*k for k in range(K)]
B=[[max(255-p[x,y] for y in range(int(round(yc[k]))-1,int(round(yc[k]))+2))/255.0 for x in range(W)] for k in range(K)]
x0=float(sys.argv[1]);x1=float(sys.argv[2])
X=[x0+i*(x1-x0)/(N-1) for i in range(N)]
TH=0.45
dark={(k,x) for k in range(K) for x in range(W) if B[k][x]>TH}
def cellsof(i): 
    x=X[i]; return [c for c in (int(x),int(x)+1) if 0<=c<W]
Wt={c:1.0 for c in dark}
def run(lam):
    prev=None;bps=[]
    for i in range(N):
        cs=cellsof(i)
        e=[]
        for k in range(K):
            ds=[B[k][x] for x in cs]
            if max(ds)<0.3: e.append(4.0);continue
            e.append(-sum(Wt.get((k,x),0) for x in cs))
        if prev is None: prev=e;bps.append([0]*K);continue
        cur=[0]*K;bp=[0]*K
        for k in range(K):
            best=1e9;bj=0
            for j in range(K):
                v=prev[j]+lam*abs(j-k)+(0 if abs(j-k)<=4 else 3)
                if v<best:best=v;bj=j
            cur[k]=best+e[k];bp[k]=bj
        prev=cur;bps.append(bp)
    k=min(range(K),key=lambda k:prev[k]);seq=[0]*N
    for i in range(N-1,-1,-1): seq[i]=k;k=bps[i][k]
    return seq
best=None
for it in range(12):
    seq=run(0.05)
    cov=set((k,x) for i,k in enumerate(seq) for x in cellsof(i))
    un=dark-cov; fp=sum(1 for c in cov if B[c[0]][c[1]]<0.3)
    if best is None or len(un)+fp<best[0]: best=(len(un)+fp,seq)
    print(it,len(dark),len(un),fp)
    for c in un: Wt[c]*=2
    for c in cov&dark: Wt[c]=max(0.2,Wt[c]*0.6)
json.dump([K-1-s for s in best[1]],open('vals3.json','w'))
