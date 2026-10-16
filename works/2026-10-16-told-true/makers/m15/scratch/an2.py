from PIL import Image
import math
im=Image.open('/tmp/claude-0/s130/mk/m15/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
x0,x1=2.0,297.0
pxh=(x1-x0)/1463
ys=[]
for x in range(W):
    ws=sum(max(0,230-p[x,y]) for y in range(H))
    ys.append(sum(y*max(0,230-p[x,y]) for y in range(H))/ws if ws>50 else None)
v=[y for y in ys if y];m=sum(v)/len(v)
s=[(y-m) if y else 0 for y in ys]
def amp(P):
    re=sum(q*math.cos(2*math.pi*i/P) for i,q in enumerate(s));im_=sum(q*math.sin(2*math.pi*i/P) for i,q in enumerate(s))
    return math.hypot(re,im_), math.atan2(im_,re)
best=max([(amp(P/100)[0],P/100) for P in range(470,500)]);print('best period px',best, 'expected 24h px',24*pxh)
for P in [24*pxh*k for k in (0.5,1,2,3.5,7,14)]:
    print('period hours',round(P/pxh),round(amp(P)[0],1))
# folded profile by hour-of-day (assuming first value hour 0)
bins=[[] for _ in range(24)]
for x in range(W):
    if ys[x] is None: continue
    h=((x-x0)/pxh)%24
    bins[int(h)].append(ys[x])
print('hour-of-day mean y (lower=higher value):')
for h,b in enumerate(bins): print(h, round(sum(b)/len(b),2) if b else '-', len(b))
