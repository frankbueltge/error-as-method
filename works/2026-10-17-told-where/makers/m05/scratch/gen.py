import json
from PIL import Image, ImageDraw
D=json.load(open('hist.json'))
days=D['days']; FLOOR=D['floor']; SPAN=D['span']
def val(y): return max(0.0,(FLOOR-y)/SPAN)
VMAX=max(val(y) for y in range(81))
def profile(h):
    # h: hours per row 0..80. returns list of (t,v) monotone from noon outward
    pts=[];cum=0.0;T0=0.1
    for y,c in enumerate(h):
        if c<=0: continue
        a=cum;cum+=c
        if cum<T0: continue
        v=val(y)/1.0
        pts.append((max(a,T0)-T0,v));pts.append((cum-T0,v))
    return pts
def sample(pts,t):
    # step-ish with linear interp between consecutive points
    if not pts: return 0.0
    if t<=pts[0][0]: return pts[0][1]
    for (t1,v1),(t2,v2) in zip(pts,pts[1:]):
        if t1<=t<=t2:
            return v1 if t2==t1 else v1+(v2-v1)*(t-t1)/(t2-t1)
    # beyond total: ramp to 0 over 0.4h
    tl,vl=pts[-1]; r=(t-tl)/0.4
    return max(0.0,vl*(1-r))
Wd,Ht=1100,800
CX=550; PXH=33.0; MAXH=118.0
TOP=186; BOT=694
n=len(days); step=(BOT-TOP)/(n-1)
def smooth(a,k=2):
    out=[]
    for i in range(len(a)):
        s=a[max(0,i-k):i+k+1]; out.append(sum(s)/len(s))
    return out
ridges=[]
DT=0.1
ts=[i*DT for i in range(0,int(12.6/DT)+1)]
for i,dd in enumerate(days):
    am=profile(dd['am']); pm=profile(dd['pm'])
    L=[sample(am,t) for t in ts]; R=[sample(pm,t) for t in ts]
    L=smooth(L,4);R=smooth(R,4)
    base=TOP+i*step
    xy=[(CX-t*PXH, base-v*MAXH) for t,v in zip(ts,L)][::-1]+[(CX+t*PXH, base-v*MAXH) for t,v in zip(ts[1:],R[1:])]
    ridges.append((base,xy,max(L+R)))
json.dump([[b,[[round(x,1),round(y,1)] for x,y in xy],m] for b,xy,m in ridges],open('ridges.json','w'))
print('peaks',[round(r[2],2) for r in ridges])
# ---- SVG
X0=CX-12.6*PXH; X1=CX+12.6*PXH
stops=[(0,'#2c3646',1),(0.05,'#4a2a1c',1),(0.2,'#8a3a14',1),(0.45,'#d06a1e',1),(0.72,'#f4b54e',1),(1.0,'#fff6dc',1)]
o=[]
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd} {Ht}" width="{Wd}" height="{Ht}">')
o.append('<defs>')
for i,(b,xy,m) in enumerate(ridges):
    o.append(f'<linearGradient id="g{i}" gradientUnits="userSpaceOnUse" x1="0" y1="{b:.1f}" x2="0" y2="{b-MAXH:.1f}">'+''.join(f'<stop offset="{s}" stop-color="{c}"/>' for s,c,_ in stops)+'</linearGradient>')
o.append('<radialGradient id="sky" cx="0.5" cy="0.42" r="0.75"><stop offset="0" stop-color="#15161d"/><stop offset="1" stop-color="#07080b"/></radialGradient>')
o.append('</defs>')
o.append(f'<rect width="{Wd}" height="{Ht}" fill="url(#sky)"/>')
# noon guide
o.append(f'<line x1="{CX}" y1="{TOP-MAXH-14}" x2="{CX}" y2="{BOT+18}" stroke="#ffffff" stroke-opacity="0.05"/>')
for i,(b,xy,m) in enumerate(ridges):
    pts=' '.join(f'{x:.1f},{y:.1f}' for x,y in xy)
    # night line full width, then hill
    poly=f'{X0:.1f},{b:.1f} '+pts+f' {X1:.1f},{b:.1f} {X1:.1f},{b+3:.1f} {X0:.1f},{b+3:.1f}'
    o.append(f'<polygon points="{poly}" fill="#0a0b0f"/>')
    o.append(f'<polygon points="{X0:.1f},{b:.1f} {pts} {X1:.1f},{b:.1f}" fill="url(#g{i})" fill-opacity="0.16"/>')
    o.append(f'<polyline points="{X0:.1f},{b:.1f} {pts} {X1:.1f},{b:.1f}" fill="none" stroke="url(#g{i})" stroke-width="1.15" stroke-linejoin="round"/>')
