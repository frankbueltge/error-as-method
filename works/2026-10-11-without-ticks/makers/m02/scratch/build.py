import json,math,datetime as dt
d=json.load(open('res.json'))
W,H=1100,800
x0,y0,cw,rh,gap=64,162,2.72,27,3
def col(m,dd): return (dt.date(2000,m,dd)-dt.date(2000,1,1)).days
def X(m,dd): return x0+col(m,dd)*cw
def Y(y): return y0+(y-2000)*(rh+gap)
paper=(246,243,238); mid=(228,222,212); ink=(24,30,44); hot=(196,58,36)
def mix(a,b,t): return tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))
def color(r):
  lr=math.log(r)
  if lr<0: t=min(1,max(0,-lr-0.03)/0.52)**0.8; c=mix(mid,ink,t)
  else: t=min(1,max(0,lr-0.03)/0.14)**0.8; c=mix(mid,hot,t)
  return '#%02x%02x%02x'%c
o=[]
A=o.append
A(f'<rect width="{W}" height="{H}" fill="#f6f3ee"/>')
# title
A('<text x="64" y="58" class="t">Appointed Days</text>')
A('<text x="64" y="86" class="s">Births in the United States, every day from 1 January 2000 to 31 December 2014, measured against the day one would expect</text>')
# month labels
mn=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
for i,n in enumerate(mn):
  x=X(i+1,1)
  A(f'<line x1="{x:.1f}" y1="{y0-14}" x2="{x:.1f}" y2="{y0-4}" class="tk"/>')
  A(f'<text x="{x+3:.1f}" y="{y0-6}" class="m">{n}</text>')
# cells
for y,m,dd,dw,b,r in d:
  A(f'<rect x="{X(m,dd):.2f}" y="{Y(y)}" width="{cw+0.35:.2f}" height="{rh}" fill="{color(r)}"/>')
for y in range(2000,2015):
  A(f'<text x="{x0-10}" y="{Y(y)+rh/2+4}" class="y">{y}</text>')
xe=X(12,31)+cw
# staircase: n/n/0n
pts=[]
for n in range(1,13):
  y=2000+n; x=X(n,n)+cw/2; yy=Y(y)+rh/2; pts.append((x,yy,n))
A('<polyline points="'+' '.join(f'{x:.1f},{yy:.1f}' for x,yy,n in pts)+'" class="st"/>')
for x,yy,n in pts:
  cls='ring6' if n==6 else 'ring'
  A(f'<rect x="{x-4.5:.1f}" y="{yy-rh/2-2.5:.1f}" width="9" height="{rh+5}" rx="1.5" class="{cls}"/>')
# labels for staircase
x,yy,_=pts[5]
A(f'<text x="{x+9:.1f}" y="{yy-1:.1f}" class="a">6/6/06</text>')
A(f'<text x="{x+9:.1f}" y="{yy+11:.1f}" class="a2">16% below expected, the date avoided</text>')
x,yy,_=pts[8]
A(f'<text x="{x+9:.1f}" y="{yy-1:.1f}" class="a">9/9/09 · 16,081 births</text>')
A(f'<text x="{x+9:.1f}" y="{yy+11:.1f}" class="a2">the busiest day in fifteen years</text>')
x,yy,_=pts[11]
A(f'<text x="{x-9:.1f}" y="{yy+4:.1f}" class="a" text-anchor="end">12/12/12</text>')
x,yy,_=pts[10]
A(f'<text x="{x-9:.1f}" y="{yy+4:.1f}" class="a" text-anchor="end">11/11/11 · 20% above</text>')
x,yy,_=pts[1]
A(f'<text x="{x+9:.1f}" y="{yy+4:.1f}" class="a">2/2/02</text>')
x,yy,_=pts[0]
A(f'<text x="{x+9:.1f}" y="{yy+4:.1f}" class="a">1/1/01 (also New Year’s Day)</text>')
# bottom holiday labels
yb=Y(2014)+rh+14
def low(m,dd,txt,anchor='middle',dx=0):
  x=X(m,dd)+cw/2
  A(f'<line x1="{x:.1f}" y1="{yb-9}" x2="{x:.1f}" y2="{yb-3}" class="tk"/>')
  A(f'<text x="{x+dx:.1f}" y="{yb+9}" class="h" text-anchor="{anchor}">{txt}</text>')
