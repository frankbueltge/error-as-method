from PIL import Image
import sys
g=Image.open(sys.argv[1]).convert('L'); W,H=g.size
for x in range(W):
    col=[255-g.getpixel((x,y)) for y in range(H)]
    ink=[y for y in range(H) if col[y]>128]
    s=sum(col); c=sum(y*v for y,v in enumerate(col))/s
    print(x, round(x*1464/75/24,1), min(ink), max(ink), max(ink)-min(ink)+1, round(c,2))
