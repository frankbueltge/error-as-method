from PIL import Image
import math
im=Image.open('/tmp/claude-0/s130/mk/m15/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
cols=[]
for x in range(W):
    ws=sum(max(0,230-p[x,y]) for y in range(H))
    my=sum(y*max(0,230-p[x,y]) for y in range(H))/ws if ws else None
    cols.append((ws,my))
dark=[x for x in range(W) if cols[x][0]>50]
print('first/last col with ink',dark[0],dark[-1])
ys=[c[1] for c in cols]
m=sum(y for y in ys if y)/len([y for y in ys if y])
s=[(y-m) if y else 0 for y in ys]
for P in [x/10 for x in range(30,120,2)]:
    re=sum(v*math.cos(2*math.pi*i/P) for i,v in enumerate(s));im_=sum(v*math.sin(2*math.pi*i/P) for i,v in enumerate(s))
    print(P, round(math.hypot(re,im_),1))
