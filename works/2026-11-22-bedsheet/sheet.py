"""Make a contact sheet of flag PNGs: sheet.py OUT.png LABELS(yes|no) PNG..."""
import sys
from PIL import Image, ImageDraw
out, labels, files = sys.argv[1], sys.argv[2] == "yes", sys.argv[3:]
cols = 10; cw, ch = 180, 140 if labels else 125
rows = (len(files) + cols - 1) // cols
S = Image.new("RGB", (cols * cw, rows * ch), "white"); d = ImageDraw.Draw(S)
for k, f in enumerate(files):
    im = Image.open(f).convert("RGB"); im.thumbnail((170, 113))
    x, y = (k % cols) * cw + 5, (k // cols) * ch + 5
    S.paste(im, (x, y)); d.rectangle([x - 1, y - 1, x + im.width, y + im.height], outline=(160, 160, 160))
    if labels: d.text((x, y + 117), f.split("/")[-1][:-4].replace("-", " ").title(), fill=(0, 0, 0))
S.save(out)
