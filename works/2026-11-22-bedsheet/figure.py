"""figure.svg: the people's 26 seal-on-field flags, their other 24, and the makers' 16, as small embedded thumbnails.
usage: python3.13 figure.py PEOPLE_PNG_DIR MAKER_PNG_DIR"""
import sys, json, base64, io
from PIL import Image
pdir, mdir = sys.argv[1], sys.argv[2]
pc = json.load(open("people_coding.json"))["flags"]
def thumb(path):
    im = Image.open(path).convert("RGB"); im.thumbnail((84, 56)); b = io.BytesIO(); im.save(b, "PNG", optimize=True)
    return im.size, base64.b64encode(b.getvalue()).decode()
rows = [("The fifty: a seal or arms on one colour (26)", [f"{pdir}/{k}.png" for k, v in pc.items() if v["seal_on_field"]]),
        ("The fifty: the other 24", [f"{pdir}/{k}.png" for k, v in pc.items() if not v["seal_on_field"]]),
        ("Made tonight, not shown the fifty (8)", [f"{mdir}/W{i}-{f}.png" for i in range(1, 5) for f in ("superior", "shore")]),
        ("Made tonight, after looking at the fifty (8)", [f"{mdir}/T{i}-{f}.png" for i in range(1, 5) for f in ("superior", "shore")])]
W, cw, ch, cols = 960, 92, 64, 10
out, y = [], 10
for title, files in rows:
    out.append(f'<text x="10" y="{y+14}" font-family="Georgia,serif" font-size="15" fill="#1d1b18">{title}</text>'); y += 24
    for k, f in enumerate(files):
        (w, h), d = thumb(f); x = 10 + (k % cols) * cw; yy = y + (k // cols) * ch
        out.append(f'<image x="{x}" y="{yy + (56-h)/2}" width="{w}" height="{h}" href="data:image/png;base64,{d}"/>')
        out.append(f'<rect x="{x}" y="{yy + (56-h)/2}" width="{w}" height="{h}" fill="none" stroke="#bbb" stroke-width="0.6"/>')
    y += ((len(files) + cols - 1) // cols) * ch + 12
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {y}" width="{W}" height="{y}"><rect width="{W}" height="{y}" fill="#f2efe7"/>' + "".join(out) + "</svg>"
open("figure.svg", "w").write(svg); print(y, len(svg))
