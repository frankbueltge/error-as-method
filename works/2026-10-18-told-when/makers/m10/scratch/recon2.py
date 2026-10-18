from PIL import Image
import json
im=Image.open('/tmp/claude-0/s135/mk/m10/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
N=1464;K=18
yc=[5.5+4.588*k for k in range(K)]
def band(k,x):
    y0=int(round(yc[k]))
    return max(255-p[x,y] for y in range(y0-1,y0+2))/255.0
B=[[band(k,x) for x in range(W)] for k in range(K)]
x0,x1=0.0,298.0
X=[x0+i*(x1-x0)/(N-1) for i in range(N)]
def cells(xf):
    x=int(round(xf)); return [c for c in (x,x+1) if 0<=c<W]
# Wt: weight per dark cell (bonus for covering); start 1
Wt=[[1.0]*W for _ in range(K)]
def run(lam):
    INF=1e9
    prev=None;bps=[]
    for i in range(N):
        e=[]
        for k in range(K):
            cs=cells(X[i]); c=0
            for x in cs:
                d=B[k][x]
                if d<0.25: c+=3.0      # drawing on white: bad
                else: c-=d*Wt[k][x]
            e.append(c)
        if prev is None: prev=e;bps.append([0]*K);continue
        cur=[0]*K;bp=[0]*K
        for k in range(K):
            best=INF;bj=0
            for j in range(max(0,k-3),min(K,k+4)):
                v=prev[j]+lam*abs(j-k)
                if v<best:best=v;bj=j
            cur[k]=best+e[k];bp[k]=bj
        prev=cur;bps.append(bp)
    k=min(range(K),key=lambda k:prev[k]);seq=[0]*N
    for i in range(N-1,-1,-1):
        seq[i]=k;k=bps[i][k]
    return seq
def score(seq):
    cov=set()
    for i,k in enumerate(seq):
        for x in cells(X[i]): cov.add((k,x))
    dark={(k,x) for k in range(K) for x in range(W) if B[k][x]>0.45}
    fp=sum(1 for c in cov if B[c[0]][c[1]]<0.25)
    return len(dark),len(dark-cov),fp,cov,dark
for it in range(8):
    seq=run(0.15)
    nd,nu,fp,cov,dark=score(seq)
    print(it,nd,nu,fp)
    for (k,x) in dark-cov: Wt[k][x]*=2.5
    for (k,x) in cov: Wt[k][x]=max(0.3,Wt[k][x]*0.7)
vals=[K-1-s for s in seq]
json.dump(vals,open('vals2.json','w'))
for d in range(61):
    day=vals[d*24:(d+1)*24]
    print(d, ''.join('%x'%v if v<16 else 'ghi'[v-16] for v in day), min(day),max(day))
out=Image.new('L',(W,H),255);q=out.load()
for i,k in enumerate(seq):
    y=int(round(yc[k]))
    for x in cells(X[i]):
        for dy in(-1,0): q[x,y+dy]=0
out.save('recon2.png')
