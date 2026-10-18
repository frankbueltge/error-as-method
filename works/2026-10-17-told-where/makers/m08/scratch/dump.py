from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m08/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
print(W,H)
for y in range(H):
    print('%2d '%y+''.join('#' if p[x,y]<100 else ('+' if p[x,y]<180 else ('.' if p[x,y]<235 else ' ')) for x in range(W)))
