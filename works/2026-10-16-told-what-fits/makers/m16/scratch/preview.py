import re
from PIL import Image, ImageDraw
svg=open('/tmp/claude-0/s131/mk/m16/scratch/work.svg').read()
K=2
img=Image.new('RGB',(1100*K,800*K),(242,237,227)); dr=ImageDraw.Draw(img,'RGBA')
paths=re.findall(r'<path d="([^"]+)" fill="([^"]+)"(?: fill-opacity="([^"]+)")? stroke="([^"]+)"(?: stroke-width="([^"]+)")?',svg)
def h2(c,a): c=c.lstrip('#'); return tuple(int(c[i:i+2],16) for i in (0,2,4))+(int(255*a),)
for d,fill,fo,st,sw in paths:
    subs=[s for s in re.split(r'(?=M)',d) if s]
    for s in subs:
        pts=[(float(x)*K,float(y)*K) for x,y in re.findall(r'(-?[\d.]+),(-?[\d.]+)',s)]
        if fill!='none': dr.polygon(pts,fill=h2(fill,float(fo)))
        else: dr.line(pts,fill=h2(st,1.0),width=max(1,int(float(sw)*K)))
for x,y in re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)"',svg):
    x,y=float(x)*K,float(y)*K; r=0.9*K; dr.ellipse([x-r,y-r,x+r,y+r],fill=(31,26,21))
img.resize((1100,800),Image.LANCZOS).save('/tmp/claude-0/s131/mk/m16/scratch/preview.png')
