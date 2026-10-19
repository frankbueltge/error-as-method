import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; p=im.load()
T=int(sys.argv[2]) if len(sys.argv)>2 else 128
rows=[]
for x in range(W):
    ys=[y for y in range(H) if p[x,y]<T]
    w=[255-p[x,y] for y in ys]
    if ys:
        m=sum(y*wi for y,wi in zip(ys,w))/sum(w)
        rows.append((x,min(ys),max(ys),round(m,1),len(ys)))
    else: rows.append((x,None,None,None,0))
for r in rows: print(*r)