# ticks
ty=BOT+24
for h in (-12,-9,-6,-3,0,3,6,9,12):
    x=CX+h*PXH
    o.append(f'<line x1="{x}" y1="{ty-4}" x2="{x}" y2="{ty}" stroke="#8a7a66" stroke-opacity="0.6"/>')
    lab='noon' if h==0 else f'{abs(h)} h'
    o.append(f'<text x="{x}" y="{ty+14}" fill="#8a7a66" font-size="10" text-anchor="middle" font-family="Georgia, \'Times New Roman\', serif" letter-spacing="0.5">{lab}</text>')
F="font-family=\"Georgia, 'Times New Roman', serif\""
o.append(f'<text x="64" y="768" fill="#efe2c8" font-size="24" {F} letter-spacing="1">Gathered Light</text>')
o.append(f'<text x="64" y="788" fill="#9a8b76" font-size="12.5" {F} font-style="italic">1,464 hours, one ridge for each turn of the day, the first at the top</text>')
o.append(f'<text x="1036" y="752" fill="#9a8b76" font-size="11" {F} text-anchor="end" font-style="italic">each morning’s hours and each afternoon’s hours</text>')
o.append(f'<text x="1036" y="768" fill="#9a8b76" font-size="11" {F} text-anchor="end" font-style="italic">are laid out from noon, the strongest nearest;</text>')
o.append(f'<text x="1036" y="784" fill="#9a8b76" font-size="11" {F} text-anchor="end" font-style="italic">a ridge is as wide as the hours that rose above the dark</text>')
o.append('</svg>')
svg='\n'.join(o)
open('art.svg','w').write(svg)
# ---- PIL preview
S=1
img=Image.new('RGB',(Wd,Ht),(10,11,15))
def grad(v):
    import bisect
    cols=[(0,(0x2c,0x36,0x46)),(0.05,(0x4a,0x2a,0x1c)),(0.2,(0x8a,0x3a,0x14)),(0.45,(0xd0,0x6a,0x1e)),(0.72,(0xf4,0xb5,0x4e)),(1.0,(0xff,0xf6,0xdc))]
    v=max(0,min(1,v))
    for (a,ca),(b,cb) in zip(cols,cols[1:]):
        if a<=v<=b:
            f=(v-a)/(b-a); return tuple(int(ca[j]+(cb[j]-ca[j])*f) for j in range(3))
for i,(b,xy,m) in enumerate(ridges):
    poly=[(X0,b)]+xy+[(X1,b)]
    dr=ImageDraw.Draw(img)
    dr.polygon(poly+[(X1,b+3),(X0,b+3)],fill=(10,11,15))
    # gradient fill
    mask=Image.new('L',(Wd,Ht),0); ImageDraw.Draw(mask).polygon(poly,fill=41)
    gl=Image.new('RGB',(Wd,Ht))
    gd=ImageDraw.Draw(gl)
    for y in range(int(b-MAXH)-1,int(b)+2):
        gd.line([(0,y),(Wd,y)],fill=grad((b-y)/MAXH))
    img=Image.composite(gl,img,mask)
    dr=ImageDraw.Draw(img)
    for (x1,y1),(x2,y2) in zip(poly,poly[1:]):
        dr.line([(x1,y1),(x2,y2)],fill=grad((b-(y1+y2)/2)/MAXH),width=1)
img.save('preview.png')
