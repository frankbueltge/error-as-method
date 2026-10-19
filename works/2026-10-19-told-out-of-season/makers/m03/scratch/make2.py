import json
v=json.load(open('series.json'))
W,H=1100,800; L,R=90,90; top,bot=64,76; rows=61
dy=(H-top-bot)/rows; span=W-L-R; hx=span/48; K=2.4
paper='#f3efe6'; ink='#1c2440'
def cr(pts):
    d='M%.1f,%.1f'%pts[0]
    for i in range(len(pts)-1):
        p0=pts[max(i-1,0)];p1=pts[i];p2=pts[i+1];p3=pts[min(i+2,len(pts)-1)]
        c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6); c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
        d+=' C%.1f,%.1f %.1f,%.1f %.1f,%.1f'%(c1+c2+p2)
    return d
paths=[]
for d in range(rows):
    base=top+(d+1)*dy; seg=v[d*24:d*24+48]
    pts=[(L+(i+0.5)*hx, base-K*dy*max(0,val-4)/89) for i,val in enumerate(seg)]
    xe=L+len(seg)*hx
    p=f'M{L},{base:.1f} L{L},{pts[0][1]:.1f} L'+cr(pts)[1:]+f' L{xe:.1f},{pts[-1][1]:.1f} L{xe:.1f},{base:.1f} Z'
    paths.append(f'<path d="{p}"/>')
mid=L+24*hx
serif="Georgia, 'Times New Roman', serif"
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="An hourly record of 61 days, cut into days and stacked, each row showing two consecutive days. The dark band of each day's peak slants steadily to the left, wrapping round twice: the rhythm runs about half an hour short of a day.">
<rect width="{W}" height="{H}" fill="{paper}"/>
<g fill="{ink}" fill-opacity="0.55" stroke="none">
{chr(10).join(paths)}
</g>
<line x1="{mid:.1f}" y1="{top-14}" x2="{mid:.1f}" y2="{top-4}" stroke="{ink}" stroke-width="0.8" stroke-opacity="0.6"/>
<line x1="{mid:.1f}" y1="{H-bot+6}" x2="{mid:.1f}" y2="{H-bot+16}" stroke="{ink}" stroke-width="0.8" stroke-opacity="0.6"/>
<text x="{L}" y="{H-26}" font-family="{serif}" font-size="16" fill="{ink}" letter-spacing="0.3">Twenty-Three and a Half</text>
<text x="{W-R}" y="{H-26}" text-anchor="end" font-family="{serif}" font-style="italic" font-size="12" fill="#6b6658">sixty-one days, cut every twenty-four hours and stacked; each row holds two days</text>
</svg>'''
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Twenty-Three and a Half</title>
<style>html,body{{margin:0;height:100%;background:{paper}}}body{{display:flex;align-items:center;justify-content:center;overflow:hidden}}svg{{display:block;width:100vw;height:100vh;max-width:{W*1.5}px}}</style>
</head><body>
{svg}
</body></html>'''
open('/tmp/claude-0/s137/mk/m03/work/index.html','w').write(html)
print(len(html))