low(1,1,'1 Jan','start',-1.5)
low(7,4,'4 Jul')
low(10,31,'31 Oct')
low(12,25,'25 Dec','end',1.5)
# Thanksgiving & Labor Day: label the moving lines
A(f'<text x="{X(11,25)+cw/2:.1f}" y="{yb+21}" class="h" text-anchor="middle">Thanksgiving</text>')
A(f'<line x1="{X(11,22):.1f}" y1="{yb-6}" x2="{X(11,28)+cw:.1f}" y2="{yb-6}" class="tk"/>')
A(f'<text x="{X(9,4)+cw/2:.1f}" y="{yb+9}" class="h" text-anchor="middle">Labor Day</text>')
A(f'<line x1="{X(9,1):.1f}" y1="{yb-6}" x2="{X(9,7)+cw:.1f}" y2="{yb-6}" class="tk"/>')
A(f'<text x="{X(5,28)+cw/2:.1f}" y="{yb+9}" class="h" text-anchor="middle">Memorial Day</text>')
A(f'<line x1="{X(5,25):.1f}" y1="{yb-6}" x2="{X(5,31)+cw:.1f}" y2="{yb-6}" class="tk"/>')
A(f'<text x="{X(2,29)+cw/2:.1f}" y="{yb+9}" class="h" text-anchor="middle">29 Feb</text>')
A(f'<line x1="{X(2,29)+cw/2:.1f}" y1="{yb-9}" x2="{X(2,29)+cw/2:.1f}" y2="{yb-3}" class="tk"/>')
# legend
ly=yb+44
A(f'<text x="64" y="{ly-8}" class="lg">births ÷ expected for that weekday and season</text>')
stops=[0.5,0.6,0.7,0.8,0.9,1.0,1.05,1.1,1.15,1.2]
lw=440; lx=64
N=120
lo,hi=math.log(0.5),math.log(1.2)
for i in range(N):
  r=math.exp(lo+(hi-lo)*(i+0.5)/N)
  A(f'<rect x="{lx+i*lw/N:.2f}" y="{ly}" width="{lw/N+0.4:.2f}" height="10" fill="{color(r)}"/>')
for s in [0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2]:
  x=lx+(math.log(s)-lo)/(hi-lo)*lw
  A(f'<line x1="{x:.1f}" y1="{ly+10}" x2="{x:.1f}" y2="{ly+14}" class="tk"/>')
  A(f'<text x="{x:.1f}" y="{ly+25}" class="lg" text-anchor="middle">{"as expected" if s==1.0 else ("×%.1f"%s)}</text>')
# note text
nx=560
note=["Each cell is one day: a row per year, a column per date. The weekly beat",
"is taken out (a typical Tuesday has 13,100 births, a Sunday 7,500), and so",
"is the slow swell of the seasons. What is left is what the calendar did:",
"births pushed off holidays into the days around them, and drawn toward",
"dates that read well on a birth certificate."]
for i,t in enumerate(note): A(f'<text x="{nx}" y="{ly-8+i*15}" class="n">{t}</text>')
A(f'<text x="{W-40}" y="{H-14}" class="src" text-anchor="end">Data: Social Security Administration, via FiveThirtyEight (CC BY 4.0) · 5,479 days</text>')
css='''
body{margin:0;background:#f6f3ee}
svg{display:block}
text{font-family:Georgia,"Times New Roman",serif;fill:#1d2230}
.t{font-size:34px;letter-spacing:.5px}
.s{font-size:14.5px;font-style:italic;fill:#4a4f5c}
.m{font-size:11px;fill:#4a4f5c}
.y{font-size:11.5px;text-anchor:end;fill:#4a4f5c;font-variant-numeric:tabular-nums}
.h{font-size:10.5px;fill:#4a4f5c}
.a{font-size:11.5px;font-weight:bold;fill:#1d2230;paint-order:stroke;stroke:#f6f3ee;stroke-width:3px}
.a2{font-size:10.5px;font-style:italic;fill:#1d2230;paint-order:stroke;stroke:#f6f3ee;stroke-width:3px}
.lg{font-size:10.5px;fill:#4a4f5c}
.n{font-size:12px;fill:#30364a}
.src{font-size:9.5px;fill:#7a7e88}
.tk{stroke:#7a7e88;stroke-width:.8}
.st{fill:none;stroke:#1d2230;stroke-width:.9;stroke-dasharray:2 2.5;opacity:.75}
.ring{fill:none;stroke:#1d2230;stroke-width:1.2}
.ring6{fill:none;stroke:#1d2230;stroke-width:1.2;stroke-dasharray:2 1.5}
'''
html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Appointed Days</title>
<meta name="viewport" content="width=1100"><style>{css}</style></head><body>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" shape-rendering="auto">
{chr(10).join(o)}
</svg></body></html>'''
open('../work/index.html','w').write(html)
print(len(html))
