import json, math, sys
from PIL import Image, ImageDraw
v=json.load(open('series2.json'))
N=len(v); W,H=1100,800; S=2
k=float(sys.argv[1]); a=float(sys.argv[2]); r0=float(sys.argv[3]); out=sys.argv[4]
cx,cy=550,400
mean=sum(v)/N
im=Image.new('RGB',(W*S,H*S),(244,241,234)); dr=ImageDraw.Draw(im)
pts=[]
for t,q in enumerate(v):
    ang=2*math.pi*(t%24)/24
    r=r0+k*t/24+a*(q-mean)
    pts.append((cx-r*math.sin(ang), cy+r*math.cos(ang)))
dr.line([(x*S,y*S) for x,y in pts],fill=(200,195,185),width=1)
for x,y in pts:
    R=1.3*S; dr.ellipse([x*S-R,y*S-R,x*S+R,y*S+R],fill=(29,27,24))
im.resize((W,H),Image.LANCZOS).save(out)
