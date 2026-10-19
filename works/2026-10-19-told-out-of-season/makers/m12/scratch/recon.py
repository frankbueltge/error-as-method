import json
from PIL import Image, ImageDraw
cols=json.load(open('peaks.json'))
N=1464; S=295.6/N
ys=[[y for y,_ in c] for c in cols]
def mean(l): return sum(l)/len(l)
# fill empty columns
for x in range(300):
    if not ys[x]:
        for d in range(1,5):
            for xx in (x-d,x+d):
                if 0<=xx<300 and ys[xx]: ys[x]=ys[xx]; break
            if ys[x]: break
hours={}
for h in range(N):
    hours.setdefault(min(299,int(h*S+0.5)),[]).append(h)
val=[None]*N
for x,hs in hours.items():
    l=sorted(ys[x])  # ascending y = descending value
    pm=mean(ys[max(0,x-1)]); nm=mean(ys[min(299,x+1)])
    rising = nm < pm   # next has smaller y => higher value
    seq = l[::-1] if rising else l   # rising: y goes from large to small
    n=len(hs)
    for i,h in enumerate(hs):
        if len(seq)==1: v=seq[0]
        else:
            t=i*(len(seq)-1)/(n-1) if n>1 else 0
            a=int(t); b=min(a+1,len(seq)-1); f=t-a
            v=seq[a]*(1-f)+seq[b]*f
        val[h]=v
# convert to value (higher = larger), 0..1 over picture height
v=[(90-y) for y in val]
# light 3-pt median
sm=[sorted(v[max(0,i-1):i+2])[len(v[max(0,i-1):i+2])//2] for i in range(N)]
json.dump([round(a,1) for a in sm],open('series.json','w'))
im=Image.new('L',(300,90),255); d=ImageDraw.Draw(im)
for h,a in enumerate(sm):
    x=h*S; y=90-a; d.ellipse([x-0.7,y-0.7,x+0.7,y+0.7],fill=0)
im=im.resize((900,270)); im.save('recon.png')
orig=Image.open('/tmp/claude-0/s137/mk/m12/work/record.jpg').resize((900,270)); orig.save('orig_big.png')
print(min(sm),max(sm))
