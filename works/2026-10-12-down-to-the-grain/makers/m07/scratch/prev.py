import json,math
from PIL import Image,ImageDraw
D=json.load(open('embed.json'))
L=2*D['p'];FX0,FW,TOP,PITCH,VS=170,760,78,10.6,1.75
im=Image.new('RGB',(2200,1600),(243,239,230));dr=ImageDraw.Draw(im)
n=math.ceil((D['pts'][-1][0]/100-D['x_start'])/L); print('rows',n)
for r in range(n):
  y=(TOP+50+r*PITCH)*2; dr.line([(FX0*2,y),((FX0+FW)*2,y)],fill=(225,223,218))
for xi,yi,v in D['pts']:
  x,y=xi/100,yi/100;t=(x-D['x_start'])/L;r=math.floor(t);u=t-r
  px=(FX0+u*FW)*2;py=(TOP+50+r*PITCH+(y-D['mean'])*VS)*2
  dr.ellipse([px-3,py-3,px+3,py+3],fill=(29,36,51))
src=Image.open('/tmp/claude-0/s122/mk/m07/work/record.jpg').resize((600,140))
im.paste(src,(340,1424))
im.resize((1100,800)).save('prev.png'); print('lowest',max((TOP+50+math.floor((xi/100-D['x_start'])/L)*PITCH+(yi/100-D['mean'])*VS) for xi,yi,v in D['pts']), 'highest',min((TOP+50+math.floor((xi/100-D['x_start'])/L)*PITCH+(yi/100-D['mean'])*VS) for xi,yi,v in D['pts']))
