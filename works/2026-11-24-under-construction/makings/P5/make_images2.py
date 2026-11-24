import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

random.seed(41)
OUT = "../P5/"
F = ImageFont.load_default()

# --- darker, more photographic curio cabinet: flash glare on glass, murky edges
src = Image.open(OUT + "cabinet.jpg").convert("RGB")
ph = src.resize((240, 180))
ph = ImageEnhance.Brightness(ph).enhance(0.62)
ph = ImageEnhance.Contrast(ph).enhance(0.8)
# vignette
vig = Image.new("L", ph.size, 0)
vd = ImageDraw.Draw(vig)
vd.ellipse((-30, -30, 270, 210), fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(30))
ph = Image.composite(ph, Image.new("RGB", ph.size, (25, 18, 10)), vig)
# hard flash hotspot on the glass door
gl = Image.new("L", ph.size, 0)
gd = ImageDraw.Draw(gl)
gd.ellipse((150, 28, 178, 52), fill=255)
gl = gl.filter(ImageFilter.GaussianBlur(6))
ph = Image.composite(Image.new("RGB", ph.size, (255, 255, 245)), ph, gl)
# glass door frame line + reflection streak
d = ImageDraw.Draw(ph)
d.line((120, 10, 120, 175), fill=(60, 40, 25), width=2)
ph = ph.filter(ImageFilter.GaussianBlur(1.1))
px = ph.load()
for y in range(ph.size[1]):
    for x in range(ph.size[0]):
        r, g, b = px[x, y]
        n = random.randint(-14, 14)
        px[x, y] = (max(0, min(255, r + n + 8)), max(0, min(255, g + n)), max(0, min(255, b + n - 12)))
ph.save(OUT + "cabinet2.jpg", quality=28)

# --- award from her friend Bev's site
aw = Image.new("RGB", (100, 100), (255, 250, 228))
d = ImageDraw.Draw(aw)
d.ellipse((5, 5, 95, 95), fill=(255, 215, 0), outline=(150, 100, 0))
d.ellipse((14, 14, 86, 86), fill=(255, 240, 140), outline=(150, 100, 0))
d.polygon([(30, 85), (20, 99), (38, 92)], fill=(0, 0, 200))
d.polygon([(70, 85), (80, 99), (62, 92)], fill=(0, 0, 200))
for i, t in enumerate(["Bev's", "SHAKER", "SHACK", "Cool Site", "Award!"]):
    w = d.textlength(t, font=F)
    d.text((50 - w / 2, 22 + i * 11), t, fill=(150, 0, 0) if i in (1, 2) else (0, 0, 0), font=F)
aw.convert("P", palette=Image.ADAPTIVE, colors=32).save(OUT + "award.gif")

# --- webring logo
wr = Image.new("RGB", (88, 31), (0, 100, 100))
d = ImageDraw.Draw(wr)
d.rectangle((0, 0, 87, 30), outline=(255, 255, 255))
d.text((5, 4), "Shaker", fill=(255, 255, 255), font=F)
d.text((5, 16), "Collectors Ring", fill=(255, 255, 0), font=F)
d.ellipse((66, 3, 76, 13), fill=(255, 255, 255), outline=(0, 0, 0))
d.ellipse((76, 3, 86, 13), fill=(40, 40, 40), outline=(255, 255, 255))
wr.convert("P", palette=Image.ADAPTIVE, colors=16).save(OUT + "ring.gif")
print("ok")
