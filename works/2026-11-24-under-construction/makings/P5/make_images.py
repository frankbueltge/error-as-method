import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

random.seed(1998)
OUT = "../P5/"
F = ImageFont.load_default()


def gif(img, name, **kw):
    img.convert("P", palette=Image.ADAPTIVE, colors=64).save(OUT + name, **kw)


# --- tiled background: cream calico with tiny teal flowers
bg = Image.new("RGB", (64, 64), (255, 250, 228))
d = ImageDraw.Draw(bg)
for (x, y) in [(8, 10), (40, 26), (22, 46), (54, 56)]:
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        d.point((x + dx, y + dy), fill=(120, 190, 185))
    d.point((x, y), fill=(230, 160, 170))
for _ in range(30):
    d.point((random.randrange(64), random.randrange(64)), fill=(240, 228, 200))
gif(bg, "bg.gif")


# --- salt & pepper shakers (little hens), animated: they wiggle
def shaker_frame(tilt):
    im = Image.new("RGB", (90, 70), (255, 250, 228))
    d = ImageDraw.Draw(im)
    for i, (body, x0) in enumerate([((255, 255, 255), 8), ((60, 60, 60), 48)]):
        off = tilt if i == 0 else -tilt
        y0 = 14 + off
        d.ellipse((x0, y0 + 10, x0 + 32, y0 + 48), fill=body, outline=(0, 0, 0))
        d.ellipse((x0 + 6, y0, x0 + 26, y0 + 20), fill=body, outline=(0, 0, 0))
        d.polygon([(x0 + 12, y0 - 4), (x0 + 16, y0 + 2), (x0 + 20, y0 - 4)], fill=(220, 30, 30))
        d.polygon([(x0 + 25, y0 + 8), (x0 + 31, y0 + 11), (x0 + 25, y0 + 13)], fill=(240, 180, 0))
        d.point((x0 + 20, y0 + 7), fill=(0, 0, 0) if i == 0 else (255, 255, 255))
        for k in range(3):
            d.point((x0 + 13 + k * 3, y0 + 3), fill=(0, 0, 0) if i == 0 else (200, 200, 200))
        d.text((x0 + 13, y0 + 28), "S" if i == 0 else "P", fill=(0, 0, 160) if i == 0 else (255, 255, 0), font=F)
    return im


frames = [shaker_frame(t) for t in (0, 2, 0, -2)]
frames = [f.convert("P", palette=Image.ADAPTIVE, colors=32) for f in frames]
frames[0].save(OUT + "shakers.gif", save_all=True, append_images=frames[1:], duration=250, loop=0)

# --- under construction sign
uc = Image.new("RGB", (120, 40), (255, 220, 0))
d = ImageDraw.Draw(uc)
for x in range(-40, 160, 16):
    d.polygon([(x, 0), (x + 8, 0), (x + 8 - 8, 8), (x - 8, 8)], fill=(0, 0, 0))
    d.polygon([(x, 32), (x + 8, 32), (x, 40), (x - 8, 40)], fill=(0, 0, 0))
d.rectangle((0, 0, 119, 39), outline=(0, 0, 0))
d.text((8, 11), "UNDER", fill=(0, 0, 0), font=F)
d.text((8, 20), "CONSTRUCTION!!", fill=(0, 0, 0), font=F)
# little digging man
d.ellipse((100, 11, 105, 16), fill=(0, 0, 0))
d.line((102, 16, 102, 24), fill=(0, 0, 0))
d.line((102, 24, 99, 30), fill=(0, 0, 0))
d.line((102, 24, 105, 30), fill=(0, 0, 0))
d.line((102, 19, 110, 14), fill=(0, 0, 0))
d.line((110, 14, 113, 29), fill=(0, 0, 0))
gif(uc, "construct.gif")

# --- hit counter
digits = "0004127"
cnt = Image.new("RGB", (len(digits) * 12 + 2, 18), (0, 0, 0))
d = ImageDraw.Draw(cnt)
for i, ch in enumerate(digits):
    d.rectangle((1 + i * 12, 1, 11 + i * 12, 16), fill=(20, 20, 20), outline=(90, 90, 90))
    d.text((4 + i * 12, 3), ch, fill=(60, 255, 60), font=F)
gif(cnt, "counter.gif")

