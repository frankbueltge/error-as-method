from PIL import Image
import math
im=Image.open('/tmp/claude-0/s122/mk/m06/work/record.jpg').convert('L')
W,H=im.size
px=[[im.getpixel((x,y)) for x in range(W)] for y in range(H)]
N=1464
# hours per column: hour h -> column floor(h*W/N)
hours=[0]*W
for h in range(N): hours[h*W//N]+=1
NOISE=30  # JPEG ringing floor: lighter than 225 counts as paper
counts=[[0]*W for _ in range(H)]
for x in range(W):
    w=[max(0,(255-px[y][x])-NOISE) for y in range(H)]
    s=sum(w); n=hours[x]
    q=[n*v/s for v in w]
    base=[int(v) for v in q]
    rem=n-sum(base)
    order=sorted(range(H),key=lambda y:-(q[y]-base[y]))
    for y in order[:rem]: base[y]+=1
    for y in range(H): counts[y][x]=base[y]
assert sum(map(sum,counts))==N
print(max(max(r) for r in counts))
for y in range(H): print(''.join(str(c) if c else '.' for c in counts[y]))
# layout
VW,VH=1100,800
cw=13.6; ch=22
gx=(VW-W*cw)/2; gy=118
out=[]
def rnd(a,b):  # deterministic hash 0..1
    v=math.sin(a*12.9898+b*78.233)*43758.5453; return v-math.floor(v)
for y in range(H):
    for x in range(W):
        v=px[y][x]
        if v<250:
            g=255-v
            out.append(f'<rect x="{gx+x*cw:.1f}" y="{gy+y*ch:.1f}" width="{cw-1.2:.1f}" height="{ch-1.2:.1f}" fill="#8a8172" fill-opacity="{g/255*0.22:.3f}"/>')
dots=[]
slots=[(0.5,0.5),(0.3,0.28),(0.7,0.72),(0.7,0.28),(0.3,0.72),(0.5,0.12),(0.5,0.88),(0.22,0.5),(0.78,0.5)]
hcount=0
for x in range(W):
  for y in range(H):
    n=counts[y][x]
    for k in range(n):
        sx,sy=slots[k] if n>1 else (0.5,0.5)
        jx=(rnd(x*31+k,y)-0.5)*1.6; jy=(rnd(y*17+k,x)-0.5)*1.6
        cx=gx+x*cw+(cw-1.2)*sx+jx; cy=gy+y*ch+(ch-1.2)*sy+jy
        dots.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.05"/>')
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nineteen and a Half Hours</title>
<style>
:root{{--paper:#f4f1ea;--ink:#1d1b18;--soft:#8a8172}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--paper:#f4f1ea;--ink:#1d1b18}}}}
html,body{{margin:0;height:100%;background:var(--paper)}}
body{{display:flex;align-items:center;justify-content:center;overflow:hidden}}
svg{{width:100vw;height:100vh;max-width:1100px;max-height:800px;display:block}}
</style></head><body>
<svg viewBox="0 0 {VW} {VH}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="1,464 dots, one per hour, placed back into the 75 by 23 pixel grid in which the record survived. Each pixel square holds as many dots as its darkness can account for.">
<rect width="{VW}" height="{VH}" fill="#f4f1ea"/>
<g>{''.join(out)}</g>
<g fill="#1d1b18">{''.join(dots)}</g>
<g font-family="Georgia, 'Times New Roman', serif" fill="#5f584d" font-size="13" letter-spacing="0.4">
<text x="{gx:.1f}" y="{gy+H*ch+48:.1f}" font-style="italic" font-size="17" fill="#1d1b18">Nineteen and a Half Hours</text>
<text x="{gx:.1f}" y="{gy+H*ch+72:.1f}">1,464 hourly values survive only as 75 &#215; 23 pixels. Each column held about 19.5 hours; each square here holds the dots its darkness can account for.</text>
<text x="{gx:.1f}" y="{gy+H*ch+92:.1f}">The order of hours inside a square, and their exact heights, did not survive.</text>
</g>
</svg></body></html>'''
open('/tmp/claude-0/s122/mk/m06/work/index.html','w').write(html)
print(len(html))
