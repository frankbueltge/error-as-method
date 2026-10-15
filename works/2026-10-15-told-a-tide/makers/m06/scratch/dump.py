from PIL import Image
im=Image.open('/tmp/claude-0/s128/mk/m06/work/record.jpg')
print(im.size, im.mode)
g=im.convert('L'); W,H=g.size; p=g.load()
for y in range(H):
    print(''.join('#' if p[x,y]<100 else ('+' if p[x,y]<170 else ('.' if p[x,y]<230 else ' ')) for x in range(W)))
