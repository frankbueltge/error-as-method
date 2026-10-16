from PIL import Image, ImageDraw
import json
im=Image.open('/tmp/claude-0/s130/mk/m18/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
N=1464; x0,x1=2.3,296.7   # approx centers of first/last dot
ink=[[max(0,200-px[x,y])/200.0 for y in range(H)] for x in range(W)]
def inkat(xf,y):
    xa=int(xf); f=xf-xa
    a=ink[xa][y]; b=ink[min(W-1,xa+1)][y]
    return a*(1-f)+b*f
Y=range(15,88)
lam=0.0008
INF=1e18
cost=[];back=[]
prev=None
for i in range(N):
    xf=x0+i*(x1-x0)/(N-1)
    c={y:-inkat(xf,y)-0.5*(inkat(xf,y-1)+inkat(xf,y+1))*0.5 for y in Y}
    if prev is None:
        cur=c; bk={y:None for y in Y}
    else:
        cur={};bk={}
        for y in Y:
            best=INF;by=None
            for yp in range(max(15,y-25),min(87,y+25)+1):
                v=prev[yp]+lam*(y-yp)**2
                if v<best: best=v;by=yp
            cur[y]=best+c[y]; bk[y]=by
    back.append(bk); prev=cur
y=min(prev,key=prev.get); path=[y]
for i in range(N-1,0,-1):
    y=back[i][y]; path.append(y)
path=path[::-1]
json.dump(path,open('/tmp/claude-0/s130/mk/m18/scratch/path_0.0008.json','w'))
# redraw
out=Image.new('L',(W,H),255); d=ImageDraw.Draw(out)
for i,y in enumerate(path):
    xf=x0+i*(x1-x0)/(N-1); d.point((round(xf),y),0)
big=Image.new('L',(W,H*2+4),128); big.paste(im,(0,0)); big.paste(out,(0,H+4))
big.resize((W*3,(H*2+4)*3),Image.NEAREST).save('/tmp/claude-0/s130/mk/m18/scratch/compare_0.0008.png')
print(min(path),max(path))
