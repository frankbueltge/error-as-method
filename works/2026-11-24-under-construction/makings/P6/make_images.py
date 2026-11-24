import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

random.seed(1998)
F = ImageFont.load_default()

# --- background tile: pale icy blue with faint speckle
bg = Image.new("RGB", (64, 64), (226, 236, 246))
d = ImageDraw.Draw(bg)
for _ in range(140):
    x, y = random.randrange(64), random.randrange(64)
    c = random.choice([(214, 226, 240), (238, 244, 250), (220, 232, 244)])
    d.point((x, y), c)
for _ in range(5):
    x, y = random.randrange(64), random.randrange(64)
    d.line((x, y, x + random.randint(3, 9), y + random.randint(-2, 2)), (206, 220, 236))
bg.convert("P", palette=Image.ADAPTIVE, colors=16).save("bg.gif")


def scanned(img, q=38):
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            n = random.randint(-7, 7)
            px[x, y] = (min(255, max(0, r + n + 6)), min(255, max(0, g + n)), min(255, max(0, b + n - 8)))
    return img


# --- the fish house photo (a "scan" of a snapshot)
W, H = 240, 170
p = Image.new("RGB", (W, H))
d = ImageDraw.Draw(p)
for y in range(80):
    t = y / 80
    d.line((0, y, W, y), (int(150 + 60 * t), int(170 + 50 * t), int(200 + 35 * t)))
# far shoreline trees
for x in range(0, W, 5):
    th = random.randint(8, 20)
    d.polygon([(x - 4, 82), (x + 2, 82 - th), (x + 7, 82)], (52, 70, 60))
d.rectangle((0, 80, W, H), (236, 238, 242))
for _ in range(400):
    x, y = random.randrange(W), random.randrange(84, H)
    d.point((x, y), (222, 226, 234))
# tire tracks
d.line((0, 150, 120, 118), (205, 208, 214), 3)
d.line((0, 162, 130, 124), (205, 208, 214), 3)
# fish house body
d.polygon([(70, 128), (70, 78), (150, 78), (150, 128)], (150, 32, 30))
d.polygon([(150, 128), (150, 78), (176, 86), (176, 122)], (112, 22, 22))
# roof
d.polygon([(64, 80), (110, 58), (156, 80)], (60, 60, 64))
d.polygon([(156, 80), (110, 58), (140, 60), (182, 87)], (44, 44, 48))
# white trim + door + window
d.rectangle((82, 92, 104, 127), (232, 226, 210))
d.rectangle((85, 95, 101, 125), (128, 26, 24))
d.point((99, 110), (230, 210, 120))
d.rectangle((118, 92, 138, 106), (232, 226, 210))
d.rectangle((120, 94, 136, 104), (90, 110, 140))
d.line((128, 94, 128, 104), (232, 226, 210))
# stovepipe + smoke
d.rectangle((136, 52, 140, 68), (90, 90, 94))
for i, (sx, sy, r) in enumerate([(142, 46, 4), (148, 38, 5), (156, 30, 6), (166, 24, 7)]):
    d.ellipse((sx - r, sy - r, sx + r, sy + r), (200 - i * 6, 204 - i * 6, 212 - i * 6))
# hand painted sign
d.rectangle((88, 80, 132, 87), (232, 226, 210))
d.text((90, 78), "HILTON", (20, 20, 20), font=F)
# truck at left
d.rectangle((14, 112, 50, 132), (40, 70, 110))
d.rectangle((20, 102, 38, 114), (40, 70, 110))
d.rectangle((23, 104, 35, 112), (150, 170, 190))
d.ellipse((16, 128, 26, 138), (20, 20, 20))
d.ellipse((38, 128, 48, 138), (20, 20, 20))
# a person (Gary) next to house
d.rectangle((186, 104, 194, 126), (200, 80, 20))
d.ellipse((186, 94, 194, 103), (230, 190, 160))
d.rectangle((185, 92, 195, 96), (30, 30, 30))
d.line((188, 126, 186, 136), (40, 40, 60), 3)
d.line((192, 126, 194, 136), (40, 40, 60), 3)
p = scanned(p)
# photo-lab date stamp
d = ImageDraw.Draw(p)
d.text((178, 156), "'98 1 17", (255, 140, 40), font=F)
p.save("fishhouse.jpg", quality=55)

# --- Duke the dog
W, H = 150, 112
p = Image.new("RGB", (W, H), (180, 160, 128))
d = ImageDraw.Draw(p)
d.rectangle((0, 0, W, 50), (196, 184, 150))  # wall paneling
for x in range(0, W, 14):
    d.line((x, 0, x, 50), (160, 140, 104))
