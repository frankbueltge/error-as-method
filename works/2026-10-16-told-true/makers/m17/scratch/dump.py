from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m17/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
print(W,H)
for y in range(H):
    print('%2d '%y+''.join('#' if px[x,y]<100 else ('+' if px[x,y]<170 else ('.' if px[x,y]<230 else ' ')) for x in range(0,150)))
