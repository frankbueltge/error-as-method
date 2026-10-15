import math, numpy as np
from PIL import Image
im=np.asarray(Image.open('/tmp/claude-0/s128/mk/m09/work/record.jpg').convert('L')).astype(float)
H,W=im.shape
ink=np.clip(255-im-28,0,None)   # suppress jpeg haze
X0,X1=3.0,297.0      # centres of first / last hour, estimated from the ink extent
NH=1463.0
def t_of(x): return (x-X0)/(X1-X0)*NH   # hours since first value
# reference level: the typical (median) height of ink
ys,xs=np.nonzero(ink>60)
yref=float(np.median(ys))
CX,CY=550,412
R0,SP,K=52,5.05,0.42   # inner radius, spacing per day, px per image row
def base(t): return R0+SP*t/24.0
def pol(t,r):
    a=2*math.pi*(t%24)/24-math.pi/2
    return CX+r*math.cos(a), CY+r*math.sin(a)
paths=[]
for x in range(W):
    for y in range(H):
        v=ink[y,x]
        if v<=8: continue
        ta,tb=t_of(x-0.5),t_of(x+0.5)
        ta=max(ta,-0.5); tb=min(tb,NH+0.5)
        if tb<=ta: continue
        off=(yref-y)*K
        n=6
        pts=[pol(ta+(tb-ta)*i/n, base(ta+(tb-ta)*i/n)+off) for i in range(n+1)]
        d='M'+' L'.join('%.1f %.1f'%p for p in pts)
        op=min(1,v/200)*0.55
        paths.append('<path d="%s" stroke-opacity="%.2f"/>'%(d,op))
# ghost: where low water would come back if the rhythm were the moon's (12.42 h), anchored to the first observed daily low
# find first daily low: column of max mean y in first day
first=None;best=-1
for x in range(3,9):
    col=ink[:,x]
    if col.sum()==0: continue
    lowest=max(np.nonzero(col>60)[0]) if (col>60).any() else 0
    if lowest>best: best=lowest;first=x
t0=t_of(first)
ghost=[]
t=t0
while t<=NH:
    r=base(t)-(best-yref)*K
    a=2*math.pi*(t%24)/24-math.pi/2
    r1,r2=r-3.2,r+3.2
    ghost.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'%(CX+r1*math.cos(a),CY+r1*math.sin(a),CX+r2*math.cos(a),CY+r2*math.sin(a)))
    t+=12.42
# same anchor, the sun's rhythm: one low every 24 h
sun=[]
t=t0
while t<=NH:
    r=base(t)-(best-yref)*K
    a=2*math.pi*(t%24)/24-math.pi/2
    sun.append((CX+(r)*math.cos(a),CY+(r)*math.sin(a)))
    t+=24
print(len(paths),'paths; first low col',first,'t0',t0,'yref',yref)
svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 800" width="1100" height="800">
<rect width="1100" height="800" fill="#f3efe6"/>
<g fill="none" stroke="#1c1b19" stroke-width="1.15" stroke-linecap="round">%s</g>
<g stroke="#b4442c" stroke-width="1.1" stroke-opacity="0.85">%s</g>
<g font-family="Georgia, 'Times New Roman', serif" fill="#1c1b19">
<text x="56" y="86" font-size="30" letter-spacing="0.5">Told a Tide</text>
<text x="56" y="116" font-size="14" fill="#5a564e" font-style="italic">sixty-one days, one turn per day</text>
<text x="56" y="660" font-size="13" fill="#5a564e"><tspan x="56" dy="0">Each hour of the record is wound onto a spiral</tspan><tspan x="56" dy="19">that turns once in twenty-four hours, starting</tspan><tspan x="56" dy="19">at the centre. Higher water pushes outward.</tspan><tspan x="56" dy="19">Each mark is as long as the hours it might be;</tspan><tspan x="56" dy="19">the picture it came from could not say which.</tspan></text>
<text x="1044" y="660" font-size="13" fill="#5a564e" text-anchor="end"><tspan x="1044" dy="0"><tspan fill="#b4442c">|</tspan>  where the lows would fall if they</tspan><tspan x="1044" dy="19">kept the moon's time, 12 h 25 min apart,</tspan><tspan x="1044" dy="19">set going from the first low seen.</tspan><tspan x="1044" dy="19">The lows that came kept the sun's:</tspan><tspan x="1044" dy="19">once a day, in the same place.</tspan></text>
</g>
</svg>'''%(''.join(paths),''.join(ghost))
open('/tmp/claude-0/s128/mk/m09/scratch/work.svg','w').write(svg)
html='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Told a Tide</title>
<style>html,body{margin:0;height:100%%;background:#f3efe6}body{display:flex;align-items:center;justify-content:center}svg{display:block;width:100vw;height:100vh;max-width:1100px;max-height:800px}</style>
</head><body>
%s
</body></html>'''%svg.replace('width="1100" height="800"','preserveAspectRatio="xMidYMid meet"',1)
open('/tmp/claude-0/s128/mk/m09/work/index.html','w').write(html)
