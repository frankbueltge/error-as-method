import json
from PIL import Image, ImageDraw
v=[x/1000 for x in json.load(open('vals.json'))]
W,H=1100,800
L,R=250,850
top,gap,amp=78,9.6,125
paper='#f2efe7'; ink='#1c1a17'
def pts(d):
    seg=v[d*24:d*24+25]
    base=top+d*gap+amp
    n=24
    return [(L+(R-L)*i/n, base-amp*seg[i]) for i in range(len(seg))], base
def smooth(p):
    s=f'M{p[0][0]:.1f},{p[0][1]:.1f}'
    for i in range(len(p)-1):
        p0=p[i-1] if i>0 else p[i]; p1=p[i]; p2=p[i+1]; p3=p[i+2] if i+2<len(p) else p[i+1]
        c1=(p1[0]+(p2[0]-p0[0])/6, p1[1]+(p2[1]-p0[1])/6)
        c2=(p2[0]-(p3[0]-p1[0])/6, p2[1]-(p3[1]-p1[1])/6)
        s+=f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return s
paths=[]
prev=Image.new('RGB',(W,H),paper); dr=ImageDraw.Draw(prev)
for d in range(61):
    p,base=pts(d)
    s=smooth(p)
    xe=p[-1][0]
    fill=s+f' L{xe:.1f},{base+3:.1f} L{L:.1f},{base+3:.1f} Z'
    paths.append(f'<path d="{fill}" fill="{paper}" stroke="none"/><path d="{s}"/>')
    dr.polygon(p+[(xe,base+3),(L,base+3)],fill=paper); dr.line(p,fill=ink,width=1)
prev.save('preview.png')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Sixty-one stacked lines, one per day of an hourly record">
<rect width="{W}" height="{H}" fill="{paper}"/>
<g fill="none" stroke="{ink}" stroke-width="1.05" stroke-linejoin="round" stroke-linecap="round">
{chr(10).join(paths)}
</g>
<g font-family="Georgia, 'Times New Roman', serif" fill="{ink}">
<text x="{L}" y="84" font-size="15" letter-spacing="3">THE DRYING</text>
<text x="{R}" y="84" font-size="11" text-anchor="end" fill="#6d675d" font-style="italic">sixty-one days, one line each · twenty-four hours across</text>
</g>
</svg>'''
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Drying</title>
<style>html,body{{margin:0;height:100%;background:{paper}}}body{{display:flex;align-items:center;justify-content:center}}svg{{display:block;max-width:100vw;max-height:100vh;width:auto;height:auto}}</style>
</head><body>
{svg}
</body></html>'''
open('/tmp/claude-0/s131/mk/m08/work/index.html','w').write(html)
print(len(html))
