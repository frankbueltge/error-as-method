import json
from PIL import Image, ImageDraw
cols=json.load(open('peaks.json'))
N=1464; S=295.6/N
ys=[[y for y,_ in c] for c in cols]
for x in range(300):
    if not ys[x]:
        for d in range(1,5):
            for xx in (x-d,x+d):
                if 0<=xx<300 and ys[xx]: ys[x]=ys[xx]; break
            if ys[x]: break
hours={}
for h in range(N):
    hours.setdefault(min(299,int(h*S+0.5)),[]).append(h)
X=sorted(hours)
def seq(x,o):
    l=sorted(ys[x]); return l if o==0 else l[::-1]   # o=0: y increasing (falling value)
# viterbi
INF=1e18
cost={0:[0,0]}; back={}
prev=X[0]
cost=[0.0,0.0]
backs=[]
for x in X[1:]:
    nc=[INF,INF]; bk=[0,0]
    for o in (0,1):
        s=seq(x,o)[0]
        for po in (0,1):
            e=seq(prev,po)[-1]
            c=cost[po]+(s-e)**2
            if c<nc[o]: nc[o]=c; bk[o]=po
    backs.append(bk); cost=nc; prev=x
o=0 if cost[0]<cost[1] else 1
orient=[o]
for bk in reversed(backs):
    o=bk[o]; orient.append(o)
orient=orient[::-1]
val=[None]*N
for x,o in zip(X,orient):
    s=seq(x,o); hs=hours[x]; n=len(hs)
    for i,h in enumerate(hs):
        if len(s)==1: v=s[0]
        else:
            t=i*(len(s)-1)/(n-1) if n>1 else 0
            a=int(t); b=min(a+1,len(s)-1); f=t-a
            v=s[a]*(1-f)+s[b]*f
        val[h]=v
v=[90-y for y in val]
json.dump([round(a,1) for a in v],open('series.json','w'))
im=Image.new('L',(300,90),255); d=ImageDraw.Draw(im)
for h,a in enumerate(v):
    x=h*S; y=90-a; d.ellipse([x-0.6,y-0.6,x+0.6,y+0.6],fill=0)
im.resize((900,270)).save('recon.png')
# daily profile: mean per hour of day over days 0-41 vs 43-60
for rng,name in (((0,42),'active'),((43,61),'quiet')):
    prof=[]
    for hh in range(24):
        l=[v[d*24+hh] for d in range(*rng)]
        prof.append(round(sum(l)/len(l),1))
    print(name,prof)
