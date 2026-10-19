import json,sys
from PIL import Image, ImageDraw
o=Image.open('/tmp/claude-0/s137/mk/m17/work/record.jpg').convert('L').resize((1200,360))
fs=sys.argv[2:]
im=Image.new('L',(1200,370*(1+len(fs))),255); im.paste(o,(0,0)); d=ImageDraw.Draw(im)
for k,f in enumerate(fs):
  Y=json.load(open(f));N=len(Y);pts=[]
  for h,y in enumerate(Y):
    x=(3.2+294*h/(N-1))*4; yy=370*(k+1)+y*4; pts.append((x,yy)); d.ellipse([x-2,yy-2,x+2,yy+2],fill=0)
  d.line(pts,fill=150)
im.save(sys.argv[1])
