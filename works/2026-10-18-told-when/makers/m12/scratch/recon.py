from PIL import Image
import json,sys,math
im=Image.open(sys.argv[1]).convert('L'); p=im.load()
W,H=im.size
N=1464
x0,x1=3.0,297.0
k=(x1-x0)/(N-1)
Y=[5.5+j*(78/17) for j in range(18)]   # j=0 top
def dark(x,y):
    if 0<=x<W and 0<=y<H: return (255-p[x,y])/255
    return 0
def em(i,lev):
    c=x0+i*k; yc=Y[17-lev]
    xs=[int(math.floor(c-0.5)),int(math.floor(c+0.5))]
    ys=[int(math.floor(yc-0.5)),int(math.floor(yc+0.5))]
    return sum(dark(x,y) for x in xs for y in ys)/4
lam=float(sys.argv[2]) if len(sys.argv)>2 else 0.6
INF=1e9
cost=[[-3*em(0,l) for l in range(18)]]; back=[]
for i in range(1,N):
    e=[-3*em(i,l) for l in range(18)]
    row=[];b=[]
    for l in range(18):
        best=INF;bj=0
        for j in range(18):
            v=cost[-1][j]+lam*abs(l-j)**1.5
            if v<best: best=v;bj=j
        row.append(best+e[l]);b.append(bj)
    cost.append(row);back.append(b)
l=min(range(18),key=lambda j:cost[-1][j]); path=[l]
for i in range(N-2,-1,-1):
    l=back[i][l]; path.append(l)
path=path[::-1]
# coverage check vs original lit pixels
lit=set()
for x in range(W):
    for j,yc in enumerate(Y):
        if max(dark(x,y) for y in (int(yc-0.5),int(yc+0.5)))>0.35: lit.add((x,17-j))
cov=set()
for i,lv in enumerate(path):
    c=x0+i*k
    for x in (int(math.floor(c-0.5)),int(math.floor(c+0.5))): cov.add((x,lv))
print('lit',len(lit),'covered',len(lit&cov),'false',len(cov-lit),file=sys.stderr)
json.dump(path,open('hourly.json','w'))
