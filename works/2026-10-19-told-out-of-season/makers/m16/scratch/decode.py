import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; px=im.load()
# per column: darkness-weighted mean y of dark pixels, and list of dark rows
out=[]
for x in range(W):
    ys=[(y,255-px[x,y]) for y in range(H) if px[x,y]<160]
    out.append(ys)
for x in range(W):
    print(x, ' '.join(f"{y}" for y,w in out[x]))
