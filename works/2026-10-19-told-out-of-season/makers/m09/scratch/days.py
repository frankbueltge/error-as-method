import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; px=im.load()
X0,X1=2.0,297.0; pph=(X1-X0)/1463; SHIFT=3
cells=[[] for _ in range(61)]
for x in range(W):
    for y in range(H):
        if px[x,y]<150:
            h=(x-X0)/pph+SHIFT; k=min(60,max(0,int(h//24)))
            cells[k].append(y)
out=[]
for k,ys in enumerate(cells):
    ys.sort(); n=len(ys)
    lo=ys[int(0.04*(n-1))]; hi=ys[int(0.96*(n-1))]; med=ys[n//2]
    out.append((lo,med,hi,n))
    print(k,n,lo,med,hi)
open(sys.argv[2],'w').write(";".join(f"{a},{b},{c}" for a,b,c,n in out))
