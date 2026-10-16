from PIL import Image
import math
im=Image.open('/tmp/claude-0/s130/mk/m10/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
f=0.2073; B=10
bins=[[0]*H for _ in range(B)]
for x in range(298):
    ph=((x*f)%1.0); b=int(ph*B)
    for y in range(H):
        bins[b][y]+=max(0,200-p[x,y])
for b in range(B):
    tot=sum(bins[b]); m=sum(y*w for y,w in enumerate(bins[b]))/tot
    cum=0;q=[]
    for y,w in enumerate(bins[b]):
        cum+=w
        for t in (0.1,0.5,0.9):
            if cum>=t*tot and len(q)<[0.1,0.5,0.9].index(t)+1: q.append(y)
    print('phase %.1f mean y %.1f q10/50/90 %s'%(b/B,m,q))
# blobs: local minima detection
pts=[]
for x in range(W):
    for y in range(1,H-1):
        v=p[x,y]
        if v<150 and v<=p[x,y-1] and v<=p[x,y+1]:
            pts.append((x,y,v))
print('n local-min pts',len(pts))
# outliers: points far above column-neighbourhood median
import statistics
for x,y,v in pts:
    nb=[yy for xx,yy,_ in pts if abs(xx-x)<=6]
    med=statistics.median(nb)
    if med-y>18: print('outlier x=%d y=%d med=%.0f dark=%d'%(x,y,med,v))
