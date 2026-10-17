import json, math
from PIL import Image, ImageDraw
d=json.load(open('/tmp/claude-0/s133/mk/m06/scratch/data.json'))['days']
S=3;W,H=1100,800
im=Image.new('RGB',(W*S,H*S),(12,15,21));dr=ImageDraw.Draw(im,'RGBA')
COLS=11; X0=50; CW=(W-2*X0)/COLS; Y0=120; RH=104; R=44
for k,day in enumerate(d):
    col=k%COLS; row=k//COLS
    cx=X0+CW*(col+0.5); cy=Y0+RH*row+72
    dr.arc([(cx-R)*S,(cy-R)*S,(cx+R)*S,(cy+R)*S],180,360,fill=(45,48,56),width=2)
    dr.line([(cx-R-3)*S,cy*S,(cx+R+3)*S,cy*S],fill=(45,48,56),width=2)
    for h,v in sorted(day,key=lambda t:-t[1]):
        a=2*math.pi*h/24; x,y=cx-R*v*math.sin(a),cy+R*v*math.cos(a)
        c=(255,int(170+80*v),int(90+140*v),220)
        dr.line([cx*S,cy*S,x*S,y*S],fill=c,width=int(1.6*S))
        dr.ellipse([(x-1.5)*S,(y-1.5)*S,(x+1.5)*S,(y+1.5)*S],fill=(255,248,232))
im.resize((W,H),Image.LANCZOS).save('preview2.png')
