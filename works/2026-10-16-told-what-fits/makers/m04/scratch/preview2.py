import json
from PIL import Image, ImageDraw, ImageFont
V=json.load(open('vals.json')); SC=3
im=Image.new('RGB',(1100*SC,800*SC),(242,238,229)); g=ImageDraw.Draw(im)
L,R,TOP,STEP,S=170,1010,150,9.4,8.9/83
hx=lambda h:L+(R-L)*h/23
def cr(pts,n=10):
    out=[]
    for i in range(len(pts)-1):
        p0=pts[max(0,i-1)];p1=pts[i];p2=pts[i+1];p3=pts[min(len(pts)-1,i+2)]
        for k in range(n):
            t=k/n
            out.append(tuple(0.5*((2*p1[j])+(-p0[j]+p2[j])*t+(2*p0[j]-5*p1[j]+4*p2[j]-p3[j])*t*t+(-p0[j]+3*p1[j]-3*p2[j]+p3[j])*t**3) for j in (0,1)))
    out.append(pts[-1]); return out
for d in range(61):
    cy=TOP+d*STEP
    up=[(hx(h),cy-max(.6,V[d*24+h]/10*S)/2) for h in range(24)]
    dn=[(hx(h),cy+max(.6,V[d*24+h]/10*S)/2) for h in range(24)][::-1]
    g.polygon([(x*SC,y*SC) for x,y in cr(up)+cr(dn)],fill=(31,28,24))
for i,v in enumerate(V):
    x=L+(R-L)*i/1463; y=776-(v/10)/85*30; g.rectangle([x*SC,y*SC,(x+.7)*SC,(y+.7)*SC],fill=(130,125,118))
g.text((70*SC,40*SC),"The Day Takes",fill=(31,28,24),font=ImageFont.load_default(28*SC) if hasattr(ImageFont,'load_default') else None)
im.resize((1100,800),Image.LANCZOS).save('preview2.png')
