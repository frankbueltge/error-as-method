import json, math
from PIL import Image, ImageDraw
s=json.load(open('/tmp/claude-0/s122/mk/m08/scratch/series.json'))
rec=s['rec']; N=len(rec)
ys=sorted(rec); med=ys[N//2]
val=[med-y for y in rec]               # up = larger
W,H=1100,800
X0,X1=180,920; TOP=100; STEP=10.0; K=1.1; DEPTH=70
BG='#ece7dc'; INK='#1c2430'
def px(h): return X0+(X1-X0)*h/24
rows=[]
OFF=12
for d in range(62):
    base=TOP+d*STEP
    pts=[]
    for h in range(25):
        t=d*24+h-OFF
        if t<0 or t>=N: continue
        pts.append((px(h), base-K*val[t]))
    rows.append((base,pts))
# --- SVG
out=[]
for base,pts in rows:
    poly=' '.join('%.1f,%.1f'%p for p in pts)
    fillpts=poly+' %.1f,%.1f %.1f,%.1f'%(pts[-1][0],base+DEPTH,pts[0][0],base+DEPTH)
    out.append('<polygon points="%s" fill="%s" stroke="none"/>'%(fillpts,BG))
    out.append('<polyline points="%s"/>'%poly)
svg_rows='\n'.join(out)
html='''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fifty Minutes Later</title>
<style>
html,body{margin:0;height:100%%;background:%(bg)s}
body{display:flex;align-items:center;justify-content:center;overflow:hidden}
svg{width:min(100vw,137.5vh);height:auto;display:block}
</style></head><body>
<svg viewBox="0 0 %(W)d %(H)d" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Sixty-one days of hourly readings, one line per day, stacked top to bottom. Two crests a day drift slowly to the right; in the lower third one day throws a single tall peak up through the days above it.">
<rect width="%(W)d" height="%(H)d" fill="%(bg)s"/>
<g fill="none" stroke="%(ink)s" stroke-width="1.1" stroke-linejoin="round" stroke-linecap="round">
%(rows)s
</g>
<g font-family="Georgia, 'Times New Roman', serif" fill="%(ink)s">
<text x="%(x0)d" y="748" font-size="15" letter-spacing="0.5">Fifty Minutes Later</text>
<text x="%(x0)d" y="768" font-size="11" opacity="0.62" font-style="italic">1,464 hourly readings in rows of twenty-four hours, the earliest at the top</text>
</g>
</svg>
</body></html>
'''%dict(bg=BG,ink=INK,W=W,H=H,rows=svg_rows,x0=X0)
open('/tmp/claude-0/s122/mk/m08/work/index.html','w').write(html)
# --- preview
S=2
im=Image.new('RGB',(W*S,H*S),BG); d=ImageDraw.Draw(im)
for base,pts in rows:
    P=[(x*S,y*S) for x,y in pts]
    d.polygon(P+[(P[-1][0],(base+DEPTH)*S),(P[0][0],(base+DEPTH)*S)],fill=BG)
    d.line(P,fill=INK,width=2*S//2+0,joint='curve')
im=im.resize((W,H),Image.LANCZOS); im.save('/tmp/claude-0/s122/mk/m08/scratch/preview.png')
print(len(html))
