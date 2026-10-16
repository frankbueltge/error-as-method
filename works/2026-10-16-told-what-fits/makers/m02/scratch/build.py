import json
from PIL import Image, ImageDraw
v=[round(x) for x in json.load(open('vals.json'))]
W,H=1100,800
L,R=150,950; TOP=200; BOT=690
D=61; step=(BOT-TOP)/(D-1); amp=1.5
PAPER='#f1ece2'; INK='#1c1b19'; ACC='#8a2b1d'
def pts(d):
    base=TOP+d*step
    out=[]
    for h in range(25):  # include first hour of next day for continuity
        i=min(d*24+h,len(v)-1)
        if d*24+h>=len(v): break
        x=L+(R-L)*h/24
        out.append((x, base-(v[i]-40)*amp))
    return base,out
def smooth(p):
    s=f'M{p[0][0]:.1f},{p[0][1]:.1f}'
    for i in range(1,len(p)-1):
        mx=(p[i][0]+p[i+1][0])/2; my=(p[i][1]+p[i+1][1])/2
        s+=f' Q{p[i][0]:.1f},{p[i][1]:.1f} {mx:.1f},{my:.1f}'
    s+=f' L{p[-1][0]:.1f},{p[-1][1]:.1f}'
    return s
allp=[pts(d)[1] for d in range(D)]
ys=[y for p in allp for _,y in p]
SH=(130-min(ys)) ; SC=(745-130)/(max(ys)-min(ys))
_pts=pts
def pts(d):
    b,p=_pts(d)
    return 130+(b+SH-130)*SC, [(x,130+(y+SH-130)*SC) for x,y in p]
dmax=[max(v[d*24:d*24+24]) for d in range(D)]
paths=[];prev=None
img=Image.new('RGB',(W*2,H*2),PAPER); dr=ImageDraw.Draw(img)
for d in range(D):
    base,p=pts(d)
    rise = d>0 and dmax[d]-dmax[d-1]>=6
    col=ACC if rise else INK
    sw=1.6 if rise else 0.9
    line=smooth(p)
    fill=line+f' L{p[-1][0]:.1f},{base+90:.1f} L{p[0][0]:.1f},{base+90:.1f} Z'
    paths.append(f'<path d="{fill}" fill="{PAPER}"/><path d="{line}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>')
    poly=[(x*2,y*2) for x,y in p]
    dr.polygon(poly+[(poly[-1][0],(base+90)*2),(poly[0][0],(base+90)*2)],fill=PAPER)
    dr.line(poly,fill=col,width=int(sw*2)+1)
    if False:
        paths.append(f'<text x="{L-14}" y="{p[0][1]+3:.1f}" text-anchor="end" class="n">{d+1}</text>')
        dr.text(((L-30)*2,p[0][1]*2),str(d+1),fill=INK)
img.resize((W,H)).save('preview.png')
svg='\n'.join(paths)
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Each Day a Little Lower</title>
<style>
html,body{{margin:0;height:100%;background:{PAPER};}}
body{{display:flex;align-items:center;justify-content:center;}}
svg{{width:100vw;height:100vh;max-width:1100px;max-height:800px;display:block}}
.n{{font:10px Georgia,'Times New Roman',serif;fill:#8b857a;letter-spacing:.04em}}
.t{{font:italic 26px Georgia,'Times New Roman',serif;fill:{INK}}}
.s{{font:11px Georgia,'Times New Roman',serif;fill:#6f695f;letter-spacing:.06em}}
</style></head><body>
<svg viewBox="0 0 {W} {H}" role="img" aria-label="Sixty-one days of an hourly record, one line per day, stacked top to bottom">
<rect width="{W}" height="{H}" fill="{PAPER}"/>
<text x="{L}" y="64" class="t">Each Day a Little Lower</text>
<text x="{L}" y="88" class="s">61 days, one line each, read downward · 24 hours, left to right · a line drawn in red rose above the day before</text>
{svg}
<line x1="{L}" y1="{760}" x2="{R}" y2="{760}" stroke="#b7b0a3" stroke-width="0.6"/>
<line x1="{L}" y1="{756}" x2="{L}" y2="{764}" stroke="#b7b0a3" stroke-width="0.6"/>
<line x1="{R}" y1="{756}" x2="{R}" y2="{764}" stroke="#b7b0a3" stroke-width="0.6"/>
<text x="{(L+R)/2}" y="{780}" text-anchor="middle" class="s">one day, from the hour the record begins</text>
</svg></body></html>'''
open('/tmp/claude-0/s131/mk/m02/work/index.html','w').write(html)
