from PIL import Image
im=Image.open('/tmp/claude-0/s124/mk/m01/work/record.jpg').convert('L'); w,h=im.size
T=128
out=[]
for x in range(w):
    c=[im.getpixel((x,y)) for y in range(h)]
    # top crossing
    top=bot=None
    for y in range(1,h):
        if c[y-1]>=T and c[y]<T: top=y-1+(c[y-1]-T)/(c[y-1]-c[y]); break
    for y in range(h-1,0,-1):
        if c[y]>=T and c[y-1]<T: bot=y-1+(c[y-1]-T)/(c[y-1]-c[y]); break
    mass=sum((255-v) for v in c); cen=sum(y*(255-v) for y,v in enumerate(c))/mass
    out.append((x,round(top,2),round(bot,2),round(cen,2),mass))
for o in out: print(*o)
