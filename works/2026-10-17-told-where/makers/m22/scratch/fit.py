from PIL import Image
import json, math, sys
im=Image.open('/tmp/claude-0/s133/mk/m22/work/record.jpg').convert('L')
W,H=im.size;px=im.load()
D=[[max(0,255-px[x,y]) for x in range(W)] for y in range(H)]
N=1464
X0=float(sys.argv[1]) if len(sys.argv)>1 else 2.25
X1=float(sys.argv[2]) if len(sys.argv)>2 else 296.8
R=0.8;C=200.0;BASE=83.6
dx=(X1-X0)/(N-1)
xs=[X0+i*dx for i in range(N)]
# coverage kernel for center c (x,y): dict pixel->cov
SS=8
def kernel(cx,cy):
    out={}
    for p in range(math.floor(cx-R-0.5),math.ceil(cx+R+0.5)+1):
        for q in range(math.floor(cy-R-0.5),math.ceil(cy+R+0.5)+1):
            n=0
            for a in range(SS):
                for b in range(SS):
                    u=p-0.5+(a+0.5)/SS; v=q-0.5+(b+0.5)/SS
                    if (u-cx)**2+(v-cy)**2<=R*R: n+=1
            if n: out[(p,q)]=n/(SS*SS)*C
    return out
kcache={}
def K(cx,cy):
    key=(round(cx*10),round(cy*4))
    if key not in kcache: kcache[key]=kernel(key[0]/10,key[1]/4)
    return kcache[key]
M=[[0.0]*W for _ in range(H)]
def add(k,s):
    for (p,q),c in k.items():
        if 0<=p<W and 0<=q<H: M[q][p]+=s*c
def err_patch(pix):
    e=0.0
    for (p,q) in pix:
        if 0<=p<W and 0<=q<H:
            d=min(255.0,M[q][p])-D[q][p]; e+=d*d
    return e
ys=[BASE]*N
for i in range(N): add(K(xs[i],ys[i]),1)
cands=[BASE]+[y/4 for y in range(0,int(83*4))]
LAM=float(sys.argv[3]) if len(sys.argv)>3 else 0.5
for sweep in range(8):
    moved=0
    order=list(range(N))
    if sweep%2: order.reverse()
    for i in order:
        k0=K(xs[i],ys[i]); add(k0,-1)
        nb=[ys[j] for j in (i-1,i+1) if 0<=j<N]
        best=None
        for y in cands:
            k=K(xs[i],y)
            pix=set(k)|set(k0)
            # error with dot at y minus without, on union patch
            e0=err_patch(pix); add(k,1); e1=err_patch(pix); add(k,-1)
            reg=LAM*sum(min((y-z)**2,400) for z in nb)
            sc=e1-e0+reg
            if best is None or sc<best[0]: best=(sc,y)
        if best[1]!=ys[i]: moved+=1
        ys[i]=best[1]; add(K(xs[i],ys[i]),1)
    tot=sum((min(255,M[q][p])-D[q][p])**2 for q in range(H) for p in range(W))
    print('sweep',sweep,'moved',moved,'err',round(tot),flush=True)
json.dump(dict(X0=X0,X1=X1,ys=ys),open('fit_%s_%s_%s.json'%(X0,X1,LAM),'w'))
