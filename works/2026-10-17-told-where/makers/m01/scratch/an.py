from PIL import Image
import math
im=Image.open('/tmp/claude-0/s133/mk/m01/work/record.jpg').convert('L')
W,H=im.size
P=W/61
# bottom band profile
band=[sum(255-im.getpixel((x,y)) for y in (83,84)) for x in range(W)]
# fit phase: light gap -> minimum of band; complex demod at period P
re=sum(band[x]*math.cos(2*math.pi*(x+0.5)/P) for x in range(W))
im_=sum(band[x]*math.sin(2*math.pi*(x+0.5)/P) for x in range(W))
ph=math.atan2(im_,re)  # max darkness phase
maxpos=(ph/(2*math.pi))*P % P
minpos=(maxpos+P/2)%P
print('band darkest phase px',maxpos,'lightest',minpos,'hour of lightest',minpos*1464/W)
# halves
for a,b in [(0,100),(100,200),(200,300)]:
  s=band[a:b]; print(a,b,'mean band',sum(s)/len(s))
# per day: topmost dark pixel and darkness sum above row 82
days=[]
for d in range(61):
  x0=int(round(d*P)); x1=int(round((d+1)*P))
  top=None; tot=0
  for y in range(0,82):
    for x in range(x0,x1):
      v=255-im.getpixel((x,y))
      if v>110 and top is None: top=y
      tot+=v
  days.append((d,top,tot))
for d in days: print(d)
