from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m14/work/record.jpg').convert('L')
W,H=im.size; print(W,H)
px=im.load()
for y in range(H):
    print(''.join('#' if px[x,y]<110 else ('+' if px[x,y]<190 else '.') for x in range(W)))
