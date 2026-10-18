import json, math
from PIL import Image, ImageDraw
d=json.load(open('/tmp/claude-0/s133/mk/m06/scratch/data.json'))['days']
S=3;W,H=1100,800
im=Image.new('RGB',(W*S,H*S),(12,15,21));dr=ImageDraw.Draw(im,'RGBA')
COLS=8; X0=40; CW=(W-2*X0)/COLS; Y0=110; RH=78; R=58
def P(cx,cy,h,r):
    a=2*math.pi*h/24; return ((cx-r*math.sin(a))*S,(cy+r*math.cos(a))*S)
for k,day in enumerate(d):
    col=k%COLS; row=k//COLS
    cx=X0+CW*(col+0.5); cy=Y0+RH*row+62
    dr.arc([(cx-R)*S,(cy-R)*S,(cx+R)*S,(cy+R)*S],180,360,fill=(42,45,53),width=2)
    dr.line([(cx-R-4)*S,cy*S,(cx+R+4)*S,cy*S],fill=(42,45,53),width=2)
    for h,v in sorted(day,key=lambda t:-t[1]):
        pts=[(cx*S,cy*S)]+[P(cx,cy,h+t,R*v) for t in [i*0.1-0.5 for i in range(11)]]
        dr.polygon(pts,fill=(255,int(150+90*v),int(60+120*v),95))
im.resize((W,H),Image.LANCZOS).save('preview3.png')
