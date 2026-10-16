import json, math, numpy as np, sys
from PIL import Image, ImageDraw
v=np.array(json.load(open('series3.json')))
gain=float(sys.argv[1]); R0=float(sys.argv[2]); R1=float(sys.argv[3])
S=3; W,H=1100*S,800*S; cx,cy=550*S,400*S
im=Image.new('RGB',(W,H),(243,240,233)); dr=ImageDraw.Draw(im)
m=v.mean()
# catmull-rom in (t, r) space then to xy
N=len(v); P=[]
for i in range(N-1):
    p0=v[max(i-1,0)];p1=v[i];p2=v[i+1];p3=v[min(i+2,N-1)]
    for k in range(8):
        s=k/8
        val=0.5*((2*p1)+(-p0+p2)*s+(2*p0-5*p1+4*p2-p3)*s*s+(-p0+3*p1-3*p2+p3)*s**3)
        t=(i+s)/24
        r=(R0+(R1-R0)*t/61+gain*(val-m))*S
        a=2*math.pi*t-math.pi/2
        P.append((cx+r*math.cos(a),cy+r*math.sin(a)))
dr.line(P,fill=(28,28,32),width=int(1.2*S),joint='curve')
im.resize((1100,800),Image.LANCZOS).save(sys.argv[4])
