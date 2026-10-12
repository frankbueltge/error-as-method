from PIL import Image, ImageDraw
g=Image.open('../work/record.jpg').convert('L'); W,H=g.size
N=1464
cw,ch=13,22; X0=(1100-W*cw)//2; Y0=118
px=[[g.getpixel((x,y)) for x in range(W)] for y in range(H)]
# hours per column
bounds=[round(x*N/W) for x in range(W+1)]
cnt=[bounds[x+1]-bounds[x] for x in range(W)]
assert sum(cnt)==N
els=[]; dots=[]
# faint pixel grid
for y in range(H):
    for x in range(W):
        v=px[y][x]
        if v<250:
            a=round((255-v)/255*0.22,3)
            els.append(f'<rect x="{X0+x*cw+0.5}" y="{Y0+y*ch+0.5}" width="{cw-1}" height="{ch-1}" fill="#2b2a28" fill-opacity="{a}"/>')
# dots by inverse CDF of ink within each column
for x in range(W):
    w=[max(0,(255-px[y][x])-40) for y in range(H)]
    s=sum(w); cum=0; cdf=[]
    for y in range(H): cum+=w[y]/s; cdf.append(cum)
    n=cnt[x]
    for k in range(n):
        q=(k+0.5)/n; prev=0
        for y in range(H):
            if cdf[y]>=q:
                lo=cdf[y-1] if y else 0
                f=(q-lo)/(cdf[y]-lo) if cdf[y]>lo else .5
                yy=y+f; break
        cx=X0+x*cw+cw/2; cy=Y0+yy*ch
        dots.append((cx,cy))
        els.append(f'<circle cx="{cx:.1f}" cy="{cy:.2f}" r="2.1" fill="#1d1c1a"/>')
gy=Y0+H*ch
# hour strip: 1464 ticks grouped under their column
sy=gy+34
for x in range(W):
    n=cnt[x]
    for k in range(n):
        tx=X0+x*cw+1.5+k*(cw-3)/(n-1)
        els.append(f'<line x1="{tx:.2f}" x2="{tx:.2f}" y1="{sy}" y2="{sy+(14 if n==20 else 10)}" stroke="#1d1c1a" stroke-width="0.35"/>')
# day marks
for d in range(0,62,1):
    tx=X0+d*24/N*W*cw
    els.append(f'<line x1="{tx:.2f}" x2="{tx:.2f}" y1="{sy+22}" y2="{sy+(30 if d%7==0 else 26)}" stroke="#8a857c" stroke-width="0.7"/>')
svg_body='\n'.join(els)
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=1100">
<title>Nineteen or Twenty</title>
<style>
:root{{--paper:#f3f0e8;--ink:#1d1c1a;--mute:#7d786e}}
html,body{{margin:0;background:var(--paper)}}
body{{width:1100px;height:800px;overflow:hidden;font-family:Georgia,"Times New Roman",serif;color:var(--ink)}}
svg{{display:block}}
</style></head><body>
<svg width="1100" height="800" viewBox="0 0 1100 800" xmlns="http://www.w3.org/2000/svg">
<rect width="1100" height="800" fill="#f3f0e8"/>
<text x="{X0}" y="52" font-size="22" letter-spacing="0.5">Nineteen or Twenty</text>
<text x="{X0}" y="76" font-size="13" fill="#7d786e" font-style="italic">1,464 hourly values survive only as 75 × 23 grains. Each column now holds nineteen or twenty hours whose order is lost;</text>
<text x="{X0}" y="94" font-size="13" fill="#7d786e" font-style="italic">they are given back here, one dot per hour, stacked inside their column in proportion to the ink it kept.</text>
{svg_body}
<text x="{X0}" y="{sy-10}" font-size="11" fill="#7d786e" font-style="italic">the hours, as they fall into the columns</text>
<text x="{X0}" y="{sy+46}" font-size="11" fill="#7d786e" font-style="italic">the days, sixty-one of them, a longer mark every seventh</text>
<text x="{X0+W*cw}" y="{sy+46}" font-size="11" fill="#7d786e" font-style="italic" text-anchor="end">one value every hour, larger values higher</text>
</svg>
</body></html>'''
open('../work/index.html','w').write(html)
print(X0,gy,sy, cnt.count(19),cnt.count(20), len(html))
# preview
im=Image.new('RGB',(1100,800),(243,240,232)); d=ImageDraw.Draw(im)
for y in range(H):
    for x in range(W):
        v=px[y][x]; a=(255-v)/255*0.22
        c=tuple(int(243*(1-a)+43*a) for _ in range(3))
        d.rectangle([X0+x*cw+1,Y0+y*ch+1,X0+x*cw+cw-1,Y0+y*ch+ch-1],fill=c)
for cx,cy in dots: d.ellipse([cx-2.1,cy-2.1,cx+2.1,cy+2.1],fill=(29,28,26))
im.save('preview.png')
