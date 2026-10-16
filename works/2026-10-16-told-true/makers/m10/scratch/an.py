from PIL import Image
import math
im=Image.open('/tmp/claude-0/s130/mk/m10/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
# column darkness-weighted mean y and spread
my=[];cnt=[];lo=[];hi=[]
for x in range(W):
    s=0;sy=0;ys=[]
    for y in range(H):
        d=max(0,230-p[x,y])
        s+=d;sy+=d*y
        if p[x,y]<170: ys.append(y)
    my.append(sy/s if s else float('nan')); cnt.append(s)
    lo.append(min(ys) if ys else -1); hi.append(max(ys) if ys else -1)
nan=[i for i,v in enumerate(my) if v!=v]; print('empty cols',nan)
good=[i for i,v in enumerate(my) if v==v]
for i in nan:
    j=min(good,key=lambda g:abs(g-i)); my[i]=my[j]
print('mean y cols:',' '.join('%d'%round(v) for v in my))
print('ink per col:',' '.join('%d'%(c/1000) for c in cnt))
# periodogram of my
n=W; m=sum(my)/n; z=[v-m for v in my]
res=[]
for k in range(1,150):
    f=k/n
    c=sum(z[i]*math.cos(2*math.pi*f*i) for i in range(n)); s=sum(z[i]*math.sin(2*math.pi*f*i) for i in range(n))
    res.append(((c*c+s*s)/n, k, n/k, n/k*1464/300))
res.sort(reverse=True)
for r in res[:15]: print('pow %.1f k=%d periodpx=%.2f hours=%.1f'%r)
