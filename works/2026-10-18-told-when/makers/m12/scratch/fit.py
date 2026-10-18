from PIL import Image
import json,sys,math
im=Image.open(sys.argv[1]).convert('L'); p=im.load()
W,H=im.size; N=1464
T=[[(255-p[x,y])/255 for y in range(H)] for x in range(W)]
Y=[5.5+j*(78/17) for j in range(18)]
R=float(sys.argv[3]) if len(sys.argv)>3 else 1.0
A=float(sys.argv[4]) if len(sys.argv)>4 else 0.85
def footprint(cx,cy):
    out={}
    S=6
    for x in range(int(cx-R-1),int(cx+R+2)):
        for y in range(int(cy-R-1),int(cy+R+2)):
            n=0
            for a in range(S):
                for b in range(S):
                    px=x-0.5+(a+0.5)/S; py=y-0.5+(b+0.5)/S
                    if (px-cx)**2+(py-cy)**2<=R*R: n+=1
            if n: out[(x,y)]=A*n/(S*S)
    return out
def run(x0,x1,iters=6,init=None):
    k=(x1-x0)/(N-1)
    FP=[[footprint(x0+i*k,Y[17-l]) for l in range(18)] for i in range(N)]
    path=init[:] if init else [9]*N
    if not init:
        # init: per hour level with max local darkness
        for i in range(N):
            path[i]=max(range(18),key=lambda l:sum(T[x][y] for (x,y) in FP[i][l] if 0<=x<W and 0<=y<H))
    # transparency product per pixel
    Q=[[1.0]*H for _ in range(W)]
    for i,l in enumerate(path):
        for (x,y),a in FP[i][l].items():
            if 0<=x<W and 0<=y<H: Q[x][y]*=(1-a)
    def err_local(pix):
        return sum(((1-Q[x][y])-T[x][y])**2 for (x,y) in pix)
    for it in range(iters):
        ch=0
        for i in range(N):
            cur=path[i]
            # remove
            for (x,y),a in FP[i][cur].items():
                if 0<=x<W and 0<=y<H: Q[x][y]/=(1-a)
            best=None
            for l in range(18):
                pix=[(x,y) for (x,y) in FP[i][l] if 0<=x<W and 0<=y<H]
                before=err_local(pix)
                after=sum(((1-Q[x][y]*(1-FP[i][l][(x,y)]))-T[x][y])**2 for (x,y) in pix)
                d=after-before
                if best is None or d<best[0]-1e-12: best=(d,l)
            l=best[1]
            if l!=cur: ch+=1
            path[i]=l
            for (x,y),a in FP[i][l].items():
                if 0<=x<W and 0<=y<H: Q[x][y]*=(1-a)
        tot=sum(((1-Q[x][y])-T[x][y])**2 for x in range(W) for y in range(H))
        print(x0,x1,'iter',it,'changes',ch,'err %.2f'%tot,file=sys.stderr)
        if ch==0: break
    return path,tot,Q
x0=float(sys.argv[2].split(',')[0]); x1=float(sys.argv[2].split(',')[1])
path,tot,Q=run(x0,x1)
json.dump(path,open('fit_%s_%s.json'%(x0,x1),'w'))
img=Image.new('L',(W,H))
for x in range(W):
    for y in range(H): img.putpixel((x,y),int(255*Q[x][y]))
img.save('render_%s_%s.png'%(x0,x1))
print('FINAL',x0,x1,R,A,round(tot,2))
