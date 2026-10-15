import re
from PIL import Image, ImageDraw
s=open('/tmp/claude-0/s128/mk/m09/scratch/work.svg').read()
S=2
im=Image.new('RGB',(1100*S,800*S),(243,239,230)); ov=Image.new('L',im.size,0)
d=ImageDraw.Draw(ov)
for m in re.finditer(r'<path d="([^"]+)" stroke-opacity="([\d.]+)"',s):
    pts=[tuple(float(v)*S for v in p.strip().split()) for p in m.group(1)[1:].split('L')]
    a=int(float(m.group(2))*255)
    tmp=Image.new('L',im.size,0)
    # approximate: max blend
    d.line(pts,fill=a,width=int(1.15*S))
im.paste(Image.new('RGB',im.size,(28,27,25)),mask=ov)
dd=ImageDraw.Draw(im)
for m in re.finditer(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)"',s):
    dd.line([float(v)*S for v in m.groups()],fill=(180,68,44),width=2)
im.resize((1100,800),Image.LANCZOS).save('/tmp/claude-0/s128/mk/m09/scratch/preview.png')
