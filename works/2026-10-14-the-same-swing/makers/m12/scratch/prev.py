from PIL import Image,ImageDraw
import json
D=json.load(open('/tmp/claude-0/s124/mk/m12/scratch/dark.json'))
im=Image.new('RGB',(1100,800),(244,241,234));dr=ImageDraw.Draw(im,'RGBA')
L,R=90,1010;span=R-L;colW=span/40;top,bot=70,470;rowH=(bot-top)/12
for c in range(40):
  x0=L+c*colW+1.5
  for y in range(top,bot):
    r=(y+.5-top)/rowH-.5
    if r<=0:v=D[c][0]
    elif r>=11:v=D[c][11]
    else:
      i=int(r);f=r-i;v=D[c][i]*(1-f)+D[c][i+1]*f
    v=max(0,min(1,v));dr.line([(x0,y),(x0+colW-3,y)],fill=(26,24,22,int(v*.92*255)))
PER=1464/40
for h in range(1464):
  xh=L+(h+.5)*span/1464;c=min(39,int((h+.5)/PER));u=((h+.5)-c*PER)/PER-.5
  xm=L+(c+.5)*colW+u*3
  dr.line([(xh,700),(xm,520),(xm,472)],fill=(26,24,22,40))
im.save('/tmp/claude-0/s124/mk/m12/scratch/preview.png')
