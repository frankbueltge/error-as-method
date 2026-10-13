from PIL import Image
g=Image.open('/tmp/claude-0/s123/mk/m09/work/record.jpg').convert('L')
W,H=g.size
for x in range(W):
    d=[max(0,1-g.getpixel((x,y))/255) for y in range(H)]
    s=sum(d); c=sum(y*v for y,v in enumerate(d))/s
    # top edge: first y where cumulative darkness crosses 0.5 of a pixel, subpixel
    def edge(seq):
        acc=0
        for i,v in enumerate(seq):
            if acc+v>=0.5: return i+(0.5-acc)/v if v else i
            acc+=v
    top=edge(d); bot=H-edge(d[::-1])
    print(x, round(s,2), round(c,2), round(top,2), round(bot,2))
