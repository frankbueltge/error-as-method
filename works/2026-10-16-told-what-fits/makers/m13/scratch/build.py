import json
raw=json.load(open('series.json'))
n=len(raw)
v=[0.25*raw[max(i-1,0)]+0.5*raw[i]+0.25*raw[min(i+1,n-1)] for i in range(n)]
W,H=1100,800
L,R=150,950; top=180; pitch=9.4; A=112
lo,hi=min(v),max(v)
def curve(pts):
    s='M%.1f %.1f'%pts[0]
    for i in range(len(pts)-1):
        p0=pts[max(i-1,0)];p1=pts[i];p2=pts[i+1];p3=pts[min(i+2,len(pts)-1)]
        c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6)
        c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
        s+=' C%.1f %.1f %.1f %.1f %.1f %.1f'%(c1+c2+p2)
    return s
days=[]
for d in range(61):
    base=top+d*pitch
    seg=v[d*24:d*24+25]
    if len(seg)<25: seg=seg+[seg[-1]]
    pts=[(L+(R-L)*h/24, base-A*(val-lo)/(hi-lo)) for h,val in enumerate(seg)]
    p=curve(pts)
    days.append(f'<path d="{p} L{R+0.0:.1f} {base+3:.1f} L{L:.1f} {base+3:.1f} Z" fill="#f3efe6"/><path d="{p}" fill="none" stroke="#17283c" stroke-width="0.9"/>')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Sixty-one daily curves stacked from top to bottom, each a ridge of one day's hourly values">
<rect width="{W}" height="{H}" fill="#f3efe6"/>
<g stroke-linejoin="round" stroke-linecap="round">{''.join(days)}</g>
<g font-family="Georgia, 'Times New Roman', serif" fill="#4a5462">
<text x="{L}" y="{H-30}" font-size="16" font-style="italic">Dew Line</text>
<text x="{R}" y="{H-30}" font-size="11" text-anchor="end" letter-spacing="0.5">61 days, one to a ridge, the first at the back  ·  24 hours across  ·  height is the value</text>
</g>
</svg>'''
open('work.svg','w').write(svg)
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dew Line</title>
<style>html,body{{margin:0;height:100%;background:#f3efe6}}body{{display:flex;align-items:center;justify-content:center;overflow:hidden}}svg{{display:block;width:100vw;height:100vh;max-width:1100px;max-height:800px}}</style>
</head><body>
{svg}
</body></html>'''
open('/tmp/claude-0/s131/mk/m13/work/index.html','w').write(html)
