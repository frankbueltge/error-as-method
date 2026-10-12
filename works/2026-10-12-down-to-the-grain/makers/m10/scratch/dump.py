import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L')
W,H=im.size; p=im.load()
print(W,H,im.info)
for y in range(H):
    print(''.join(' ' if p[x,y]>200 else ('.' if p[x,y]>128 else '#') for x in range(W)))
