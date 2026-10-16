import json, math
import numpy as np
v=np.array(json.load(open('/tmp/claude-0/s131/mk/m16/scratch/series.json')))
N=len(v); W,H=1100,800
cx,cy=640,400
r0,pitch,amp=24.0,5.5,26.0
mean=v.mean()
# light smoothing of the reconstruction noise (3-hour kernel)
vs=np.convolve(np.pad(v,1,mode='edge'),[0.25,0.5,0.25],'valid')
def pt(t,val):
    th=2*math.pi*t/24.0
    r=r0+pitch*t/24.0+amp*(val-mean)
    return cx+r*math.sin(th), cy-r*math.cos(th)
# subdivide with linear interp of values at 6 steps/hour
S=6
ts=np.arange(0,(N-1)*S+1)/S
vals=np.interp(ts,np.arange(N),vs)
P=[pt(t,x) for t,x in zip(ts,vals)]
d='M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in P)
B=[pt(t,mean) for t in ts]
db='M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in B)
# shaded band between baseline and data, split by sign: draw per-hour quads
hi=[];lo=[]
for i in range(len(ts)-1):
    a,b=P[i],P[i+1]; c,e=B[i+1],B[i]
    q=f'M{a[0]:.1f},{a[1]:.1f}L{b[0]:.1f},{b[1]:.1f}L{c[0]:.1f},{c[1]:.1f}L{e[0]:.1f},{e[1]:.1f}Z'
    (hi if vals[i]>mean else lo).append(q)
dots=''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="0.9"/>' for x,y in (pt(i,vs[i]) for i in range(N)))
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="#f2ede3"/>
<path d="{''.join(hi)}" fill="#6b4a32" fill-opacity="0.30" stroke="none"/>
<path d="{''.join(lo)}" fill="#3f6b4a" fill-opacity="0.16" stroke="none"/>
<path d="{db}" fill="none" stroke="#8a7f70" stroke-width="0.35" stroke-opacity="0.5"/>
<path d="{d}" fill="none" stroke="#2b241d" stroke-width="0.7" stroke-linejoin="round"/>
<g fill="#1f1a15" fill-opacity="0.75">{dots}</g>
<g font-family="Georgia, 'Times New Roman', serif" fill="#2b241d">
<text x="64" y="636" font-size="26" letter-spacing="0.5">Breath Rings</text>
<text x="64" y="666" font-size="13.5" fill="#5a5146">Sixty-one days of carbon dioxide in the air,</text>
<text x="64" y="684" font-size="13.5" fill="#5a5146">one turn per day, the first day at the centre.</text>
<text x="64" y="708" font-size="13.5" fill="#5a5146">Each of the 1,464 hours is a dot. The ring swells</text>
<text x="64" y="726" font-size="13.5" fill="#5a5146">(brown) where the air held more, and draws in</text>
<text x="64" y="744" font-size="13.5" fill="#5a5146">(green) where the leaves had taken it back.</text>
</g>
</svg>'''
open('/tmp/claude-0/s131/mk/m16/scratch/work.svg','w').write(svg)
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Breath Rings</title>
<style>html,body{{margin:0;height:100%;background:#f2ede3}}body{{display:flex;align-items:center;justify-content:center}}svg{{display:block;max-width:100vw;max-height:100vh;width:auto;height:auto}}</style>
</head><body>
{svg}
</body></html>'''
open('/tmp/claude-0/s131/mk/m16/work/index.html','w').write(html)
print(len(html))
