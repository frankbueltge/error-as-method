from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m18/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
print(W,H)
# ascii dump, 2x scale down vertically none
for y in range(H):
    print(''.join('#' if px[x,y]<100 else ('+' if px[x,y]<180 else '.') for x in range(W)))
