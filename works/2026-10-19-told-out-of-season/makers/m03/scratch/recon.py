import json,sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; p=im.load()
N=1464
cnt=[0]*W
for h in range(N): cnt[int((h+0.5)*W/N)]+=1
cols=[]
for x in range(W):
    d=[max(0,230-p[x,y]) for y in range(H)]
    d=[v if v>25 else 0 for v in d]
    S=sum(d); k=cnt[x]; pts=[]
    if S==0: print('empty col',x); cols.append(None); continue
    else:
        cum=0;j=0;targets=[(i+0.5)/k*S for i in range(k)]
        for y in range(H):
            prev=cum; cum+=d[y]
            while j<k and targets[j]<=cum:
                f=(targets[j]-prev)/d[y] if d[y] else 0
                pts.append(y-0.5+f+0.5); j+=1
        while len(pts)<k: pts.append(pts[-1])
    cols.append(sorted(pts))  # ascending y = descending value
for x in range(W):
    if cols[x] is None:
        a=cols[x-1] if x>0 else cols[x+1]; b=cols[x+1] if x<W-1 and cols[x+1] else a
        m=(sum(a)/len(a)+sum(b)/len(b))/2; cols[x]=[m]*cnt[x]
# DP: orientation per column (0: as sorted y asc => values descending, 1: reversed)
INF=1e18
def seq(x,o): return cols[x] if o==0 else cols[x][::-1]
cost=[[0,0]];back=[]
for x in range(1,W):
    row=[];br=[]
    for o in (0,1):
        best=None
        for po in (0,1):
            c=cost[-1][po]+abs(seq(x-1,po)[-1]-seq(x,o)[0])
            if best is None or c<best[0]: best=(c,po)
        row.append(best[0]);br.append(best[1])
    cost.append(row);back.append(br)
o=0 if cost[-1][0]<=cost[-1][1] else 1
ors=[o]
for x in range(W-1,0,-1):
    o=back[x-1][o]; ors.append(o)
ors=ors[::-1]
ys=[]
for x in range(W): ys+=seq(x,ors[x])
vals=[round((H-y)/H*100,1) for y in ys]
print(len(vals), sum(ors), min(vals), max(vals))
json.dump(vals,open('series.json','w'))
