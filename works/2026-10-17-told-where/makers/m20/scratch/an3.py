from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m20/work/record.jpg').convert('L')
w,h=im.size; px=im.load()
P=4.820057; c0=3.884
for d in range(61):
    lo=c0+P*d; hi=lo+P  # from night center to next night center
    cols=[x for x in range(w) if lo<=x+0.5<hi]
    ys=[y for x in cols for y in range(0,82) if px[x,y]<140]
    top=min(ys) if ys else None
    # zero-width: columns around block center lo with strong baseline & nothing above row 80
    s=sum(255-px[x,y] for x in cols for y in range(0,81))
    zc=sum(1 for x in range(int(lo-3),int(lo+3)) if 0<=x<w and (255-px[x,83])>120 and all(px[x,y]>200 for y in range(60,81)))
    print(d, cols, top, round((83.5-top)/78,2) if top else '-', s, zc)
