import json
d=json.load(open('/tmp/claude-0/s137/mk/m05/scratch/series2.json'))
v=d['mean']; N=len(v)
W,H=1100,800
PH=17                    # fold so each row opens at the mean daily low
XL,XR=230,870
YT,YB=262,742
rows=[]
r=0
while True:
    start=r*24-(24-PH) if False else r*24+PH-24
    if start>=N: break
    rows.append(start); r+=1
nr=len(rows)
sp=(YB-YT)/(nr-1)
K=2.7; V0=6
def xpos(j): return XL+j*(XR-XL)/23
def cr(pts):
    s=f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts)-1):
        p0=pts[i-1] if i>0 else pts[i]; p1=pts[i]; p2=pts[i+1]; p3=pts[i+2] if i+2<len(pts) else p2
        c1=(p1[0]+(p2[0]-p0[0])/6, p1[1]+(p2[1]-p0[1])/6)
        c2=(p2[0]-(p3[0]-p1[0])/6, p2[1]-(p3[1]-p1[1])/6)
        s+=f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return s
out=[]
for k,start in enumerate(rows):
    base=YT+k*sp
    pts=[]
    for j in range(24):
        i=start+j
        if 0<=i<N: pts.append((xpos(j), base-(v[i]-V0)*K))
    if len(pts)<2: continue
    line=cr(pts)
    fill=line+f"L{pts[-1][0]:.1f},{base+1.5:.1f}L{pts[0][0]:.1f},{base+1.5:.1f}Z"
    out.append(f'<path class="f" d="{fill}"/><path class="l" d="{line}"/>')
svg="\n".join(out)
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sixty-One Falls</title>
<style>
:root{{--paper:#efebe2;--ink:#1c1b19;--faint:#8b867c}}
html,body{{margin:0;height:100%;background:var(--paper)}}
body{{display:flex;align-items:center;justify-content:center;overflow:hidden}}
svg{{width:100vw;height:100vh;max-width:1100px;max-height:800px;display:block}}
.f{{fill:var(--paper);fill-opacity:.8;stroke:none}}
.l{{fill:none;stroke:var(--ink);stroke-width:1.05;stroke-linejoin:round;stroke-linecap:round}}
text{{font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;fill:var(--ink)}}
.cap{{font-size:12.5px;fill:var(--faint);letter-spacing:.04em}}
</style></head>
<body>
<svg viewBox="0 0 {W} {H}" role="img" aria-label="Sixty-one days of an hourly record, each day drawn as one line, stacked from first day at top to last at bottom.">
<rect width="{W}" height="{H}" fill="var(--paper)"/>
{svg}
<text x="{XR}" y="776" text-anchor="end" style="font-size:19px;font-style:italic">Sixty-One Falls</text>
<text x="{XL}" y="776" class="cap">1,464 hours · cut every twenty-four · first day at the top</text>
</svg>
</body></html>'''
open('/tmp/claude-0/s137/mk/m05/work/index.html','w').write(html)
print(nr, sp, len(html))
