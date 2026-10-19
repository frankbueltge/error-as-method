import json,sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; p=im.load()
cols=[]
tot=[]
for x in range(W):
    d=[max(0,235-p[x,y]) for y in range(H)]
    tot.append(sum(d))
    # blobs
    blobs=[];y=0
    while y<H:
        if d[y]>40:
            s=y
            while y<H and d[y]>40: y+=1
            m=sum(d[s:y]); c=sum(i*d[i] for i in range(s,y))/m
            blobs.append((round(c,2),m))
        y+=1
    cols.append(blobs)
import statistics
print('mass per col mean',statistics.mean(tot),'median',statistics.median(tot))
print('blobs per col', statistics.mean(len(b) for b in cols))
ms=[m for b in cols for _,m in b]; print('blob mass median',statistics.median(ms))
json.dump(cols,open('blobs.json','w'))
