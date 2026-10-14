from PIL import Image
im=Image.open('/tmp/claude-0/s124/mk/m02/work/record.jpg').convert('L')
w,h=im.size;print(w,h)
px=im.load()
for y in range(h):
    print(''.join('#' if px[x,y]<100 else ('+' if px[x,y]<180 else '.') for x in range(w)))
