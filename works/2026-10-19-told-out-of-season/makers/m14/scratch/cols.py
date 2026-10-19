from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m14/work/record.jpg').convert('L')
W,H=im.size;px=im.load()
for x in range(W):
    ink=[255-px[x,y] for y in range(H)]
    tot=sum(ink)
    rows=[y for y in range(H) if px[x,y]<150]
    print(x, tot, min(rows) if rows else '-', max(rows) if rows else '-', len(rows))
