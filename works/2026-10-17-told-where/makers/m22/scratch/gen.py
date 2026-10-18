import json
ys=json.load(open('/tmp/claude-0/s133/mk/m22/scratch/fitc_2.36_296.48_5.0.json'))['ys']
h=[max(0.0,83.6-y) for y in ys]
VMAX=max(h)
days=[]
for d in range(-1,61):
    lo=7+24*d; vals=[h[i] for i in range(max(0,lo),min(1464,lo+24))]
    days.append(vals)
json.dump([[round(v,2) for v in dv] for dv in days],open('days.json','w'))
W,H=1100,800
cols,rows=10,7
ml,mr,mt,mb=50,50,40,22
cw=(W-ml-mr)/cols; rh=(H-mt-mb)/rows
RM=45.0
def lerp(a,b,t): return a+(b-a)*t
def col(t):
    stops=[(0,(122,52,22)),(0.45,(214,120,46)),(0.8,(246,204,128)),(1,(255,246,222))]
    for (t0,c0),(t1,c1) in zip(stops,stops[1:]):
        if t<=t1:
            u=(t-t0)/(t1-t0); return '#%02x%02x%02x'%tuple(round(lerp(a,b,u)) for a,b in zip(c0,c1))
    return '#fff6de'
out=[]
out.append('<rect width="1100" height="800" fill="#0b0d12"/>')
# horizons
for r in range(rows):
    y=mt+r*rh+rh*0.66
    x1 = W-mr if r<rows-1 else ml+cw*2
    out.append(f'<line x1="{ml-18}" y1="{y:.1f}" x2="{x1+18 if r<rows-1 else x1+4:.1f}" y2="{y:.1f}" stroke="#3a4152" stroke-width="0.8"/>')
for k,vals in enumerate(days):
    r,c=divmod(k,cols)
    cx=ml+c*cw+cw/2; cy=mt+r*rh+rh*0.66
    # ghost of the record's highest hour
    out.append(f'<path d="M{cx-RM:.1f},{cy:.1f}A{RM},{RM} 0 0 1 {cx+RM:.1f},{cy:.1f}" fill="none" stroke="#ffffff" stroke-opacity="0.045" stroke-width="0.7"/>')
    lit=sorted(v for v in vals if v>=2)
    dark=[v for v in vals if v<2]
    # soft glow proportional to the day's total
    tot=sum(lit)/VMAX
    for v in lit:
        t=v/VMAX; rr=RM*t
        out.append(f'<path d="M{cx-rr:.2f},{cy:.1f}A{rr:.2f},{rr:.2f} 0 0 1 {cx+rr:.2f},{cy:.1f}" fill="none" stroke="{col(t)}" stroke-opacity="{0.42+0.5*t:.2f}" stroke-width="{0.7+0.9*t:.2f}"/>')
    n=len(dark); sp=3.4
    for j in range(n):
        x=cx+(j-(n-1)/2)*sp
        out.append(f'<circle cx="{x:.1f}" cy="{cy+8:.1f}" r="0.95" fill="#7d8aa6" fill-opacity="0.75"/>')
# caption block in the trailing cells (row 5, cols 7..10)
tx=ml+2*cw+cw*0.45; ty=mt+6*rh+rh*0.26
cap=f'''<g font-family="Georgia, 'Times New Roman', serif" fill="#e9dcc2">
<text x="{tx:.1f}" y="{ty+6:.1f}" font-size="21" letter-spacing="0.3">What the Ground Received</text>
<text x="{tx:.1f}" y="{ty+28:.1f}" font-size="11.5" fill="#a59b88" font-style="italic">Fort Peck, Montana &#183; 634 m &#183; 1,464 hours, one sun to each day; the first and last are cut short</text>
</g>
<g font-family="-apple-system, 'Helvetica Neue', Arial, sans-serif" font-size="9.6" fill="#8b8778" letter-spacing="0.2">
<text x="{tx:.1f}" y="{ty+50:.1f}">Each arc is one hour of sunlight on level ground; its radius is that</text>
<text x="{tx:.1f}" y="{ty+63:.1f}">hour&#8217;s strength. Points beneath the line are hours that gave none.</text>
<text x="{tx:.1f}" y="{ty+76:.1f}">The faint outer ring is the brightest hour in the whole record.</text>
</g>'''
out.append(cap)
svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 800" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Sixty-two day cells (61 days of hourly record split at local midnight) of nested semicircular arcs, one arc per sunlit hour, recorded at Fort Peck, Montana">'+''.join(out)+'</svg>'
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>What the Ground Received</title>
<style>
:root{{--bg:#0b0d12}}
html,body{{margin:0;height:100%;background:var(--bg)}}
body{{display:flex;align-items:center;justify-content:center;overflow:hidden}}
svg{{width:100vw;height:100vh;display:block}}
</style></head>
<body>
{svg}
</body></html>
'''
open('/tmp/claude-0/s133/mk/m22/work/index.html','w').write(html)
print(len(html), 'VMAX',VMAX, 'cells',len(days))
