import json
v=json.load(open('series.json'))
W,H=1100,800
L,R=86,86
top,bot=96,62
rows=61
dy=(H-top-bot)/(rows-1)
span=W-L-R
xs=lambda i: L+i*span/47
amp=0.62
paper='#f3efe6'; ink='#1d1b18'
def path(pts):
    d='M%.1f,%.1f'%pts[0]
    for i in range(len(pts)-1):
        p0=pts[max(i-1,0)];p1=pts[i];p2=pts[i+1];p3=pts[min(i+2,len(pts)-1)]
        c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6)
        c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
        d+=' C%.1f,%.1f %.1f,%.1f %.1f,%.1f'%(c1+c2+p2)
    return d
out=[]
for d in range(rows):
    base=top+d*dy
    seg=v[d*24:d*24+48]
    pts=[(xs(i),base-amp*(val-6)) for i,val in enumerate(seg)]
    line=path(pts)
    fill=line+' L%.1f,%.1f L%.1f,%.1f Z'%(pts[-1][0],base+2,pts[0][0],base+2)
    sw=0.9 if d%7 else 0.9
    out.append(f'<path d="{fill}" fill="{paper}" stroke="none"/>')
    out.append(f'<path d="{line}" fill="none" stroke="{ink}" stroke-width="1.05" stroke-linejoin="round" stroke-linecap="round"/>')
mid=xs(23.5)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Sixty-one days of an hourly record folded into a double-plotted ridge chart; the daily peak drifts about half an hour earlier each day.">
<rect width="{W}" height="{H}" fill="{paper}"/>
<line x1="{mid:.1f}" y1="{top-70}" x2="{mid:.1f}" y2="{H-bot+14}" stroke="#b9b1a2" stroke-width="0.6" stroke-dasharray="1 4"/>
{''.join(out)}
<text x="{L}" y="{H-22}" font-family="Georgia, 'Times New Roman', serif" font-size="15" fill="{ink}" letter-spacing="0.4">Twenty-Three and a Half</text>
<text x="{W-R}" y="{H-22}" text-anchor="end" font-family="Georgia, 'Times New Roman', serif" font-style="italic" font-size="12" fill="#6f685c">61 days, one line per day, each line two days long</text>
</svg>'''
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Twenty-Three and a Half</title>
<style>html,body{{margin:0;height:100%;background:{paper}}}body{{display:flex;align-items:center;justify-content:center}}svg{{display:block;max-width:100vw;max-height:100vh;width:auto;height:auto}}</style>
</head><body>
{svg}
</body></html>'''
open('/tmp/claude-0/s137/mk/m03/work/index.html','w').write(html)
open('preview.svg','w').write(svg)
