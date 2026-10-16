from PIL import Image, ImageDraw; import numpy as np
v=np.load('v.npy'); N=len(v); S=3
im=Image.new('RGB',(1100*S,800*S),(242,236,224)); d=ImageDraw.Draw(im)
cx,cy=550,400
d.ellipse([(cx-(34+5.4*1463/24+29))*S,(cy-(34+5.4*1463/24+29))*S,(cx+(34+5.4*1463/24+29))*S,(cy+(34+5.4*1463/24+29))*S],fill=(235,225,205))
for h in range(N-1):
    t=np.linspace(h,h+1,9); vv=np.interp(t,np.arange(N),v)
    r=34+5.4*t/24+46*(vv-0.5); a=2*np.pi*t/24-np.pi/2
    m=(v[h]+v[h+1])/2; w=0.45+1.9*(1-m)**1.6; op=0.55+0.4*(1-m)
    c=tuple(int(242*(1-op)+k*op) for k in (59,40,28))
    d.line(list(zip((cx+r*np.cos(a))*S,(cy+r*np.sin(a))*S)),fill=c,width=max(1,int(round(w*S))),joint='curve')
im.resize((1100,800),Image.LANCZOS).save('p3.png')
