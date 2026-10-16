import json, math, numpy as np
from PIL import Image, ImageDraw
v=np.array(json.load(open('series3.json')))
import sys
gain=float(sys.argv[1]); R0=float(sys.argv[2]); R1=float(sys.argv[3])
S=2; W,H=1100*S,800*S; cx,cy=550*S,400*S
im=Image.new('RGB',(W,H),(243,240,233)); dr=ImageDraw.Draw(im)
m=v.mean(); pts=[]
for i,val in enumerate(v):
    t=i/24.0
    r=(R0+(R1-R0)*t/61+gain*(val-m))*S
    a=2*math.pi*(i%24)/24-math.pi/2
    pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
dr.line(pts,fill=(200,193,182),width=1*S)
for x,y in pts: dr.ellipse([x-1.6*S,y-1.6*S,x+1.6*S,y+1.6*S],fill=(30,30,34))
im.resize((1100,800),Image.LANCZOS).save(sys.argv[4])
