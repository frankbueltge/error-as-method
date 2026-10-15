import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L')
W,H=im.size
px=im.load()
print(W,H)
# ascii dump, darkness thresholds
for y in range(H):
    print(''.join(' .:#'[min(3,(255-px[x,y])//64)] for x in range(W)))
