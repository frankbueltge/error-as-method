import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; p=im.load()
print(W,H)
for y in range(H):
    print(''.join(' .:-=+*#%@'[min(9,(255-p[x,y])//26)] for x in range(0,W)))
