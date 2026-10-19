import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; px=im.load()
for x in range(W):
    d=[y for y in range(H) if px[x,y]<150]
    print(x, len(d), min(d) if d else '-', max(d) if d else '-', round(sum(255-px[x,y] for y in range(H))/255,1))
