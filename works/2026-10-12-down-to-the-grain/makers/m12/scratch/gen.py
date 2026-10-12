import json,math
F=json.load(open('/tmp/claude-0/s122/mk/m12/scratch/fit.json'))
v=F['v'][:]; meas=[1-x for x in F['f']]; N=len(v)
def rough(a,b):
  return sum(abs(v[t-1]-2*v[t]+v[t+1]) for t in range(max(1,a),min(N-1,b)))
# swap adjacent mis-ordered pairs
sw=0
for t in range(1,N-2):
  r0=rough(t-1,t+3); v[t],v[t+1]=v[t+1],v[t]; r1=rough(t-1,t+3)
  if r1<r0*0.6 and r0-r1>60: sw+=1
  else: v[t],v[t+1]=v[t+1],v[t]
# remaining single outliers -> unmeasured
def interp():
  for t in range(N):
    if not meas[t]:
      a=t-1
      while a>=0 and not meas[a]: a-=1
      b=t+1
      while b<N and not meas[b]: b+=1
      if a<0: v[t]=v[b]
      elif b>=N: v[t]=v[a]
      else: v[t]=v[a]+(v[b]-v[a])*(t-a)/(b-a)
interp()
out=0
for t in range(1,N-1):
  if (v[t]-v[t-1])*(v[t]-v[t+1])>0 and min(abs(v[t]-v[t-1]),abs(v[t]-v[t+1]))>25:
    meas[t]=0; out+=1
interp()
print('swaps',sw,'outliers',out,'unmeasured',N-sum(meas))
json.dump({'v':[round(x,1) for x in v],'m':meas},open('/tmp/claude-0/s122/mk/m12/scratch/clean.json','w'))

L=24.8412; off=-6.37
W,H=1100,800
x0,x1=170,930
top=104; gap=9.6; k=0.55; base=26
rows=math.ceil((N-off)/L)
def val(t):
  if t<=0: return v[0]
  if t>=N-1: return v[N-1]
  i=int(t); f=t-i; return v[i]*(1-f)+v[i+1]*f
paths=[]
for r in range(rows):
  t0=off+r*L; t1=t0+L
  ts=max(t0,0); te=min(t1,N-1)
  pts=[ts]+[t for t in range(math.ceil(ts),math.floor(te)+1) if ts<t<te]+[te]
  yb=top+r*gap
  X=lambda t:x0+(t-t0)/L*(x1-x0)
  Y=lambda t:yb-(val(t)-base)*k
  line=' '.join('%.1f,%.1f'%(X(t),Y(t)) for t in pts)
  poly='%.1f,%.1f '%(X(pts[0]),yb+1.5)+line+' %.1f,%.1f'%(X(pts[-1]),yb+1.5)
  dots=''.join('<circle cx="%.1f" cy="%.1f" r="1.25"/>'%(X(t),Y(t)) for t in range(math.ceil(ts),math.floor(te)+1) if t0<=t<t1 and meas[t])
  paths.append('<g><polygon class="f" points="%s"/><polyline class="l" points="%s"/><g class="d">%s</g></g>'%(poly,line,dots))
# hour ticks for lunar day: high water columns at 1/4,3/4
ylast=top+(rows-1)*gap
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Sixty-one days of hourly values folded into rows of 24 hours 50 minutes, stacked as ridgelines">
<rect width="{W}" height="{H}" fill="#f3efe6"/>
<line x1="{x0+(x1-x0)/4:.1f}" y1="{top-70}" x2="{x0+(x1-x0)/4:.1f}" y2="{ylast+14}" class="g"/>
<line x1="{x0+3*(x1-x0)/4:.1f}" y1="{top-70}" x2="{x0+3*(x1-x0)/4:.1f}" y2="{ylast+14}" class="g"/>
{''.join(paths)}
<text x="{x0}" y="{ylast+52}" class="t">Twice a Moon-Day</text>
<text x="{x0}" y="{ylast+71}" class="s">1,464 hours, one dot each, cut every 24 h 50 min and stacked downward. Same height on the page, same moment in the moon's day.</text>
</svg>'''
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Twice a Moon-Day</title>
<style>
html,body{{margin:0;background:#f3efe6;}}
body{{display:flex;align-items:center;justify-content:center;min-height:100vh;}}
svg{{display:block;max-width:100vw;max-height:100vh;width:auto;height:auto;}}
.f{{fill:#f3efe6;stroke:none}}
.l{{fill:none;stroke:#1d2a33;stroke-width:.7;stroke-linejoin:round;opacity:.55}}
.d circle{{fill:#14202a}}
.g{{stroke:#9fb3bf;stroke-width:.6;stroke-dasharray:1 4}}
.t{{font:600 17px Georgia,'Times New Roman',serif;fill:#14202a;letter-spacing:.02em}}
.s{{font:12px Georgia,'Times New Roman',serif;fill:#55626b;font-style:italic}}
</style></head><body>
{svg}
</body></html>'''
open('/tmp/claude-0/s122/mk/m12/work/index.html','w').write(html)
print(rows, ylast)
