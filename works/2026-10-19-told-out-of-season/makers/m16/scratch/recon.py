import sys, json
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; px=im.load()
TH=150
cols=[]
for x in range(W):
    ys=[y for y in range(H) if px[x,y]<TH]
    cols.append(ys)
xs=[x for x in range(W) if cols[x]]
x0,x1=xs[0],xs[-1]
print('x range',x0,x1, file=sys.stderr)
# blobs per column: runs; long run -> multiple points
def blobs(ys):
    runs=[];cur=[]
    for y in ys:
        if cur and y!=cur[-1]+1: runs.append(cur);cur=[]
        cur.append(y)
    if cur: runs.append(cur)
    pts=[]
    for r in runs:
        a,b=r[0],r[-1]
        n=max(1,round((b-a+1)/2.2))
        if n==1: pts.append((a+b)/2)
        else:
            for i in range(n): pts.append(a+0.6+(b-a-1.2)*i/(n-1))
    return pts
seq=[]  # list of (x, y)
prev=None
for x in range(x0,x1+1):
    p=blobs(cols[x])
    if not p: continue
    # order: decay (y increasing) by default; but if column contains a rise
    # (some points far above previous col bottom), order: low-ones-near-prev first? Rise happens: low pts then high pts then decay.
    p.sort()
    if prev is not None:
        pb=max(prev)
        # points below/near prev bottom come first (end of decay), then rise points ascending (y decreasing), top, then decay
        lows=[y for y in p if y>=pb-1]
        highs=[y for y in p if y<pb-1]
        if lows and highs and min(highs)<pb-8:
            # rise: lows (desc y→ already end of decay sorted asc), then highs from bottom up to top, then? keep simple
            seq+= [(x,y) for y in sorted(lows)] + [(x,y) for y in sorted(highs,reverse=True)]
            prev=p; continue
    seq+=[(x,y) for y in p]
    prev=p
# resample to 1464 by arc index proportional mapping within each column: assign each point a time = x + frac
pts=[]
from collections import defaultdict
byx=defaultdict(list)
for x,y in seq: byx[x].append(y)
for x in sorted(byx):
    L=byx[x]
    for i,y in enumerate(L): pts.append((x-0.5+(i+0.5)/len(L), y))
N=1464
span=(x1+0.5)-(x0-0.5)
vals=[]
j=0
for t in range(N):
    xt=x0-0.5+(t+0.5)*span/N
    while j<len(pts)-2 and pts[j+1][0]<xt: j+=1
    (xa,ya),(xb,yb)=pts[j],pts[j+1]
    f=0 if xb==xa else min(1,max(0,(xt-xa)/(xb-xa)))
    y=ya+(yb-ya)*f
    vals.append(round((H-1-y)/(H-1),4))
json.dump(vals,open('vals.json','w'))
print(len(pts),file=sys.stderr)
