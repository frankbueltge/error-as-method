import json, math
v=json.load(open('vals.json')); N=len(v)
W,H=1100,800
CUT=15
ncol=62  # partial first and last day
gx0,gx1=92,1008
gy0=150; dy=18.2
dx=(gx1-gx0)/(ncol-1)
rmax=dx*0.49
paper='#eeebe3'; ink='#1a1c22'
cells=[]
for i in range(N):
    k=(i-CUT)//24+1; p=(i-CUT)%24
    x=gx0+k*dx; y=gy0+p*dy
    r=rmax*(0.07+0.93*v[i])
    cells.append((x,y,r))
dots=''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}"/>' for x,y,r in cells)
gb=gy0+23*dy
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Sixty-one Nights: 1,464 hourly carbon dioxide values as a field of dots, one column per day">
<rect width="{W}" height="{H}" fill="{paper}"/>
<g fill="{ink}">{dots}</g>
<g font-family="Georgia, 'Times New Roman', serif" fill="{ink}">
<text x="{gx0-rmax:.0f}" y="{gb+64:.0f}" font-size="20" letter-spacing="0.4">Sixty-one Nights</text>
<text x="{gx0-rmax:.0f}" y="{gb+88:.0f}" font-size="12" fill-opacity="0.6">Carbon dioxide in the air at one station, one dot for each hour, 1,464 in all. Each column is a day, read downward from one afternoon low to the next;</text>
<text x="{gx0-rmax:.0f}" y="{gb+105:.0f}" font-size="12" fill-opacity="0.6">the days run left to right. The larger the dot, the more carbon dioxide; sizes are relative, from the lowest hour in the record to the highest.</text>
</g>
</svg>'''
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sixty-one Nights</title>
<style>html,body{{margin:0;background:{paper};}}body{{display:flex;justify-content:center;align-items:center;min-height:100vh;}}svg{{display:block;max-width:100vw;max-height:100vh;width:auto;height:auto;}}</style>
</head><body>
{svg}
</body></html>'''
open('/tmp/claude-0/s131/mk/m07/work/index.html','w').write(html)
from PIL import Image, ImageDraw
S=3; img=Image.new('RGB',(W*S,H*S),paper); d=ImageDraw.Draw(img)
for x,y,r in cells: d.ellipse([(x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S],fill=ink)
d.rectangle([(gx0-rmax)*S,(gb+50)*S,(gx0+150)*S,(gb+66)*S],fill=(120,120,120))
d.rectangle([(gx0-rmax)*S,(gb+80)*S,(gx0+880)*S,(gb+88)*S],fill=(190,190,190))
d.rectangle([(gx0-rmax)*S,(gb+97)*S,(gx0+800)*S,(gb+105)*S],fill=(190,190,190))
img.resize((W,H),Image.LANCZOS).save('prev2.png')
print(dx,rmax,gb, len(html))
