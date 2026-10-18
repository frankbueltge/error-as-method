from PIL import Image
import json,random
im=Image.open('/tmp/claude-0/s135/mk/m10/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
N=1464;K=18
yc=[5.5+4.588*k for k in range(K)]
B=[[max(255-p[x,y] for y in range(int(round(yc[k]))-1,int(round(yc[k]))+2))/255.0 for x in range(W)] for k in range(K)]
import sys; x0,x1=float(sys.argv[1]),float(sys.argv[2])
X=[x0+i*(x1-x0)/(N-1) for i in range(N)]
def cellsof(i):
    x=X[i]; return [c for c in (int(x),int(x)+1) if 0<=c<W]
dark={(k,x) for k in range(K) for x in range(W) if B[k][x]>0.45}
def ok(k,i): return max(B[k][x] for x in cellsof(i))>=0.3
seq=[17-v for v in json.load(open('vals.json'))]  # smooth DP start
from collections import Counter
def covcount(seq):
    c=Counter()
    for i,k in enumerate(seq):
        for x in cellsof(i): c[(k,x)]+=1
    return c
cc=covcount(seq)
def jumps(seq,i):
    s=0
    for j in (i-1,i+1):
        if 0<=j<N: s+=abs(seq[i]-seq[j])
    return s
random.seed(1)
for sweep in range(60):
    un=[c for c in dark if cc[c]==0]
    random.shuffle(un);changed=0
    for (k,x) in un:
        if cc[(k,x)]>0: continue
        cands=[i for i in range(N) if x in cellsof(i)]
        best=None
        for i in cands:
            old=seq[i]
            # removing old must not uncover a dark cell
            lose=any(cc[(old,xx)]==1 and (old,xx) in dark for xx in cellsof(i))
            if lose: continue
            if any(B[k][xx]<0.3 for xx in cellsof(i)) and sweep<30: continue
            seq[i]=k; jcost=jumps(seq,i); seq[i]=old
            if jcost>8: continue
            if best is None or jcost<best[0]: best=(jcost,i)
        if best:
            i=best[1]; old=seq[i]
            for xx in cellsof(i): cc[(old,xx)]-=1; cc[(k,xx)]+=1
            seq[i]=k;changed+=1
    un=[c for c in dark if cc[c]==0]
    fp=sum(1 for c,v in cc.items() if v>0 and B[c[0]][c[1]]<0.3)
    if sweep%10==0 or changed==0: print(sweep,len(un),fp,changed)
    if changed==0 and sweep>30: break
vals=[17-s for s in seq]
json.dump(vals,open('vals4.json','w'))
for d in range(61):
    day=vals[d*24:(d+1)*24]
    print(d, ''.join('%x'%v if v<16 else 'ghi'[v-16] for v in day), min(day),max(day))
out=Image.new('L',(W,H),255);q=out.load()
for i,k in enumerate(seq):
    y=int(round(yc[k]))
    for x in cellsof(i):
        for dy in(-1,0): q[x,y+dy]=0
out.save('recon4.png')
