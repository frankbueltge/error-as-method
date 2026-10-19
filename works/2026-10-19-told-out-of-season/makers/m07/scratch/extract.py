import json
from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m07/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
N=1464; x0,x1=3.0,296.6
xs=[x0+i*(x1-x0)/(N-1) for i in range(N)]
# darkness profile per column
dark=[[max(0,200-px[x,y]) for y in range(H)] for x in range(W)]
def colmean(c):
    w=sum(dark[c]); return sum(y*d for y,d in enumerate(dark[c]))/w if w else None
groups={}
for i,x in enumerate(xs): groups.setdefault(int(round(x)),[]).append(i)
ys=[None]*N
for c,idx in sorted(groups.items()):
    prof=dark[c]; tot=sum(prof); k=len(idx)
    # quantiles
    qs=[]; acc=0; targets=[(j+0.5)/k*tot for j in range(k)]; t=0
    for y,d in enumerate(prof):
        while t<k and acc+d>=targets[t]:
            frac=(targets[t]-acc)/d if d else 0
            qs.append(y+frac); t+=1
        acc+=d
    while len(qs)<k: qs.append(qs[-1] if qs else H/2)
    pm=colmean(c-1) if c>0 else None; nm=colmean(c+1) if c<W-1 else None
    if pm is None: pm=colmean(c)
    if nm is None: nm=colmean(c)
    # falling (y increasing) -> ascending y order
    qs.sort(reverse=(nm<pm))
    for j,i in enumerate(idx): ys[i]=qs[j]
ymin,ymax=5.0,86.0
vals=[round((ymax-y)/(ymax-ymin),4) for y in ys]
json.dump(vals,open('/tmp/claude-0/s137/mk/m07/scratch/series.json','w'))
# re-render check
out=Image.new('L',(W,H),255); op=out.load()
for x,y in zip(xs,ys):
    for dx in (0,1):
        for dy in (0,1):
            X=int(x+dx-0.5);Y=int(y+dy-0.5)
            if 0<=X<W and 0<=Y<H: op[X,Y]=40
out=out.resize((W*3,H*3)); out.save('/tmp/claude-0/s137/mk/m07/scratch/rerender.png')
im.resize((W*3,H*3)).save('/tmp/claude-0/s137/mk/m07/scratch/orig3.png')
# daily stats
for d in range(61):
    v=vals[d*24:(d+1)*24]
    print(d, min(v), max(v), v.index(max(v)), v.index(min(v)))
