from PIL import Image
im=Image.open('/tmp/claude-0/s135/mk/m05/work/record.jpg').convert('L')
W,H=im.size
d=[[255-im.getpixel((x,y)) for x in range(W)] for y in range(H)]
rows=[sum(r) for r in d]
for y,v in enumerate(rows):
    if v>300: print(y,v)
