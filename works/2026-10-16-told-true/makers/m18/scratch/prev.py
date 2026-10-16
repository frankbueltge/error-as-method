import json
from PIL import Image, ImageDraw
ys=json.load(open('ys.json')); V=[round(90-y,1) for y in ys]
X0,X1,TOP,BOT,D,Hh,V0,K=300,900,170,760,61,24,17,2.0
step=(BOT-TOP)/(D-1); dx=(X1-X0)/(Hh-1); S=2
im=Image.new('RGB',(1100*S,800*S),(243,239,230)); dr=ImageDraw.Draw(im)
def curve(p):
    out=[]
    for i in range(len(p)-1):
        p0=p[i-1] if i>0 else p[i]; p1=p[i]; p2=p[i+1]; p3=p[i+2] if i+2<len(p) else p2
        c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6); c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
        for k in range(12):
            t=k/12; a=(1-t)**3; b=3*(1-t)**2*t; c=3*(1-t)*t*t; e=t**3
            out.append((S*(a*p1[0]+b*c1[0]+c*c2[0]+e*p2[0]),S*(a*p1[1]+b*c1[1]+c*c2[1]+e*p2[1])))
    out.append((S*p[-1][0],S*p[-1][1])); return out
for d in range(D):
    base=TOP+d*step; pts=[(X0+h*dx,base-(V[d*Hh+h]-V0)*K) for h in range(Hh)]
    c=curve(pts)
    dr.polygon(c+[(X1*S,(base+24)*S),(X0*S,(base+24)*S)],fill=(243,239,230))
    dr.line(c,fill=(29,27,24),width=2)
    for x,y in pts: dr.ellipse((S*x-2.3,S*y-2.3,S*x+2.3,S*y+2.3),fill=(29,27,24))
im.resize((1100,800),Image.LANCZOS).save('preview.png')
