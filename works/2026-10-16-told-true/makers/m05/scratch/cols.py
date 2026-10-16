from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m05/work/record.jpg').convert('L')
W,H=im.size;px=im.load()
for x in range(W):
    ys=[y for y in range(H) if px[x,y]<140]
    w=sum((255-px[x,y]) for y in range(H) if px[x,y]<200)
    if ys: print(x,min(ys),max(ys),max(ys)-min(ys),len(ys),round(sum(y*(255-px[x,y]) for y in range(H) if px[x,y]<200)/w,1))
    else: print(x,'-')
