import json
D=json.load(open('samples.json')); S=D['S']; ppd=D['ppd']; ph=D['ph']; x0=D['x0']
bins={}
for x,v,d in S:
    t=(x+0.5-x0-ph)/ppd; k=int(t//1)+1
    bins.setdefault(k,[]).append((t-(k-1),v,d,x))
K=sorted(bins)
floor={}
for k in K:
    b=sorted([s for s in bins[k] if s[2]>90],key=lambda s:s[1]); tot=sum(s[2] for s in b); acc=0
    for s in b:
        acc+=s[2]
        if acc>=0.08*tot: floor[k]=s[1]; break
# the first bin is a ~4h sliver: give it the floor of the next
floor[0]=min(floor[0],floor[1])
INK='#1f1c19'; RUST='#b0532c'; PAPER='#f3efe6'; GREY='#8d877c'
L,R=70,1030; n=len(K); cw=(R-L)/n
base=500; sy=5.2
out=[]
# upper register: each cycle from its own floor
for k in K:
    cx=L+k*cw
    for t,v,d,x in bins[k]:
        e=v-floor[k]
        if e < -3: continue
        y=base-e*sy
        a=min(1,(d/255)**1.4*1.15)
        out.append(f'<circle cx="{cx+2+t*cw*0.62:.1f}" cy="{y:.1f}" r="1.9" fill="{INK}" fill-opacity="{a:.2f}"/>')
upper='\n'.join(out); out=[]
# lower register: whole record at true value
lb=772; ls=2.1
def X(x): return L+(x+0.5-x0-ph)/ppd*cw + 2
for x,v,d in S:
    a=min(1,(d/255)**1.3)*0.8
    out.append(f'<circle cx="{X(x):.1f}" cy="{lb-v*ls:.1f}" r="1.4" fill="#6f695f" fill-opacity="{a:.2f}"/>')
lower='\n'.join(out)
fp=[(L+k*cw+cw*0.31, lb-floor[k]*ls) for k in K]
fpath='M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in fp)
farea=fpath+f' L{fp[-1][0]:.1f},{lb+8} L{fp[0][0]:.1f},{lb+8} Z'
# rust tick under each upper column, its length = that day's floor height (link between registers)
ticks='\n'.join(f'<line x1="{L+k*cw+cw*0.43:.1f}" y1="{base+3}" x2="{L+k*cw+cw*0.43:.1f}" y2="{base+3+floor[k]*0.9:.1f}" stroke="{RUST}" stroke-width="2" stroke-opacity="0.75"/>' for k in K)
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=1100">
<title>Breath over a Floor</title>
<style>
html,body{{margin:0;background:{PAPER};}}
body{{display:flex;justify-content:center;align-items:center;min-height:100vh;}}
svg{{display:block;width:1100px;height:800px;}}
text{{font-family:Georgia,'Times New Roman',serif;fill:{INK};}}
.cap{{font-family:Georgia,serif;font-size:12px;fill:{GREY};font-style:italic;letter-spacing:.2px}}
</style></head><body>
<svg viewBox="0 0 1100 800" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Sixty-one days of carbon dioxide: each daily rise drawn up from a common line, above the slow floor the days stand on.">
<rect width="1100" height="800" fill="{PAPER}"/>
<text x="{L}" y="58" font-size="26">Breath over a Floor</text>
<text x="{L}" y="80" class="cap">Sixty-one days of carbon dioxide in the air at one station, one reading an hour, cut where each day is lowest.</text>
<text x="{L}" y="96" class="cap">Above, each day's rise is lifted off its own lowest hours. Below is the whole record, with those lowest hours joined.</text>
<line x1="{L-10}" y1="{base}" x2="{R+10}" y2="{base}" stroke="{RUST}" stroke-width="1"/>
{upper}
<path d="{farea}" fill="{RUST}" fill-opacity="0.10"/>
{lower}
<path d="{fpath}" fill="none" stroke="{RUST}" stroke-width="2" stroke-linejoin="round"/>
<text x="{R}" y="{base-388}" class="cap" text-anchor="end">what each day adds</text>
<text x="{R}" y="{lb+24}" class="cap" text-anchor="end">what it stands on</text>
</svg></body></html>'''
open('/tmp/claude-0/s130/mk/m12/work/index.html','w').write(html)
print(len(html))
