import json, math, statistics
from PIL import Image, ImageDraw
pts=json.load(open('pts.json'))
X0,X1=2.4988,296.0037; HP=1463/(X1-X0)
recs=[]
for cx,cy,w in pts:
    t=(cx-X0)*HP; v=-cy
    recs.append([t,cy,w])
# local median for spike flag
for r in recs:
    nb=[q[1] for q in recs if abs(q[0]-r[0])<=30]
    r.append(statistics.median(nb)-r[1])   # height above local median (px)
ymed=statistics.median(r[1] for r in recs)
# daily phase of max
c=sum((ymed-r[1])*complex(math.cos(2*math.pi*r[0]/24),math.sin(2*math.pi*r[0]/24)) for r in recs)
phmax=(math.degrees(math.atan2(c.imag,c.real))%360)/360*24
print('hour-of-day of daily max (from record start):',round(phmax,2),' n',len(recs))
Wd,Ht=1100,800
L,R,T,B=84,44,118,92
PW=Wd-L-R; PH=Ht-T-B
NR=61; rowh=PH/(NR-1+0.0); hx=PW/48; K=0.40
BG='#f3efe6'; INK='#1c2630'; RUST='#b4502c'; GUIDE='#cfc7b8'; MUTED='#7d7468'
els=[]
def circ(x,y,r,col,op): els.append(('c',x,y,r,col,op))
for t,cy,w,up in recs:
    d=int(t//24); h=t-d*24
    dev=(ymed-cy)*K
    spike=up>18
    rr=0.9+0.55*math.sqrt(w/600)
    col=RUST if spike else INK; op=0.95 if spike else 0.78
    # double plot: day d appears in row d (left half) and row d-1 (right half)
    if d<NR: circ(L+h*hx, T+d*rowh-dev, rr, col, op)
    if d-1>=0: circ(L+(h+24)*hx, T+(d-1)*rowh-dev, rr, col, op)
# svg
s=[]
s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd} {Ht}" width="{Wd}" height="{Ht}" role="img" aria-label="Sixty-one days of an hourly record stacked one day per row, double-plotted over 48 hours; a single dark stripe stands upright through every row.">')
s.append(f'<rect width="{Wd}" height="{Ht}" fill="{BG}"/>')
# guides
for hh in range(0,49,3):
    x=L+hh*hx
    sw=1.1 if hh in (0,24,48) else 0.6
    op=0.9 if hh in (0,24,48) else (0.55 if hh%6==0 else 0.25)
    s.append(f'<line x1="{x:.1f}" y1="{T-22}" x2="{x:.1f}" y2="{T+PH+18}" stroke="{GUIDE}" stroke-width="{sw}" opacity="{op}"/>')
    if hh%6==0:
        s.append(f'<text x="{x:.1f}" y="{T+PH+40}" text-anchor="middle" class="tk">{hh%24 if hh<48 else 24}</text>')
for d in range(0,NR,10):
    s.append(f'<text x="{L-16}" y="{T+d*rowh+3:.1f}" text-anchor="end" class="tk">{d+1}</text>')
s.append(f'<text x="{L-16}" y="{T+(NR-1)*rowh+3:.1f}" text-anchor="end" class="tk">61</text>')
# lunar ghost: a rhythm of 24.84 h would drift +0.84 h per day; start at phmax
gx=[];
for d in range(NR):
    h=phmax+0.84*d
    gx.append((L+(h%48)*hx, T+d*rowh))
seg=' '.join(f'{x:.1f},{y:.1f}' for x,y in gx)
s.append(f'<polyline points="{seg}" fill="none" stroke="{RUST}" stroke-width="1" stroke-dasharray="2 5" opacity="0.55"/>')
lx,ly=gx[-1]
s.append(f'<text x="{lx+8:.1f}" y="{ly+4:.1f}" class="gh">where a lunar day would have carried it</text>')
for kind,x,y,r,col,op in els:
    s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{col}" fill-opacity="{op}"/>')
# titles
s.append(f'<text x="{L}" y="52" class="ti">Held to the Sun</text>')
s.append(f'<text x="{L}" y="80" class="st">Sixty-one days of a harbour record, one day to a row, each row followed by the next day. The highs stand upright: they keep a 24-hour clock.</text>')
s.append(f'<text x="{L+PW/2:.1f}" y="{T+PH+62}" text-anchor="middle" class="ax">hours, counted from the first reading</text>')
s.append(f'<text x="{L-46}" y="{T+PH/2:.1f}" text-anchor="middle" class="ax" transform="rotate(-90 {L-46} {T+PH/2:.1f})">day</text>')
s.append(f'<circle cx="{Wd-R-262}" cy="{Ht-26}" r="2.6" fill="{RUST}"/><text x="{Wd-R-254}" y="{Ht-22}" class="tk" text-anchor="start">readings that leap far above their neighbours</text>')
s.append('</svg>')
svg='\n'.join(s)
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Held to the Sun</title>
<style>
:root{{--bg:{BG};}}
html,body{{margin:0;background:var(--bg);}}
body{{display:flex;justify-content:center;align-items:center;min-height:100vh;}}
svg{{display:block;width:100%;max-width:1100px;height:auto;}}
text{{font-family:Georgia,"Iowan Old Style","Palatino Linotype",serif;fill:{INK};}}
.ti{{font-size:30px;letter-spacing:.5px;}}
.st{{font-size:15px;fill:{MUTED};font-style:italic;}}
.tk{{font-size:11.5px;fill:{MUTED};font-family:ui-monospace,Menlo,Consolas,monospace;}}
.ax{{font-size:12.5px;fill:{MUTED};font-style:italic;}}
.gh{{font-size:11.5px;fill:{RUST};font-style:italic;opacity:.8;}}
</style></head><body>
{svg}
</body></html>
'''
open('/tmp/claude-0/s130/mk/m10/work/index.html','w').write(html)
# preview
im=Image.new('RGB',(Wd,Ht),BG); dr=ImageDraw.Draw(im)
for hh in range(0,49,3):
    x=L+hh*hx; dr.line([(x,T-22),(x,T+PH+18)],fill=GUIDE)
dr.line(gx,fill=RUST)
for kind,x,y,r,col,op in els:
    dr.ellipse([x-r,y-r,x+r,y+r],fill=col)
dr.text((L,40),"Held to the Sun",fill=INK)
im.save('preview.png')
print('html bytes',len(html))
