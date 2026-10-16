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
base=84.0; KV=1.05; SIG=1.4
ok=[r for r in recs if r[3]<=18]; spikes=[r for r in recs if r[3]>18]
print('spikes',len(spikes))
def val(tabs):
    num=den=0.0
    for t,cy,w,up in ok:
        dt=t-tabs
        if abs(dt)>4*SIG: continue
        k=w*math.exp(-0.5*(dt/SIG)**2); num+=k*(base-cy); den+=k
    return num/den if den>1e-9 else None
def runmean(tabs):
    num=den=0.0
    for t,cy,w,up in ok:
        if abs(t-tabs)<=12: num+=w*(base-cy); den+=w
    return num/den if den else 0
RM={}
def rm(ta):
    k=round(ta*2)/2
    if k not in RM: RM[k]=runmean(k)
    return RM[k]
rows=[]
for d in range(NR):
    pts_=[]
    for i in range(0,48*4+1):
        h=i/4; ta=d*24+h
        if ta>1463.0: break
        v=val(ta)
        if v is None: continue
        pts_.append((L+h*hx, T+d*rowh - (v-rm(ta))*KV))
    rows.append(pts_)
dots=[]
for t,cy,w,up in recs:
    d=int(t//24); h=t-d*24
    for row,hh in ((d,h),(d-1,h+24)):
        if 0<=row<NR: dots.append((L+hh*hx, T+row*rowh-((base-cy)-rm(t))*KV, up>18, w, T+row*rowh))
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
# lunar ghost: a 24.84 h rhythm drifts +0.84 h/day; plotted in both halves, broken at wraps
segs=[]; cur=[]; prev=None
for d in range(NR):
    for off in (0,):
        pass
for half in (0,1):
    cur=[]; prev=None
    for d in range(NR):
        h=(phmax+0.84*d)%24
        x=L+(h+24*half)*hx; y=T+d*rowh+4
        if prev is not None and h<prev:
            if len(cur)>1: segs.append(cur)
            cur=[]
        cur.append((x,y)); prev=h
    if len(cur)>1: segs.append(cur)
gx=max(segs,key=len)
for sg in segs:
    seg=' '.join(f'{x:.1f},{y:.1f}' for x,y in sg)
    s.append(f'<polyline points="{seg}" fill="none" stroke="{RUST}" stroke-width="1.1" stroke-dasharray="1.5 4.5" stroke-linecap="round" opacity="0.7"/>')
for d,pr in enumerate(rows):
    if len(pr)<2: continue
    by=T+d*rowh
    pos=[(x,min(y,by)) for x,y in pr]
    path='M%.1f,%.1f '%(pos[0][0],by)+' '.join('L%.1f,%.1f'%p_ for p_ in pos)+' L%.1f,%.1f Z'%(pos[-1][0],by)
    s.append(f'<path d="{path}" fill="{INK}" fill-opacity="0.9"/>')
    line=' '.join('%.1f,%.1f'%(x,max(y,by-0.0) if y>by else by) for x,y in pr)
    low=' '.join('%.1f,%.1f'%(x,y) for x,y in pr)
    s.append(f'<polyline points="{low}" fill="none" stroke="{INK}" stroke-width="0.55" stroke-opacity="0.45"/>')
for x,y,sp,w,by in dots:
    if sp: s.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{by:.1f}" stroke="{RUST}" stroke-width="1.1"/><circle cx="{x:.1f}" cy="{y:.1f}" r="1.8" fill="{RUST}"/>')
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
for sg in segs: dr.line(sg,fill=RUST)
for d,pr in enumerate(rows):
    if len(pr)<2: continue
    by=T+d*rowh
    pos=[(x,min(y,by)) for x,y in pr]
    dr.polygon([(pos[0][0],by)]+pos+[(pos[-1][0],by)],fill=INK)
    dr.line(pr,fill='#9a9a96')
for x,y,sp,w,by in dots:
    if sp: dr.line([(x,y),(x,by)],fill=RUST); dr.ellipse([x-2,y-2,x+2,y+2],fill=RUST)
im.save('preview.png')
print('html bytes',len(html))
