from PIL import Image
import json
im=Image.open('/tmp/claude-0/s135/mk/m10/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
N=1464;K=18
yc=[5.5+4.588*k for k in range(K)]
# darkness per level per column: max over band rows
def band(k,x):
    y0=int(round(yc[k]))
    return max(255-p[x,y] for y in range(y0-1,y0+2) if 0<=y<H)
B=[[band(k,x) for x in range(W)] for k in range(K)]
# x position of hour i: plot spans px 0..299, dot ~2px wide, centre range ~1..298
import sys; x0,x1=float(sys.argv[1]),float(sys.argv[2])
def ev(k,xf):
    x=int(xf); f=xf-x
    a=B[k][max(0,min(W-1,x))]; b=B[k][max(0,min(W-1,x+1))]
    return (a*(1-f)+b*f)/255.0
lam=0.35
INF=1e9
cost=[[0]*K for _ in range(N)];bp=[[0]*K for _ in range(N)]
for i in range(N):
    xf=x0+i*(x1-x0)/(N-1)
    e=[-ev(k,xf) for k in range(K)]
    if i==0:
        cost[0]=e;continue
    for k in range(K):
        best=INF;bj=0
        for j in range(K):
            c=cost[i-1][j]+lam*abs(j-k)+ (0 if abs(j-k)<=3 else 5)
            if c<best:best=c;bj=j
        cost[i][k]=best+e[k];bp[i][k]=bj
k=min(range(K),key=lambda k:cost[N-1][k])
seq=[0]*N
for i in range(N-1,-1,-1):
    seq[i]=k;k=bp[i][k]
vals=[K-1-s for s in seq]  # 0=lowest,17=highest
json.dump(vals,open('vals.json','w'))
# re-render to compare
out=Image.new('L',(W,H),255);q=out.load()
for i,v in enumerate(vals):
    xf=x0+i*(x1-x0)/(N-1); y=int(round(yc[K-1-v]))
    for dx in (0,1):
        for dy in (-1,0):
            xx=int(xf)+dx
            if 0<=xx<W:q[xx,y+dy]=0
out.save('recon.png')
# coverage check: dark pixels in original not explained
miss=0;tot=0
for k in range(K):
    for x in range(W):
        if B[k][x]>120:
            tot+=1
            y=int(round(yc[k]))
            if q[x,y]>128 and q[x,y-1]>128: miss+=1
print('dark cells',tot,'unexplained',miss)
for d in range(61):
    day=vals[d*24:(d+1)*24]
    print(d, ''.join('%x'%v if v<16 else 'ghi'[v-16] for v in day), min(day),max(day))
