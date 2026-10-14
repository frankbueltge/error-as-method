import json,sys
from PIL import Image
im=Image.open('/tmp/claude-0/s124/mk/m02/work/record.jpg').convert('L')
W,H=im.size;px=im.load()
D=[[max(0,255-px[x,y])/255 for y in range(H)] for x in range(W)]
N=1464
x0=float(sys.argv[1]) if len(sys.argv)>1 else 2.6
x1=float(sys.argv[2]) if len(sys.argv)>2 else 296.4
lam=float(sys.argv[3]) if len(sys.argv)>3 else 0.004
S=2 # substeps per px
Y=[k/S for k in range(H*S)]
def dark(x,y):
    # bilinear
    xi=int(x); yi=int(y); fx=x-xi; fy=y-yi
    v=0
    for dx,wx in ((0,1-fx),(1,fx)):
        for dy,wy in ((0,1-fy),(1,fy)):
            X=min(W-1,xi+dx);Yy=min(H-1,yi+dy)
            v+=wx*wy*D[X][Yy]
    return v
xs=[x0+i*(x1-x0)/(N-1) for i in range(N)]
M=len(Y);R=24*S
cost=[-dark(xs[0],y) for y in Y]
back=[]
for i in range(1,N):
    loc=[-dark(xs[i],y) for y in Y]
    nc=[0]*M;bk=[0]*M
    for k in range(M):
        best=1e9;bj=k
        for j in range(max(0,k-R),min(M,k+R+1)):
            c=cost[j]+lam*(j-k)**2/S/S
            if c<best:best=c;bj=j
        nc[k]=best+loc[k];bk[k]=bj
    cost=nc;back.append(bk)
k=min(range(M),key=lambda k:cost[k])
path=[k]
for bk in reversed(back):
    k=bk[k];path.append(k)
path.reverse()
ys=[Y[k] for k in path]
json.dump({'x':xs,'y':ys},open('recon.json','w'))
# evaluation: render and compare
from PIL import ImageDraw
out=Image.new('L',(W,H),255);dr=ImageDraw.Draw(out)
for x,y in zip(xs,ys): dr.ellipse([x-1,y-1,x+1,y+1],fill=40)
out.save('recon.png')
# coverage
op=out.load()
ink=[(x,y) for x in range(W) for y in range(H) if px[x,y]<110]
cov=sum(1 for x,y in ink if any(op[min(W-1,max(0,x+a)),min(H-1,max(0,y+b))]<128 for a in (-1,0,1) for b in (-1,0,1)))
print('ink covered',cov/len(ink), 'mean dark at pts',sum(dark(x,y) for x,y in zip(xs,ys))/N)
