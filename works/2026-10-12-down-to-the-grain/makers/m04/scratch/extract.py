from PIL import Image; import json,sys
im=Image.open(sys.argv[1]).convert('L'); w,h=im.size
g=[[im.getpixel((x,y)) for x in range(w)] for y in range(h)]
json.dump(g,open(sys.argv[2],'w'))
# weighted centre and extent per column
for x in range(w):
    ink=[255-g[y][x] for y in range(h)]
    s=sum(ink); c=sum(y*i for y,i in enumerate(ink))/s
    rows=[y for y in range(h) if ink[y]>60]
    print(x, round(c,1), min(rows), max(rows), end=' | ')
