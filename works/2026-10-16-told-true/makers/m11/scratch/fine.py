from PIL import Image
import math
im=Image.open('/tmp/claude-0/s130/mk/m11/work/record.jpg').convert('L'); p=im.load()
W,H=im.size
d=[[max(0,255-p[x,y]-15) for y in range(H)] for x in range(W)]
xs=[x for x in range(W) if sum(d[x])>0]
cen={x:sum(y*c for y,c in enumerate(d[x]))/sum(d[x]) for x in xs if sum(d[x])>300}
# time per px: assume values i=0..1463 at x = x0 + i*(x1-x0)/1463
x0,x1=3.0,296.0
hpp=1463/(x1-x0)
print('h/px',hpp)
X=sorted(cen); m=sum(cen[x] for x in X)/len(X)
res=[]
f=0.80
while f<2.2:
    re=sum((cen[x]-m)*math.cos(2*math.pi*f*(x-x0)*hpp/24) for x in X)
    im_=sum((cen[x]-m)*math.sin(2*math.pi*f*(x-x0)*hpp/24) for x in X)
    res.append((f,math.hypot(re,im_)))
    f+=0.005
for f,a in res:
    print('%.3f cpd %6.1f h %s'%(f,24/f,'#'*int(a/15)))
