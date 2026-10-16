import json, numpy as np
v=np.array(json.load(open('vals2.json')))
# light 3-pt median to remove reconstruction spikes
m=v.copy()
for i in range(1,len(v)-1): m[i]=np.median(v[i-1:i+2])
v=m
D=v.reshape(61,24)
W,H=1100,800
X0,X1=380,1040
TOP,BOT=180,764
sp=(BOT-TOP)/60
k=1.55
vmin=v.min()
paper='#f1ede4'; ink='#1d1c1a'
def xy(i,h,val):
    x=X0+(X1-X0)*h/24
    y=TOP+i*sp-(val-vmin)*k
    return x,y
paths=[]
for i in range(61):
    pts=[xy(i,h,D[i,h]) for h in range(24)]
    if i<60: pts.append(xy(i,24,D[i+1,0]))
    else: pts.append(xy(i,24,D[i,23]))
    # smooth curve via Catmull-Rom -> bezier
    def cr(p):
        s=f"M{p[0][0]:.1f},{p[0][1]:.1f}"
        for j in range(len(p)-1):
            p0=p[j-1] if j>0 else p[j]; p1=p[j]; p2=p[j+1]; p3=p[j+2] if j+2<len(p) else p[j+1]
            c1=(p1[0]+(p2[0]-p0[0])/6, p1[1]+(p2[1]-p0[1])/6)
            c2=(p2[0]-(p3[0]-p1[0])/6, p2[1]-(p3[1]-p1[1])/6)
            s+=f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
        return s
    line=cr(pts)
    base=TOP+i*sp+4
    fill=line+f" L{X1:.1f},{BOT+30:.1f} L{X0:.1f},{BOT+30:.1f} Z"
    rng=D[i].max()-D[i].min()
    sw=0.9 if rng>25 else 1.4
    paths.append(f'<path d="{fill}" fill="{paper}" stroke="none"/><path d="{line}" fill="none" stroke="{ink}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>')
# day ticks on left: small dot every 7th line
ticks=''.join(f'<circle cx="{X0-14}" cy="{TOP+i*sp:.1f}" r="1.6" fill="{ink}" opacity="0.55"/>' for i in range(0,61,7))
hrs=''.join(f'<line x1="{X0+(X1-X0)*h/24:.1f}" y1="{BOT+12}" x2="{X0+(X1-X0)*h/24:.1f}" y2="{BOT+15 if h%6 else BOT+18}" stroke="{ink}" stroke-width="0.8" opacity="0.6"/>' for h in range(0,25,3))
font="font-family:Georgia,'Times New Roman',serif"
text=f'''
<text x="70" y="168" style="{font};font-size:34px;letter-spacing:0.5px" fill="{ink}">The Long Exhale</text>
<text x="70" y="200" style="{font};font-size:15px;font-style:italic" fill="#5b5750">sixty-one days, one line each</text>
<g style="{font};font-size:13px" fill="#4a4740">
<text x="70" y="262">Each line is one day of the record,</text>
<text x="70" y="280">its twenty-four hourly values read</text>
<text x="70" y="298">left to right; the next day hangs</text>
<text x="70" y="316">just below. Where a line rises it</text>
<text x="70" y="334">covers the days before it.</text>
<text x="70" y="370">Most days sag in the middle and</text>
<text x="70" y="388">recover by night. The sag deepens,</text>
<text x="70" y="406">day after day, until something</text>
<text x="70" y="424">lifts the whole line and stills it,</text>
<text x="70" y="442">drawn heavier here. Seven times it</text>
<text x="70" y="460">comes; each time the sag returns.</text>
</g>
<g style="{font};font-size:11px" fill="#7a756c">
<text x="70" y="740">1,464 values, recovered from a plot</text>
<text x="70" y="756">of dots; heights are approximate.</text>
<text x="{X0-22}" y="{TOP+4:.1f}" text-anchor="end">day 1</text>
<text x="{X0-22}" y="{TOP+60*sp+4:.1f}" text-anchor="end">61</text>
<text x="{X0}" y="{BOT+28}" text-anchor="middle">hour 0</text>
<text x="{(X0+X1)/2}" y="{BOT+28}" text-anchor="middle">12</text>
<text x="{X1}" y="{BOT+28}" text-anchor="middle">24</text>
</g>'''
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="{paper}"/>{"".join(paths)}{ticks}{hrs}{text}</svg>'
open('preview.svg','w').write(svg)
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=1100">
<title>The Long Exhale</title>
<style>html,body{{margin:0;padding:0;background:{paper};}}body{{display:flex;justify-content:center;align-items:center;min-height:100vh;}}svg{{display:block;max-width:100vw;height:auto;}}</style>
</head><body>
{svg}
</body></html>'''
open('/tmp/claude-0/s131/mk/m15/work/index.html','w').write(html)
print(len(html))
