from PIL import Image, ImageDraw, ImageFont
import random, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
F = ImageFont.load_default()
random.seed(7)

def pal(img):
    return img.convert("P", palette=Image.ADAPTIVE, colors=64)

# background tile: pale blue sky w/ faint flecks (a "free backgrounds" tile)
bg = Image.new("RGB", (96, 96), (214, 228, 247))
d = ImageDraw.Draw(bg)
for _ in range(260):
    x, y = random.randrange(96), random.randrange(96)
    c = random.choice([(205, 221, 243), (225, 236, 250), (200, 216, 240)])
    d.point((x, y), fill=c)
for (x, y) in [(14, 20), (60, 70), (80, 12), (30, 80)]:
    for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
        d.point(((x+dx) % 96, (y+dy) % 96), fill=(245, 250, 255))
pal(bg).save("bg.gif")

# animated mailbox, flag up / down
frames = []
for up in (True, False):
    im = Image.new("RGB", (48, 48), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.rectangle((22, 28, 25, 47), fill=(110, 70, 30))  # post
    d.rectangle((6, 14, 38, 28), fill=(80, 80, 90), outline=(0, 0, 0))
    d.pieslice((6, 6, 38, 22), 180, 360, fill=(80, 80, 90), outline=(0, 0, 0))
    d.rectangle((7, 14, 37, 27), fill=(80, 80, 90))
    d.line((6, 14, 6, 28), fill=(0, 0, 0)); d.line((38, 14, 38, 28), fill=(0, 0, 0))
    d.line((6, 28, 38, 28), fill=(0, 0, 0))
    d.ellipse((3, 10, 9, 28), fill=(60, 60, 70), outline=(0, 0, 0))
    if up:
        d.rectangle((33, 2, 35, 16), fill=(200, 0, 0)); d.rectangle((33, 2, 42, 6), fill=(200, 0, 0))
    else:
        d.rectangle((33, 15, 46, 17), fill=(200, 0, 0)); d.rectangle((43, 15, 46, 21), fill=(200, 0, 0))
    frames.append(pal(im))
frames[0].save("mailbox.gif", save_all=True, append_images=frames[1:], duration=600, loop=0, transparency=frames[0].getpixel((0, 0)))

# under construction sign, blinking light
frames = []
for on in (True, False):
    im = Image.new("RGB", (88, 60), (255, 255, 255))
    d = ImageDraw.Draw(im)
    for i in range(-60, 100, 12):
        d.polygon([(i, 52), (i+6, 52), (i+14, 60), (i+8, 60)], fill=(0, 0, 0))
    d.rectangle((0, 52, 87, 59), outline=(0, 0, 0))
    for i in range(0, 88, 12):
        d.polygon([(i, 52), (i+6, 52), (i+12, 59), (i+6, 59)], fill=(0, 0, 0))
    d.polygon([(44, 2), (82, 30), (44, 52), (6, 30)], fill=(255, 210, 0), outline=(0, 0, 0))
    # little man with shovel
    d.ellipse((40, 14, 46, 20), fill=(0, 0, 0))
    d.line((43, 20, 41, 32), fill=(0, 0, 0), width=2)
    d.line((41, 32, 37, 40), fill=(0, 0, 0), width=2); d.line((41, 32, 46, 40), fill=(0, 0, 0), width=2)
    d.line((42, 24, 52, 28), fill=(0, 0, 0), width=2); d.line((52, 22, 54, 40), fill=(0, 0, 0))
    d.polygon([(51, 38), (57, 38), (54, 44)], fill=(0, 0, 0))
    d.polygon([(26, 40), (34, 40), (30, 34)], fill=(0, 0, 0))
    d.ellipse((60, 4, 70, 14), fill=(255, 40, 0) if on else (120, 40, 0), outline=(0, 0, 0))
    frames.append(pal(im))
frames[0].save("construction.gif", save_all=True, append_images=frames[1:], duration=500, loop=0)

# "NEW!" blinking
frames = []
for c in ((255, 0, 0), (255, 255, 0)):
    im = Image.new("RGB", (32, 14), (214, 228, 247))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 31, 13), fill=c, outline=(0, 0, 0))
    d.text((5, 1), "NEW!", fill=(0, 0, 0) if c[1] else (255, 255, 255), font=F)
    frames.append(pal(im))
frames[0].save("new.gif", save_all=True, append_images=frames[1:], duration=400, loop=0)

# divider bar: blue/gold "loon lake" bar
im = Image.new("RGB", (500, 8), (255, 255, 255))
d = ImageDraw.Draw(im)
for x in range(500):
    t = x / 499
    r = int(20 + 200 * abs(0.5 - t) * 0)  # flat blue body
    d.line((x, 0, x, 7), fill=(0, 40 + int(80 * (1 - abs(0.5 - t) * 2)), 150 + int(90 * (1 - abs(0.5 - t) * 2))))
