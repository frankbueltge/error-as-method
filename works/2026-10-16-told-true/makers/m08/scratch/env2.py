import json
d=json.load(open('/tmp/claude-0/s130/mk/m08/scratch/data.json'))
from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m08/work/record.jpg').convert('L'); p=im.load()
W,H=im.size
for y in range(0,12):
    for x in range(W):
        if p[x,y]<220: print('top px',x,y,p[x,y])
# per 5-col (≈1 day) block: rows with dark ink
for b in range(0,W,5):
    rows=sorted(set(y for x in range(b,min(W,b+5)) for y in range(H) if p[x,y]<140))
    print(b, rows[:3], '...', rows[-3:], 'n',len(rows))
