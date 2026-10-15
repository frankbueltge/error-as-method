from PIL import Image
im=Image.open('/tmp/claude-0/s128/mk/m10/work/record.jpg').convert('L')
W,H=im.size; print(W,H)
px=im.load()
for y in range(H):
    print(''.join('#' if px[x,y]<100 else ('+' if px[x,y]<170 else ('.' if px[x,y]<225 else ' ')) for x in range(W)))
