import json
from PIL import Image, ImageDraw
V=json.load(open('vals.json')); SC=2
im=Image.new('RGB',(1100*SC,800*SC),(242,238,229)); g=ImageDraw.Draw(im)
L,R,TOP,STEP,S=170,1010,196,8.25,0.92
hx=lambda h:L+(R-L)*h/23
def cr(pts,n=8):
    out=[]
    for i in range(len(pts)-1):
        p0=pts[max(0,i-1)];p1=pts[i];p2=pts[i+1];p3=pts[min(len(pts)-1,i+2)]
        for k in range(n):
            t=k/n
            out.append(tuple(0.5*((2*p1[j])+(-p0[j]+p2[j])*t+(2*p0[j]-5*p1[j]+4*p2[j]-p3[j])*t*t+(-p0[j]+3*p1[j]-3*p2[j]+p3[j])*t**3) for j in (0,1)))
    out.append(pts[-1]); return out
for d in range(61):
    base=TOP+d*STEP; vs=[V[d*24+h]/10 for h in range(24)]
    q=max(vs)-min(vs)<16; col=(168,67,42) if q else (31,28,24)
    pts=[(hx(h),base-vs[h]*S) for h in range(24)]; c=cr(pts)
    poly=[(x*SC,y*SC) for x,y in c]+[(R*SC,(base+2)*SC),(L*SC,(base+2)*SC)]
    g.polygon(poly,fill=(242,238,229))
    g.line([(x*SC,y*SC) for x,y in c],fill=col,width=3 if q else 2)
    for x,y in pts: g.ellipse([(x-1.35)*SC,(y-1.35)*SC,(x+1.35)*SC,(y+1.35)*SC],fill=col)
for i,v in enumerate(V):
    x=L+(R-L)*i/1463; y=772-(v/10)/85*34; g.rectangle([x*SC,y*SC,(x+.7)*SC,(y+.7)*SC],fill=(130,125,118))
im.resize((1100,800),Image.LANCZOS).save('preview.png')
