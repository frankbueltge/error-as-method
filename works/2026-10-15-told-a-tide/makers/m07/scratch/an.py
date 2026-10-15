from PIL import Image
import math
im=Image.open('/tmp/claude-0/s128/mk/m07/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
mean=[];sd=[];lo=[];hi=[];ink=[]
for x in range(W):
    w=[max(0,230-px[x,y]) for y in range(H)]
    s=sum(w)
    ink.append(s)
    if s<50: mean.append(None); sd.append(None); continue
    m=sum(y*wi for y,wi in enumerate(w))/s
    v=sum((y-m)**2*wi for y,wi in enumerate(w))/s
    mean.append(H-m); sd.append(math.sqrt(v))
print('ink first/last cols', ink[:4], ink[-4:])
valid=[x for x in range(W) if mean[x] is not None]
print('valid range',valid[0],valid[-1], len(valid))
# periodogram of mean and sd
def pg(series, name):
    xs=[x for x in valid]; ys=[series[x] for x in xs]
    mu=sum(ys)/len(ys)
    res=[]
    for i in range(1,400):
        P=2+i*0.05  # period in columns from 2.05 to 22
        P=None
    out=[]
    for k in range(200):
        P=2.05+k*0.1
        c=sum((y-mu)*math.cos(2*math.pi*x/P) for x,y in zip(xs,ys)); s=sum((y-mu)*math.sin(2*math.pi*x/P) for x,y in zip(xs,ys))
        out.append((c*c+s*s, P))
    for k in range(1,100):
        P=20+k*2
        c=sum((y-mu)*math.cos(2*math.pi*x/P) for x,y in zip(xs,ys)); s=sum((y-mu)*math.sin(2*math.pi*x/P) for x,y in zip(xs,ys))
        out.append((c*c+s*s, P))
    out.sort(reverse=True)
    print(name, [(round(p,1),round(P*1464/len(valid)/1.0,1) if False else round(P,2)) for p,P in out[:12]])
pg(mean,'mean'); pg(sd,'sd')
open('colstats.txt','w').write('\n'.join(f"{x} {mean[x]} {sd[x]}" for x in range(W)))