for x in range(0, 500, 20):
    d.ellipse((x + 7, 2, x + 11, 5), fill=(255, 210, 0))
pal(im).save("bar.gif")

# ice house, "drawn in Paint"
im = Image.new("RGB", (260, 170), (255, 255, 255))
d = ImageDraw.Draw(im)
d.rectangle((0, 0, 259, 95), fill=(160, 200, 255))  # sky
d.rectangle((0, 96, 259, 169), fill=(255, 255, 255))  # ice/snow
d.line((0, 96, 259, 96), fill=(128, 128, 128))
d.ellipse((205, 12, 240, 47), fill=(255, 255, 0), outline=(0, 0, 0))
# pines far shore
for x in range(0, 260, 22):
    d.polygon([(x, 96), (x + 9, 70 + (x * 7) % 12), (x + 18, 96)], fill=(0, 100, 0), outline=(0, 0, 0))
# the house
d.rectangle((70, 70, 150, 130), fill=(200, 0, 0), outline=(0, 0, 0))
d.polygon([(64, 72), (110, 48), (156, 72)], fill=(128, 128, 128), outline=(0, 0, 0))
d.rectangle((96, 96, 118, 130), fill=(128, 64, 0), outline=(0, 0, 0))
d.ellipse((112, 112, 115, 115), fill=(255, 255, 0))
d.rectangle((76, 82, 90, 94), fill=(255, 255, 160), outline=(0, 0, 0))
d.line((83, 82, 83, 94), fill=(0, 0, 0)); d.line((76, 88, 90, 88), fill=(0, 0, 0))
# stove pipe + smoke
d.rectangle((132, 44, 138, 62), fill=(0, 0, 0))
for i, (x, y) in enumerate([(136, 36), (142, 26), (150, 17), (160, 10)]):
    d.ellipse((x - 4 - i, y - 4 - i, x + 4 + i, y + 4 + i), outline=(128, 128, 128))
# truck
d.rectangle((175, 108, 235, 128), fill=(0, 0, 200), outline=(0, 0, 0))
d.rectangle((205, 96, 228, 110), fill=(0, 0, 200), outline=(0, 0, 0))
d.rectangle((209, 99, 224, 107), fill=(160, 200, 255), outline=(0, 0, 0))
d.ellipse((180, 122, 194, 136), fill=(0, 0, 0)); d.ellipse((215, 122, 229, 136), fill=(0, 0, 0))
# dog
d.ellipse((30, 118, 54, 130), fill=(0, 0, 0))
d.ellipse((50, 110, 60, 120), fill=(0, 0, 0))
for lx in (33, 38, 46, 51):
    d.line((lx, 128, lx, 136), fill=(0, 0, 0), width=2)
d.line((30, 122, 24, 116), fill=(0, 0, 0), width=2)
d.text((22, 140), "DUCHESS", fill=(0, 0, 0), font=F)
d.text((86, 136), "MY ICE HOUSE", fill=(0, 0, 0), font=F)
d.text((84, 150), "Knife Lake  Jan. '98", fill=(0, 0, 0), font=F)
d.text((178, 140), "the Ford", fill=(0, 0, 0), font=F)
d.rectangle((0, 0, 259, 169), outline=(0, 0, 0))
pal(im).save("icehouse.gif")

# hit counter digits
def counter(n, name):
    s = str(n).zfill(6)
    im = Image.new("RGB", (len(s) * 11 + 2, 17), (0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, ch in enumerate(s):
        x = 1 + i * 11
        d.rectangle((x, 1, x + 9, 15), fill=(20, 20, 20), outline=(90, 90, 90))
        d.text((x + 2, 3), ch, fill=(0, 255, 0), font=F)
    pal(im).save(name)
counter(213, "counter.gif")

# envelope
im = Image.new("RGB", (40, 26), (214, 228, 247))
d = ImageDraw.Draw(im)
d.rectangle((1, 1, 38, 24), fill=(255, 255, 230), outline=(0, 0, 0))
d.line((1, 1, 20, 14), fill=(0, 0, 0)); d.line((38, 1, 20, 14), fill=(0, 0, 0))
d.rectangle((30, 4, 35, 10), fill=(200, 0, 0))
pal(im).save("email.gif")

# raindrop bullet
im = Image.new("RGB", (11, 11), (214, 228, 247))
d = ImageDraw.Draw(im)
d.ellipse((1, 1, 9, 9), fill=(0, 0, 200), outline=(0, 0, 90))
d.point((3, 3), fill=(255, 255, 255)); d.point((4, 3), fill=(255, 255, 255))
pal(im).save("ball.gif")
