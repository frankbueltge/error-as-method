import random
from PIL import Image, ImageDraw

random.seed(7)
D = '../P4/'

def pal(img):
    return img.convert('P', palette=Image.ADAPTIVE, colors=32)

# 1. background tile: light gray "ballast" speckle
bg = Image.new('RGB', (64, 64), (192, 192, 192))
d = ImageDraw.Draw(bg)
for _ in range(500):
    x, y = random.randrange(64), random.randrange(64)
    v = random.choice([160, 170, 176, 208, 216, 224])
    d.point((x, y), fill=(v, v, v - 6))
pal(bg).save(D + 'ballast.gif')

# 2. track divider: ties and rails, 500x12
tr = Image.new('RGB', (500, 12), (255, 255, 255))
d = ImageDraw.Draw(tr)
for x in range(0, 500, 10):
    d.rectangle([x, 0, x + 5, 11], fill=(102, 66, 33))
d.line([0, 3, 499, 3], fill=(80, 80, 80), width=2)
d.line([0, 8, 499, 8], fill=(80, 80, 80), width=2)
im = pal(tr)
im.info['transparency'] = im.getpixel((7, 1)) if False else None
tr2 = tr.convert('P', palette=Image.ADAPTIVE, colors=8)
white = tr2.getpixel((7, 0))
tr2.save(D + 'track.gif', transparency=white)

# 3. animated steam loco, crude Paint style, 120x50, 4 frames of smoke
def loco(frame):
    im = Image.new('RGB', (120, 50), (255, 255, 255))
    d = ImageDraw.Draw(im)
    blk = (0, 0, 0)
    red = (204, 0, 0)
    # boiler
    d.rectangle([20, 18, 75, 34], fill=blk)
    # cab
    d.rectangle([75, 8, 98, 34], fill=blk)
    d.rectangle([80, 12, 92, 20], fill=(255, 255, 153))
    d.rectangle([73, 6, 100, 9], fill=red)
    # stack
    d.rectangle([28, 9, 34, 18], fill=blk)
    # pilot
    d.polygon([(20, 34), (10, 42), (20, 42)], fill=red)
    # headlight
    d.rectangle([17, 20, 20, 25], fill=(255, 255, 0))
    # wheels
    for cx in (34, 50, 66):
        d.ellipse([cx - 7, 33, cx + 7, 47], fill=red, outline=blk)
    d.ellipse([86, 37, 96, 47], fill=red, outline=blk)
    # rod moves
    off = [0, 2, 0, -2][frame]
    d.line([34, 40 + off, 66, 40 + off], fill=(160, 160, 160), width=2)
    # rail
    d.line([0, 48, 119, 48], fill=(90, 90, 90), width=2)
    # smoke puffs drift
    g = (150, 150, 150)
    for i in range(3):
        k = (frame + i * 2) % 6
        x = 30 - k * 4 + 2
        y = 6 - k
        r = 2 + k
        if x - r > -10:
            d.ellipse([x - r + 30 - 30, y - r + 2, x + r, y + r + 2], fill=g)
    return im.convert('P', palette=Image.ADAPTIVE, colors=16)

frames = [loco(f) for f in range(4)]
frames[0].save(D + 'loco.gif', save_all=True, append_images=frames[1:], duration=180, loop=0)

