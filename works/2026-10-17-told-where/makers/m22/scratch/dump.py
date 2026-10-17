from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m22/work/record.jpg').convert('L')
W,H=im.size;print(W,H,im.mode)
px=im.load()
for y in range(H):
    print('%2d '%y+''.join('#' if px[x,y]<100 else ('+' if px[x,y]<180 else ('.' if px[x,y]<230 else ' ')) for x in range(W)))
