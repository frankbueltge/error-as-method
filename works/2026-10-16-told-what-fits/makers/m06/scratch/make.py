import json, numpy as np, math
from PIL import Image, ImageDraw
v=np.array(json.load(open('series.json')))
k=np.array([1,2,1])/4; vs=np.convolve(np.pad(v,1,mode='edge'),k,'valid')
W,H=1100,800; cx,cy=470,400
r0,c,a=34,5.0,24
pts=[]
for i,val in enumerate(vs):
    t=i/24.0
    r=r0+c*t+a*val
    th=2*math.pi*t - math.pi/2
    pts.append((cx+r*math.cos(th), cy+r*math.sin(th)))
# densify via Catmull-Rom for smoother path in SVG: use quadratic smoothing through midpoints
def path(p):
    s=f"M{p[0][0]:.1f},{p[0][1]:.1f}"
    for j in range(1,len(p)-1):
        mx=(p[j][0]+p[j+1][0])/2; my=(p[j][1]+p[j+1][1])/2
        s+=f"Q{p[j][0]:.1f},{p[j][1]:.1f} {mx:.1f},{my:.1f}"
    s+=f"L{p[-1][0]:.1f},{p[-1][1]:.1f}"
    return s
# split into day segments to tone them
segs=[]
for d in range(61):
    p=pts[d*24:min(len(pts),d*24+25)]
    segs.append((path(p), float(vs[d*24:d*24+24].mean())))
json.dump({'segs':segs},open('segs.json','w'))
# preview
im=Image.new('RGB',(W*2,H*2),(243,238,228)); dr=ImageDraw.Draw(im)
dr.line([(x*2,y*2) for x,y in pts],fill=(52,36,26),width=2)
im.save('preview.png')
print(max(math.hypot(x-cx,y-cy) for x,y in pts))
