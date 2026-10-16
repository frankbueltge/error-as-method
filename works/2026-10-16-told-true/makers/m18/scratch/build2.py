import json
ys=json.load(open('ys.json'))
V=[round(90-y,1) for y in ys]
X0,X1,TOP,BOT,D,Hh,V0,K=300,900,170,760,61,24,17,2.0
step=(BOT-TOP)/(D-1); dx=(X1-X0)/(Hh-1)
f=lambda n:('%.1f'%n).rstrip('0').rstrip('.')
def path(p):
    s="M%s,%s"%(f(p[0][0]),f(p[0][1]))
    for i in range(len(p)-1):
        p0=p[i-1] if i>0 else p[i]; p1=p[i]; p2=p[i+1]; p3=p[i+2] if i+2<len(p) else p2
        c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6)
        c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
        s+="C%s,%s %s,%s %s,%s"%tuple(map(f,(*c1,*c2,*p2)))
    return s
rows=[]
for d in range(D):
    base=TOP+d*step
    pts=[(X0+h*dx,base-(V[d*Hh+h]-V0)*K) for h in range(Hh)]
    ln=path(pts)
    dots="".join('<circle cx="%s" cy="%s" r="1.15"/>'%(f(x),f(y)) for x,y in pts)
    rows.append('<g><path class="m" d="%sL%s,%sL%s,%sZ"/><path class="l" d="%s"/>%s</g>'%(ln,X1,f(base+24),X0,f(base+24),ln,dots))
svg='''<svg viewBox="0 0 1100 800" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">
<style>
.m{fill:#f3efe6}.l{fill:none;stroke:#1d1b18;stroke-width:1.05;stroke-linejoin:round}
circle{fill:#1d1b18}
text{font-family:Georgia,"Times New Roman",serif;fill:#1d1b18}
.cap{fill:#867f73;font-size:11.5px;letter-spacing:.02em}
</style>
<rect width="1100" height="800" fill="#f3efe6"/>
<text x="64" y="86" font-size="26">Sixty-One Breaths</text>
<text class="cap" x="64" y="112">carbon dioxide in the air at one station</text>
<text class="cap" x="64" y="130">one line for each day, one point for each hour</text>
<text class="cap" x="64" y="742">The first day is at the top, the sixty-first at the foot.</text>
<text class="cap" x="64" y="760">Heights are relative: the record carried no scale.</text>
%s
</svg>'''%"\n".join(rows)
open('preview.svg','w').write(svg)
html='''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sixty-One Breaths</title>
<style>
html,body{margin:0;height:100%%;background:#f3efe6}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
svg{width:100vw;height:100vh;max-width:1100px;max-height:800px;display:block}
</style></head><body>
%s
</body></html>
'''%svg
open('/tmp/claude-0/s130/mk/m18/work/index.html','w').write(html)
