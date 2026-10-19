from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m07/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
N=1464; x0,x1=3.0,296.6
pts=[]
for x in range(W):
    for y in range(H):
        d=max(0,170-px[x,y])
        if d>0:
            t=(x-x0)*(N-1)/(x1-x0); pts.append((t,y,d))
# per-day extent
import collections
def pct(vals,q):
    vals=sorted(vals); return vals[min(len(vals)-1,int(q*len(vals)))]
days=collections.defaultdict(list)
for t,y,d in pts:
    days[int(t//24)].append(y)
ext={k:(pct(v,0.03),pct(v,0.97)) for k,v in days.items()}
out=Image.new('RGB',(480,200),'white'); op=out.load()
bins=collections.defaultdict(list)
for t,y,d in pts:
    k=int(t//24)
    if k<0 or k>41: continue
    top,bot=ext[k]
    if bot-top<10: continue
    n=(bot-y)/(bot-top); h=t%24
    X=int(h*20); Y=int(180-n*160)
    if 0<=X<480 and 0<=Y<200: op[X,Y]=(0,0,0)
    bins[int(h)].append(n)
out.save('/tmp/claude-0/s137/mk/m07/scratch/fold.png')
for h in range(24):
    b=sorted(bins[h]); print(h, len(b), round(b[len(b)//4],2), round(b[len(b)//2],2), round(b[3*len(b)//4],2))
