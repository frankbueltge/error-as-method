from PIL import Image, ImageDraw; import numpy as np, sys
v=np.load('v.npy'); N=len(v)
S=2; W,H=1100*S,800*S; cx,cy=W/2,H/2
r0,step,A=float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3])
im=Image.new('RGB',(W,H),(242,236,224)); d=ImageDraw.Draw(im)
t=np.arange(0,N-1,0.125); vv=np.interp(t,np.arange(N),v)
import numpy as _n
th=2*np.pi*t/24 - np.pi/2
r=(r0+step*t/24+A*(vv-0.5))*S
pts=list(zip(cx+r*np.cos(th),cy+r*np.sin(th)))
d.line(pts,fill=(60,40,28),width=int(1.4*S),joint='curve')
im.resize((1100,800),Image.LANCZOS).save(sys.argv[4])
