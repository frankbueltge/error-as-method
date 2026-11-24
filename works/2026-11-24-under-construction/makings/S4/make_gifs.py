import random
from PIL import Image, ImageDraw, ImageFont

D = "../S4/"
random.seed(42)
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def save(im, name, transparent=None):
    im = im.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=32)
    kw = {}
    if transparent is not None:
        # find palette index closest to transparent colour
        pal = im.getpalette()
        best = min(range(len(pal)//3), key=lambda i: sum((pal[3*i+k]-transparent[k])**2 for k in range(3)))
        kw["transparency"] = best
    im.save(D + name, **kw)


# tiled background: pale icy blue with speckles
bg = Image.new("RGB", (64, 64), (214, 232, 246))
d = ImageDraw.Draw(bg)
for _ in range(70):
    x, y = random.randrange(64), random.randrange(64)
    c = random.choice([(232, 243, 252), (198, 220, 240), (245, 250, 255)])
    d.point((x, y), fill=c)
for _ in range(4):
    x, y = random.randrange(64), random.randrange(64)
    d.line((x, y, x + random.randint(3, 8), y + random.randint(-2, 2)), fill=(200, 222, 241))
save(bg, "ice.gif")

# title: shadowed serif text on transparent-ish background colour matching tile
W, H = 470, 64
t = Image.new("RGB", (W, H), (214, 232, 246))
d = ImageDraw.Draw(t)
f = ImageFont.truetype(FB, 36)
txt = "Gordy's Ice Shanty"
tw = d.textlength(txt, font=f)
x = (W - tw) // 2
d.text((x + 3, 13), txt, font=f, fill=(40, 40, 90))
d.text((x, 10), txt, font=f, fill=(0, 70, 160))
save(t, "title.gif", transparent=(214, 232, 246))

# shanty picture: drawn scene
S = Image.new("RGB", (240, 160), (170, 196, 222))
d = ImageDraw.Draw(S)
# sky gradient-ish
for y in range(0, 92):
    c = (150 + y // 3, 178 + y // 4, 214 + y // 8)
    d.line((0, y, 240, y), fill=c)
# far shore with trees
d.polygon([(0, 84), (40, 78), (90, 82), (150, 76), (240, 83), (240, 92), (0, 92)], fill=(92, 104, 110))
for i in range(0, 240, 7):
    h = random.randint(4, 10)
    d.polygon([(i, 84), (i + 3, 84 - h), (i + 6, 84)], fill=(60, 74, 70))
# ice
d.rectangle((0, 92, 240, 160), fill=(232, 238, 244))
for _ in range(120):
    x, y = random.randrange(240), random.randrange(92, 160)
    d.point((x, y), fill=random.choice([(210, 220, 232), (250, 252, 255)]))
# shanty body
d.rectangle((70, 68, 140, 128), fill=(176, 40, 32), outline=(90, 20, 16))
# roof
d.polygon([(64, 70), (105, 50), (146, 70)], fill=(70, 70, 70), outline=(30, 30, 30))
# door
d.rectangle((96, 96, 114, 128), fill=(120, 26, 20), outline=(70, 14, 10))
d.point((110, 112), fill=(220, 200, 80))
# window
d.rectangle((76, 82, 90, 94), fill=(250, 230, 140), outline=(60, 20, 10))
d.line((83, 82, 83, 94), fill=(60, 20, 10))
# stove pipe + smoke
d.rectangle((126, 46, 131, 62), fill=(50, 50, 50))
for i, (sx, sy, r) in enumerate([(130, 40, 4), (135, 33, 5), (142, 25, 6), (151, 18, 7)]):
    d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(205, 208, 214))
# lettering "PFAFF"
fs = ImageFont.truetype(FSB, 9)
d.text((118, 99), "#14", font=fs, fill=(250, 240, 200))
# snow on roof
d.line((66, 69, 105, 51), fill=(250, 250, 250), width=2)
d.line((105, 51, 144, 69), fill=(250, 250, 250), width=2)
# truck
d.rectangle((168, 108, 214, 124), fill=(40, 70, 120), outline=(20, 30, 60))
d.rectangle((174, 98, 196, 110), fill=(40, 70, 120), outline=(20, 30, 60))
d.rectangle((178, 101, 192, 108), fill=(180, 210, 230))
d.ellipse((172, 120, 182, 130), fill=(20, 20, 20))
d.ellipse((200, 120, 210, 130), fill=(20, 20, 20))
# person
d.ellipse((38, 100, 46, 108), fill=(230, 190, 160))
d.rectangle((37, 97, 47, 101), fill=(200, 140, 20))
d.rectangle((36, 108, 48, 124), fill=(60, 90, 60))
d.line((39, 124, 39, 132), fill=(30, 30, 30), width=3)
d.line((45, 124, 45, 132), fill=(30, 30, 30), width=3)
# bucket
d.rectangle((52, 124, 60, 132), fill=(230, 230, 230), outline=(120, 120, 120))
# hole in ice
d.ellipse((20, 134, 32, 138), fill=(30, 50, 70))
S = S.quantize(colors=48, dither=Image.FLOYDSTEINBERG)
S.save(D + "shanty.gif")

# small walleye bullet
fw = Image.new("RGB", (40, 16), (214, 232, 246))
d = ImageDraw.Draw(fw)
d.ellipse((4, 3, 30, 13), fill=(196, 170, 60), outline=(90, 80, 30))
d.polygon([(28, 8), (38, 2), (38, 14)], fill=(170, 150, 50), outline=(90, 80, 30))
d.point((9, 7), fill=(255, 255, 255))
d.point((9, 7), fill=(255, 255, 255))
d.rectangle((8, 6, 10, 8), fill=(250, 250, 230))
d.point((9, 7), fill=(0, 0, 0))
d.line((14, 4, 22, 3), fill=(110, 100, 40))
save(fw, "walleye.gif", transparent=(214, 232, 246))

# divider bar: blue-white gradient with snowflake dots
bw, bh = 500, 6
bar = Image.new("RGB", (bw, bh))
d = ImageDraw.Draw(bar)
for x in range(bw):
    k = abs((x % 100) - 50) / 50
    c = (int(30 + 180 * k), int(80 + 150 * k), int(170 + 80 * k))
    d.line((x, 0, x, bh), fill=c)
save(bar, "bar.gif")

# counter digits, odometer style
num = "004871"
cw = 15
cnt = Image.new("RGB", (cw * len(num) + 2, 22), (0, 0, 0))
d = ImageDraw.Draw(cnt)
fc = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 15)
for i, ch in enumerate(num):
    x0 = 1 + i * cw
    d.rectangle((x0, 1, x0 + cw - 2, 20), fill=(20, 20, 20), outline=(90, 90, 90))
    d.text((x0 + 3, 2), ch, font=fc, fill=(80, 255, 80))
save(cnt, "counter.gif")

# under construction strip
uc = Image.new("RGB", (88, 31), (255, 210, 0))
d = ImageDraw.Draw(uc)
for x in range(-31, 88, 12):
    d.polygon([(x, 31), (x + 6, 31), (x + 37, 0), (x + 31, 0)], fill=(0, 0, 0))
d.rectangle((6, 8, 81, 22), fill=(255, 210, 0), outline=(0, 0, 0))
fsm = ImageFont.truetype(FSB, 9)
d.text((9, 10), "UNDER CONST.", font=fsm, fill=(0, 0, 0))
save(uc, "construct.gif")

# envelope
env = Image.new("RGB", (36, 24), (214, 232, 246))
d = ImageDraw.Draw(env)
d.rectangle((1, 2, 34, 22), fill=(250, 250, 240), outline=(80, 80, 80))
d.line((1, 2, 17, 14, 34, 2), fill=(80, 80, 80))
d.rectangle((27, 4, 32, 9), fill=(200, 40, 40))
save(env, "mail.gif", transparent=(214, 232, 246))

# photo of the dog: grainy "scanned snapshot"
P = Image.new("RGB", (130, 100), (120, 140, 90))
d = ImageDraw.Draw(P)
for y in range(100):
    d.line((0, y, 130, y), fill=(110 + y // 4, 130 + y // 5, 80 + y // 6))
d.rectangle((0, 0, 130, 38), fill=(200, 200, 190))  # siding of house
for y in range(4, 38, 6):
    d.line((0, y, 130, y), fill=(170, 170, 160))
# dog body (black lab)
d.ellipse((30, 50, 96, 80), fill=(22, 20, 18))
d.ellipse((84, 36, 110, 60), fill=(26, 24, 22))  # head
d.ellipse((100, 46, 116, 58), fill=(30, 28, 26))  # snout
d.ellipse((86, 38, 94, 54), fill=(14, 12, 10))  # ear
d.rectangle((36, 74, 42, 92), fill=(20, 18, 16))
d.rectangle((50, 74, 56, 92), fill=(20, 18, 16))
d.rectangle((76, 74, 82, 92), fill=(20, 18, 16))
d.rectangle((86, 72, 92, 92), fill=(20, 18, 16))
d.line((30, 60, 16, 50), fill=(22, 20, 18), width=4)
d.point((101, 44), fill=(200, 180, 120))
d.ellipse((112, 48, 116, 52), fill=(5, 5, 5))
d.line((104, 58, 108, 62), fill=(200, 60, 80), width=2)
# grain
for _ in range(900):
    x, y = random.randrange(130), random.randrange(100)
    r, g, b = P.getpixel((x, y))
    n = random.randint(-22, 22)
    P.putpixel((x, y), (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n))))
# date stamp
fd = ImageFont.truetype(FSB, 8)
d.text((84, 90), "'96 3 14", font=fd, fill=(255, 140, 40))
P.save(D + "duke.jpg", quality=55)
print("ok")
