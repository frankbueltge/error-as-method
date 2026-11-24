from PIL import Image, ImageDraw, ImageFont
import os, random

D = os.path.dirname(os.path.abspath(__file__))
def P(n): return os.path.join(D, n)
random.seed(42)

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
MONOB = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"

def nonaa(draw):
    draw.fontmode = "1"  # no antialiasing, like 1998

# background tile: pale sky blue with a few lighter specks (dithered look)
bg = Image.new("RGB", (96, 96), (176, 216, 248))
d = ImageDraw.Draw(bg)
for _ in range(260):
    x, y = random.randrange(96), random.randrange(96)
    d.point((x, y), fill=random.choice([(192, 228, 252), (160, 204, 240), (200, 232, 255)]))
# soft cloud puff
for cx, cy, r in [(30, 30, 9), (40, 27, 11), (50, 31, 8), (75, 72, 7), (83, 70, 9)]:
    d.ellipse((cx - r, cy - r // 2, cx + r, cy + r // 2), fill=(214, 236, 255))
bg.save(P("skyback.gif"))

# title graphic, transparent background, shadow
W, H = 520, 64
t = Image.new("P", (W, H), 0)
t.putpalette([255, 0, 255, 40, 0, 70, 120, 40, 170, 255, 255, 255] + [0] * (256 * 3 - 12))
d = ImageDraw.Draw(t); nonaa(d)
f = ImageFont.truetype(BOLD, 42)
txt = "Dwayne's Purple Martin Page"
tw = d.textlength(txt, font=f)
x = (W - tw) / 2
d.text((x + 3, 9), txt, font=f, fill=1)
d.text((x, 6), txt, font=f, fill=2)
t.save(P("title.gif"), transparency=0)

# martin house on a pole
mh = Image.new("P", (130, 190), 0)
pal = [255, 0, 255,   255, 255, 255,   40, 40, 40,   200, 30, 30,   150, 150, 150,  60, 60, 90]
mh.putpalette(pal + [0] * (768 - len(pal)))
d = ImageDraw.Draw(mh)
d.rectangle((61, 100, 68, 189), fill=4)  # pole
d.polygon([(10, 34), (65, 4), (120, 34)], fill=3, outline=2)  # roof
for row in range(3):
    y0 = 34 + row * 22
    d.rectangle((14, y0, 116, y0 + 22), fill=1, outline=2)
    for col in range(4):
        cx = 27 + col * 25
        d.ellipse((cx - 5, y0 + 6, cx + 5, y0 + 16), fill=2)
    d.rectangle((10, y0 + 20, 120, y0 + 22), fill=4)  # porch rail
d.rectangle((50, 102, 79, 105), fill=2)
# two birds on porch
for bx, by in [(38, 52), (88, 74)]:
    d.ellipse((bx, by, bx + 9, by + 7), fill=5)
    d.polygon([(bx + 9, by + 2), (bx + 14, by + 5), (bx + 9, by + 5)], fill=5)
mh.save(P("martinhouse.gif"), transparency=0)

# flying martin, 2-frame animation
frames = []
for up in (True, False):
    im = Image.new("P", (48, 28), 0)
    im.putpalette([255, 0, 255, 50, 30, 100] + [0] * (768 - 6))
    d = ImageDraw.Draw(im)
    d.ellipse((16, 11, 34, 18), fill=1)              # body
    d.polygon([(34, 13), (40, 15), (34, 16)], fill=1)  # head/beak
    d.polygon([(16, 14), (8, 10), (10, 15), (6, 19), (16, 16)], fill=1)  # forked tail
    if up:
        d.polygon([(20, 13), (26, 1), (30, 13)], fill=1)
    else:
        d.polygon([(20, 15), (26, 27), (30, 15)], fill=1)
    frames.append(im)
frames[0].save(P("martin.gif"), save_all=True, append_images=frames[1:], duration=250, loop=0, transparency=0, disposal=2)

# divider bar
bar = Image.new("RGB", (450, 8), (255, 255, 255))
d = ImageDraw.Draw(bar)
for x in range(450):
    c = int(80 + 100 * abs((x % 90) - 45) / 45)
    d.line((x, 0, x, 7), fill=(c - 30, 20, c + 60 if c + 60 < 256 else 255))
d.line((0, 0, 449, 0), fill=(220, 200, 255)); d.line((0, 7, 449, 7), fill=(40, 0, 60))
bar.save(P("purplebar.gif"))

# counter digits
cnt = "004817"
c = Image.new("RGB", (6 * 15 + 2, 22), (0, 0, 0))
d = ImageDraw.Draw(c); nonaa(d)
f = ImageFont.truetype(MONOB, 18)
for i, ch in enumerate(cnt):
    d.rectangle((1 + i * 15, 1, 14 + i * 15, 20), fill=(20, 20, 20), outline=(90, 90, 90))
    d.text((3 + i * 15, 1), ch, font=f, fill=(0, 255, 0))
c.save(P("counter.gif"))

# under construction 88x31
uc = Image.new("RGB", (88, 31), (255, 210, 0))
d = ImageDraw.Draw(uc); nonaa(d)
for k in range(-31, 88, 12):
    d.polygon([(k, 31), (k + 6, 31), (k + 37, 0), (k + 31, 0)], fill=(0, 0, 0))
d.rectangle((4, 8, 83, 22), fill=(255, 210, 0), outline=(0, 0, 0))
f = ImageFont.truetype(SANSB, 9)
d.text((8, 10), "UNDER CONSTR.", font=f, fill=(0, 0, 0))
uc.save(P("construct.gif"))

# mailbox / envelope icon, 2 frames
fr = []
for k in range(2):
    e = Image.new("P", (44, 30), 0)
    e.putpalette([255, 0, 255, 255, 255, 240, 0, 0, 0, 220, 0, 0] + [0] * (768 - 12))
    d = ImageDraw.Draw(e)
    oy = 0 if k == 0 else 2
    d.rectangle((2, 4 + oy, 41, 27 + oy - 2), fill=1, outline=2)
    d.line((2, 4 + oy, 21, 17 + oy), fill=2); d.line((41, 4 + oy, 21, 17 + oy), fill=2)
    d.rectangle((33, 7 + oy, 38, 12 + oy), fill=3)
    fr.append(e)
fr[0].save(P("mail.gif"), save_all=True, append_images=fr[1:], duration=400, loop=0, transparency=0, disposal=2)

# NEW! blinking
fr = []
for k in range(2):
    n = Image.new("P", (40, 16), 0)
    n.putpalette([255, 0, 255, 255, 0, 0, 255, 255, 0] + [0] * (768 - 9))
    d = ImageDraw.Draw(n); nonaa(d)
    f = ImageFont.truetype(SANSB, 12)
    d.text((2, 1), "NEW!", font=f, fill=1 if k == 0 else 2)
    fr.append(n)
fr[0].save(P("new.gif"), save_all=True, append_images=fr[1:], duration=500, loop=0, transparency=0, disposal=2)
print("ok")
