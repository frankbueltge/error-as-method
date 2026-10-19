import sys, json
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; px=im.load()
# dots: per column, darkness profile; find local maxima of darkness (smoothed over x-1..x+1 lightly)
dots=[]
for x in range(W):
    prof=[255-px[x,y] for y in range(H)]
    for y in range(H):
        v=prof[y]
        if v<90: continue
        if v>=(prof[y-1] if y>0 else 0) and v>(prof[y+1] if y<H-1 else 0):
            # subpixel centroid
            a=prof[y-1] if y>0 else 0; c=prof[y+1] if y<H-1 else 0
            dots.append((x, y+(c-a)/(a+v+c)))
# group per column, order in time with sawtooth assumption
from collections import defaultdict
col=defaultdict(list)
for x,y in dots: col[x].append(y)
seq=[]
for x in sorted(col):
    ys=sorted(col[x])
    gaps=[(ys[i+1]-ys[i],i) for i in range(len(ys)-1)]
    if gaps and max(gaps)[0]>9:
        i=max(gaps)[1]
        ys=ys[i+1:]+ys[:i+1]
    for y in ys: seq.append((x,y))
print(len(dots), file=sys.stderr)
json.dump(seq, open('seq.json','w'))
