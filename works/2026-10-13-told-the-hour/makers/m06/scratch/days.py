import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; p=im.load()
x0,x1=3,296.99; N=1464
pw=(x1-x0)/N  # px per hour
# per-day top/bottom/mean
for d in range(61):
    a=x0+d*24*pw; b=a+24*pw
    ys=[];
    for x in range(int(a),int(b)+1):
        if x<a-0.5 or x>b-0.5: continue
        for y in range(H):
            if p[x,y]<140: ys.append(y)
    ys.sort()
    q=lambda f: ys[int(f*(len(ys)-1))]
    print(d, 'dow',d%7, 'top',ys[0],'p10',q(.1),'med',q(.5),'p90',q(.9),'bot',ys[-1], '#'*max(0,(60-q(.1))//2))
