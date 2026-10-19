import json
v=json.load(open('/tmp/claude-0/s137/mk/m16/scratch/vals.json'))
W,H=1100,800
L,R=78,1022; T,B=96,700
D=61; cw=(R-L)/D; rh=(B-T)/24
lo,hi=0.05,0.95
stops=[(0.0,(46,58,74)),(0.25,(92,84,92)),(0.45,(150,82,52)),(0.65,(214,112,48)),(0.82,(244,170,80)),(1.0,(255,232,178))]
def col(t):
    t=max(0,min(1,t))
    for (a,ca),(b,cb) in zip(stops,stops[1:]):
        if t<=b:
            f=(t-a)/(b-a); return '#%02x%02x%02x'%tuple(round(ca[i]+(cb[i]-ca[i])*f) for i in range(3))
def nt(x): return (x-lo)/(hi-lo)
out=[]
for d in range(D):
    cx=L+cw*(d+0.5)
    day=v[d*24:(d+1)*24]
    # each hour: a band; draw as trapezoids between hour centers for continuity
    for h in range(24):
        a=day[h]
        y0=T+rh*h; y1=y0+rh
        w=0.6+nt(a)*(cw-2.2)
        hw=w/2
        out.append(f'<rect x="{cx-hw:.2f}" y="{y0+0.6:.2f}" width="{w:.2f}" height="{rh-1.2:.2f}" fill="{col(nt(a))}"/>')
svg_cells='\n'.join(out)
# month marks: day index 17 = 1 Nov, 47 = 1 Dec
ticks=''
for d,lab in [(0,'15 Oct'),(17,'1 Nov'),(47,'1 Dec'),(60,'14 Dec')]:
    x=L+cw*(d+0.5)
    anchor='middle'
    ticks+=f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{B+12}" y2="{B+20}" stroke="#6b6560" stroke-width="1"/><text x="{x:.1f}" y="{B+38}" text-anchor="{anchor}">{lab}</text>'
# original trace, small, under the grid
pts=' '.join(f'{L+(i+0.5)*(R-L)/1464:.1f},{B+92-v[i]*34:.1f}' for i in range(1464))
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sixty-One Wicks</title>
<style>
:root{{--bg:#0f0e0d;--ink:#8a827a}}
html,body{{margin:0;height:100%;background:var(--bg)}}
body{{display:flex;align-items:center;justify-content:center;overflow:hidden}}
svg{{width:100vw;height:100vh;max-width:1100px;max-height:800px;display:block}}
text{{font-family:Georgia,'Times New Roman',serif;fill:var(--ink);font-size:13px;letter-spacing:.04em}}
</style></head><body>
<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="61 columns, one per day; each column stacks 24 hourly values as bars whose width and warmth follow the value. The columns are wide and glowing through October and most of November, then thin to grey threads from late November.">
<rect width="{W}" height="{H}" fill="#0f0e0d"/>
<text x="{L}" y="56" style="font-size:22px;fill:#d9cbb8;letter-spacing:.02em">Sixty-One Wicks</text>
<text x="{R}" y="56" text-anchor="end">one column a day · one bar an hour · width and warmth: the value</text>
{svg_cells}
{ticks}
<polyline points="{pts}" fill="none" stroke="#5c544c" stroke-width="0.9" stroke-linejoin="round"/>
<text x="{R}" y="{H-14}" text-anchor="end" style="font-size:11px">the record as received, unfolded</text>
</svg>
</body></html>'''
open('/tmp/claude-0/s137/mk/m16/work/index.html','w').write(html)
open('/tmp/claude-0/s137/mk/m16/scratch/art.svg','w').write(html.split('<body>')[1].split('</body>')[0])
