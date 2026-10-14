from PIL import Image
im=Image.open('/tmp/claude-0/s124/mk/m09/work/record.jpg')
print(im.mode, im.info, getattr(im,'quantization',None) and len(im.quantization))
g=im.convert('L'); w,h=g.size
T=128
out=[]
for x in range(w):
    col=[g.getpixel((x,y)) for y in range(h)]
    dark=[y for y in range(h) if col[y]<T]
    # subpixel edges: darkness coverage
    cov=[(255-v)/255 for v in col]
    top=None;bot=None
    for y in range(h):
        if col[y]<T: 
            top=y-(cov[y-1] if y>0 else 0); break
    for y in range(h-1,-1,-1):
        if col[y]<T:
            bot=y+1+(cov[y+1] if y<h-1 else 0); break
    mass=sum(cov); cen=sum((y+.5)*c for y,c in enumerate(cov))/mass
    out.append((x,round(top,2),round(bot,2),round(bot-top,2),round(cen,2),''.join('#' if v<T else ('+' if v<200 else '.') for v in col)))
for o in out: print(*o)
