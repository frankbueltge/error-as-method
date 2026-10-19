from PIL import Image
import json
im=Image.open('/tmp/claude-0/s137/mk/m12/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
cols=[]
for x in range(W):
    d=[max(0,235-p[x,y]) for y in range(H)]
    # peaks
    pk=[]
    for y in range(H):
        if d[y]>60 and d[y]>=d[y-1 if y>0 else 0] and d[y]>=(d[y+1] if y<H-1 else 0):
            # subpixel centroid
            a=d[y-1] if y>0 else 0; b=d[y]; c=d[y+1] if y<H-1 else 0
            off=(c-a)/(a+b+c) if a+b+c else 0
            pk.append((round(y+off,2),b))
    cols.append(pk)
json.dump(cols,open('peaks.json','w'))
import statistics
n=[len(c) for c in cols]
print(sum(n), statistics.mean(n), min(n), max(n))
