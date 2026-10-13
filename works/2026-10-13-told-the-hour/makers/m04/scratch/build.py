import sys, base64, math
from PIL import Image
src=sys.argv[1]; out=sys.argv[2]
g=Image.open(src).convert('L'); W,H=g.size
N=1464
raw=open(src,'rb').read(); b64=base64.b64encode(raw).decode()
# darkness with noise floor
D=[[max(0,(1-g.getpixel((x,y))/255-0.12)/0.88) for y in range(H)] for x in range(W)]
# hours per column: column x covers [x*N/W, (x+1)*N/W)
cnt=[round((x+1)*N/W)-round(x*N/W) for x in range(W)]
assert sum(cnt)==N
alloc=[]
for x in range(W):
    w=D[x]; s=sum(w); q=[cnt[x]*v/s for v in w]
    f=[int(v) for v in q]; r=cnt[x]-sum(f)
    for i in sorted(range(H),key=lambda i:-(q[i]-f[i]))[:r]: f[i]+=1
    alloc.append(f)
assert sum(map(sum,alloc))==N
CW=25; X0=50; Y0=170; CH=25
ink='var(--ink)'
parts=[]
# washes
for x in range(W):
    for y in range(H):
        v=g.getpixel((x,y)); a=(255-v)/255
        if a>0.02: parts.append(f'<rect x="{X0+x*CW}" y="{Y0+y*CH}" width="{CW}" height="{CH}" fill="var(--wash)" fill-opacity="{a*0.55:.3f}"/>')
# dots on a lattice inside each cell
for x in range(W):
    for y in range(H):
        n=alloc[x][y]
        if not n: continue
        k=math.ceil(math.sqrt(n)); rows=math.ceil(n/k)
        step=CW/(k+1); vstep=CH/(rows+1)
        i=0
        for r in range(rows):
            m=min(k,n-r*k); off=(CW-(m-1)*step)/2
            for c in range(m):
                cx=X0+x*CW+off+c*step; cy=Y0+y*CH+(r+1)*vstep
                parts.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="1.55"/>')
                i+=1
dots='\n'.join(parts)
# time strip
TY=Y0+H*CH+48; TW=W*CW
strip=[]
for x in range(W+1):
    px=X0+x*CW
    strip.append(f'<line x1="{px}" y1="{TY}" x2="{px}" y2="{TY+14}" class="col"/>')
for d in range(62):
    px=X0+d*TW/61
    strip.append(f'<line x1="{px:.2f}" y1="{TY+22}" x2="{px:.2f}" y2="{TY+36}" class="day"/>')
# per-column hour counts
for x in range(W):
    strip.append(f'<text x="{X0+x*CW+CW/2}" y="{TY-8}" class="n">{cnt[x]}</text>')
strip='\n'.join(strip)
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Thirty-Six and a Half Hours</title>
<style>
:root{{--bg:#f3f0e8;--ink:#1d1c1a;--wash:#8a8478;--soft:#8c877c;--rule:#bdb7aa}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#16161a;--ink:#ece8de;--wash:#9a948a;--soft:#8a857c;--rule:#4a4842}}}}
:root[data-theme="dark"]{{--bg:#16161a;--ink:#ece8de;--wash:#9a948a;--soft:#8a857c;--rule:#4a4842}}
html,body{{margin:0;background:var(--bg);color:var(--ink)}}
body{{display:flex;justify-content:center;align-items:center;min-height:100vh;overflow:hidden}}
svg{{width:1100px;height:800px;max-width:100vw;max-height:100vh;display:block}}
text{{font-family:Georgia,'Times New Roman',serif;fill:var(--ink)}}
.t{{font-size:22px;letter-spacing:.01em}}
.s{{font-size:13px;fill:var(--soft);font-style:italic}}
.n{{font-size:8.5px;fill:var(--soft);text-anchor:middle;font-family:ui-monospace,Menlo,monospace}}
.lab{{font-size:11px;fill:var(--soft);font-family:ui-monospace,Menlo,monospace}}
.col{{stroke:var(--ink);stroke-width:1}}
.day{{stroke:var(--soft);stroke-width:.8}}
circle{{fill:var(--ink)}}
img.orig{{image-rendering:auto}}
</style></head><body>
<svg viewBox="0 0 1100 800" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="1,464 hourly values redrawn from a 40 by 12 pixel picture: each pixel column holds about 36.6 hours, shown as dots placed by how dark the pixel was">
<text x="{X0}" y="78" class="t">Thirty-Six and a Half Hours</text>
<text x="{X0}" y="104" class="s">1,464 hours, as they survived a picture forty pixels wide. Every dot is one hour; it is put in the pixel that went dark, not where the value was.</text>
<g>{dots}</g>
<rect x="{X0}" y="{Y0}" width="{TW}" height="{H*CH}" fill="none" stroke="var(--rule)" stroke-width=".8"/>
<g>{strip}</g>
<text x="{X0+TW+8}" y="{TY+11}" class="lab">pixels</text>
<text x="{X0+TW+8}" y="{TY+33}" class="lab">days</text>
<text x="{X0}" y="{TY+60}" class="lab">hour 1</text>
<text x="{X0+TW}" y="{TY+60}" class="lab" text-anchor="end">hour 1,464</text>
<image x="{X0}" y="{TY+100}" width="40" height="12" href="data:image/jpeg;base64,{b64}"/>
<text x="{X0+52}" y="{TY+110}" class="s">the whole record, as received, at its own size. Forty columns cannot keep sixty-one days: each takes a day and a half,</text>
<text x="{X0+52}" y="{TY+128}" class="s">so no pixel holds a single day, and whatever rose and fell within a day survives only as the thickness of the band.</text>
</svg>
</body></html>'''
open(out,'w').write(html)
print(len(html), max(max(a) for a in alloc))
