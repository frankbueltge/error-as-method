from PIL import Image
import math, json
im=Image.open('/tmp/claude-0/s130/mk/m09/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
X0,SPAN=2.8,293.7
dots=[]
for x in range(W):
    col=[255-px[x,y] for y in range(H)]
    for y in range(1,H-1):
        if col[y]>=80 and col[y]>=col[y-1] and col[y]>col[y+1]:
            # subpixel centroid
            a,b,c=col[y-1],col[y],col[y+1]
            dots.append((x,y+(c-a)/max(1,(a+b+c)),b))
print(len(dots))
# fold
nb=8
bins=[[] for _ in range(nb)]
for x,y,b in dots:
    t=(x-X0)/SPAN*1463
    ph=(t/24.0)%1
    bins[int(ph*nb)].append(y)
for i,bb in enumerate(bins):
    bb.sort(); n=len(bb)
    print(i*3,'h', n, 'mean',round(sum(bb)/n,1),'p10',round(bb[n//10],1),'p50',round(bb[n//2],1),'p90',round(bb[9*n//10],1))
json.dump(dots,open('dots.json','w'))
