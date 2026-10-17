import json, math, re
from PIL import Image, ImageDraw, ImageChops
s=open('/tmp/claude-0/s133/mk/m06/work/index.html').read()
S=2;W,H=1100,800
bg=Image.new('RGB',(W*S,H*S),(11,14,20))
for m in re.finditer(r'<path d="M([\d.]+),([\d.]+)L([\d.]+),([\d.]+)A([\d.]+),[\d.]+ 0 0 1 ([\d.]+),([\d.]+)Z" fill="#(\w+)"',s):
    cx,cy,x1,y1,r,x2,y2=map(float,m.groups()[:7]);c=m.group(8)
    rgb=tuple(int(c[i:i+2],16) for i in (0,2,4))
    a1=math.degrees(math.atan2(y1-cy,x1-cx));a2=math.degrees(math.atan2(y2-cy,x2-cx))
    lay=Image.new('RGB',bg.size,(0,0,0));dl=ImageDraw.Draw(lay)
    dl.pieslice([(cx-r)*S,(cy-r)*S,(cx+r)*S,(cy+r)*S],a1,a2,fill=tuple(int(v*.5) for v in rgb))
    bg=ImageChops.screen(bg,lay)
bg.resize((W,H),Image.LANCZOS).save('preview4.png')
