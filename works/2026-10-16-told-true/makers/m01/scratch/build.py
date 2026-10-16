import json
v=json.load(open('/tmp/claude-0/s130/mk/m01/scratch/series.json'))
N=len(v); SHIFT=5
W,H=1100,800
X0,X1=150,1010
rows=(N-1+SHIFT)//24+1
Y0,Y1=232,742
dy=(Y1-Y0)/(rows-1)
K=1.75; FLOOR=11
hx=(X1-X0)/23
pts={}
for i,val in enumerate(v):
    r,p=divmod(i+SHIFT,24)
    pts.setdefault(r,[]).append((X0+p*hx, Y0+r*dy-max(0,val-FLOOR)*K, val))
out=[]
def cr(P,t=0.5):
    segs=[]
    for k in range(len(P)-1):
        p0=P[k-1] if k>0 else P[k]; p1=P[k]; p2=P[k+1]; p3=P[k+2] if k+2<len(P) else P[k+1]
        c1=(p1[0]+(p2[0]-p0[0])/6*t*2, p1[1]+(p2[1]-p0[1])/6*t*2)
        c2=(p2[0]-(p3[0]-p1[0])/6*t*2, p2[1]-(p3[1]-p1[1])/6*t*2)
        segs.append("C%.1f %.1f %.1f %.1f %.1f %.1f"%(c1[0],c1[1],c2[0],c2[1],p2[0],p2[1]))
    return " ".join(segs)
for r in range(rows):
    P=pts[r]; base=Y0+r*dy
    curve=cr(P)
    d="M%.1f %.1f L%.1f %.1f "%(P[0][0],base,P[0][0],P[0][1])+curve+" L%.1f %.1f Z"%(P[-1][0],base)
    line="M%.1f %.1f "%(P[0][0],P[0][1])+curve
    g=['<path d="%s" class="f"/>'%d,'<path d="%s" class="l"/>'%line,
       '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="b"/>'%(P[0][0],base,P[-1][0],base)]
    for x,y,val in P:
        g.append('<circle cx="%.1f" cy="%.1f" r="%s" class="%s"/>'%(x,y,'2.1' if val>=52 else '1.05','h' if val>=52 else 'd'))
    out.append('<g>'+''.join(g)+'</g>')
svg="\n".join(out)
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sixty-One Risings</title>
<style>
:root{{--paper:#f2eee5;--ink:#1c1b19;--soft:#8a857a;--hot:#c2411d}}
html,body{{margin:0;height:100%;background:var(--paper)}}
body{{display:flex;align-items:center;justify-content:center;overflow:hidden}}
svg{{width:100vw;height:100vh;max-width:1100px;max-height:800px;display:block}}
.f{{fill:var(--paper);stroke:none}}
.l{{fill:none;stroke:var(--ink);stroke-width:.9;stroke-opacity:.8;stroke-linejoin:round}}
.b{{stroke:var(--ink);stroke-width:.4;stroke-opacity:.18}}
.d{{fill:var(--ink)}}
.h{{fill:var(--hot)}}
text{{font-family:Georgia,'Times New Roman',serif;fill:var(--ink)}}
.t{{font-size:30px;letter-spacing:.5px}}
.s{{font-size:12.5px;fill:var(--soft);font-style:italic}}
.m{{font-size:11px;fill:var(--soft);letter-spacing:1.5px}}
</style></head><body>
<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Sixty-one days of an hourly record stacked as ridgelines, one row per day, each rising and falling once.">
<rect width="{W}" height="{H}" fill="var(--paper)"/>
<text x="{X0}" y="62" class="t">Sixty-One Risings</text>
<text x="{X0}" y="86" class="s">1,464 hours of one measured quantity, cut into days at the hour it is usually lowest and laid one beneath the next.</text>
<text x="{X0}" y="104" class="s">Each row climbs once and falls once. Red marks the hours that broke well above the usual swell.</text>
{svg}
<text x="{X0-18}" y="{Y0+3}" class="m" text-anchor="end">FIRST</text>
<text x="{X0-18}" y="{Y1+3}" class="m" text-anchor="end">LAST</text>
<text x="{X0}" y="{Y1+28}" class="m">LOW</text>
<text x="{(X0+X1)/2}" y="{Y1+28}" class="m" text-anchor="middle">TWELVE HOURS ON</text>
<text x="{X1}" y="{Y1+28}" class="m" text-anchor="end">LOW AGAIN</text>
</svg></body></html>'''
open('/tmp/claude-0/s130/mk/m01/work/index.html','w').write(html)
print(rows, len(html))
