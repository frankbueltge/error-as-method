import json,math
C=json.load(open('/tmp/claude-0/s122/mk/m12/scratch/clean.json')); v=C['v']; meas=C['m']; N=len(v)
L=24.8412; off=-6.37
W,H=1100,800
x0,x1=170,930; top=50; bh=9.9; gap=0.7
rows=math.ceil((N-off)/L)
stops=[(28,(241,234,217)),(80,(204,212,206)),(125,(131,158,170)),(170,(52,88,112)),(215,(19,38,58)),(334,(4,7,12))]
def col(x):
  if x<=stops[0][0]: c=stops[0][1]
  elif x>=stops[-1][0]: c=stops[-1][1]
  else:
    for (a,ca),(b,cb) in zip(stops,stops[1:]):
      if a<=x<=b:
        f=(x-a)/(b-a); c=tuple(round(ca[i]+(cb[i]-ca[i])*f) for i in range(3)); break
  return '#%02x%02x%02x'%c
def val(t):
  if t<=0: return v[0]
  if t>=N-1: return v[N-1]
  i=int(t); f=t-i; return v[i]*(1-f)+v[i+1]*f
defs=[];body=[]
for r in range(rows):
  t0=off+r*L; t1=t0+L
  ts=max(t0,0); te=min(t1,N-1)
  pts=[ts]+[t for t in range(math.ceil(ts),math.floor(te)+1) if ts<t<te]+[te]
  xa=x0+(ts-t0)/L*(x1-x0); xb=x0+(te-t0)/L*(x1-x0)
  st=''.join('<stop offset="%.4f" stop-color="%s"/>'%((t-ts)/(te-ts),col(val(t))) for t in pts)
  defs.append('<linearGradient id="g%d" gradientUnits="userSpaceOnUse" x1="%.1f" x2="%.1f" y1="0" y2="0">%s</linearGradient>'%(r,xa,xb,st))
  y=top+r*(bh+gap)
  body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="url(#g%d)"/>'%(xa,y,xb-xa,bh,r))
ylast=top+(rows-1)*(bh+gap)+bh
legend=''
lx=x1-200; ly=ylast+40
for i in range(101):
  x=28+(334-28)*i/100
  legend+='<rect x="%.1f" y="%d" width="2.1" height="6" fill="%s"/>'%(lx+i*2,ly,col(x))
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="1,464 hourly values folded into sixty rows of 24 hours 50 minutes; two dark columns of high water run down the page, darkening and fading over the fortnight, broken by one black blot of exceptionally high values late in the record">
<defs>{''.join(defs)}</defs>
<rect width="{W}" height="{H}" fill="#f6f2e9"/>
{''.join(body)}
<text x="{x0}" y="{ylast+46}" class="t">Twice a Moon-Day</text>
<text x="{x0}" y="{ylast+66}" class="s">1,464 hours, cut every 24 h 50 min and laid in rows, first at top. Darker is higher.</text>
{legend}
<text x="{lx}" y="{ly+20}" class="k">lowest</text>
<text x="{lx+202}" y="{ly+20}" class="k" text-anchor="end">highest</text>
</svg>'''
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Twice a Moon-Day</title>
<style>
html,body{{margin:0;background:#f6f2e9;}}
body{{display:flex;align-items:center;justify-content:center;min-height:100vh;}}
svg{{display:block;max-width:100vw;max-height:100vh;width:auto;height:auto;}}
.t{{font:600 17px Georgia,'Times New Roman',serif;fill:#14202a;letter-spacing:.02em}}
.s{{font:italic 12px Georgia,'Times New Roman',serif;fill:#55626b}}
.k{{font:10px Georgia,'Times New Roman',serif;fill:#6b767d}}
</style></head><body>
{svg}
</body></html>'''
open('/tmp/claude-0/s122/mk/m12/work/index.html','w').write(html)
print(rows, ylast)
