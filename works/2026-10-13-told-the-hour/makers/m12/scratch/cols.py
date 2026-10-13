from PIL import Image
im=Image.open('/tmp/claude-0/s123/mk/m12/work/record.jpg').convert('L')
W,H=im.size
for x in range(W):
    ys=[y for y in range(H) if im.getpixel((x,y))<140]
    dark=sum(255-im.getpixel((x,y)) for y in range(H))
    if ys: print(x, len(ys), min(ys), max(ys), round(sum(ys)/len(ys),1), dark)
    else: print(x,0)
