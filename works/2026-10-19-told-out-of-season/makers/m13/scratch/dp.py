from PIL import Image, ImageFilter
import json, math
im=Image.open('/tmp/claude-0/s137/mk/m13/work/record.jpg').convert('L')
W,H=im.size
p=im.load()
def dark(x,y):
    # bilinear darkness 0..1
    x0=int(math.floor(x)); y0=int(math.floor(y)); fx=x-x0; fy=y-y0
    s=0
    for dx,wx in ((0,1-fx),(1,fx)):
        for dy,wy in ((0,1-fy),(1,fy)):
            xx=min(max(x0+dx,0),W-1); yy=min(max(y0+dy,0),H-1)
            s+=wx*wy*(255-p[xx,yy])/255
    return s
N=1464; X0=2.4; X1=297.4
xs=[X0+(X1-X0)*t/(N-1) for t in range(N)]
R=2  # states per pixel
ys=[i/R for i in range(0,H*R)]
S=len(ys)
lam=0.04; maxj=45*R
INF=1e18
cost=[[1-dark(xs[t]-0.0,y) for y in ys] for t in range(N)]
prev=cost[0][:]; back=[]
for t in range(1,N):
    cur=[INF]*S; bk=[0]*S
    c=cost[t]
    for j in range(S):
        best=INF;bi=0
        lo=max(0,j-maxj); hi=min(S,j+maxj+1)
        for i in range(lo,hi):
            v=prev[i]+lam*abs(i-j)/R
            if v<best: best=v;bi=i
        cur[j]=best+c[j]; bk[j]=bi
    back.append(bk); prev=cur
j=min(range(S),key=lambda k:prev[k]); path=[j]
for t in range(N-2,-1,-1):
    j=back[t][j]; path.append(j)
path.reverse()
vals=[ys[j] for j in path]
json.dump(vals,open('series_y.json','w'))
# render check
out=Image.new('L',(W*4,H*4),255)
from PIL import ImageDraw
d=ImageDraw.Draw(out)
for t,y in enumerate(vals):
    d.ellipse([xs[t]*4-2,y*4-2,xs[t]*4+2,y*4+2],fill=0)
out.save('recon.png')
im.resize((W*4,H*4)).save('orig4.png')
