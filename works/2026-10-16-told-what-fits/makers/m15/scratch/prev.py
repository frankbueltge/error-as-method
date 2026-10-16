import json, numpy as np
from PIL import Image, ImageDraw
v=np.array(json.load(open('vals2.json')))
m=v.copy()
for i in range(1,len(v)-1): m[i]=np.median(v[i-1:i+2])
D=m.reshape(61,24)
S=2
X0,X1,TOP,BOT=380,1040,180,764; sp=(BOT-TOP)/60; k=1.55; vmin=m.min()
im=Image.new('RGB',(1100*S,800*S),'#f1ede4'); dr=ImageDraw.Draw(im)
for i in range(61):
    nxt=D[i+1,0] if i<60 else D[i,23]
    vals=np.append(D[i],nxt)
    hh=np.linspace(0,24,241); vv=np.interp(hh,np.arange(25),vals)
    pts=[((X0+(X1-X0)*h/24)*S,(TOP+i*sp-(q-vmin)*k)*S) for h,q in zip(hh,vv)]
    dr.polygon(pts+[(X1*S,(BOT+30)*S),(X0*S,(BOT+30)*S)],fill='#f1ede4')
    rng=D[i].max()-D[i].min()
    dr.line(pts,fill='#1d1c1a',width=int((0.9 if rng>25 else 1.4)*S+0.5))
im.resize((1100,800),Image.LANCZOS).save('preview.png')
