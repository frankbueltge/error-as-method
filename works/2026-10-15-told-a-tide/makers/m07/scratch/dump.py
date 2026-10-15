from PIL import Image
im=Image.open('/tmp/claude-0/s128/mk/m07/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
print(W,H, im.info)
# per column: list of dark rows
for x in range(W):
    rows=[y for y in range(H) if px[x,y]<128]
    print(x, len(rows), min(rows) if rows else '-', max(rows) if rows else '-', ''.join('#' if px[x,y]<100 else ('+' if px[x,y]<180 else '.') for y in range(H)))
