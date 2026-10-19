from PIL import Image, ImageDraw, ImageFilter
import math
V=[int(x) for x in open('/tmp/claude-0/s137/mk/m01/scratch/data.txt').read().strip().split(',')]
stops=[(0,(38,30,27)),(0.12,(70,34,26)),(0.3,(128,38,22)),(0.5,(196,72,24)),(0.7,(234,136,44)),(0.88,(248,200,120)),(1,(255,240,205))]
def col(t):
    t=max(0,min(1,t))
    for i in range(1,len(stops)):
        if t<=stops[i][0]:
            a,ca=stops[i-1];b,cb=stops[i];f=(t-a)/(b-a);return tuple(round(c+(cb[j]-c)*f) for j,c in enumerate(ca))
    return (255,240,205)
W,H,cx,cy=1100,800,600,392
im=Image.new('RGB',(W,H),(13,11,10));d=ImageDraw.Draw(im)
N=len(V);R0,R1=372,34;pitch=(R0-R1)/(N/24);band=pitch*0.82;PH=22
ang=lambda h:-math.pi/2+((h-PH)/24)*2*math.pi
for h in range(N):
    a0,a1=ang(h),ang(h+1)+0.004;r=R0-(h/24)*pitch;r2=R0-((h+1)/24)*pitch
    pts=[];st=4
    for k in range(st+1):
        f=k/st;a=a0+(a1-a0)*f;rr=r+(r2-r)*f;pts.append((cx+math.cos(a)*rr,cy+math.sin(a)*rr))
    for k in range(st,-1,-1):
        f=k/st;a=a0+(a1-a0)*f;rr=r+(r2-r)*f-band;pts.append((cx+math.cos(a)*rr,cy+math.sin(a)*rr))
    d.polygon(pts,fill=col((V[h]/100)**0.9))
im.save('/tmp/claude-0/s137/mk/m01/scratch/prev.png')
