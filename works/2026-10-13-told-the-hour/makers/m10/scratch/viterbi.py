from PIL import Image
import json, sys
im=Image.open('/tmp/claude-0/s123/mk/m10/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
ink=[[max(0,255-px[x,y]-20)/235 for y in range(H)] for x in range(W)]
N=1464
x0,x1=float(sys.argv[1]),float(sys.argv[2]); lam=float(sys.argv[3])
def em(xf,y):
    s=0
    for dx in (-1,0,1):
        x=int(round(xf))+dx
        if 0<=x<W:
            w=1.0 if dx==0 else 0.35
            for dy in (-1,0,1):
                yy=y+dy
                if 0<=yy<H: s+=w*ink[x][yy]*(1.0 if dy==0 else 0.5)
    return s
xs=[x0+i*(x1-x0)/(N-1) for i in range(N)]
E=[[em(xs[i],y) for y in range(H)] for i in range(N)]
INF=-1e18
score=E[0][:]; back=[]
for i in range(1,N):
    ns=[INF]*H; bk=[0]*H
    for y in range(H):
        best=INF;arg=0
        for yp in range(max(0,y-25),min(H,y+26)):
            v=score[yp]-lam*(y-yp)**2/100
            if v>best: best=v;arg=yp
        ns[y]=best+E[i][y]; bk[y]=arg
    score=ns; back.append(bk)
y=max(range(H),key=lambda k:score[k]); path=[y]
for bk in reversed(back):
    y=bk[y]; path.append(y)
path.reverse()
tot=sum(E[i][path[i]] for i in range(N))
print('total emission',round(tot,1),'mean',round(tot/N,3))
json.dump(path,open(sys.argv[4],'w'))
