import sys, json, math
from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m24/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
D=[[max(0,255-p[x,y])/255 for x in range(W)] for y in range(H)]
N=1464; S=4.81980/24
R=float(sys.argv[2]) if len(sys.argv)>2 else 0.85; OP=0.92
SS=6
cache={}
def patch(cx,cy):
    # coverage of disk radius R centred (cx,cy) in pixel grid (pixel x covers [x,x+1))
    key=(round(cx*8),round(cy*8))
    if key in cache: return cache[key]
    cx=key[0]/8; cy=key[1]/8
    out=[]
    for px in range(int(math.floor(cx-R)),int(math.floor(cx+R))+1):
        for py in range(int(math.floor(cy-R)),int(math.floor(cy+R))+1):
            c=0
            for i in range(SS):
                for j in range(SS):
                    sx=px+(i+.5)/SS; sy=py+(j+.5)/SS
                    if (sx-cx)**2+(sy-cy)**2<=R*R: c+=1
            if c and 0<=px<W and 0<=py<H: out.append((px,py,OP*c/SS/SS))
    cache[key]=out; return out
def run(x0, sweeps=8, lam=float(sys.argv[3]) if len(sys.argv)>3 else 2e-5, verbose=False):
    xs=[x0+i*S for i in range(N)]
    # init: column darkest-weighted mean? start at baseline
    ys=[]
    for k in range(N):
        cx=int(xs[k]); col=[(D[y][cx],y) for y in range(H)]
        tot=sum(a for a,_ in col)
        # hours in this column
        ks=[j for j in range(N) if int(xs[j])==cx]
        q=(ks.index(k)+0.5)/len(ks)
        acc=0; yy=84.0
        for a,y in sorted(col,key=lambda t:t[1]):
            acc+=a
            if acc>=q*tot: yy=y+0.5; break
        ys.append(yy)
    # transmittance log-sum: T = prod(1-a)
    L=[[0.0]*W for _ in range(H)]  # sum log(1-a)
    def add(k,sign):
        for px,py,a in patch(xs[k],ys[k]):
            L[py][px]+=sign*math.log(1-a)
    for k in range(N): add(k,1)
    cands=[c/4 for c in range(4*2,4*87)]
    def err_at(pts):
        return sum((1-math.exp(L[py][px])-D[py][px])**2 for px,py in pts)
    for sw in range(sweeps):
        order=range(N) if sw%2==0 else range(N-1,-1,-1)
        moved=0
        for k in order:
            add(k,-1)
            best=None
            for c in cands:
                pt=patch(xs[k],c)
                # error delta for adding this dot
                d=0
                for px,py,a in pt:
                    m0=1-math.exp(L[py][px]); m1=1-math.exp(L[py][px]+math.log(1-a))
                    t=D[py][px]
                    d+=(m1-t)**2-(m0-t)**2
                sm=0
                if k>0: sm+=(c-ys[k-1])**2
                if k<N-1: sm+=(c-ys[k+1])**2
                d+=lam*sm
                if best is None or d<best[0]: best=(d,c)
            if best[1]!=ys[k]: moved+=1
            ys[k]=best[1]; add(k,1)
        tot=sum((1-math.exp(L[y][x])-D[y][x])**2 for y in range(H) for x in range(W))
        if verbose: print('sweep',sw,'moved',moved,'err',round(tot,2),flush=True)
    return xs,ys,tot
if __name__=='__main__':
    x0=float(sys.argv[1])
    xs,ys,tot=run(x0,verbose=True)
    json.dump({'x0':x0,'R':R,'ys':ys,'err':tot},open('fit_%s_%s.json'%(x0,R),'w'))
    print('final',x0,R,tot)
