import json, math
from PIL import Image, ImageDraw
d=json.load(open('recon.json')); v=d['vals']; N=len(v)
gm=sum(v)/N
# light smoothing (3-hour) to soften pixel quantisation
s=[(v[max(0,i-1)]+2*v[i]+v[min(N-1,i+1)])/4 for i in range(N)]
def run(a,k):
    out=[]
    for i in range(len(a)):
        w=a[max(0,i-k):i+k+1]; out.append(sum(w)/len(w))
    return out
slow=run(s,12)
fast=[a-b for a,b in zip(s,slow)]
CX,CY=660,400
def cr(a,i,f):
    g=lambda j:a[min(len(a)-1,max(0,j))]
    p0,p1,p2,p3=g(i-1),g(i),g(i+1),g(i+2)
    return 0.5*((2*p1)+(-p0+p2)*f+(2*p0-5*p1+4*p2-p3)*f*f+(-p0+3*p1-3*p2+p3)*f**3)
R0,STEP,K1,K2=40,4.6,0.7,2.4
SUB=4
pts=[]
for i in range(N*SUB):
    t=i/SUB
    i0=int(t); f=t-i0; i1=min(N-1,i0+1)
    sl=cr(slow,i0,f); fa=cr(fast,i0,f)
    # angle: day starts at top, clockwise
    a=-math.pi/2+2*math.pi*(t/24)
    r=R0+STEP*(t/24)+K1*(sl-gm)+K2*fa
    r=max(6,r)
    pts.append((CX+r*math.cos(a),CY+r*math.sin(a)))
json.dump(pts,open('pts.json','w'))
rs=[math.hypot(x-CX,y-CY) for x,y in pts]; print('rmax',max(rs),'rmin',min(rs))
# preview
S=2
im=Image.new('RGB',(1100*S,800*S),(242,238,230)); dr=ImageDraw.Draw(im)
dr.line([(x*S,y*S) for x,y in pts],fill=(40,36,34),width=1*S)
im.resize((1100,800),Image.LANCZOS).save('preview.png')

# ---- variable-weight version + SVG ----
lo=min(s); hi=max(s)
def norm(i):
    t=i/SUB; i0=int(t); f=t-i0; i1=min(N-1,i0+1)
    return min(1,max(0,(cr(s,i0,f)-lo)/(hi-lo)))
segs=[]
for i in range(0,len(pts)-1):
    n=norm(i)
    w=0.45+3.2*n**1.6
    a=0.38+0.6*n**0.8
    segs.append((pts[i],pts[i+1],w,a))
S=3
im=Image.new('RGB',(1100*S,800*S),(242,238,230)); dr=ImageDraw.Draw(im,'RGBA')
for p,q,w,a in segs:
    dr.line([(p[0]*S,p[1]*S),(q[0]*S,q[1]*S)],fill=(34,30,30,int(255*a)),width=max(1,round(w*S)))
im.resize((1100,800),Image.LANCZOS).save('preview2.png')
# group consecutive runs into paths by quantised class
paths=[]
cur=None
for p,q,w,a in segs:
    k=(round(w*4)/4, round(a*20)/20)
    if cur and cur[0]==k:
        cur[1].append(q)
    else:
        if cur: paths.append(cur)
        cur=[k,[p,q]]
paths.append(cur)
out=[]
for (w,a),ps in paths:
    dd='M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in ps)
    out.append(f'<path d="{dd}" stroke-width="{w}" stroke-opacity="{a}"/>')
open('paths.svgfrag','w').write('\n'.join(out))
print(len(paths), sum(len(o) for o in out))
