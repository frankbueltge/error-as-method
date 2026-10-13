from PIL import Image
g=Image.open('/tmp/claude-0/s123/mk/m08/work/record.jpg').convert('L')
W,H=g.size; N=1464
px=[[g.getpixel((x,y)) for x in range(W)] for y in range(H)]
bounds=[round(i*N/W) for i in range(W+1)]
alloc=[[0]*H for _ in range(W)]
for x in range(W):
    n=bounds[x+1]-bounds[x]
    ink=[max(0,255-px[y][x]) for y in range(H)]
    s=sum(ink); q=[n*i/s for i in ink]
    a=[int(v) for v in q]; rem=n-sum(a)
    for y in sorted(range(H),key=lambda y:-(q[y]-a[y]))[:rem]: a[y]+=1
    for y in range(H): alloc[x][y]=a[y]
assert sum(map(sum,alloc))==N
# layout
VW,VH=1100,800; L,T=70,64; cw,ch=24,56; PW,PH=cw*W,ch*H
L=(VW-PW)//2
out=[]
# pixel tint
for y in range(H):
  for x in range(W):
    v=px[y][x]; t=round(255-(255-v)*0.16)
    out.append(f'<rect x="{L+x*cw}" y="{T+y*ch}" width="{cw}" height="{ch}" fill="rgb({t},{t-1},{t-3})"/>')
# grid lines
for x in range(W+1):
  out.append(f'<line x1="{L+x*cw}" y1="{T}" x2="{L+x*cw}" y2="{T+PH}" stroke="#e4e1da" stroke-width="0.6"/>')
for y in range(H+1):
  out.append(f'<line x1="{L}" y1="{T+y*ch}" x2="{L+PW}" y2="{T+y*ch}" stroke="#e4e1da" stroke-width="0.6"/>')
# dots: lattice, 4 across, 5.2px pitch; fill in hour order left->right, top->bottom
dots=[]
for x in range(W):
  for y in range(H):
    n=alloc[x][y]
    if not n: continue
    for k in range(n):
      cx=L+x*cw+cw*(0.32 if k%2==0 else 0.68)
      cy=T+y*ch+ch*(k+0.5)/n
      dots.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.4"/>')
out.append('<g fill="#1d1c1a">'+''.join(dots)+'</g>')
# hour ticks beneath: 1464 ticks, alternating per column
ty=T+PH+14
ticks=[]
for x in range(W):
  a,b=bounds[x],bounds[x+1]
  for h in range(a,b):
    hx=L+PW*(h+0.5)/N
    ln=7 if h%24==0 else 3
    ticks.append(f'<line x1="{hx:.2f}" y1="{ty}" x2="{hx:.2f}" y2="{ty+ln}"/>')
out.append('<g stroke="#8a8780" stroke-width="0.35">'+''.join(ticks)+'</g>')
# column brackets
br=[]
for x in range(W):
  x1=L+PW*bounds[x]/N+1; x2=L+PW*bounds[x+1]/N-1
  br.append(f'<path d="M{x1:.1f} {ty+11} V{ty+14} H{x2:.1f} V{ty+11}"/>')
out.append('<g fill="none" stroke="#b5b1a8" stroke-width="0.6">'+''.join(br)+'</g>')
cap=f'<text x="{L}" y="{T-26}" class="t">Thirty-Six and a Half Hours</text><text x="{L+PW}" y="{T-26}" text-anchor="end" class="s">1,464 hours, filed into 480 pixels</text>'
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" width="{VW}" height="{VH}"><rect width="{VW}" height="{VH}" fill="#f7f5f0"/>{cap}'+''.join(out)+'</svg>'
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Thirty-Six and a Half Hours</title>
<style>html,body{{margin:0;background:#f7f5f0}}body{{display:flex;justify-content:center;align-items:center;min-height:100vh}}
svg{{display:block;max-width:100vw;height:auto}}
.t{{font:italic 17px Georgia,'Times New Roman',serif;fill:#2a2926}}.s{{font:12px Georgia,serif;fill:#8a8780;letter-spacing:.04em}}</style>
</head><body>
{svg}
</body></html>'''
open('/tmp/claude-0/s123/mk/m08/work/index.html','w').write(html)
for y in range(H): print(''.join('%2d'%alloc[x][y] if alloc[x][y] else ' .' for x in range(W)))
