from PIL import Image
import math
im=Image.open('/tmp/claude-0/s130/mk/m13/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
top=[];mean=[];bot=[]
for x in range(W):
    ws=[(y,max(0,200-px[x,y])) for y in range(H)]
    tot=sum(w for y,w in ws)
    ys=[y for y,w in ws if w>60]
    top.append(min(ys) if ys else None); bot.append(max(ys) if ys else None)
    mean.append(sum(y*w for y,w in ws)/tot if tot else None)
def detrend(s,k=10):
    out=[]
    for i in range(len(s)):
        win=[v for v in s[max(0,i-k):i+k+1] if v is not None]
        out.append(s[i]-sum(win)/len(win) if s[i] is not None else 0)
    return out
for name,s in [('top',top),('mean',mean),('bot',bot)]:
    d=detrend(s)
    best=[]
    for p10 in range(30,120):
        p=p10/10
        c=sum(d[x]*math.cos(2*math.pi*x/p) for x in range(W)); sn=sum(d[x]*math.sin(2*math.pi*x/p) for x in range(W))
        best.append((math.hypot(c,sn),p,math.atan2(sn,c)))
    best.sort(reverse=True)
    print(name,[(round(a,1),p,round(ph,2)) for a,p,ph in best[:6]])
print('top',top)
print('bot',bot)
