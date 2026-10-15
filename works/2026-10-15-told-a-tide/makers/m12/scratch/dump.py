from PIL import Image
im=Image.open('/tmp/claude-0/s128/mk/m12/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
print(W,H)
for y in range(H):
    print(''.join('#' if px[x,y]<100 else ('+' if px[x,y]<170 else ('.' if px[x,y]<230 else ' ')) for x in range(W)))
