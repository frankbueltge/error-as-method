import json
from PIL import Image, ImageDraw
exec(open('make.py').read().split("out=[]")[0])
S=2
im=Image.new('RGB',(W*S,H*S),paper); dr=ImageDraw.Draw(im)
def cr(pts):
    o=[]
    for i in range(len(pts)-1):
        p0=pts[max(i-1,0)];p1=pts[i];p2=pts[i+1];p3=pts[min(i+2,len(pts)-1)]
        c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6); c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
        for k in range(8):
            t=k/8; a=(1-t)**3;b=3*(1-t)**2*t;c=3*(1-t)*t*t;e=t**3
            o.append(((a*p1[0]+b*c1[0]+c*c2[0]+e*p2[0])*S,(a*p1[1]+b*c1[1]+c*c2[1]+e*p2[1])*S))
    o.append((pts[-1][0]*S,pts[-1][1]*S)); return o
for d in range(rows):
    base=top+d*dy; seg=v[d*24:d*24+48]
    pts=[(xs(i),base-amp*(val-6)) for i,val in enumerate(seg)]
    pl=cr(pts)
    dr.polygon(pl+[(pl[-1][0],(base+2)*S),(pl[0][0],(base+2)*S)],fill=paper)
    dr.line(pl,fill=ink,width=2)
im.resize((W,H),Image.LANCZOS).save('preview.png')
