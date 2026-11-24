import random
from PIL import Image, ImageDraw, ImageFilter
OUT = "../S3/"
random.seed(7)
# snapshot of the gauge, taken from a few steps back, a little crooked, drugstore print scanned
W, H = 240, 180
im = Image.new("RGB", (W, H))
d = ImageDraw.Draw(im)
for y in range(H):
    if y < 92:
        c = (170 + y // 4, 190 + y // 6, 212)
    else:
        t = y - 92
        c = (150 - t // 3 + random.randint(-6, 6), 135 - t // 3, 80 - t // 6)
    d.line((0, y, W, y), fill=c)
# windbreak of cedars on horizon left, farmhouse right
for x in range(0, 110, 4):
    h = random.randint(10, 24)
    d.polygon([(x, 94), (x + 3, 94 - h), (x + 7, 94)], fill=(52, 70, 48))
d.rectangle((150, 74, 196, 94), fill=(225, 222, 210))
d.polygon([(146, 75), (173, 60), (200, 75)], fill=(110, 60, 55))
d.rectangle((158, 80, 166, 88), fill=(80, 90, 110))
d.rectangle((180, 80, 188, 88), fill=(80, 90, 110))
d.rectangle((205, 70, 212, 94), fill=(150, 150, 150))  # grain bin-ish
d.ellipse((203, 66, 214, 74), fill=(160, 160, 160))
# grass texture
for _ in range(900):
    x = random.randrange(W); y = random.randrange(96, H)
    d.line((x, y, x + random.randint(-1, 1), y - random.randint(2, 5)), fill=(120 + random.randint(-20, 20), 110, 60))
# fence wire and posts receding to the right
for i, px in enumerate([30, 140, 200, 232]):
    w = max(2, 14 - i * 4); top = 70 + i * 10
    d.rectangle((px, top, px + w, 140 - i * 12), fill=(105, 88, 66))
d.line((0, 104, W, 100), fill=(70, 70, 70))
d.line((0, 118, W, 112), fill=(70, 70, 70))
# the gauge on the near post
d.rectangle((36, 60, 41, 63), fill=(150, 150, 150))
d.rectangle((38, 40, 45, 72), fill=(215, 222, 228), outline=(130, 130, 140))
d.rectangle((39, 62, 44, 71), fill=(160, 180, 210))
d.polygon([(36, 40), (47, 40), (45, 44), (38, 44)], fill=(200, 205, 210))
# a dog
d.ellipse((96, 128, 122, 142), fill=(60, 45, 35))
d.ellipse((116, 120, 128, 132), fill=(60, 45, 35))
d.line((100, 140, 99, 150), fill=(60, 45, 35), width=2)
d.line((118, 140, 119, 150), fill=(60, 45, 35), width=2)
im = im.rotate(-2.2, resample=Image.BICUBIC, expand=False, fillcolor=(235, 232, 220))
im = im.filter(ImageFilter.GaussianBlur(0.9))
px = im.load()
for x in range(W):
    for y in range(H):
        r, g, b = px[x, y]
        n = random.randint(-10, 10)
        # warm cast, faded
        r = int(r * 0.92 + 30) + n; g = int(g * 0.9 + 22) + n; b = int(b * 0.82 + 10) + n
        px[x, y] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
d = ImageDraw.Draw(im)
d.text((186, 166), "5 12 98", fill=(255, 130, 40))
im.save(OUT + "gauge2.jpg", quality=50)

# construction sign, fixed
im = Image.new("P", (88, 40), 0)
im.putpalette([255, 255, 255, 255, 210, 0, 0, 0, 0] + [0] * (253 * 3))
d = ImageDraw.Draw(im)
d.rectangle((0, 0, 87, 39), fill=1, outline=2)
for x in range(-40, 90, 10):
    d.polygon([(x, 39), (x + 5, 39), (x + 15, 33), (x + 10, 33)], fill=2)
d.text((29, 5), "UNDER", fill=2)
d.text((8, 18), "CONSTRUCTION", fill=2)
im.save(OUT + "constr2.gif")
# geocities-ish hosted-by button? no: keep text only
print("ok")
