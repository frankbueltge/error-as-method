import json
from PIL import Image, ImageDraw
ys=json.load(open('ys.json')); V=[round(90-y,1) for y in ys]
X0,X1,TOP,BOT,D,Hh,K=330,930,190,758,61,24,1.7
step=(BOT-TOP)/(D-1); dx=(X1-X0)/(Hh-1)
PAPER='#f3efe6'; INK='#1d1b18'; FAINT='#867f73'
f=lambda n:('%.1f'%n).rstrip('0').rstrip('.')
def ctrl(p):
    segs=[]
    for i in range(len(p)-1):
        p0=p[i-1] if i>0 else p[i]; p1=p[i]; p2=p[i+1]; p3=p[i+2] if i+2<len(p) else p2
        segs.append((p1,(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6),(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6),p2))
    return segs
def svgpath(segs):
    s="M%s,%s"%(f(segs[0][0][0]),f(segs[0][0][1]))
    for _,c1,c2,p2 in segs: s+="C%s,%s %s,%s %s,%s"%tuple(map(f,(*c1,*c2,*p2)))
    return s
def poly(segs,S):
    out=[]
    for p1,c1,c2,p2 in segs:
        for k in range(12):
            t=k/12;a=(1-t)**3;b=3*(1-t)**2*t;c=3*(1-t)*t*t;e=t**3
            out.append((S*(a*p1[0]+b*c1[0]+c*c2[0]+e*p2[0]),S*(a*p1[1]+b*c1[1]+c*c2[1]+e*p2[1])))
    out.append((S*segs[-1][3][0],S*segs[-1][3][1])); return out
mins=[min(V[d*Hh:(d+1)*Hh]) for d in range(D)]
lo,hi=min(mins),max(mins)
# floor trace at left: x from 150 to 250
TX0,TX1=180,262
fx=lambda m:TX0+(m-lo)/(hi-lo)*(TX1-TX0)
S=2
im=Image.new('RGB',(1100*S,800*S),PAPER); dr=ImageDraw.Draw(im)
rows=[]; tr=[]
for d in range(D):
    base=TOP+d*step; m=mins[d]
    pts=[(X0+h*dx,base-(V[d*Hh+h]-m)*K) for h in range(Hh)]
    segs=ctrl(pts); p=svgpath(segs)
    dots="".join('<circle cx="%s" cy="%s" r="0.95"/>'%(f(x),f(y)) for x,y in pts)
    rows.append('<path class="m" d="%sL%s,%sL%s,%sZ"/><path class="l" d="%s"/>%s'%(p,X1,f(base+6),X0,f(base+6),p,dots))
    pl=poly(segs,S)
    dr.polygon(pl+[(X1*S,(base+6)*S),(X0*S,(base+6)*S)],fill=PAPER)
    dr.line(pl,fill=INK,width=2)
    for x,y in pts: dr.ellipse((S*x-1.9,S*y-1.9,S*x+1.9,S*y+1.9),fill=INK)
    tr.append((fx(m),base))
# trace
trs="M"+" L".join("%s,%s"%(f(x),f(y)) for x,y in tr)
trdots="".join('<circle cx="%s" cy="%s" r="1.6"/>'%(f(x),f(y)) for x,y in tr)
dr.line([(x*S,y*S) for x,y in tr],fill=FAINT,width=2)
for x,y in tr: dr.ellipse((S*x-3,S*y-3,S*x+3,S*y+3),fill=INK)
for d in range(D):
    y=(TOP+d*step)*S; dr.line([(278*S,y),(X0*S-10,y)],fill=(214,208,196),width=1)
im.resize((1100,800),Image.LANCZOS).save('preview3.png')
guides="".join('<line x1="278" y1="%s" x2="%s" y2="%s"/>'%(f(TOP+d*step),X0-5,f(TOP+d*step)) for d in range(D))
svg='''<svg viewBox="0 0 1100 800" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Sixty-one stacked daily curves of hourly carbon dioxide">
<style>
.m{fill:%(P)s}.l{fill:none;stroke:%(I)s;stroke-width:1;stroke-linejoin:round}
circle{fill:%(I)s}
.g line{stroke:#d6d0c4;stroke-width:.6}
.t{fill:none;stroke:%(F)s;stroke-width:.9}
text{font-family:Georgia,"Times New Roman",serif;fill:%(I)s}
.cap{fill:%(F)s;font-size:11.5px;letter-spacing:.02em}
</style>
<rect width="1100" height="800" fill="%(P)s"/>
<text x="64" y="62" font-size="26">Sixty-One Breaths</text>
<text class="cap" x="64" y="88">Carbon dioxide in the air at one station, hour by hour.</text>
<text class="cap" x="64" y="106">Each line is one day, its twenty-four hours left to right, rising from that day's lowest hour.</text>
<text class="cap" x="64" y="124">The thin trace at left follows those lowest hours: further right, higher.</text>
<text class="cap" x="64" y="778">First day at the top, sixty-first at the foot. Heights are relative; the record carried no scale.</text>
<g class="g">%(G)s</g>
<path class="t" d="%(T)s"/>%(TD)s
%(R)s
</svg>'''%dict(P=PAPER,I=INK,F=FAINT,G=guides,T=trs,TD=trdots,R="\n".join(rows))
html='''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sixty-One Breaths</title>
<style>
html,body{margin:0;height:100%%;background:%s}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
svg{width:100vw;height:100vh;max-width:1100px;max-height:800px;display:block}
</style></head><body>
%s
</body></html>
'''%(PAPER,svg)
open('/tmp/claude-0/s130/mk/m18/work/index.html','w').write(html)
print(round(lo,1),round(hi,1))
