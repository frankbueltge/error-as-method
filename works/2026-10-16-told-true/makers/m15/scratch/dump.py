from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m15/work/record.jpg').convert('L')
W,H=im.size; print(W,H,im.mode)
p=im.load()
for y in range(H):
    print('%2d '%y+''.join('#' if p[x,y]<100 else ('+' if p[x,y]<170 else ('.' if p[x,y]<230 else ' ')) for x in range(W)))
