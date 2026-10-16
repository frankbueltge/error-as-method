import re
from PIL import Image, ImageDraw
s=open('/tmp/claude-0/s130/mk/m12/scratch/p.svg').read()
im=Image.new('RGBA',(1100,800),(243,239,230,255)); d=ImageDraw.Draw(im,'RGBA')
def col(h,a=1): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))+(int(255*a),)
for m in re.finditer(r'<(rect|circle|line|path|text)([^>]*)>',s):
    t,a=m.groups(); A=dict(re.findall(r'([\w-]+)="([^"]*)"',a))
    if t=="circle":
        x,y,r=(float(A[k]) for k in ("cx","cy","r")); d.ellipse([x-r,y-r,x+r,y+r],fill=col(A["fill"],float(A.get("fill-opacity",1))))
    elif t=="rect" and "x" in A:
        x,y,w,h=(float(A[k]) for k in ('x','y','width','height'))
        d.rectangle([x,y,x+w,y+h],fill=col(A['fill'],float(A.get('fill-opacity',1))))
    elif t=='line':
        d.line([float(A['x1']),float(A['y1']),float(A['x2']),float(A['y2'])],fill=col(A['stroke'],float(A.get('stroke-opacity',1))),width=int(float(A.get('stroke-width',1))))
    elif t=='path':
        pts=[tuple(map(float,p.split(','))) for p in re.findall(r'[-\d.]+,[-\d.]+',A['d'])]
        if A['fill']!='none': d.polygon(pts,fill=col(A['fill'],float(A.get('fill-opacity',1))))
        else: d.line(pts,fill=col(A['stroke']),width=2)
    elif t=='text':
        d.text((float(A['x']),float(A['y'])-12),'TEXT',fill=(0,0,0,255))
im.save('/tmp/claude-0/s130/mk/m12/scratch/p.png')
