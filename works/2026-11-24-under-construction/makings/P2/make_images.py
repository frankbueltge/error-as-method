from PIL import Image, ImageDraw, ImageFilter
import random, os
D = os.path.dirname(os.path.abspath(__file__))
def P(n): return os.path.join(D, n)
random.seed(7)

# background tile: pale yellow with little lavender paw prints
t = Image.new("RGB", (96, 96), (255, 252, 222))
d = ImageDraw.Draw(t)
def paw(x, y, c):
    d.ellipse([x, y+5, x+8, y+12], fill=c)
    for dx, dy in [(-3, 0), (1, -3), (6, -3), (10, 0)]:
        d.ellipse([x+dx, y+dy, x+dx+3, y+dy+4], fill=c)
paw(12, 14, (226, 214, 246)); paw(60, 62, (226, 214, 246))
t.save(P("pawtile.gif"))

# rainbow divider bar
w, h = 500, 8
b = Image.new("RGB", (w, h))
cols = [(255,0,0),(255,140,0),(255,230,0),(0,190,0),(0,90,255),(140,0,200)]
bd = ImageDraw.Draw(b)
for i in range(w):
    seg = i * (len(cols)-1) / (w-1); k = int(seg); f = seg - k
    c2 = cols[min(k+1, len(cols)-1)]; c1 = cols[k]
    c = tuple(int(c1[j]*(1-f)+c2[j]*f) for j in range(3))
    bd.line([i, 0, i, h], fill=c)
bd.line([0, 0, w, 0], fill=(255,255,255)); bd.line([0, h-1, w, h-1], fill=(90,90,90))
b.save(P("rainbowbar.gif"))

# school bus, 88x40
bus = Image.new("RGB", (88, 40), (255, 255, 255))
d = ImageDraw.Draw(bus)
d.rectangle([4, 8, 80, 30], fill=(255, 200, 0), outline=(0, 0, 0))
d.rectangle([66, 14, 86, 30], fill=(255, 200, 0), outline=(0, 0, 0))
for x in range(8, 62, 11):
    d.rectangle([x, 11, x+8, 18], fill=(150, 210, 255), outline=(0, 0, 0))
d.rectangle([70, 16, 78, 22], fill=(150, 210, 255), outline=(0, 0, 0))
d.line([4, 23, 86, 23], fill=(0, 0, 0))
d.text((30, 22), "7", fill=(0, 0, 0))
for cx in (18, 70):
    d.ellipse([cx-6, 26, cx+6, 38], fill=(30, 30, 30)); d.ellipse([cx-2, 30, cx+2, 34], fill=(180,180,180))
bus = bus.convert("P", palette=Image.ADAPTIVE, colors=32)
bus.info["transparency"] = bus.getpixel((0, 0)); bus.save(P("bus.gif"), transparency=bus.getpixel((0, 0)))

# "scanned photo" of a cat: crude, soft, a bit washed out, with the white border of a 4x6 print
def catphoto(name, body, stripe, bg, sofa, size=(160, 120), pose=0):
    im = Image.new("RGB", size, bg)
    d = ImageDraw.Draw(im)
    W, H = size
    d.rectangle([0, int(H*0.55), W, H], fill=sofa)  # couch cushion
    for i in range(0, W, 18):
        d.line([i, int(H*0.55), i+9, H], fill=tuple(max(0, c-25) for c in sofa))
    cx, cy = W//2 + (pose*14), int(H*0.62)
    d.ellipse([cx-42, cy-22, cx+38, cy+26], fill=body)            # body curled
    d.ellipse([cx+14, cy-40, cx+50, cy-6], fill=body)             # head
    d.polygon([(cx+16, cy-30), (cx+20, cy-52), (cx+30, cy-36)], fill=body)
    d.polygon([(cx+36, cy-36), (cx+46, cy-52), (cx+49, cy-28)], fill=body)
    if stripe:
        for k in range(-34, 30, 9):
            d.arc([cx+k-6, cy-20, cx+k+6, cy+20], 200, 340, fill=stripe, width=3)
    d.ellipse([cx+22, cy-28, cx+28, cy-22], fill=(200, 230, 80))
    d.ellipse([cx+36, cy-28, cx+42, cy-22], fill=(200, 230, 80))
    d.ellipse([cx+24, cy-27, cx+26, cy-23], fill=(0, 0, 0)); d.ellipse([cx+38, cy-27, cx+40, cy-23], fill=(0,0,0))
    d.polygon([(cx+31, cy-19), (cx+34, cy-19), (cx+32, cy-16)], fill=(230, 140, 150))
    d.arc([cx-60, cy-10, cx-20, cy+30], 90, 250, fill=body, width=7)  # tail
    # flash glare + grain
    d.ellipse([cx+21, cy-29, cx+29, cy-21], fill=(190, 255, 120)); d.ellipse([cx+35, cy-29, cx+43, cy-21], fill=(190, 255, 120))
    im = im.filter(ImageFilter.GaussianBlur(1.8))
    px = im.load()
    fx, fy = cx+10, cy-20
    for y in range(H):
        for x in range(W):
            r, g, b2 = px[x, y]; n = random.randint(-14, 14)
            dist = ((x-fx)**2 + (y-fy)**2) ** 0.5 / (W*0.75)
            k = 1.25 - 0.75*min(1, dist)
            px[x, y] = tuple(min(255, max(0, int(v*k)+n+o)) for v, o in ((r, 10), (g, 2), (b2, -12)))
    out = Image.new("RGB", (W+10, H+10), (250, 250, 246))
    out.paste(im, (5, 5))
    out = out.rotate(-1.2 if pose else 0.8, expand=False, fillcolor=(255,252,222)); out.save(P(name), quality=40)