d.rectangle((0, 50, W, H), (120, 96, 70))  # carpet
d.ellipse((30, 54, 120, 100), (24, 22, 22))  # body
d.ellipse((96, 34, 136, 70), (28, 26, 26))  # head
d.ellipse((112, 54, 140, 72), (34, 32, 30))  # snout
d.ellipse((96, 38, 108, 62), (16, 14, 14))  # ear
d.ellipse((116, 44, 120, 48), (200, 170, 90))  # eye
d.ellipse((134, 56, 140, 61), (10, 10, 10))
d.ellipse((18, 82, 46, 92), (24, 22, 22))  # tail curled
d.rectangle((0, 98, W, H), (128, 102, 76))
p = scanned(p)
p.save("duke.jpg", quality=50)

# --- little walleye clipart (animated: tail wiggle)
frames = []
for k in range(2):
    im = Image.new("P", (60, 26), 0)
    im.putpalette([255, 255, 255, 140, 120, 40, 196, 170, 70, 230, 220, 170, 0, 0, 0, 250, 250, 250, 220, 120, 40] + [0] * (256 * 3 - 21))
    d = ImageDraw.Draw(im)
    d.ellipse((10, 6, 50, 21), 1)
    d.ellipse((12, 11, 48, 21), 2)
    d.ellipse((14, 15, 44, 21), 3)
    if k == 0:
        d.polygon([(12, 13), (1, 4), (3, 13), (1, 22)], 1)
    else:
        d.polygon([(12, 13), (2, 6), (5, 13), (2, 20)], 1)
    d.polygon([(22, 7), (26, 1), (34, 2), (36, 7)], 1)
    d.ellipse((42, 9, 47, 14), 5)
    d.point((45, 11), 4)
    d.point((44, 11), 4)
    d.line((50, 15, 46, 16), 4)
    frames.append(im)
frames[0].save("walleye.gif", save_all=True, append_images=frames[1:], duration=300, loop=0, transparency=0, disposal=2)

# --- under construction (animated flashing lamp)
frames = []
for k in range(2):
    im = Image.new("RGB", (110, 46), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 30, 109, 45), (0, 0, 0))
    for x in range(-20, 120, 14):
        d.polygon([(x, 45), (x + 7, 45), (x + 22, 30), (x + 15, 30)], (250, 210, 0))
    d.rectangle((6, 4, 104, 28), (250, 210, 0))
    d.rectangle((6, 4, 104, 28), outline=(0, 0, 0))
    d.text((12, 5), "UNDER", (0, 0, 0), font=F)
    d.text((12, 16), "CONSTRUCTION", (0, 0, 0), font=F)
    d.ellipse((88, 6, 100, 18), (255, 60, 0) if k == 0 else (120, 40, 0))
    frames.append(im.convert("P", palette=Image.ADAPTIVE, colors=16))
frames[0].save("construction.gif", save_all=True, append_images=frames[1:], duration=500, loop=0)

# --- hit counter digits
digits = "004127"
im = Image.new("RGB", (len(digits) * 13 + 2, 20), (0, 0, 0))
d = ImageDraw.Draw(im)
for i, ch in enumerate(digits):
    x = 1 + i * 13
    d.rectangle((x, 1, x + 11, 18), (24, 24, 24))
    big = Image.new("RGB", (6, 10), (24, 24, 24))
    ImageDraw.Draw(big).text((0, -1), ch, (60, 255, 60), font=F)
    big = big.resize((12, 18), Image.NEAREST)
    im.paste(big, (x, 1))
im.convert("P", palette=Image.ADAPTIVE, colors=8).save("counter.gif")

# --- divider: a fishing line with bobber
im = Image.new("P", (400, 14), 0)
im.putpalette([255, 255, 255, 60, 60, 60, 220, 30, 30, 250, 250, 250] + [0] * (256 * 3 - 12))
d = ImageDraw.Draw(im)
for x in range(0, 400, 1):
    y = 7 + (1 if (x // 20) % 2 else 0)
    d.point((x, y), 1)
for cx in range(30, 400, 90):
    d.ellipse((cx, 2, cx + 9, 11), 3, outline=1)
    d.pieslice((cx, 2, cx + 9, 11), 180, 360, 2)
im.save("line.gif", transparency=0)

# --- mailbox
frames = []
for k in range(2):
    im = Image.new("P", (40, 36), 0)
    im.putpalette([255, 255, 255, 40, 40, 40, 160, 160, 170, 200, 30, 30, 120, 90, 60, 250, 250, 250] + [0] * (256 * 3 - 18))
    d = ImageDraw.Draw(im)
    d.rectangle((18, 20, 21, 35), 4)
    d.pieslice((4, 4, 34, 24), 180, 360, 2)
    d.rectangle((4, 13, 34, 21), 2)
    d.line((4, 14, 4, 21), 1)
    d.line((34, 14, 34, 21), 1)
    if k == 0:
        d.rectangle((30, 4, 32, 14), 3)
        d.rectangle((30, 4, 37, 8), 3)
    else:
        d.rectangle((30, 9, 32, 18), 3)
        d.rectangle((30, 16, 37, 19), 3)
    frames.append(im)
frames[0].save("mailbox.gif", save_all=True, append_images=frames[1:], duration=600, loop=0, transparency=0)
print("ok")
