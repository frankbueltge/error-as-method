from PIL import Image
import json, math
im=Image.open('/tmp/claude-0/s130/mk/m18/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
cols=[]
for x in range(W):
    ys=[(y,255-px[x,y]) for y in range(H) if px[x,y]<170]
    cols.append(ys)
# per column: weighted mean, min y, max y, ink
for x in range(W):
    ys=cols[x]
    if not ys: print(x,'-'); continue
    w=sum(v for _,v in ys); m=sum(y*v for y,v in ys)/w
    print(x, len(ys), round(m,1), min(y for y,_ in ys), max(y for y,_ in ys))
