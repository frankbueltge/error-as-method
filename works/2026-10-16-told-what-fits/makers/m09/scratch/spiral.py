import json, math, sys
v=json.load(open('series2.json'))
N=len(v); W,H=1100,800
cx,cy=550,410
k=float(sys.argv[1]); a=float(sys.argv[2]); r0=float(sys.argv[3])
mean=sum(v)/N
pts=[]
for t,q in enumerate(v):
    ang=2*math.pi*(t%24)/24  # 0 = midnight at bottom
    r=r0+k*t/24+a*(q-mean)
    x=cx+r*math.sin(ang)*-1; y=cy+r*math.cos(ang)
    pts.append((x,y))
s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#f4f1ea"/>']
d='M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)
s.append(f'<path d="{d}" fill="none" stroke="#1d1b18" stroke-opacity=".25" stroke-width=".6"/>')
for x,y in pts: s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.3" fill="#1d1b18"/>')
s.append('</svg>')
open('sp.svg','w').write('\n'.join(s))
