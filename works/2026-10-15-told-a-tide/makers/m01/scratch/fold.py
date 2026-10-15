from PIL import Image
im=Image.open('/tmp/claude-0/s128/mk/m01/work/record.jpg').convert('L'); p=im.load()
W,H=im.size
pts=[]
for x in range(W):
    for y in range(H):
        w=max(0,170-p[x,y])
        if w>0: pts.append((x,y,w))
# baseline: weighted median y within +-7 px
import bisect
def wmed(vals):
    vals=sorted(vals); tot=sum(w for y,w in vals); c=0
    for y,w in vals:
        c+=w
        if c>=tot/2: return y
base={}
for x in range(W):
    v=[(y,w) for xx,y,w in pts if abs(xx-x)<=7]
    base[x]=wmed(v) if v else 0
x0,x1=2.0,297.0
hpp=1464/(x1-x0)
import collections
B=collections.defaultdict(list)
for x,y,w in pts:
    t=(x+0.5-x0)*hpp
    ph=int(t%24)
    B[ph].append((base[x]-y,w))
for ph in range(24):
    v=B[ph]; tot=sum(w for d,w in v)
    m=sum(d*w for d,w in v)/tot
    md=wmed(v)
    low=sum(w for d,w in v if d<-8)/tot
    print(ph, round(m,1), md, round(low,2))
