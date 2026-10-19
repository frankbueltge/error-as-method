import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; px=im.load()
for y in range(H):
    print(''.join('#' if px[x,y]<100 else ('+' if px[x,y]<180 else ('.' if px[x,y]<230 else ' ')) for x in range(W)))
