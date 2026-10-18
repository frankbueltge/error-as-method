import math, json, sys
d=open('rec.raw','rb').read(); W,H=300,90
img=[[ (255-d[y*W+x])/255 for x in range(W)] for y in range(H)]
N=1464; NL=18
X0=float(sys.argv[1]) if len(sys.argv)>1 else 3.0
X1=float(sys.argv[2]) if len(sys.argv)>2 else 296.0
R=float(sys.argv[3]) if len(sys.argv)>3 else 1.1
A=float(sys.argv[4]) if len(sys.argv)>4 else 0.6
xs=[X0+i*(X1-X0)/(N-1) for i in range(N)]
YOFF=float(sys.argv[5]) if len(sys.argv)>5 else 0.5
yl=[83.5+YOFF-L*78/17 for L in range(NL)]
LS=int(sys.argv[6]) if len(sys.argv)>6 else 1
def samp(x,y):
    x0=int(math.floor(x)); y0=int(math.floor(y)); fx=x-x0; fy=y-y0; s=0
    for dx,wx in ((0,1-fx),(1,fx)):
        for dy,wy in ((0,1-fy),(1,fy)):
            xx,yy=min(W-1,max(0,x0+dx)),min(H-1,max(0,y0+dy)); s+=wx*wy*img[yy][xx]
    return s
# pixel-center coords: pixel (px,py) covers [px,px+1); centre px+0.5. treat x,y as centre coords
E=[[samp(xs[i]-0.5,yl[L]-0.5) for L in range(NL)] for i in range(N)]
INF=1e18; lam=0.35
cost=[[ -E[0][L] for L in range(NL)]]; bp=[]
for i in range(1,N):
    row=[];b=[]
    for L in range(NL):
        best=INF;bl=0
        for M in range(max(0,L-2),min(NL,L+3)):
            c=cost[-1][M]+lam*abs(L-M)**1.5
            if c<best: best=c;bl=M
        row.append(best-E[i][L]); b.append(bl)
    cost.append(row); bp.append(b)
L=min(range(NL),key=lambda l:cost[-1][l]); path=[L]
for i in range(N-2,-1,-1):
    L=bp[i][L]; path.append(L)
path.reverse()
# forward render
def render(path):
    trans=[[1.0]*W for _ in range(H)]
    for i,L in enumerate(path):
        cx,cy=xs[i],yl[L]
        for py in range(int(cy-R-1),int(cy+R+2)):
            for px in range(int(cx-R-1),int(cx+R+2)):
                if 0<=px<W and 0<=py<H:
                    # coverage by 3x3 supersample
                    c=0
                    for sy in (0.17,0.5,0.83):
                        for sx in (0.17,0.5,0.83):
                            if (px+sx-cx)**2+(py+sy-cy)**2<=R*R: c+=1
                    if c: trans[py][px]*=(1-A*c/9)
    return [[1-t for t in r] for r in trans]
def err(r):
    return sum((r[y][x]-img[y][x])**2 for y in range(H) for x in range(W))
r=render(path); e=err(r)
print('viterbi err',e)
# local search
def local_err(path,i0,i1,x_lo,x_hi):
    pass
improved=True; it=0
while LS and improved and it<6:
    improved=False; it+=1; ch=0
    for i in range(N):
        best=path[i]; be=None
        x_lo=int(xs[i]-R-3); x_hi=int(xs[i]+R+4)
        def lerr(p):
            # render only nearby hours
            trans={}
            for j in range(max(0,i-30),min(N,i+31)):
                cx,cy=xs[j],yl[p[j]]
                for py in range(int(cy-R-1),int(cy+R+2)):
                    for px in range(max(x_lo,int(cx-R-1)),min(x_hi,int(cx+R+2))):
                        if 0<=py<H and 0<=px<W:
                            c=0
                            for sy in (0.17,0.5,0.83):
                                for sx in (0.17,0.5,0.83):
                                    if (px+sx-cx)**2+(py+sy-cy)**2<=R*R: c+=1
                            if c: trans[(px,py)]=trans.get((px,py),1.0)*(1-A*c/9)
            s=0
            for px in range(max(0,x_lo),min(W,x_hi)):
                for py in range(H):
                    s+=((1-trans.get((px,py),1.0))-img[py][px])**2
            return s
        be=lerr(path)
        for cand in (path[i]-1,path[i]+1,path[i]-2,path[i]+2):
            if 0<=cand<NL:
                old=path[i]; path[i]=cand; e2=lerr(path); path[i]=old
                if e2<be-1e-9: be=e2; best=cand
        if best!=path[i]: path[i]=best; improved=True; ch+=1
    print('iter',it,'changes',ch, file=sys.stderr)
r=render(path); print('final err',err(r))
json.dump(path,open('series.json','w'))
# write render for comparison
open('render.raw','wb').write(bytes(int(255-255*min(1,v)) for row in r for v in row))
