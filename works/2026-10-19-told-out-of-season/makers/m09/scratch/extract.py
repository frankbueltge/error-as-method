import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; px=im.load()
print(W,H)
# per column: dark pixels (rows)
cols=[]
for x in range(W):
    ys=[y for y in range(H) if px[x,y]<140]
    cols.append(ys)
for x in range(W):
    ys=cols[x]
    print(x, len(ys), (min(ys),max(ys)) if ys else None, sum(ys)/len(ys) if ys else None)
