from PIL import Image
im=Image.open('/tmp/claude-0/s135/mk/m04/work/record.jpg').convert('L')
w,h=im.size;p=im.load()
for y in range(h):
    print('%2d '%y+''.join('#' if p[x,y]<100 else ('+' if p[x,y]<180 else '.') for x in range(w)))
# row darkness sums
