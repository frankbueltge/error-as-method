import json, collections
from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m07/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
N=1464; x0,x1=3.0,296.6
X=lambda t: x0+t*(x1-x0)/(N-1)
T=lambda x: (x-x0)*(N-1)/(x1-x0)
dk=lambda x,y: max(0,170-px[x,y])
# fold shape (half-hour bins, weighted median of per-day normalized height)
pts=[(T(x),y,dk(x,y)) for x in range(W) for y in range(H) if dk(x,y)>0]
days=collections.defaultdict(list)
for t,y,d in pts: days[int(t//24)].append(y)
def pct(v,q): v=sorted(v); return v[min(len(v)-1,int(q*len(v)))]
ext={k:(pct(v,.03),pct(v,.97)) for k,v in days.items()}
bins=collections.defaultdict(list)
for t,y,d in pts:
    k=int(t//24)
    if 0<=k<=41:
        top,bot=ext[k]; bins[int(t%24)].append((bot-y)/(bot-top))
med=[sorted(bins[h])[len(bins[h])//2] for h in range(24)]
# circular smoothing
f=[(med[(h-1)%24]+2*med[h]+med[(h+1)%24])/4 for h in range(24)]
lo,hi=min(f),max(f); f=[(v-lo)/(hi-lo) for v in f]
print('shape',[round(v,2) for v in f])
PEAKH=0; TROUGHH=15
def colrange(xc,w=1.0):
    ys=[]
    for x in range(max(0,int(xc-w)),min(W,int(xc+w)+1)):
        for y in range(H):
            if px[x,y]<140: ys.append(y)
    return ys
tops={};bots={}
for d in range(0,44):
    tp=24*d+PEAKH
    ys=colrange(X(tp),1.6)
    if ys: tops[tp]=min(ys)+1
    tb=24*d+TROUGHH
    ys=colrange(X(tb),1.2)
    if ys: bots[tb]=max(ys)-1
def interp(anch,t):
    ks=sorted(anch)
    if t<=ks[0]: return anch[ks[0]]
    if t>=ks[-1]: return anch[ks[-1]]
    for a,b in zip(ks,ks[1:]):
        if a<=t<=b: return anch[a]+(anch[b]-anch[a])*(t-a)/(b-a)
# column-mean curve
cm=[]
for x in range(W):
    w=sum(dk(x,y) for y in range(H)); cm.append(sum(y*dk(x,y) for y in range(H))/w if w else None)
def cmi(t):
    xc=X(t); a=int(xc); b=a+1; fr=xc-a
    return cm[a]*(1-fr)+cm[b]*fr
ys=[]
SWITCH=1030
for t in range(N):
    m=interp(bots,t)+(interp(tops,t)-interp(bots,t))*f[t%24]
    a=min(1,max(0,(t-1016)/14))
    y=m*(1-a)+cmi(t)*a
    ys.append(y)
# light smoothing of tail
tail=ys[SWITCH:]; sm=[]
for i in range(len(tail)):
    w=tail[max(0,i-1):i+2]; sm.append(sum(w)/len(w))
ys[SWITCH:]=sm
for t in range(SWITCH-6,SWITCH+6): print(t, round(ys[t],1))
ymin,ymax=5.0,86.0
vals=[round((ymax-y)/(ymax-ymin),3) for y in ys]
json.dump(vals,open('/tmp/claude-0/s137/mk/m07/scratch/series.json','w'))
out=Image.new('RGB',(W*3,H*3),'white'); op=out.load()
o3=im.convert('RGB').resize((W*3,H*3))
for t,y in enumerate(ys):
    xx=int(X(t)*3); yy=int(y*3)
    for dx in range(2):
        for dy in range(2):
            if 0<=xx+dx<W*3 and 0<=yy+dy<H*3: o3.putpixel((xx+dx,yy+dy),(220,30,30))
o3.save('/tmp/claude-0/s137/mk/m07/scratch/overlay.png')
