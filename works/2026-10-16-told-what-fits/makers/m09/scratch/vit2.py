from PIL import Image, ImageFilter; import numpy as np, json, sys
im0=Image.open('/tmp/claude-0/s131/mk/m09/work/record.jpg').convert('L')
a=np.asarray(im0).astype(float)/255
H,W=a.shape; N=1464
x0,x1=2.5,296.5
xs=x0+np.arange(N)*(x1-x0)/(N-1)
def col(x):
    i=int(np.floor(x)); f=x-i
    return a[:,i]*(1-f)+a[:,min(i+1,W-1)]*f
cost=np.array([col(x) for x in xs])  # N x H
mu=float(sys.argv[1]) if len(sys.argv)>1 else 0.02
S=H
yy=np.arange(S)
# state (p=y_{t-1}, c=y_t); next n. acc shape (p,c)
acc=cost[0][None,:]+cost[1][:,None]*0  # placeholder
acc=np.add.outer(cost[0],cost[1])+0.002*np.abs(yy[:,None]-yy[None,:])
bps=[]
for t in range(2,N):
    # new[c,n]=min_p acc[p,c]+mu*(n-2c+p)^2
    acc2=np.empty((S,S)); bp=np.empty((S,S),np.int16)
    for c in range(S):
        sec=(yy[None,:]-2*c+yy[:,None])  # p x n
        m=acc[:,c][:,None]+mu*np.minimum(sec**2,400)
        bp[c]=m.argmin(0); acc2[c]=m.min(0)
    acc=acc2+cost[t][None,:]
    bps.append(bp)
c,n=np.unravel_index(acc.argmin(),acc.shape)
path=[n,c]
for t in range(N-1,1,-1):
    bp=bps[t-2]; p=bp[c,n]; path.append(p); n,c=c,p
path=np.array(path[::-1])
v=90-path
json.dump([int(q) for q in v],open('series2.json','w'))
out=Image.new('L',(W*4,H*4),255);px=out.load()
for t in range(N):
    X=int(xs[t]*4);Y=int(path[t]*4)
    for dx in range(-1,2):
        for dy in range(-1,2):
            if 0<=X+dx<W*4 and 0<=Y+dy<H*4: px[X+dx,Y+dy]=0
out.save('recon2.png')
# fit metric
dark=(a<0.5); hit=np.zeros_like(dark)
for t in range(N): hit[int(path[t]),int(round(xs[t]))]=1
print('mean cost',cost[np.arange(N),path].mean(),'coverage',(dark&hit).sum()/dark.sum())
