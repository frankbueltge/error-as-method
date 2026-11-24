from PIL import Image, ImageDraw
OUT = "../S3/"
im = Image.new("P", (110, 40), 0)
im.putpalette([255, 255, 255, 255, 210, 0, 0, 0, 0] + [0] * (253 * 3))
d = ImageDraw.Draw(im)
d.rectangle((0, 0, 109, 39), fill=1, outline=2)
for x in range(-40, 120, 10):
    d.polygon([(x, 39), (x + 5, 39), (x + 15, 33), (x + 10, 33)], fill=2)
for dx in (0, 1):  # fake bold
    d.text((40 + dx, 5), "UNDER", fill=2)
    d.text((19 + dx, 18), "CONSTRUCTION", fill=2)
im.save(OUT + "constr3.gif")
