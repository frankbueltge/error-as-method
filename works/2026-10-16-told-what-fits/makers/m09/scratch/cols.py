import json, math
from PIL import Image, ImageDraw
v=json.load(open('series2.json')); N=len(v)
W,H,S=1100,800,3
L,R,T,B=74,74,92,150
cw=(W-L-R)/61
vmin,vmax=min(v),max(v)
def Y(q): return T+(vmax-q)/(vmax-vmin)*(H-T-B)
# hour colour: night ink -> day ochre
def col(h):
    s=(1-math.cos(2*math.pi*(h)/24))/2   # 0 at h=0, 1 at h=12
    night=(28,34,64); day=(214,146,52)
    return tuple(int(night[i]+(day[i]-night[i])*s) for i in range(3))
im=Image.new('RGB',(W*S,H*S),(243,239,230)); dr=ImageDraw.Draw(im,'RGBA')
for dday in range(61):
    x0=L+dday*cw; xc=x0+cw/2
    hs=v[dday*24:(dday+1)*24]
    dr.line([(xc*S,Y(max(hs))*S),(xc*S,Y(min(hs))*S)],fill=(40,40,50,70),width=S)
    order=sorted(range(24),key=lambda h:-((1-math.cos(2*math.pi*h/24))/2))
    for h in order:
        y=Y(hs[h]); c=col(h)
        dr.rectangle([(x0+2.2)*S,(y-0.9)*S,(x0+cw-2.2)*S,(y+0.9)*S],fill=c+(200,))
im=im.resize((W,H),Image.LANCZOS); im.save('c1.png')
