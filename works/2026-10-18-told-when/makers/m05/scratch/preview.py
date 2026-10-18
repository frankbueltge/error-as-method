from PIL import Image, ImageDraw
import json, math
runs=json.load(open('runs.json'))
S=2;W,H=1100,800
im=Image.new('RGB',(W*S,H*S),(242,237,227)); d=ImageDraw.Draw(im,'RGBA')
N=1464;LV=18
R=min(H/2-22,W/2-60); ox=W-R-40 if max(R+330,W/2+120)>W-R-30 else W/2+120; oy=H/2
R0=R*0.2; s=(R-R0)/LV
rad=lambda L,t:R0+(LV-L)*s-(t/N)*s*0.92
ang=lambda t:-math.pi/2+(t%24)/24*2*math.pi
stops=[(0,(180,83,42)),(.25,(201,138,58)),(.5,(125,138,106)),(.75,(63,111,143)),(1,(40,62,107))]
def col(f):
    i=0
    while i<len(stops)-2 and f>stops[i+1][0]: i+=1
    f0,c0=stops[i];f1,c1=stops[i+1];u=min(1,max(0,(f-f0)/(f1-f0)))
    return tuple(round(v+(c1[k]-v)*u) for k,v in enumerate(c0))
for L in range(LV+1):
    r=(R0+(LV-L)*s)*S; d.ellipse([ox*S-r,oy*S-r,ox*S+r,oy*S+r],outline=(60,50,40,26))
for L,a,b in sorted(runs,key=lambda r:r[1]):
    c=col((a+b)/2/N); pts=[]; t=a
    while t<=b: pts.append(((ox+rad(L,t)*math.cos(ang(t)))*S,(oy+rad(L,t)*math.sin(ang(t)))*S)); t+=0.1
    if len(pts)>1: d.line(pts,fill=c+(215,),width=3)
    else: d.ellipse([pts[0][0]-1.5,pts[0][1]-1.5,pts[0][0]+1.5,pts[0][1]+1.5],fill=c)
im.resize((W,H),Image.LANCZOS).save('preview.png')
print(ox,R)
