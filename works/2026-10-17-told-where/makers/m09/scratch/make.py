import json, math, sys
from PIL import Image
src='/tmp/claude-0/s133/mk/m09/work/record.jpg'
im=Image.open(src).convert('L'); px=im.load(); W,H=im.size
pts=json.load(open('/tmp/claude-0/s133/mk/m09/scratch/pts.json'))
CX,CY=550,400
R0=118.0; RMAX=378.0; FLOOR=83.5; TOP=2.0
k=(RMAX-R0)/(FLOOR-TOP)
X0,X1=0.0,297.5
SPAN=354.0   # degrees; the remaining notch at twelve o'clock marks where the record begins and ends
def ang(x): return math.radians(-90+3.0+ (x-X0)/(X1-X0)*SPAN)
def pol(x,r):
  a=ang(x); return CX+r*math.cos(a), CY+r*math.sin(a)
out=[]
# floor: one arc segment per source column, opacity from that column's floor ink
for x in range(W):
  f=max(255-px[x,83],255-px[x,84])
  if f<60: continue
  a0=ang(x-0.5); a1=ang(x+0.5)
  for (rr,sw,op) in ((R0,5.0,f/255*0.95),):
    xa,ya=CX+rr*math.cos(a0),CY+rr*math.sin(a0)
    xb,yb=CX+rr*math.cos(a1),CY+rr*math.sin(a1)
    out.append(f'<path d="M{xa:.2f} {ya:.2f}A{rr} {rr} 0 0 1 {xb:.2f} {yb:.2f}" stroke="var(--ink)" stroke-width="{sw}" stroke-opacity="{op:.2f}" fill="none"/>')
# values above the floor: each detected dot, placed by time (angle) and height (radius)
dots=[p for p in pts if p[2]>=90 and p[1]<81.8]
for x,y,v,s in dots:
  r=R0+(FLOOR-y)*k
  X,Y=pol(x,r)
  h=(FLOOR-y)/(FLOOR-TOP)
  rad=1.7+1.5*min(1,s/900)
  op=0.35+0.6*min(1,v/230)
  # a faint stem from floor to dot: the hour's reach
  Xa,Ya=pol(x,R0+3)
  if False: out.append(f'<line x1="{Xa:.1f}" y1="{Ya:.1f}" x2="{X:.1f}" y2="{Y:.1f}" stroke="var(--stem)" stroke-width="0.6" stroke-opacity="{0.10+0.18*h:.2f}"/>')
  out.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{rad:.2f}" fill="var(--ink)" fill-opacity="{op:.2f}"/>')
# one hairline per day: from the floor to that day's highest value
per=24*(296.0-1.0)/1463; g0=1.16
for d in range(-1,63):
  c=g0+d*per
  b=[q for q in dots if abs(q[0]-c)<=per/2]
  if not b: continue
  x,y,v,s_=min(b,key=lambda q:q[1])
  Xa,Ya=pol(x,R0+4); X,Y=pol(x,R0+(FLOOR-y)*k)
  out.insert(0,f'<line x1="{Xa:.1f}" y1="{Ya:.1f}" x2="{X:.1f}" y2="{Y:.1f}" stroke="var(--stem)" stroke-width="0.9" stroke-opacity="0.55"/>')
print(len(dots),file=sys.stderr)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 800" width="1100" height="800" role="img" aria-label="Sixty-one daily pulses of one measured quantity, wound once around a circle">
<rect width="1100" height="800" fill="var(--paper)"/>
<g>{"".join(o for o in out if o.startswith("<line"))}</g>
<g>{"".join(o for o in out if not o.startswith("<line"))}</g>
</svg>'''
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>One Turn of Days</title>
<style>
:root{{--paper:#f3efe6;--ink:#1f1c18;--stem:#7a5a2e}}
html,body{{margin:0;height:100%;background:var(--paper)}}
body{{display:flex;align-items:center;justify-content:center;overflow:hidden}}
svg{{display:block;width:100vw;height:100vh;max-width:1100px;max-height:800px}}
</style></head><body>
{svg}
</body></html>
'''
open('/tmp/claude-0/s133/mk/m09/work/index.html','w').write(html)
open('/tmp/claude-0/s133/mk/m09/scratch/preview.svg','w').write(svg.replace('var(--paper)','#f3efe6').replace('var(--ink)','#1f1c18').replace('var(--stem)','#7a5a2e'))
