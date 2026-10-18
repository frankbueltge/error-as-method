import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L')
w,h=im.size
p=im.load()
for y in range(h):
    print('%2d '%y+''.join('#' if p[x,y]<100 else ('+' if p[x,y]<180 else ('.' if p[x,y]<235 else ' ')) for x in range(w)))
