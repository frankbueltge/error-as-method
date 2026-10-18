import json,sys,math
from PIL import Image, ImageDraw
im=Image.open('/tmp/claude-0/s133/mk/m24/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
print('sumD2',sum((max(0,255-p[x,y])/255)**2 for x in range(W) for y in range(H)))
f=json.load(open(sys.argv[1])); ys=f['ys']; x0=f['x0']; S=4.8198/24
sc=4
out=Image.new('RGB',(W*sc,H*sc*2),'white'); d=ImageDraw.Draw(out)
out.paste(im.convert('RGB').resize((W*sc,H*sc),Image.NEAREST),(0,0))
for i,y in enumerate(ys):
    x=x0+i*S
    d.ellipse([x*sc-3,(y+H)*sc-3,x*sc+3,(y+H)*sc+3],fill='black')
out.save('cmp.png')
# value distribution
z=84.0
vals=[ (z-y) for y in ys]
print('min y',min(ys),'n at baseline',sum(1 for y in ys if y>=83))
