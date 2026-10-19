import json
from PIL import Image, ImageDraw
v=json.load(open('/tmp/claude-0/s137/mk/m16/scratch/vals.json'))
W,H=1100,800
L,R=74,1026; T,B=100,688
D=61; cw=(R-L)/D; rh=(B-T)/24
lo,hi=0.05,0.95
stops=[(0.0,(52,62,78)),(0.22,(88,82,92)),(0.42,(146,80,54)),(0.62,(212,108,46)),(0.8,(244,168,78)),(1.0,(255,236,186))]
def rgb(t):
    t=max(0,min(1,t))
    for (a,ca),(b,cb) in zip(stops,stops[1:]):
        if t<=b:
            f=(t-a)/(b-a); return tuple(round(ca[i]+(cb[i]-ca[i])*f) for i in range(3))
def hexc(c): return '#%02x%02x%02x'%c
def nt(x): return max(0,min(1,(x-lo)/(hi-lo)))
def width(a): return 1.1+nt(a)**2.0*(cw*1.02-1.1)
# finer vertical sampling: interpolate hourly values at sub-steps with cosine
def sample(day, n=6):
    pts=[]
    for h in range(24):
        a=day[h]; b=day[h+1] if h<23 else day[h]
        for k in range(n):
            f=k/n; f2=(1-__import__('math').cos(f*3.14159))/2
            pts.append((T+rh*(h+0.5+f), a+(b-a)*f2))
    pts.insert(0,(T, day[0])) 
    pts.append((B, day[23]))
    return pts
paths=[];defs=[];prev=Image.new('RGB',(W,H),(15,14,13));dr=ImageDraw.Draw(prev)
for d in range(D):
    cx=L+cw*(d+0.5)
    day=v[d*24:(d+1)*24]
    S=[(y,a) for y,a in sample(day) if T<=y<=B]
    right=' '.join(f'L{cx+width(a)/2:.2f},{y:.1f}' for y,a in S)
    left=' '.join(f'L{cx-width(a)/2:.2f},{y:.1f}' for y,a in reversed(S))
    pth='M'+right[1:]+' '+left+' Z'
    gid=f'g{d}'
    st=''.join(f'<stop offset="{(h+0.5)/24:.4f}" stop-color="{hexc(rgb(nt(day[h])))}"/>' for h in range(24))
    defs.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="{T}" x2="0" y2="{B}">{st}</linearGradient>')
    paths.append(f'<path d="{pth}" fill="url(#{gid})"/>')
    # preview
    for (y0,a0),(y1,a1) in zip(S,S[1:]):
        hh=min(23,max(0,int((y0-T)/rh-0.5))); 
        dr.polygon([(cx-width(a0)/2,y0),(cx+width(a0)/2,y0),(cx+width(a1)/2,y1),(cx-width(a1)/2,y1)],fill=rgb(nt(a0)))
ticks=''
for d,lab in [(0,'15 October'),(17,'1 November'),(47,'1 December'),(60,'14 December')]:
    x=L+cw*(d+0.5)
    anc='start' if d==0 else ('end' if d==60 else 'middle')
    tx=x-cw/2 if d==0 else (x+cw/2 if d==60 else x)
    ticks+=f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{B+10}" y2="{B+17}" stroke="#5f5852" stroke-width="1"/><text x="{tx:.1f}" y="{B+34}" text-anchor="{anc}">{lab}</text>'
    dr.line([(x,B+10),(x,B+17)],fill=(95,88,82))
ty=B+96
pts=' '.join(f'{L+(i+0.5)*(R-L)/1464:.1f},{ty-v[i]*30:.1f}' for i in range(1464))
dr.line([(L+(i+0.5)*(R-L)/1464, ty-v[i]*30) for i in range(1464)],fill=(92,84,76))
prev.save('/tmp/claude-0/s137/mk/m16/scratch/preview2.png')
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sixty-One Wicks</title>
<style>
html,body{{margin:0;height:100%;background:#0f0e0d}}
body{{display:flex;align-items:center;justify-content:center;overflow:hidden}}
svg{{width:100vw;height:100vh;max-width:1100px;max-height:800px;display:block}}
text{{font-family:Georgia,'Times New Roman',serif;fill:#8a827a;font-size:13px;letter-spacing:.04em}}
</style></head><body>
<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Sixty-one vertical shapes, one per day from 15 October to 14 December 2025. Each is 24 hours tall; its width and colour follow the hourly value. Wide, glowing forms through October and most of November thin to cold grey threads from 27 November.">
<defs>{''.join(defs)}</defs>
<rect width="{W}" height="{H}" fill="#0f0e0d"/>
<text x="{L}" y="58" style="font-size:24px;fill:#e2d3bf;letter-spacing:.02em">Sixty-One Wicks</text>
<text x="{R}" y="58" text-anchor="end">one column a day, read downward through its 24 hours · width and warmth are the value</text>
{''.join(paths)}
{ticks}
<polyline points="{pts}" fill="none" stroke="#5c544c" stroke-width="0.9" stroke-linejoin="round"/>
<text x="{R}" y="{H-12}" text-anchor="end" style="font-size:11px;fill:#6a635c">the same 1,464 hours, unfolded</text>
</svg>
</body></html>'''
open('/tmp/claude-0/s137/mk/m16/work/index.html','w').write(html)
