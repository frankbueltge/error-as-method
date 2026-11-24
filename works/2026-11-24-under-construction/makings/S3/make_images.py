import random
from PIL import Image, ImageDraw, ImageFilter

OUT = "../S3/"
random.seed(42)

# 1. animated rain cloud clipart, 64x56, transparent-ish on white
frames = []
for f in range(4):
    im = Image.new("P", (64, 56), 0)
    im.putpalette([255, 255, 255, 128, 128, 128, 200, 200, 210, 30, 80, 220, 0, 0, 0] + [0] * (256 * 3 - 15))
    d = ImageDraw.Draw(im)
    # cloud: overlapping ellipses, outline then fill
    blobs = [(6, 14, 30, 34), (18, 4, 44, 30), (34, 10, 58, 34), (10, 20, 54, 36)]
    for b in blobs:
        d.ellipse((b[0] - 1, b[1] - 1, b[2] + 1, b[3] + 1), fill=4)
    for b in blobs:
        d.ellipse(b, fill=2)
    d.ellipse((22, 8, 34, 16), fill=0)  # highlight
    # drops
    for i, x in enumerate([14, 24, 34, 44, 50]):
        y = 38 + ((f * 4 + i * 5) % 16)
        d.line((x, y, x - 1, y + 3), fill=3)
        d.line((x + 1, y, x, y + 3), fill=3)
    frames.append(im)
frames[0].save(OUT + "raincld.gif", save_all=True, append_images=frames[1:], duration=150, loop=0, transparency=0)

# 2. counter digits, odometer style
def counter(n, path):
    s = "%06d" % n
    w, h = 15 * len(s), 20
    im = Image.new("RGB", (w, h), (0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, ch in enumerate(s):
        x = i * 15
        d.rectangle((x, 0, x + 14, 19), fill=(20, 20, 20), outline=(90, 90, 90))
        d.text((x + 4, 4), ch, fill=(0, 255, 0))
    im.save(path)

counter(1183, OUT + "counter.gif")

# 3. a "photo" of the rain gauge on the fence post, as if scanned from a snapshot
W, H = 160, 200
im = Image.new("RGB", (W, H))
d = ImageDraw.Draw(im)
for y in range(H):
    if y < 110:  # sky, washed-out
        c = (150 + y // 3, 180 + y // 5, 215)
    else:  # pasture / brown grass
        c = (140 - (y - 110) // 4, 130 - (y - 110) // 5, 70)
    d.line((0, y, W, y), fill=c)
# horizon tree line
for x in range(0, W, 3):
    hgt = random.randint(4, 12)
    d.rectangle((x, 110 - hgt, x + 3, 112), fill=(70, 85, 55))
# barbed wire
d.line((0, 120, W, 116), fill=(60, 60, 60))
d.line((0, 140, W, 137), fill=(60, 60, 60))
# fence post
d.polygon([(64, 70), (92, 72), (95, 200), (60, 200)], fill=(115, 95, 70))
for k in range(12):
    yy = random.randint(75, 195)
    d.line((64, yy, 92, yy + random.randint(-2, 2)), fill=(95, 78, 58))
# bracket and gauge tube
d.rectangle((70, 60, 86, 64), fill=(170, 170, 170))
d.rectangle((72, 18, 84, 78), fill=(225, 230, 235), outline=(120, 120, 130))
d.polygon([(68, 18), (88, 18), (84, 26), (72, 26)], fill=(200, 205, 210), outline=(110, 110, 120))
for t in range(30, 76, 5):
    d.line((73, t, 77, t), fill=(40, 40, 40))
d.rectangle((73, 58, 83, 77), fill=(150, 175, 215))
im = im.filter(ImageFilter.GaussianBlur(0.8))
px = im.load()
for _ in range(2500):
    x, y = random.randrange(W), random.randrange(H)
    r, g, b = px[x, y]
    n = random.randint(-18, 18)
    px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))
# yellowed print + date stamp in corner like a drugstore print
d = ImageDraw.Draw(im)
d.text((100, 186), "5 12 98", fill=(255, 140, 40))
im.save(OUT + "gauge.jpg", quality=55)

# 4. raindrop divider bar
im = Image.new("P", (400, 12), 0)
im.putpalette([204, 238, 255, 30, 80, 220, 120, 160, 255] + [0] * (253 * 3))
d = ImageDraw.Draw(im)
for x in range(6, 400, 20):
    d.ellipse((x, 4, x + 6, 10), fill=1)
    d.polygon([(x + 1, 6), (x + 3, 0), (x + 5, 6)], fill=1)
    d.point((x + 2, 6), fill=2)
im.save(OUT + "drops.gif", transparency=0)

# 5. under construction sign
im = Image.new("P", (88, 40), 0)
im.putpalette([255, 255, 255, 255, 210, 0, 0, 0, 0] + [0] * (253 * 3))
d = ImageDraw.Draw(im)
d.rectangle((0, 0, 87, 39), fill=1, outline=2)
for x in range(-40, 90, 10):
    d.polygon([(x, 39), (x + 5, 39), (x + 25, 30), (x + 20, 30)], fill=2)
d.text((6, 4), "UNDER", fill=2)
d.text((6, 15), "CONSTRUCTION", fill=2)
im.save(OUT + "constr.gif")
print("ok")
