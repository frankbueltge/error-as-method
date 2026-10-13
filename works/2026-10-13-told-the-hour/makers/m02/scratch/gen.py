import json, statistics
vals=json.load(open('vals.json'))
N=len(vals); WK=168
weeks=(N+WK-1)//WK  # 9
ordinary=[w for w in range(weeks) if w not in (5,6)]
ghost=[]
for h in range(WK):
  xs=[vals[w*WK+h] for w in ordinary if w*WK+h<N]
  ghost.append(statistics.median(xs))
g2=[sum(ghost[(h+k)%WK] for k in (-2,-1,0,1,2))/5 for h in range(WK)]
ghost=g2
Wd,Hd=1100,800
L,R=86,1052
pxh=(R-L)/WK
top=116; pitch=72; rh=64
vmin,vmax=14,82
def Y(row,v): return top+row*pitch+rh-(v-vmin)/(vmax-vmin)*rh
def X(h): return L+(h+0.5)*pxh
o=[]
ap=o.append
ap(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd} {Hd}" width="{Wd}" height="{Hd}" role="img" aria-label="A record of 1,464 readings folded into nine weekly rows, each set against the median ordinary week">')
ap(f'<rect width="{Wd}" height="{Hd}" fill="#f6f3ec"/>')
# title
ap(f'<text x="{L}" y="62" font-family="Georgia, \'Times New Roman\', serif" font-size="27" fill="#23211d" letter-spacing="0.3">Against the Usual Week</text>')
ap(f'<text x="{L}" y="88" font-family="Georgia, serif" font-style="italic" font-size="13.5" fill="#6d675c">1,464 readings, cut every 168 and laid one week under the next.</text>')
for row in range(weeks):
  base=top+row*pitch+rh
  # ghost area
  pts=[f'{X(0)-pxh/2:.1f},{base:.1f}']
  hmax=min(WK,N-row*WK)
  for h in range(hmax): pts.append(f'{X(h):.1f},{Y(row,ghost[h]):.1f}')
  pts.append(f'{X(hmax-1)+pxh/2:.1f},{base:.1f}')
  ap(f'<polygon points="{" ".join(pts)}" fill="#e9e3d6"/>')
  # day ticks
  for d in range(0,8):
    if d*24>hmax: break
    x=L+d*24*pxh
    ap(f'<line x1="{x:.1f}" y1="{base+3:.1f}" x2="{x:.1f}" y2="{base+7:.1f}" stroke="#b9b1a2" stroke-width="0.8"/>')
  ap(f'<line x1="{L:.1f}" y1="{base+0.5:.1f}" x2="{L+hmax*pxh:.1f}" y2="{base+0.5:.1f}" stroke="#cfc7b8" stroke-width="0.6"/>')
  # row numeral
  ap(f'<text x="{L-22}" y="{base-rh/2+5:.1f}" text-anchor="end" font-family="Georgia, serif" font-size="12" fill="#9a9284">{row+1}</text>')
  # differences + dots
  for h in range(hmax):
    v=vals[row*WK+h]; gv=ghost[h]
    x=X(h); y=Y(row,v); gy=Y(row,gv)
    if v<gv-6:
      ap(f'<line x1="{x:.1f}" y1="{gy:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="#c4472d" stroke-width="{pxh*0.5:.2f}" stroke-opacity="{min(0.8,0.12+(gv-v)/40):.2f}"/>')
    elif v>gv+6:
      ap(f'<line x1="{x:.1f}" y1="{gy:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="#4f6f86" stroke-width="{pxh*0.5:.2f}" stroke-opacity="{min(0.7,0.12+(v-gv)/45):.2f}"/>')
  for h in range(hmax):
    v=vals[row*WK+h]
    ap(f'<circle cx="{X(h):.1f}" cy="{Y(row,v):.1f}" r="1.45" fill="#1f1d1a"/>')
# end mark
lastrow=weeks-1; hmax=N-lastrow*WK
ap(f'<text x="{X(hmax-1)+10:.1f}" y="{top+lastrow*pitch+rh-4:.1f}" font-family="Georgia, serif" font-style="italic" font-size="11.5" fill="#8a8274">the record ends</text>')
# legend
ly=top+weeks*pitch+22
ap(f'<g font-family="Georgia, serif" font-size="12" fill="#6d675c">')
ap(f'<rect x="{L}" y="{ly-9}" width="22" height="10" fill="#e9e3d6"/><text x="{L+30}" y="{ly}">the usual week: hour by hour, the median of the seven weeks that kept to it</text>')
ap(f'<rect x="{L+520}" y="{ly-9}" width="5" height="10" fill="#c4472d" fill-opacity="0.75"/><text x="{L+532}" y="{ly}">short of it</text>')
ap(f'<rect x="{L+620}" y="{ly-9}" width="5" height="10" fill="#4f6f86" fill-opacity="0.6"/><text x="{L+632}" y="{ly}">beyond it</text>')
ap(f'<text x="{R}" y="{ly}" text-anchor="end" fill="#9a9284">ticks: every 24 readings</text>')
ap('</g></svg>')
svg='\n'.join(o)
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Against the Usual Week</title>
<style>html,body{{margin:0;padding:0;background:#f6f3ec;}}body{{display:flex;justify-content:center;align-items:flex-start;min-height:100vh;}}svg{{display:block;max-width:100%;height:auto;}}</style>
</head><body>
{svg}
</body></html>'''
open('/tmp/claude-0/s123/mk/m02/work/index.html','w').write(html)
print(len(html))
