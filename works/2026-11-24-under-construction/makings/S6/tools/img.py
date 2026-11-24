import random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = sys.argv[1]
random.seed(7)
# gauge.jpg: a "scanned snapshot" of a rain gauge on a fence post, garden behind
W,H = 200,260
im = Image.new('RGB',(W,H),(150,170,190))
d = ImageDraw.Draw(im)
# sky gradient
for y in range(110):
    c = (168+y//4, 182+y//5, 196+y//6)
    d.line([(0,y),(W,y)], fill=c)
# tree line
for x in range(0,W,3):
    h = 95+random.randint(-8,6)
    d.line([(x,h),(x,118)], fill=(60+random.randint(-10,10),80+random.randint(-10,10),50))
# grass / garden
for y in range(115,H):
    for x in range(0,W,2):
        g = 95+random.randint(-25,25)+ (y-115)//6
        d.point((x,y), fill=(70+random.randint(-15,15), g, 45))
        d.point((x+1,y), fill=(70+random.randint(-15,15), g, 45))
# garden rows
for i in range(5):
    y = 140+i*22
    d.line([(0,y),(W,y+8)], fill=(110,85,55), width=3)
# fence post
d.rectangle([92,70,118,H], fill=(120,100,78))
d.line([(92,70),(92,H)], fill=(80,64,50), width=2)
for y in range(80,H,9):
    d.line([(96,y),(114,y+random.randint(-2,2))], fill=(105,88,68))
# wire
d.line([(0,150),(92,146)], fill=(90,90,90))
d.line([(118,146),(W,150)], fill=(90,90,90))
d.line([(0,190),(92,186)], fill=(90,90,90))
d.line([(118,186),(W,190)], fill=(90,90,90))
# gauge: clear plastic tube on bracket
d.rectangle([118,60,124,110], fill=(140,140,140))
d.rectangle([124,20,146,118], fill=(205,215,220), outline=(120,130,135))
d.polygon([(118,18),(152,18),(146,30),(124,30)], fill=(190,200,205), outline=(110,115,120))
for y in range(36,116,8):
    d.line([(125,y),(131,y)], fill=(40,40,90))
# water
d.rectangle([125,92,145,117], fill=(150,175,200))
im = im.filter(ImageFilter.GaussianBlur(0.8))
# slight warm cast like a drugstore print
px = im.load()
for y in range(H):
    for x in range(W):
        r,g,b = px[x,y]
        px[x,y] = (min(255,r+12), min(255,g+4), max(0,b-8))
im.save(f'{D}/gauge.jpg', quality=55)

# counter.gif: odometer digits
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 14)
digits = '002318'
cw = 13
c = Image.new('P',(cw*len(digits),20))
c.putpalette([0,0,0, 255,255,255, 200,0,0, 60,60,60]+[0]*(256*3-12))
cd = ImageDraw.Draw(c)
for i,ch in enumerate(digits):
    cd.rectangle([i*cw,0,i*cw+cw-1,19], fill=0, outline=3)
    cd.text((i*cw+2,1), ch, font=f, fill=1)
c.save(f'{D}/counter.gif')

# raindrop.gif small bullet
r = Image.new('P',(12,16),0)
r.putpalette([255,255,255, 30,80,200, 120,170,240]+[0]*(256*3-9))
rd = ImageDraw.Draw(r)
rd.polygon([(6,0),(11,10),(6,15),(1,10)], fill=1)
rd.ellipse([1,6,11,15], fill=1)
rd.point([(4,9),(4,10),(5,8)], fill=2)
r.save(f'{D}/drop.gif', transparency=0)

# rain.gif: little animated cloud with rain
frames=[]
for k in range(4):
    a = Image.new('P',(60,50),0)
    a.putpalette([255,255,255, 140,140,150, 40,90,210, 190,190,200]+[0]*(256*3-12))
    ad = ImageDraw.Draw(a)
    for (x,y,rr) in [(14,16,10),(28,11,13),(42,16,10),(22,20,9),(36,20,9)]:
        ad.ellipse([x-rr,y-rr,x+rr,y+rr], fill=3, outline=1)
    ad.rectangle([6,18,52,26], fill=3)
    for i,x in enumerate(range(12,50,7)):
        y0 = 30 + ((k*5 + i*3) % 16)
        ad.line([(x,y0),(x-2,y0+5)], fill=2, width=1)
    frames.append(a)
frames[0].save(f'{D}/rain.gif', save_all=True, append_images=frames[1:], duration=180, loop=0, transparency=0)
print('ok')
