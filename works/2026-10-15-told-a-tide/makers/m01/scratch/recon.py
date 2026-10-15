from PIL import Image
import itertools, json, math
im=Image.open('/tmp/claude-0/s128/mk/m01/work/record.jpg').convert('L'); p=im.load()
W,H=im.size
N=1464
xa,xb=2.5,296.5  # centres of first/last dot (estimated from ink extent)
xs=[xa+(xb-xa)*i/(N-1) for i in range(N)]
cols={}
for i,x in enumerate(xs): cols.setdefault(int(round(x)) if False else int(x+0.5),[]).append(i)
def dark(x,y): return max(0,235-p[x,y]) if 0<=x<W and 0<=y<H else 0
vals=[None]*N
prev=None
for c in sorted(cols):
    idx=cols[c]; n=len(idx)
    prof=[dark(c,y) for y in range(H)]
    # local maxima blobs
    peaks=[]
    for y in range(H):
        if prof[y]>40 and prof[y]>=prof[y-1 if y>0 else 0] and prof[y]>=prof[y+1 if y<H-1 else y]:
            if peaks and y-peaks[-1][0]<=1: 
                if prof[y]>peaks[-1][1]: peaks[-1]=(y,prof[y])
                continue
            # subpixel centroid
            s=sum(prof[yy] for yy in range(max(0,y-1),min(H,y+2)))
            cy=sum(yy*prof[yy] for yy in range(max(0,y-1),min(H,y+2)))/s
            peaks.append((y,prof[y],cy,s))
    peaks=[pk for pk in peaks if len(pk)==4]
    if not peaks:
        ys=[prev if prev is not None else 32.0]*n
    else:
        peaks.sort(key=lambda t:-t[3])
        ys=[pk[2] for pk in peaks[:n]]
        k=0
        while len(ys)<n:  # duplicate strongest blobs (overlapping dots)
            ys.append(peaks[k%len(peaks)][2]); k+=1
    # order within column: minimise path length from previous value
    best=None
    start=prev if prev is not None else sorted(ys)[len(ys)//2]
    for perm in set(itertools.permutations(ys)):
        cost=abs(perm[0]-start)+sum(abs(perm[j+1]-perm[j]) for j in range(n-1))
        if best is None or cost<best[0]: best=(cost,perm)
    for i,yv in zip(idx,best[1]): vals[i]=yv
    prev=best[1][-1]
v=[round(H-y,2) for y in vals]   # larger = higher
json.dump(v,open('series.json','w'))
print(min(v),max(v),len(v))
print(v[:48])
