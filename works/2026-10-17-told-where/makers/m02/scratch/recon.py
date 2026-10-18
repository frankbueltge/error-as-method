import math, json, sys
from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m02/work/record.jpg').convert('L')
W,H=im.size;px=im.load()
D=[[ (255-px[x,y])/255.0 for x in range(W)] for y in range(H)]
N=1464
S=0.6
def kern(dx,dy): return 0.97*math.exp(-(dx*dx+dy*dy)/(2*S*S))
def run(a,b,passes=6,verbose=False):
    xs=[a+b*i for i in range(N)]
    # transmission T = prod(1-c)
    T=[[1.0]*W for _ in range(H)]
    ys=[None]*N
    def patch(x,y):
        out=[]
        for yy in range(max(0,int(y)-2),min(H,int(y)+4)):
            for xx in range(max(0,int(x)-2),min(W,int(x)+4)):
                c=kern(xx-x,yy-y)
                if c>0.01: out.append((xx,yy,c))
        return out
    def apply(i,sign):
        for xx,yy,c in patch(xs[i],ys[i]):
            if sign>0: T[yy][xx]*=(1-c)
            else: T[yy][xx]/=(1-c)
    cand=[5+0.25*k for k in range(int((84-5)/0.25)+1)]
    for p in range(passes):
        changed=0
        for i in range(N):
            if ys[i] is not None: apply(i,-1)
            x=xs[i]; best=None;by=None
            # region columns
            x0=max(0,int(x)-2);x1=min(W,int(x)+4)
            # error baseline = sum over region columns all rows of (D-(1-T))^2 ; compute delta only in patch
            for y in cand:
                e=0.0
                for xx,yy,c in patch(x,y):
                    t=T[yy][xx]; old=(D[yy][xx]-(1-t))**2; new=(D[yy][xx]-(1-t*(1-c)))**2
                    e+=new-old
                if best is None or e<best: best=e;by=y
            if ys[i]!=by: changed+=1
            ys[i]=by; apply(i,1)
        err=sum((D[y][x]-(1-T[y][x]))**2 for y in range(H) for x in range(W))
        if verbose: print('pass',p,'changed',changed,'err',round(err,2),file=sys.stderr)
    return ys,err
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='scan':
        for a in [2.6,2.9,3.2,3.5]:
            for b in [0.2005,0.20096,0.2014]:
                ys,err=run(a,b,passes=2)
                print(a,b,round(err,2),flush=True)
    else:
        a=float(sys.argv[2]);b=float(sys.argv[3])
        ys,err=run(a,b,passes=8,verbose=True)
        json.dump({'a':a,'b':b,'ys':ys},open('/tmp/claude-0/s133/mk/m02/scratch/recon.json','w'))
