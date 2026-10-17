from PIL import Image
import json
im=Image.open('/tmp/claude-0/s133/mk/m20/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
D=[[max(0,255-px[x,y]) for y in range(H)] for x in range(W)]
TH=60
# column-wise vertical runs above baseline region (rows <= 81)
comps=[]
for x in range(W):
    y=0
    while y<=81:
        if D[x][y]>TH:
            y0=y
            while y<=81 and D[x][y]>TH: y+=1
            y1=y-1
            seg=list(range(y0,y1+1))
            # split long runs into ~2px dots
            n=max(1,round(len(seg)/2.2))
            for k in range(n):
                part=seg[k*len(seg)//n:(k+1)*len(seg)//n]
                wsum=sum(D[x][r] for r in part)
                cy=sum(r*D[x][r] for r in part)/wsum
                comps.append([x,cy,wsum])
        else: y+=1
# merge horizontally adjacent duplicates (same dot bleeding into neighbour column)
comps.sort()
used=[False]*len(comps); merged=[]
for i,(x,cy,w) in enumerate(comps):
    if used[i]: continue
    grp=[(x,cy,w)]; used[i]=True
    for j in range(i+1,len(comps)):
        x2,cy2,w2=comps[j]
        if x2>x+1: break
        if x2==x+1 and not used[j] and abs(cy2-cy)<=1.2:
            grp.append((x2,cy2,w2)); used[j]=True; break
    ws=sum(g[2] for g in grp)
    merged.append((sum(g[0]*g[2] for g in grp)/ws, sum(g[1]*g[2] for g in grp)/ws, ws))
print('comps',len(comps),'merged',len(merged))
a=2.45; b=0.200836; NOON=19.1
def val(cy): return max(0.0,min(1.05,(83.5-cy)/78))
def morning(x):
    hr=((x-a)/b)%24
    return hr<NOON and hr>NOON-12
items=[]
for cx,cy,w in merged:
    v=val(cy)
    key=cx+(0.35*v if morning(cx) else -0.35*v)
    items.append((key,cx,v))
items.sort()
import math
def env(i):
    t=i/1463.0
    dec=math.radians(22.5-14*t)
    lat=math.radians(48.0)
    hs=((i-NOON)%24)
    if hs>12: hs-=24
    H=math.radians(15*hs)
    se=math.sin(lat)*math.sin(dec)+math.cos(lat)*math.cos(dec)*math.cos(H)
    return max(0.0,1.05*se**1.15) if se>0 else 0.0
N=1464; M=len(items)
INF=1e18
ZC=0.9   # cost of calling an hour zero
def zcost(i):
    # zero is cheap at night: check baseline darkness at its column
    x=int(round(a+b*i)); x=min(max(x,0),W-1)
    base=D[x][83]+D[x][84]
    return 0.3 if base>250 else 2.5
# DP over (hour i, comp j) states: state j=-1..M-1 meaning last comp used index
# use banded DP
import bisect
keys=[it[0] for it in items]
cost={}
prev={(-1):(0.0,None)}  # j -> (cost, backpointer list)
back=[]
# to keep tractable: for hour i, candidate comps those with |cx - xi|<2.2
lastj_by_i=[]
dp_prev={-1:0.0}
bp=[]
for i in range(N):
    xi=a+b*i
    lo=bisect.bisect_left(keys,xi-2.6); hi=bisect.bisect_right(keys,xi+2.6)
    cands=list(range(lo,hi))
    dp_cur={}; bpi={}
    # states from prev: j
    # option zero: keep j
    zc=zcost(i)
    for j,c in dp_prev.items():
        # zero
        nc=c+zc
        if nc<dp_cur.get(j,INF): dp_cur[j]=nc; bpi[j]=(j,'z')
    for jn in cands:
        dx=items[jn][1]-xi
        mc=dx*dx*1.0
        ex=env(i); over=items[jn][2]-ex-0.10
        if over>0: mc+=60*over*over
        for j,c in dp_prev.items():
            if j==jn:
                nc=c+mc+0.25  # reuse same comp for another hour
            elif j<jn:
                skipped=jn-j-1
                nc=c+mc+skipped*3.0
            else: continue
            if nc<dp_cur.get(jn,INF): dp_cur[jn]=nc; bpi[jn]=(j,'m')
    # prune
    best=sorted(dp_cur.items(), key=lambda t:t[1])[:60]
    dp_prev=dict(best)
    bp.append(bpi)
# finalize: penalize unused comps at end
endc={j:c+(M-1-j)*3.0 for j,c in dp_prev.items()}
j=min(endc,key=endc.get)
vals=[0.0]*N
for i in range(N-1,-1,-1):
    pj,op=bp[i][j]
    if op=='m': vals[i]=items[j][2]
    else: vals[i]=0.0
    j=pj
nz=0
for i in range(N):
    if env(i)==0 and vals[i]>0: nz+=1; vals[i]=0.0
print('zeroed at night',nz)
usedj=set()
print('min cost',min(endc.values()))
json.dump(vals,open('vals.json','w'))
# render check
out=Image.new('L',(W,H),255); op=out.load()
for i,v in enumerate(vals):
    x=int(round(a+b*i)); y=int(round(83.5-v*78))
    op[min(x,W-1),y]=0
out.resize((W*3,H*3)).save('recon.png')
im.resize((W*3,H*3)).save('orig3.png')
# daily sums
for d in range(61):
    s=sum(vals[d*24:(d+1)*24]); print(d, round(s,2), round(max(vals[d*24:(d+1)*24]),2), sum(1 for v in vals[d*24:(d+1)*24] if v>0.02))
