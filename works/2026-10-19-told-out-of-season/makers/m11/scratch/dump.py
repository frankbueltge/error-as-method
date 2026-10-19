from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m11/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
for y in range(H):
    print(''.join('#' if p[x,y]<100 else ('+' if p[x,y]<180 else ('.' if p[x,y]<235 else ' ')) for x in range(W)))
