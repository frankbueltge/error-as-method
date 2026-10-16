import json
v=json.load(open('vals.json')); N=len(v)
W,H=1100,800
CUT=15             # afternoon low in the folded profile
L,R=250,950        # ridge field
top=36; gap=7.7; amp=150
rows=[]
# row k holds hours from CUT+24*(k-1) .. CUT+24*k-1 ; positions 0..23
k=0
while True:
    start=CUT+24*(k-1)
    if start>=N: break
    pts=[(p,start+p) for p in range(24) if 0<=start+p<N]
    rows.append(pts); k+=1
def X(p): return L+(R-L)*p/23
paper='#efece5'; ink='#1b1d20'
out=[]
for r,pts in enumerate(rows):
    base=top+r*gap+amp
    xy=[(X(p),base-amp*v[i]) for p,i in pts]
    line=' '.join(f'{x:.1f},{y:.1f}' for x,y in xy)
    x0=xy[0][0]; x1=xy[-1][0]
    poly=f'{x0:.1f},{base+1:.1f} '+line+f' {x1:.1f},{base+1:.1f}'
    out.append(f'<polygon points="{poly}" fill="{paper}"/>')
    out.append(f'<polyline points="{line}" fill="none" stroke="{ink}" stroke-width="0.7" stroke-opacity="0.55" stroke-linejoin="round"/>')
    out.append('<g fill="%s">'%ink+''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.25"/>' for x,y in xy)+'</g>')
bottom=top+(len(rows)-1)*gap+amp
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<rect width="{W}" height="{H}" fill="{paper}"/>
{''.join(out)}
<g font-family="Georgia, 'Times New Roman', serif" fill="{ink}">
<text x="{L}" y="{bottom+44:.0f}" font-size="19" letter-spacing="0.5">Sixty-one Nights</text>
<text x="{L}" y="{bottom+66:.0f}" font-size="11.5" fill-opacity="0.62">Carbon dioxide in the air at one station, hour by hour. Each line is one day, cut at the afternoon low so that the night sits in the middle; later days lie in front.</text>
<text x="{L}" y="{bottom+82:.0f}" font-size="11.5" fill-opacity="0.62">Height is relative: the lowest and highest hours of the record span the same distance on every line. 1,464 dots, one per hour.</text>
</g>
</svg>'''
open('work.svg','w').write(svg)
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sixty-one Nights</title>
<style>html,body{{margin:0;background:{paper};}}body{{display:flex;justify-content:center;align-items:center;min-height:100vh;}}svg{{display:block;max-width:100vw;max-height:100vh;width:auto;height:auto;}}</style>
</head><body>
{svg}
</body></html>'''
open('/tmp/claude-0/s131/mk/m07/work/index.html','w').write(html)
print(len(rows), bottom, len(html))
# PIL preview of the same geometry (2x)
from PIL import Image, ImageDraw
S=2; img=Image.new('RGB',(W*S,H*S),paper); d=ImageDraw.Draw(img)
for r,pts in enumerate(rows):
    base=top+r*gap+amp
    xy=[(X(p)*S,(base-amp*v[i])*S) for p,i in pts]
    d.polygon([(xy[0][0],(base+1)*S)]+xy+[(xy[-1][0],(base+1)*S)],fill=paper)
    d.line(xy,fill=(110,110,112),width=1)
    for x,y in xy: d.ellipse([x-2.5,y-2.5,x+2.5,y+2.5],fill=ink)
d.text((L*S,(bottom+44)*S-20),'Sixty-one Nights (title text here)',fill=ink)
img.resize((W,H),Image.LANCZOS).save('prev.png')
