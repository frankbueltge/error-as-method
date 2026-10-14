from PIL import Image
import json,sys
im=Image.open(sys.argv[1]).convert('L'); w,h=im.size
out=[]
for x in range(w):
    d=[1-im.getpixel((x,y))/255 for y in range(h)]
    # top crossing of 0.5
    top=bot=None
    for y in range(h-1):
        if top is None and d[y]<0.5<=d[y+1]: top=y+(0.5-d[y])/(d[y+1]-d[y])
    for y in range(h-1,0,-1):
        if bot is None and d[y]<0.5<=d[y-1]: bot=y-(0.5-d[y])/(d[y-1]-d[y])
    if top is None: top=0
    if bot is None: bot=h-1
    ink=sum(d)
    out.append((round(top,2),round(bot,2),round(ink,2)))
    print(x,out[-1], round(bot-top,2), round((top+bot)/2,2))
json.dump(out,open(sys.argv[2],'w'))
