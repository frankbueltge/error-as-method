import json
from PIL import Image, ImageDraw
days=json.load(open('/tmp/claude-0/s128/mk/m06/scratch/days.json'))
im=Image.new('RGBA',(1100,800),(242,237,227,255)); L,R,TOP,S,RAIL=70,1030,88,7.0,78; st=(R-L)/60
ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(im)
d.line([(L-22,RAIL),(R+22,RAIL)],fill=(28,26,23),width=2)
for i,q in enumerate(days):
  x=L+i*st; low=TOP+q[-1]*S; d.line([(x,RAIL),(x,low+7)],fill=(120,115,108),width=1)
  for v in q:
    o=Image.new('RGBA',im.size,(0,0,0,0)); 
    ImageDraw.Draw(o).ellipse([x-3.7,TOP+v*S-3.7,x+3.7,TOP+v*S+3.7],fill=(28,26,23,158)); im.alpha_composite(o)
im.convert('RGB').save('/tmp/claude-0/s128/mk/m06/scratch/preview.png')
