from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m03/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
print(W,H)
for y in range(H):
    print('%2d '%y+''.join('#' if p[x,y]<100 else ('+' if p[x,y]<170 else ('.' if p[x,y]<230 else ' ')) for x in range(W)))
