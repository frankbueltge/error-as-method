import json, numpy as np, math
from PIL import Image, ImageDraw
v=np.array(json.load(open('series.json')))
vs=np.convolve(np.pad(v,1,mode='edge'),np.array([1,2,1])/4,'valid')
W,H=1100,800; cx,cy=430,400
r0,c,a=34,5.0,24
N=len(vs)
def P(i):
    t=i/24.0; r=r0+c*t+a*vs[i]; th=2*math.pi*t-math.pi/2
    return (cx+r*math.cos(th), cy+r*math.sin(th))
pts=[P(i) for i in range(N)]
light=np.array([236,224,204]); dark=np.array([120,78,48])
def col(x):
    x=max(0,min(1,x)); return tuple(int(u) for u in light*x+dark*(1-x))
quads=[]
for i in range(N-25):
    q=[pts[i],pts[i+1],pts[i+25],pts[i+24]]
    val=(vs[i]+vs[i+1]+vs[i+24]+vs[i+25])/4
    quads.append((q,col((val-0.15)/0.8)))
# preview
S=2
im=Image.new('RGB',(W*S,H*S),(243,238,228)); dr=ImageDraw.Draw(im)
for q,cl in quads: dr.polygon([(x*S,y*S) for x,y in q],fill=cl,outline=cl)
dr.line([(x*S,y*S) for x,y in pts],fill=(46,30,20),width=2)
im.save('preview2.png')
# svg
def f(p): return f"{p[0]:.1f},{p[1]:.1f}"
polys=''.join(f'<path d="M{f(q[0])}L{f(q[1])}L{f(q[2])}L{f(q[3])}Z" fill="#{cl[0]:02x}{cl[1]:02x}{cl[2]:02x}" stroke="#{cl[0]:02x}{cl[1]:02x}{cl[2]:02x}" stroke-width=".6"/>' for q,cl in quads)
line="M"+"L".join(f(p) for p in pts)
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sixty-one Rings</title>
<style>
html,body{{margin:0;height:100%;background:#f3eee4}}
body{{display:flex;align-items:center;justify-content:center}}
svg{{display:block;width:100vw;height:100vh;max-width:1100px;max-height:800px}}
</style></head><body>
<svg viewBox="0 0 1100 800" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="An hourly record of 61 days wound into a spiral, one turn per day, read outward like the cross-section of a trunk.">
<rect width="1100" height="800" fill="#f3eee4"/>
<g>{polys}</g>
<path d="{line}" fill="none" stroke="#2e1e14" stroke-width="0.9" stroke-linejoin="round" stroke-linecap="round"/>
<g font-family="Georgia, 'Times New Roman', serif" fill="#3a2a1e">
<text x="862" y="640" font-size="26" letter-spacing="0.5">Sixty-one Rings</text>
<text x="862" y="668" font-size="13" fill="#6b5a4a" font-style="italic">1,464 hours, one turn for each day,</text>
<text x="862" y="686" font-size="13" fill="#6b5a4a" font-style="italic">wound outward from the first.</text>
</g>
</svg>
</body></html>
'''
open('/tmp/claude-0/s131/mk/m06/work/index.html','w').write(html)
print(len(html))
