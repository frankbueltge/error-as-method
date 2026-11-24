from PIL import Image, ImageDraw
import math, os

D = os.path.dirname(os.path.abspath(__file__))


def save_gif(img, name, transparent=None):
    p = img.convert("P", palette=Image.ADAPTIVE, colors=32)
    kw = {}
    if transparent is not None:
        # find palette index of the transparent colour
        pal = p.getpalette()
        best = 0
        bd = 1e9
        for i in range(len(pal) // 3):
            r, g, b = pal[i * 3:i * 3 + 3]
            d = (r - transparent[0]) ** 2 + (g - transparent[1]) ** 2 + (b - transparent[2]) ** 2
            if d < bd:
                bd, best = d, i
        kw["transparency"] = best
    p.save(os.path.join(D, name), **kw)


# --- hummingbird clip art, 100x80, flat colours, transparent white ---
W = (255, 255, 255)
im = Image.new("RGB", (100, 80), W)
d = ImageDraw.Draw(im)
green = (40, 140, 60)
dark = (20, 80, 30)
red = (210, 20, 40)
# wing (blurred-ish fan)
d.polygon([(48, 34), (30, 4), (40, 2), (58, 28)], fill=(170, 200, 170))
d.polygon([(50, 34), (42, 6), (52, 6), (60, 30)], fill=(130, 175, 135))
# body
d.ellipse((34, 30, 70, 48), fill=green, outline=dark)
# tail
d.polygon([(66, 40), (92, 52), (88, 58), (64, 46)], fill=dark)
# head
d.ellipse((26, 26, 42, 42), fill=green, outline=dark)
# throat
d.polygon([(30, 38), (40, 40), (36, 48), (28, 44)], fill=red)
# eye
d.ellipse((31, 30, 35, 34), fill=(0, 0, 0))
# beak
d.line((27, 33, 4, 36), fill=(30, 30, 30), width=2)
# belly
d.ellipse((40, 40, 60, 48), fill=(230, 235, 220))
save_gif(im, "hummer.gif", transparent=W)

# --- flipped copy for the other side of the title ---
save_gif(im.transpose(Image.FLIP_LEFT_RIGHT), "hummer2.gif", transparent=W)

# --- feeder "photo", 200x240, a scanned snapshot look ---
im = Image.new("RGB", (200, 240), (200, 205, 190))
d = ImageDraw.Draw(im)
# window frame + outdoor background (green yard, grey sky)
for y in range(240):
    t = y / 240
    c = (int(170 + 40 * (1 - t)), int(190 + 30 * (1 - t)), int(200 - 60 * t))
    d.line((0, y, 200, y), fill=c)
d.rectangle((0, 150, 200, 240), fill=(90, 130, 70))
for x in range(0, 200, 7):
    d.line((x, 150, x + 3, 140), fill=(70, 110, 55))
# a tree trunk
d.rectangle((150, 40, 165, 160), fill=(95, 75, 55))
d.ellipse((115, 0, 200, 70), fill=(80, 120, 70))
# hanging wire
d.line((80, 0, 80, 60), fill=(60, 60, 60), width=1)
# feeder jar
d.rectangle((62, 60, 98, 130), fill=(235, 120, 130), outline=(150, 60, 70))
d.rectangle((66, 64, 72, 126), fill=(250, 170, 180))
# base dish
d.ellipse((44, 125, 116, 150), fill=(200, 20, 35), outline=(120, 10, 20))
for fx in (54, 80, 106):
    d.ellipse((fx - 5, 131, fx + 5, 141), fill=(250, 220, 40), outline=(150, 120, 0))
# a bird at the feeder
d.ellipse((108, 112, 128, 122), fill=(45, 120, 60))
d.ellipse((102, 108, 112, 118), fill=(45, 120, 60))
d.line((102, 113, 92, 128), fill=(20, 20, 20), width=1)
d.polygon([(114, 112), (120, 96), (126, 98), (120, 114)], fill=(150, 170, 150))
d.polygon([(126, 118), (140, 126), (136, 128), (125, 121)], fill=(20, 70, 30))
# window muntin
d.rectangle((0, 0, 200, 240), outline=(245, 245, 240), width=6)
# date stamp, like a drugstore print
for i, ch in enumerate("5 4 '98"):
    pass
d.text((128, 222), "5 4 '98", fill=(255, 140, 0))
import random
random.seed(7)
px = im.load()
for yy in range(240):
    for xx in range(200):
        r, g, b = px[xx, yy]
        n = random.randint(-14, 14)
        px[xx, yy] = (max(0, min(255, r + n + 8)), max(0, min(255, g + n)), max(0, min(255, b + n - 10)))
from PIL import ImageFilter
im = im.filter(ImageFilter.GaussianBlur(0.8))
im.save(os.path.join(D, "feeder.jpg"), quality=55)

# --- divider: row of little red flowers on green vine, 400x14 ---
im = Image.new("RGB", (400, 14), W)
d = ImageDraw.Draw(im)
d.line((0, 7, 400, 7), fill=(40, 140, 60), width=2)
for x in range(10, 400, 30):
    d.ellipse((x - 4, 3, x + 4, 11), fill=(220, 30, 60))
    d.ellipse((x - 1, 6, x + 1, 8), fill=(255, 230, 80))
    d.ellipse((x + 10, 4, x + 16, 8), fill=(60, 160, 70))
save_gif(im, "vine.gif", transparent=W)

# --- background tile: pale yellow with faint dots ---
im = Image.new("RGB", (64, 64), (255, 255, 230))
d = ImageDraw.Draw(im)
for (x, y) in [(8, 10), (40, 22), (20, 46), (54, 54)]:
    d.point((x, y), fill=(235, 230, 190))
    d.point((x + 1, y), fill=(235, 230, 190))
save_gif(im, "bgtile.gif")

# --- under construction sign, 88x31 ---
im = Image.new("RGB", (88, 31), (250, 210, 0))
d = ImageDraw.Draw(im)
for x in range(-31, 88, 10):
    d.polygon([(x, 31), (x + 5, 31), (x + 36, 0), (x + 31, 0)], fill=(20, 20, 20))
d.rectangle((6, 8, 81, 22), fill=(250, 210, 0), outline=(0, 0, 0))
d.text((10, 10), "UNDER CONST.", fill=(0, 0, 0))
save_gif(im, "constr.gif")

# --- odometer counter, digits on black ---
num = "002417"
cw, ch = 13, 20
im = Image.new("RGB", (cw * len(num), ch), (0, 0, 0))
d = ImageDraw.Draw(im)
segs = {
    '0': "abcdef", '1': "bc", '2': "abged", '3': "abgcd", '4': "fgbc",
    '5': "afgcd", '6': "afgedc", '7': "abc", '8': "abcdefg", '9': "abcfgd",
}
for i, n in enumerate(num):
    ox = i * cw
    d.rectangle((ox, 0, ox + cw - 1, ch - 1), outline=(60, 60, 60))
    L, R, T, M, B = ox + 3, ox + 9, 3, 10, 16
    col = (60, 255, 60)
    s = segs[n]
    if 'a' in s: d.line((L, T, R, T), fill=col, width=2)
    if 'b' in s: d.line((R, T, R, M), fill=col, width=2)
    if 'c' in s: d.line((R, M, R, B), fill=col, width=2)
    if 'd' in s: d.line((L, B, R, B), fill=col, width=2)
    if 'e' in s: d.line((L, M, L, B), fill=col, width=2)
    if 'f' in s: d.line((L, T, L, M), fill=col, width=2)
    if 'g' in s: d.line((L, M, R, M), fill=col, width=2)
save_gif(im, "counter.gif")

# --- small mailbox icon 40x32 ---
im = Image.new("RGB", (40, 32), W)
d = ImageDraw.Draw(im)
d.rectangle((18, 18, 21, 31), fill=(110, 80, 50))
d.pieslice((4, 2, 30, 26), 180, 360, fill=(30, 60, 160))
d.rectangle((4, 13, 30, 20), fill=(30, 60, 160))
d.rectangle((28, 4, 30, 12), fill=(220, 20, 30))
d.rectangle((30, 4, 35, 7), fill=(220, 20, 30))
d.line((8, 12, 26, 12), fill=(10, 30, 90))
save_gif(im, "mailbox.gif", transparent=W)
print("ok")
