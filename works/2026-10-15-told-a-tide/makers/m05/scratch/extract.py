from PIL import Image
im=Image.open('/tmp/claude-0/s128/mk/m05/work/record.jpg').convert('L')
W,H=im.size
px=im.load()
import json
cols=[]
for x in range(W):
    rows=[y for y in range(H) if px[x,y]<140]
    cols.append(rows)
json.dump(cols,open('cols.json','w'))
for x in range(0,W):
    r=cols[x]
    print(x,len(r),min(r) if r else '-',max(r) if r else '-', r)
