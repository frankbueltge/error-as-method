from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m04/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
for x in range(W):
    ys=[y for y in range(H) if p[x,y]<140]
    ink=sum(max(0,200-p[x,y]) for y in range(H))
    print(x, round(x/W*61,2), len(ys), min(ys) if ys else -1, max(ys) if ys else -1, ink)
