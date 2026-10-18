import json, math
from PIL import Image, ImageDraw
d=json.load(open('/tmp/claude-0/s133/mk/m06/scratch/data.json'))['days']
S=2;W,H=1100,800
im=Image.new('RGB',(W*S,H*S),(12,15,21));dr=ImageDraw.Draw(im,'RGBA')
COLS=11; X0=58; CW=(W-2*X0)/COLS; Y0=118; RH=103; R=41
for k,day in enumerate(d):
    col=k%COLS; row=k//COLS
    cx=X0+CW*(col+0.5); cy=Y0+RH*row+58
    dr.ellipse([(cx-R)*S,(cy-R)*S,(cx+R)*S,(cy+R)*S],outline=(40,43,50))
    P=[(cx,cy)]
    for h,v in sorted(day):
        a=2*math.pi*h/24; P.append((cx-R*v*math.sin(a),cy+R*v*math.cos(a)))
    if len(P)>2: dr.polygon([(x*S,y*S) for x,y in P],fill=(255,190,100,170),outline=(255,216,144,160))
    for x,y in P[1:]: dr.ellipse([(x-1.2)*S,(y-1.2)*S,(x+1.2)*S,(y+1.2)*S],fill=(255,250,240))
im.resize((W,H),Image.LANCZOS).save('preview.png')
