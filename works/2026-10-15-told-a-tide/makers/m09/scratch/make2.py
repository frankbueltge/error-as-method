import math, json, numpy as np
v=np.array(json.load(open('/tmp/claude-0/s128/mk/m09/scratch/hourly.json'))['v'])
N=len(v)
vref=float(np.median(v))
CX,CY=550,404
R0,SP,K=46,4.9,0.75
def pos(t,val):
    r=R0+SP*t/24.0+(val-vref)*K
    a=2*math.pi*(t%24)/24-math.pi/2
    return CX+r*math.cos(a), CY+r*math.sin(a)
pts=[pos(t,v[t]) for t in range(N)]
line='M'+' L'.join('%.1f %.1f'%p for p in pts)
lows=[d*24+int(np.argmin(v[d*24:d*24+24])) for d in range(N//24)]
lowdots=''.join('<circle cx="%.1f" cy="%.1f" r="3"/>'%pts[t] for t in lows)
dots=''.join('<circle cx="%.1f" cy="%.1f" r="1.25"/>'%p for p in pts)
# first observed low (within the first day)
t0=int(np.argmin(v[:24]))
ghost=[]
t=float(t0)
while t<=N-1:
    a=2*math.pi*(t%24)/24-math.pi/2
    r=R0+SP*t/24.0+(v[t0]-vref)*K
    ghost.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'%(CX+(r-4)*math.cos(a),CY+(r-4)*math.sin(a),CX+(r+4)*math.cos(a),CY+(r+4)*math.sin(a)))
    t+=12.4206
F="Georgia, 'Times New Roman', serif"
svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 800" width="1100" height="800">
<rect width="1100" height="800" fill="#f3efe6"/>
<path d="%s" fill="none" stroke="#1c1b19" stroke-width="0.7" stroke-opacity="0.55" stroke-linejoin="round"/>
<g fill="#1c1b19">%s</g>
<g fill="#1c1b19">%s</g>
<g stroke="#b4442c" stroke-width="1.4" stroke-linecap="round">%s</g>
<g font-family="%s" fill="#1c1b19">
<text x="48" y="78" font-size="30">Told a Tide</text>
<text x="48" y="106" font-size="14" fill="#6a655b" font-style="italic">1,464 hours wound one turn to a day</text>
<text font-size="12.5" fill="#5a564e"><tspan x="44" y="686">Hour by hour from the centre outward,</tspan><tspan x="44" dy="18">one turn to a day, sixty-one turns.</tspan><tspan x="44" dy="18">Higher readings stand further out.</tspan><tspan x="44" dy="18"><tspan fill="#1c1b19">&#9679;</tspan> the lowest hour of each day.</tspan></text>
<text font-size="12.5" fill="#5a564e" text-anchor="end"><tspan x="1056" y="686"><tspan fill="#b4442c">&#8212;</tspan> where the lows would fall if they</tspan><tspan x="1056" dy="18">kept the moon&#8217;s time, 12 h 25 min apart,</tspan><tspan x="1056" dy="18">counted on from the first low recorded.</tspan><tspan x="1056" dy="18">The lows that came kept to one side.</tspan></text>
</g>
</svg>'''%(line,dots,lowdots,''.join(ghost),F)
open('/tmp/claude-0/s128/mk/m09/scratch/work.svg','w').write(svg)
html='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Told a Tide</title>
<style>html,body{margin:0;height:100%%;background:#f3efe6}body{display:flex;align-items:center;justify-content:center;overflow:hidden}svg{display:block;width:100%%;height:100%%;max-width:1100px;max-height:800px}</style>
</head><body>
%s
</body></html>'''%svg.replace(' width="1100" height="800"',' preserveAspectRatio="xMidYMid meet"',1)
open('/tmp/claude-0/s128/mk/m09/work/index.html','w').write(html)
# preview
from PIL import Image, ImageDraw
S=2; im=Image.new('RGBA',(1100*S,800*S),(243,239,230,255)); ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
d.line([(x*S,y*S) for x,y in pts],fill=(28,27,25,140),width=2)
for t in lows:
    x,y=pts[t]; d.ellipse([x*S-6,y*S-6,x*S+6,y*S+6],fill=(28,27,25,255))
for x,y in pts: d.ellipse([x*S-2.5,y*S-2.5,x*S+2.5,y*S+2.5],fill=(28,27,25,255))
im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
import re
for m in re.finditer(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)"',svg):
    d.line([float(q)*S for q in m.groups()],fill=(180,68,44),width=3)
d.text((48*S,60*S),"Told a Tide (preview, text approximate)",fill=(0,0,0))
d.rectangle([44*S,674*S,300*S,750*S],outline=(200,190,180)); d.rectangle([790*S,674*S,1056*S,750*S],outline=(200,190,180))
im.convert('RGB').resize((1100,800),Image.LANCZOS).save('/tmp/claude-0/s128/mk/m09/scratch/preview2.png')
print(t0, len(ghost), len(svg))
