import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
random.seed(7)
F = ImageFont.load_default()
exec(open('make_images.py').read().split('# --- the fish house photo')[0].split('F = ImageFont.load_default()')[1].split('# --- background tile')[0])
def scanned(img):
    img = img.filter(ImageFilter.GaussianBlur(0.6)); px = img.load(); w,h = img.size
    for y in range(h):
        for x in range(w):
            r,g,b = px[x,y]; n = random.randint(-7,7)
            px[x,y] = (min(255,max(0,r+n+6)),min(255,max(0,g+n)),min(255,max(0,b+n-8)))
    return img
# Duke: black lab sitting on the ice in front of the red house wall
W,H = 150,112
p = Image.new("RGB",(W,H),(150,34,32)); d = ImageDraw.Draw(p)
for y in range(0,70,9): d.line((0,y,W,y),(120,26,24))
d.rectangle((0,70,W,H),(232,234,240))
for _ in range(200): d.point((random.randrange(W),random.randrange(72,H)),(214,218,226))
K=(26,24,24); K2=(40,38,36)
d.ellipse((50,48,104,104),K)            # sitting body
d.rectangle((54,88,66,108),K); d.rectangle((84,88,96,108),K)  # front legs
d.ellipse((50,102,70,110),K); d.ellipse((80,102,100,110),K)  # paws
d.ellipse((96,92,128,106),K)            # back haunch / tail on ice
d.ellipse((56,14,100,54),K)             # head
d.ellipse((66,38,94,62),K2)             # muzzle
d.ellipse((76,48,86,55),(8,8,8))        # nose
d.ellipse((52,18,64,46),(14,12,12)); d.ellipse((92,18,104,46),(14,12,12))  # ears
d.ellipse((66,28,71,33),(190,150,70)); d.ellipse((85,28,90,33),(190,150,70))
d.rectangle((60,58,96,63),(190,40,40))  # red collar
d.ellipse((74,62,80,68),(220,200,80))
p = scanned(p); ImageDraw.Draw(p).text((96,98),"'98 1 17",(255,140,40),font=F)
p.save("duke.jpg",quality=50)
# counter 000347
digits="000347"
im = Image.new("RGB",(len(digits)*13+2,20),(0,0,0)); d=ImageDraw.Draw(im)
for i,ch in enumerate(digits):
    x=1+i*13; d.rectangle((x,1,x+11,18),(24,24,24))
    big=Image.new("RGB",(6,10),(24,24,24)); ImageDraw.Draw(big).text((0,-1),ch,(60,255,60),font=F)
    im.paste(big.resize((12,18),Image.NEAREST),(x,1))
im.convert("P",palette=Image.ADAPTIVE,colors=8).save("counter.gif")
# NEW! blinking
fr=[]
for k in range(2):
    im=Image.new("RGB",(34,14),(255,255,255)); d=ImageDraw.Draw(im)
    d.rectangle((0,0,33,13),(255,0,0) if k==0 else (255,220,0))
    d.text((5,1),"NEW!",(255,255,0) if k==0 else (255,0,0),font=F)
    fr.append(im.convert("P",palette=Image.ADAPTIVE,colors=8))
fr[0].save("new.gif",save_all=True,append_images=fr[1:],duration=400,loop=0)
# small GeoCities-style badge Gary made? no: webring logo
im=Image.new("RGB",(88,31),(0,60,120)); d=ImageDraw.Draw(im)
d.rectangle((0,0,87,30),outline=(255,255,255))
d.text((6,3),"FISH HOUSE",(255,255,255),font=F); d.text((20,16),"RING",(255,230,0),font=F)
d.ellipse((60,15,70,25),(255,255,255)); d.pieslice((60,15,70,25),180,360,(220,30,30))
im.convert("P",palette=Image.ADAPTIVE,colors=16).save("ring.gif")
print("ok")
