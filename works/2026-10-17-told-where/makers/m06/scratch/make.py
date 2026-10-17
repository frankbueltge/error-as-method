import json, math
d=json.load(open('/tmp/claude-0/s133/mk/m06/scratch/data.json'))['days']
W,H=1100,800
COLS=8; X0=40; CW=(W-2*X0)/COLS; Y0=104; RH=78; R=58
def P(cx,cy,h,r):
    a=2*math.pi*h/24; return cx-r*math.sin(a), cy+r*math.cos(a)
def lerp(a,b,t): return tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))
lo=(196,92,28); mid=(246,170,70); hi=(255,244,214)
def col(v):
    c=lerp(lo,mid,v/0.5) if v<0.5 else lerp(mid,hi,(v-0.5)/0.5)
    return '#%02x%02x%02x'%c
cells=[]
for k,day in enumerate(d):
    c=k%COLS; r=k//COLS
    cx=X0+CW*(c+0.5); cy=Y0+RH*r+64
    g=[f'<path class="g" d="M{cx-R-6:.1f},{cy:.1f}H{cx+R+6:.1f}M{cx-R:.1f},{cy:.1f}A{R},{R} 0 0 1 {cx+R:.1f},{cy:.1f}"/>']
    for h,v in sorted(day,key=lambda t:-t[1]):
        rr=R*v
        if rr<0.6: rr=0.6
        x1,y1=P(cx,cy,h-0.5,rr); x2,y2=P(cx,cy,h+0.5,rr)
        g.append(f'<path d="M{cx:.1f},{cy:.1f}L{x1:.1f},{y1:.1f}A{rr:.1f},{rr:.1f} 0 0 1 {x2:.1f},{y2:.1f}Z" fill="{col(v)}"/>')
    cells.append('<g class="d">'+''.join(g)+'</g>')
L=X0+CW*0.5-R
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Sixty-one days of sunlight as rows of rising fans, one per day; each hour is a fifteen-degree wedge whose length is that hour's light. The fans are wide and long early on and grow narrower and shorter toward the end.">
<rect width="{W}" height="{H}" fill="#0b0e14"/>
<text x="{L:.1f}" y="58" class="t">Sixty-One Suns</text>
<text x="{W-L:.1f}" y="58" class="s" text-anchor="end">each day a half-dial · each hour a 15° wedge, as far out as that hour’s light reached</text>
{''.join(cells)}
<text x="{L:.1f}" y="{H-26}" class="s">The record opens on a late afternoon (first dial) and closes on an afternoon sixty-one days on (last). Read left to right, row by row.</text>
</svg>'''
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sixty-One Suns</title>
<style>
html,body{{margin:0;height:100%;background:#0b0e14}}
body{{display:flex;align-items:center;justify-content:center;overflow:hidden}}
svg{{display:block;width:100vw;height:100vh}}
.d path{{fill-opacity:.5;mix-blend-mode:screen}}
.d path.g{{fill:none;stroke:#ffffff;stroke-opacity:.11;stroke-width:.8;mix-blend-mode:normal}}
.d{{isolation:isolate}}
.t{{font:400 27px Georgia,"Times New Roman",serif;fill:#f2e4c6;letter-spacing:.4px}}
.s{{font:italic 400 12.5px Georgia,"Times New Roman",serif;fill:#8c877d}}
</style></head><body>
{svg}
</body></html>
'''
open('/tmp/claude-0/s133/mk/m06/work/index.html','w').write(html)
print(len(html))
