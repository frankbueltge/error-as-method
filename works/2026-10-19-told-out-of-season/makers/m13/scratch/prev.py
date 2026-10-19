import json,sys
from PIL import Image, ImageDraw
V=json.load(open('/tmp/claude-0/s137/mk/m13/scratch/hourly.json'))
L,R,TOP,STEP,AMP,OFF=[float(a) for a in sys.argv[1:7]];OFF=int(OFF)
S=2;im=Image.new('RGB',(1100*S,800*S),(19,17,16));d=ImageDraw.Draw(im)
rows=-(-(len(V)+OFF)//24)
def col(v):
    a=(112,122,132);b=(226,205,178);e=(236,128,62)
    if v<.5: t=v/.5;return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
    t=(v-.5)/.5;return tuple(int(b[i]+(e[i]-b[i])*t) for i in range(3))
for r in range(rows):
    base=TOP+r*STEP;pts=[]
    for h in range(25):
        i=r*24+h-OFF
        if 0<=i<len(V): pts.append((L+(R-L)*h/24,base-V[i]*AMP,V[i]))
    if len(pts)<2: continue
    poly=[(pts[0][0]*S,(base+STEP*3)*S)]+[(p[0]*S,p[1]*S) for p in pts]+[(pts[-1][0]*S,(base+STEP*3)*S)]
    d.polygon(poly,fill=(19,17,16))
    for p,q in zip(pts,pts[1:]):
        d.line([p[0]*S,p[1]*S,q[0]*S,q[1]*S],fill=col((p[2]+q[2])/2),width=3)
print(rows, TOP+rows*STEP)
im.resize((1100,800),Image.LANCZOS).save(sys.argv[7])
