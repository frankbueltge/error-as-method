from PIL import Image
import json,sys
im=Image.open(sys.argv[1]).convert('L')
W,H=im.size; px=im.load()
print(W,H)
cols=[]
for x in range(W):
    c=[(y,255-px[x,y]) for y in range(H) if px[x,y]<160]
    cols.append(c)
# ascii view
for y in range(H):
    print(''.join('#' if px[x,y]<100 else ('+' if px[x,y]<180 else ' ') for x in range(0,W,2)))
json.dump([[[y,d] for y,d in c] for c in cols],open('/tmp/claude-0/s130/mk/m06/scratch/cols.json','w'))
import statistics
counts=[len(c) for c in cols]; print('dark px per col', statistics.mean(counts), min(counts), max(counts))