# 4. under construction sign, 88x40 animated flash
def uc(on):
    im = Image.new('RGB', (100, 44), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.polygon([(50, 1), (98, 42), (2, 42)], fill=(255, 204, 0) if on else (255, 153, 0), outline=(0, 0, 0))
    # stick figure digging
    d.ellipse([44, 16, 50, 22], fill=(0, 0, 0))
    d.line([47, 22, 50, 32], fill=(0, 0, 0), width=2)
    d.line([50, 32, 44, 40], fill=(0, 0, 0), width=2)
    d.line([50, 32, 56, 40], fill=(0, 0, 0), width=2)
    d.line([48, 25, 60, 28], fill=(0, 0, 0), width=2)
    d.line([60, 22, 64, 40], fill=(0, 0, 0), width=1)
    d.polygon([(30, 40), (38, 34), (42, 40)], fill=(0, 0, 0))
    return im.convert('P', palette=Image.ADAPTIVE, colors=8)
f = [uc(True), uc(False)]
f[0].save(D + 'constr.gif', save_all=True, append_images=f[1:], duration=400, loop=0)

# 5. hit counter digits as one image 0004817 (odometer)
from PIL import ImageFont
font = ImageFont.load_default()
num = '0004817'
cw = 13
ct = Image.new('RGB', (cw * len(num), 20), (0, 0, 0))
d = ImageDraw.Draw(ct)
for i, ch in enumerate(num):
    d.rectangle([i * cw, 0, i * cw + cw - 2, 19], fill=(20, 20, 20), outline=(90, 90, 90))
    d.text((i * cw + 3, 4), ch, fill=(0, 255, 0), font=font)
ct.convert('P', palette=Image.ADAPTIVE, colors=8).save(D + 'counter.gif')

# 6. mailbox icon
mb = Image.new('RGB', (32, 32), (255, 255, 255))
d = ImageDraw.Draw(mb)
d.rectangle([14, 18, 17, 31], fill=(102, 66, 33))
d.rectangle([4, 6, 26, 18], fill=(0, 0, 153))
d.ellipse([4, 2, 26, 12], fill=(0, 0, 153))
d.rectangle([24, 4, 27, 12], fill=(204, 0, 0))
d.text((8, 8), 'US', fill=(255, 255, 255), font=font)
m = mb.convert('P', palette=Image.ADAPTIVE, colors=8)
m.save(D + 'mailbox.gif', transparency=m.getpixel((0, 31)))

# 7. "NEW!" blinking
def new(on):
    im = Image.new('RGB', (30, 12), (255, 255, 255))
    d = ImageDraw.Draw(im)
    if on:
        d.rectangle([0, 0, 29, 11], fill=(255, 0, 0))
        d.text((3, 0), 'NEW', fill=(255, 255, 0), font=font)
    return im.convert('P', palette=Image.ADAPTIVE, colors=4)
f = [new(True), new(False)]
f[0].save(D + 'new.gif', save_all=True, append_images=f[1:], duration=500, loop=0)

# 8. layout "photo": a fuzzy scanned-looking picture of a basement layout, 200x130 JPEG-ish
ph = Image.new('RGB', (200, 130), (70, 90, 60))
d = ImageDraw.Draw(ph)
d.rectangle([0, 0, 199, 40], fill=(150, 170, 190))  # painted sky backdrop on wall
d.polygon([(0, 40), (40, 18), (80, 38), (130, 14), (199, 36), (199, 40)], fill=(90, 110, 80))
d.rectangle([0, 40, 199, 129], fill=(88, 110, 62))
for _ in range(60):
    x, y = random.randrange(200), random.randrange(42, 128)
    d.ellipse([x, y, x + 6, y + 5], fill=(40 + random.randrange(30), 70 + random.randrange(30), 35))
d.line([0, 95, 199, 80], fill=(60, 55, 50), width=6)
d.line([0, 95, 199, 80], fill=(120, 120, 120), width=1)
d.rectangle([60, 70, 105, 86], fill=(30, 30, 30))  # loco
d.rectangle([105, 72, 150, 84], fill=(120, 40, 30))  # boxcar
d.rectangle([150, 34, 175, 58], fill=(180, 160, 120))  # tower
d.rectangle([155, 26, 170, 34], fill=(90, 50, 40))
d.rectangle([0, 120, 199, 129], fill=(60, 45, 30))  # fascia
ph = ph.resize((100, 65)).resize((200, 130))
ph.save(D + 'layout1.jpg', quality=45)

# 9. Walt photo placeholder: crude scanned snapshot
w = Image.new('RGB', (110, 140), (200, 190, 160))
d = ImageDraw.Draw(w)
d.rectangle([0, 0, 109, 60], fill=(170, 180, 190))
d.ellipse([38, 22, 72, 62], fill=(222, 184, 150))
d.rectangle([34, 18, 76, 30], fill=(40, 60, 120))  # cap
d.rectangle([30, 28, 80, 32], fill=(40, 60, 120))
d.rectangle([48, 50, 62, 56], fill=(180, 180, 180))  # mustache
d.ellipse([46, 38, 50, 42], fill=(0, 0, 0)); d.ellipse([60, 38, 64, 42], fill=(0, 0, 0))
d.rectangle([22, 64, 88, 139], fill=(150, 30, 30))  # flannel
for x in range(22, 88, 8):
    d.line([x, 64, x, 139], fill=(100, 20, 20))
for y in range(64, 139, 8):
    d.line([22, y, 88, y], fill=(100, 20, 20))
w = w.resize((55, 70)).resize((110, 140))
w.save(D + 'walt.jpg', quality=40)
print('ok')