# --- gingham divider
bar = Image.new("RGB", (400, 10), (255, 255, 255))
d = ImageDraw.Draw(bar)
for x in range(0, 400, 10):
    for y in range(0, 10, 5):
        if (x // 5 + y // 5) % 2 == 0:
            d.rectangle((x, y, x + 4, y + 4), fill=(200, 40, 50))
        else:
            d.rectangle((x, y, x + 4, y + 4), fill=(240, 170, 175))
gif(bar, "gingham.gif")

# --- mailbox / envelope
env = Image.new("RGB", (40, 28), (255, 250, 228))
d = ImageDraw.Draw(env)
d.rectangle((2, 4, 37, 25), fill=(255, 255, 255), outline=(0, 0, 0))
d.line((2, 4, 20, 16), fill=(0, 0, 0))
d.line((37, 4, 20, 16), fill=(0, 0, 0))
d.rectangle((29, 6, 35, 11), fill=(200, 30, 30))
gif(env, "mail.gif")

# --- NEW! burst
new = Image.new("RGB", (36, 16), (255, 250, 228))
d = ImageDraw.Draw(new)
d.rectangle((0, 0, 35, 15), fill=(230, 0, 0))
d.text((5, 2), "NEW!", fill=(255, 255, 0), font=F)
gif(new, "new.gif")
new2 = Image.new("RGB", (36, 16), (255, 250, 228))
d = ImageDraw.Draw(new2)
d.rectangle((0, 0, 35, 15), fill=(255, 255, 0))
d.text((5, 2), "NEW!", fill=(230, 0, 0), font=F)
fr = [new.convert("P", palette=Image.ADAPTIVE, colors=8), new2.convert("P", palette=Image.ADAPTIVE, colors=8)]
fr[0].save(OUT + "new.gif", save_all=True, append_images=fr[1:], duration=400, loop=0)

# --- "scanned" photo of the shaker shelf (her curio cabinet), saved as low-quality JPEG
ph = Image.new("RGB", (240, 180), (120, 80, 50))
d = ImageDraw.Draw(ph)
d.rectangle((0, 0, 239, 179), fill=(196, 180, 150))  # wall
d.rectangle((20, 10, 220, 175), fill=(110, 70, 40))  # cabinet
d.rectangle((28, 16, 212, 170), fill=(210, 200, 180))  # mirrored back
colors = [(250, 250, 250), (230, 60, 60), (240, 200, 40), (60, 120, 200), (90, 160, 90),
          (240, 150, 60), (180, 120, 200), (120, 80, 40), (250, 230, 200), (30, 30, 30)]
for shelf_y in (60, 110, 160):
    d.rectangle((28, shelf_y, 212, shelf_y + 4), fill=(150, 160, 160))
    x = 32
    while x < 200:
        c = random.choice(colors)
        w = random.randint(6, 10)
        h = random.randint(14, 30)
        kind = random.random()
        for k in range(2):
            xx = x + k * (w + 1)
            if kind < 0.4:
                d.ellipse((xx, shelf_y - h, xx + w, shelf_y), fill=c, outline=(60, 50, 40))
            else:
                d.rectangle((xx, shelf_y - h, xx + w, shelf_y), fill=c, outline=(60, 50, 40))
            d.ellipse((xx + 1, shelf_y - h - 4, xx + w - 1, shelf_y - h + 2), fill=c)
        x += 2 * w + random.randint(4, 8)
# flash glare
glare = Image.new("L", ph.size, 0)
gd = ImageDraw.Draw(glare)
gd.ellipse((140, 20, 190, 60), fill=170)
glare = glare.filter(ImageFilter.GaussianBlur(10))
ph = Image.composite(Image.new("RGB", ph.size, (255, 255, 240)), ph, glare)
# yellowish cast, softness, noise
ph = ph.filter(ImageFilter.GaussianBlur(0.8))
px = ph.load()
for y in range(ph.size[1]):
    for x in range(ph.size[0]):
        r, g, b = px[x, y]
        n = random.randint(-10, 10)
        px[x, y] = (min(255, r + 12 + n), min(255, g + 6 + n), max(0, b - 14 + n))
ph.save(OUT + "cabinet.jpg", quality=35)

# --- grandkids "photo": two kids in front of a house, very rough scanner look
gk = Image.new("RGB", (160, 120), (140, 190, 235))
d = ImageDraw.Draw(gk)
d.rectangle((0, 80, 159, 119), fill=(150, 140, 90))  # dry Lubbock grass
d.rectangle((70, 35, 150, 85), fill=(200, 170, 130))  # house
d.polygon([(64, 38), (110, 10), (156, 38)], fill=(110, 60, 50))
d.rectangle((95, 55, 112, 85), fill=(120, 80, 50))
for (x, shirt, hgt) in [(22, (220, 40, 40), 52), (48, (60, 90, 200), 40)]:
    top = 100 - hgt
    d.ellipse((x - 6, top, x + 6, top + 12), fill=(230, 190, 160))
    d.rectangle((x - 6, top - 2, x + 6, top + 2), fill=(90, 60, 30))
    d.rectangle((x - 8, top + 12, x + 8, top + 32), fill=shirt)
    d.rectangle((x - 6, top + 32, x - 1, 102), fill=(40, 50, 100))
    d.rectangle((x + 1, top + 32, x + 6, 102), fill=(40, 50, 100))
gk = gk.filter(ImageFilter.GaussianBlur(0.9))
px = gk.load()
for y in range(gk.size[1]):
    for x in range(gk.size[0]):
        r, g, b = px[x, y]
        n = random.randint(-8, 8)
        px[x, y] = (min(255, r + 15 + n), min(255, g + 5 + n), max(0, b - 10 + n))
gk.save(OUT + "grandbabies.jpg", quality=35)

# --- bluebonnet bullet
bb = Image.new("RGB", (12, 12), (255, 250, 228))
d = ImageDraw.Draw(bb)
d.line((6, 11, 6, 4), fill=(40, 120, 40))
for y in range(1, 9, 2):
    d.point((5, y), fill=(40, 60, 200))
    d.point((7, y + 1), fill=(40, 60, 200))
d.point((6, 0), fill=(255, 255, 255))
gif(bb, "bonnet.gif")

# --- Texas flag small
tx = Image.new("RGB", (36, 24), (255, 255, 255))
d = ImageDraw.Draw(tx)
d.rectangle((0, 0, 11, 23), fill=(0, 40, 104))
d.rectangle((12, 12, 35, 23), fill=(191, 10, 48))
d.polygon([(6, 7), (7, 10), (10, 10), (8, 12), (9, 15), (6, 13), (3, 15), (4, 12), (2, 10), (5, 10)], fill=(255, 255, 255))
gif(tx, "texas.gif")
print("ok")
