import json, math, numpy as np, sys
from PIL import Image, ImageDraw
v=np.array(json.load(open('series3.json')))
gd=float(sys.argv[1]); R0=float(sys.argv[2]); R1=float(sys.argv[3])
N=len(v)
pad=np.concatenate([v[:12][::-1],v,v[-12:][::-1]])
rm=np.convolve(pad,np.ones(24)/24,'same')[12:12+N]
dev=v-rm
lo,hi=np.percentile(rm,2),np.percentile(rm,98)
S=3; W,H=1100*S,800*S; cx,cy=550*S,400*S
im=Image.new('RGB',(W,H),(243,240,233)); dr=ImageDraw.Draw(im)
def cr(arr,i,s):
    p0=arr[max(i-1,0)];p1=arr[i];p2=arr[i+1];p3=arr[min(i+2,N-1)]
    return 0.5*((2*p1)+(-p0+p2)*s+(2*p0-5*p1+4*p2-p3)*s*s+(-p0+3*p1-3*p2+p3)*s**3)
prev=None
for i in range(N-1):
    for k in range(6):
        s=k/6; t=(i+s)/24
        r=(R0+(R1-R0)*t/61+gd*cr(dev,i,s))*S
        a=2*math.pi*t-math.pi/2
        p=(cx+r*math.cos(a),cy+r*math.sin(a))
        q=min(1,max(0,(cr(rm,i,s)-lo)/(hi-lo)))
        if prev:
            c=int(205-185*q); w=int((0.6+2.4*q)*S)
            dr.line([prev,p],fill=(c,c-2,c-6),width=max(1,w))
        prev=p
im.resize((1100,800),Image.LANCZOS).save(sys.argv[4])