catphoto("pepper.jpg", (40, 40, 44), None, (205, 190, 160), (120, 60, 60))
catphoto("biggs.jpg", (225, 150, 70), (170, 95, 35), (190, 200, 205), (70, 90, 130), pose=-1)

# hit counter digits, green on black, odometer style
def counter(num, name):
    s = str(num).rjust(6, "0")
    im = Image.new("RGB", (15*len(s)+2, 22), (0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, ch in enumerate(s):
        x = 1 + i*15
        d.rectangle([x, 1, x+13, 20], fill=(20, 20, 20), outline=(90, 90, 90))
        seg7(d, x+3, 4, ch)
    im.save(P(name))
SEG = {'0':'abcdef','1':'bc','2':'abged','3':'abgcd','4':'fgbc','5':'afgcd','6':'afgedc','7':'abc','8':'abcdefg','9':'abcdfg'}
def seg7(d, x, y, ch, c=(60, 255, 60)):
    on = SEG[ch]; w, h = 7, 6
    L = {'a':[x, y, x+w, y+1], 'g':[x, y+h, x+w, y+h+1], 'd':[x, y+2*h, x+w, y+2*h+1],
         'f':[x, y, x+1, y+h], 'b':[x+w-1, y, x+w, y+h], 'e':[x, y+h, x+1, y+2*h], 'c':[x+w-1, y+h, x+w, y+2*h]}
    for k in on: d.rectangle(L[k], fill=c)
counter(2417, "counter.gif")

# animated NEW! badge
frames = []
for i, (bgc, fg) in enumerate([((255, 0, 0), (255, 255, 0)), ((255, 255, 0), (255, 0, 0))]):
    f = Image.new("RGB", (34, 14), bgc); fd = ImageDraw.Draw(f)
    fd.text((4, 1), "NEW!", fill=fg); frames.append(f.convert("P", palette=Image.ADAPTIVE, colors=8))
frames[0].save(P("new.gif"), save_all=True, append_images=frames[1:], duration=400, loop=0)

# under construction: yellow/black striped sign with a stick worker
uc = Image.new("RGB", (100, 46), (255, 255, 255)); d = ImageDraw.Draw(uc)
d.rectangle([0, 0, 99, 45], fill=(255, 215, 0), outline=(0, 0, 0))
for x in range(-46, 100, 12):
    d.polygon([(x, 45), (x+6, 45), (x+20, 36), (x+14, 36)], fill=(0, 0, 0))
    d.polygon([(x, 9), (x+6, 9), (x+20, 0), (x+14, 0)], fill=(0, 0, 0))
d.text((8, 12), "UNDER", fill=(0, 0, 0)); d.text((8, 23), "CONSTRUCTION", fill=(0, 0, 0))
d.ellipse([84, 12, 90, 18], fill=(0, 0, 0)); d.line([87, 18, 87, 28], fill=(0,0,0), width=2)
d.line([87, 28, 83, 34], fill=(0,0,0), width=2); d.line([87, 28, 91, 34], fill=(0,0,0), width=2)
d.line([87, 21, 94, 16], fill=(0,0,0), width=2)
uc.save(P("construction.gif"))

# mailbox / envelope
e = Image.new("RGB", (40, 28), (255, 255, 255)); d = ImageDraw.Draw(e)
d.rectangle([2, 4, 37, 25], fill=(255, 255, 240), outline=(0, 0, 0))
d.line([2, 4, 20, 17, 37, 4], fill=(0, 0, 0)); d.rectangle([29, 7, 34, 12], fill=(220, 40, 40))
e = e.convert("P", palette=Image.ADAPTIVE, colors=8); e.save(P("mail.gif"), transparency=e.getpixel((0, 0)))

# heart bullet
hb = Image.new("RGB", (12, 11), (255, 255, 255)); d = ImageDraw.Draw(hb)
d.ellipse([0, 0, 6, 6], fill=(230, 30, 110)); d.ellipse([5, 0, 11, 6], fill=(230, 30, 110))
d.polygon([(0, 4), (11, 4), (6, 10)], fill=(230, 30, 110))
hb = hb.convert("P", palette=Image.ADAPTIVE, colors=4); hb.save(P("heart.gif"), transparency=hb.getpixel((0, 10)))
rb = Image.new("RGB", (120, 64), (255, 255, 255)); d = ImageDraw.Draw(rb)
for i, c in enumerate(cols):
    d.arc([6+i*5, 8+i*5, 114-i*5, 116-i*5], 180, 360, fill=c, width=5)
for cx0 in (14, 24, 96, 106):
    d.ellipse([cx0-10, 46, cx0+10, 62], fill=(235, 240, 255))
rb = rb.convert("P", palette=Image.ADAPTIVE, colors=32); rb.save(P("rainbow.gif"), transparency=rb.getpixel((0, 0)))
print("ok")

# fix rainbow: solid overlapping bands
rb = Image.new("RGB", (120, 64), (255, 255, 255)); d = ImageDraw.Draw(rb)
for i, c in enumerate(cols):
    d.pieslice([4+i*5, 6+i*5, 116-i*5, 118-i*5], 180, 360, fill=c)
d.pieslice([4+6*5, 6+6*5, 116-6*5, 118-6*5], 180, 360, fill=(255, 255, 255))
for cx0 in (16, 28, 92, 104):
    d.ellipse([cx0-12, 46, cx0+12, 63], fill=(225, 232, 255), outline=(200, 205, 235))
rb = rb.convert("P", palette=Image.ADAPTIVE, colors=32); rb.save(P("rainbow.gif"), transparency=rb.getpixel((60, 58)))

# Amazing Grace as a tiny type-0 MIDI file, piano-ish (program 0)
import struct
N = {'D4':62,'E4':64,'G4':67,'A4':69,'B4':71,'D5':74}
tune = [('D4',1),('G4',2),('B4',.5),('G4',.5),('B4',2),('A4',1),('G4',2),('E4',1),('D4',2),('D4',1),
        ('G4',2),('B4',.5),('G4',.5),('B4',2),('A4',1),('D5',5),('B4',1),('D5',1.5),('B4',.5),('D5',.5),('B4',.5),
        ('G4',2),('D4',1),('E4',1.5),('G4',.5),('G4',.5),('E4',.5),('D4',2),('D4',1),('G4',2),('B4',.5),('G4',.5),
        ('B4',2),('A4',1),('G4',3)]
def vlq(n):
    b = [n & 0x7F]; n >>= 7
    while n: b.insert(0, (n & 0x7F) | 0x80); n >>= 7
    return bytes(b)
tpq = 96; ev = bytearray()
ev += vlq(0) + bytes([0xFF, 0x51, 3]) + (700000).to_bytes(3, 'big')
ev += vlq(0) + bytes([0xC0, 19])  # church organ, of course
for n, beats in tune:
    ev += vlq(0) + bytes([0x90, N[n], 90]); ev += vlq(int(beats*tpq)) + bytes([0x80, N[n], 0])
ev += vlq(tpq*2) + bytes([0xFF, 0x2F, 0])
open(P("amazing.mid"), "wb").write(b"MThd" + struct.pack(">IHHH", 6, 0, 1, tpq) + b"MTrk" + struct.pack(">I", len(ev)) + ev)
print("ok2")
