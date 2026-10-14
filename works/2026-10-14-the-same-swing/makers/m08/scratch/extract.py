from PIL import Image
im=Image.open('/tmp/claude-0/s124/mk/m08/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
print(W,H)
for y in range(H):
    print(''.join('#' if px[x,y]<100 else ('+' if px[x,y]<170 else '.') for x in range(0,W)))
